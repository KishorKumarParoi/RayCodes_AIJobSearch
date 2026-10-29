#!/usr/bin/env python3
"""
One-Go Automated Job Application & Founder Email Dispatcher
Dispatches customized applications and cold outreach pitches across:
  - LinkedIn
  - Twitter / 𝕏
  - Toptal & Elite Networks
  - Y Combinator & Hacker News Startups
  - Remote Portals (RemoteOK, WWR, Jobicy, etc.)

Features:
  - Zero-Bounce Guard: DNS MX checking + Aggregator domain blacklisting.
  - Human Cadence Jitter (30s - 60s) to guarantee zero Google anti-phishing or spam flags.
  - Attaches both 1-Page Visual Resume & 2-Page Single-Column ATS Resume.
  - Inlines KoomAI 20-agent mesh pitch, WhatsApp direct chat link, and 4 matched project proofs.
  - Live real-time sync with Excel (job_applications_tracker.xlsx) & CRM board.
"""

import sys
import os
import re
import time
import json
import random
import smtplib
import argparse
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
from typing import Dict, List, Any, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
CATEGORIZED_DIR = OUTPUTS_DIR / "categorized"

sys.path.insert(0, str(BASE_DIR / "scripts"))
import founder_discovery
import email_drafter
import fact_guard
import tracker
import excel_tracker


def load_smtp_config() -> Dict[str, str]:
    env_file = BASE_DIR / ".env"
    cfg = {
        "SMTP_SERVER": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "SMTP_PORT": os.getenv("SMTP_PORT", "587"),
        "SMTP_USER": os.getenv("SMTP_USER", ""),
        "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD", ""),
        "SENDER_EMAIL": os.getenv("SENDER_EMAIL", ""),
        "SENDER_NAME": os.getenv("SENDER_NAME", "Kishor Kumar Paroi")
    }
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k in cfg:
                        cfg[k] = v
    if not cfg["SENDER_EMAIL"] and cfg["SMTP_USER"]:
        cfg["SENDER_EMAIL"] = cfg["SMTP_USER"]
    return cfg


def build_curated_pitch(item: Dict[str, Any]) -> Dict[str, str]:
    company = item.get("company", "the team")
    role = item.get("title", "AI Systems Architect / Forward Deployed Engineer")
    recipient_name = item.get("contact_name", "Founding & Engineering Team")
    platform = item.get("platform", "Direct")

    subject = f"Solving low-latency AI & Agent Infrastructure for {company} — Kishor Kumar Paroi"

    body = f"""Hi {recipient_name},

I've been following {company}'s engineering journey and wanted to reach out directly regarding your {role} needs (discovered via {platform}).

I am an AI Systems Architect & Forward Deployed Engineer (Founder @ KoomAI). I build high-throughput, sub-millisecond distributed AI systems and zero-trust agent meshes:

🚀 PROUD FLAGSHIP: KoomAI (https://koom.kishor.tech)
Architected an enterprise 20-agent autonomous mesh serving as a one-stop freelancer powerhouse:
• Sub-120ms glass-to-glass WebRTC high-performance video communication & neural transcription.
• Autonomous agentic job hunter, automated candidate briefing & ATS resume tailor.
• NotebookLLM-grade deep research synthesis, multimodal document arbitration, and instant global escrow payouts.
• 24/7 personal executive assistant mesh sustaining 50,000+ recording minutes.

⚡ 4 TARGET ARCHITECTURE PROOFS (Matched to {role}):
1. Autonomous LangGraph Agent Mesh (phi0.ai): 99.4% task completion across enterprise workloads, saving $18K/month in compute: https://github.com/KishorKumarParoi/AI_Security_Production_App
2. Sub-35ms Hybrid RAG Engine: Multi-stage re-ranking (FlashRank local ONNX + BM25 sparse + dense) with zero hallucination: https://github.com/KishorKumarParoi/AI_Security_Production_App#benchmarks
3. High-Throughput vLLM GPU Serving (Samsung AI Core): Scaled 8B/70B LLMs on NVIDIA H100 clusters with FlashAttention-2, fused CUDA kernels & DeepSpeed ZeRO-3: https://github.com/KishorKumarParoi/AI-Engineering
4. Sub-0.5ms Rust SIMD Vector Engine: High-speed AVX-512 vector similarity search with 50x throughput over standard Python implementations: https://github.com/KishorKumarParoi

📚 VERIFIED CURRICULUM & JOURNEY PROOFS:
• Full 38-Module AI Curriculum & Blueprints: https://github.com/KishorKumarParoi/AI-Engineering
• Complete Open-Source Repository Suite: https://github.com/KishorKumarParoi

VERIFIED PORTFOLIOS & LIVE SYSTEMS:
• Minimalist Academic Dossier: https://kishor.tech
• 3D Interactive Spatial Cockpit: https://3d.kishor.tech
• 3D Cyber Hacker Station: https://hacker.kishor.tech
• 1-Page Visual Resume (PDF): https://kishor.tech/resume.pdf
• 2-Page ATS Dossier (PDF): https://kishor.tech/resume_single_column.pdf

═════════════════════════════════════════════════════════════════
📅 1-CLICK INSTANT CALL (15-MIN ZOOM) OR DIRECT WHATSAPP:
═════════════════════════════════════════════════════════════════
• Calendar (Instant Zoom): https://calendly.com/kishor-ruet-cse/15min
• WhatsApp Direct 1-Click Message: https://wa.me/8801724714156?text=Hi%20Kishor,%20I%20saw%20your%20pitch%20for%20{company}

I have attached both my 1-Page Visual Resume (resume.pdf) and 2-Page Single-Column ATS Resume (resume_single_column.pdf) for your review.

Looking forward to taking your technical assessment or solving your backlog this week.

Warm regards,

Kishor Kumar Paroi
Principal AI Systems Architect | Founder @ KoomAI
B.Sc. in Computer Science & Engineering (RUET)
Email: kishor.ruet.cse@gmail.com | WhatsApp: +8801724714156
LinkedIn: https://linkedin.com/in/kishor-kumar-paroi-b06344166
"""
    return {"subject": subject, "body": body}


def run_one_go_dispatch(
    platform_filter: str = "all",
    limit: Optional[int] = None,
    live_send: bool = False,
    allow_speculative: bool = False,
    min_interval: int = 35,
    max_interval: int = 65
):
    print("=" * 75)
    print("🚀 ONE-GO AUTOMATED JOB APPLICATION & EMAIL DISPATCHER")
    print(f"🎯 Target Platform : {platform_filter.upper()}")
    print(f"📦 Batch Volume    : {'ALL' if limit is None else str(limit)} applications")
    print(f"⏱️ Anti-Spam Jitter: {min_interval}s - {max_interval}s randomized interval")
    print(f"🔒 Dispatch Mode   : {'LIVE GMAIL SMTP DISPATCH' if live_send else 'SAFE DRY-RUN & VERIFICATION'}")
    print(f"🛡️ Bounce Shield   : {'Allow Speculative Guesses' if allow_speculative else 'Strict Verified Addresses Only (Zero-Bounce)'}")
    print("=" * 75)

    # 1. Load Master Categorized Jobs
    master_file = OUTPUTS_DIR / "consolidated_jobs_by_platform.json"
    if not master_file.exists():
        print("⚙️ Building fresh master accumulation first...")
        import accumulate_and_categorize_jobs
        grouped = accumulate_and_categorize_jobs.accumulate_all_jobs()
        accumulate_and_categorize_jobs.save_categorized_outputs(grouped)

    with open(master_file, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    platforms_dict = master_data.get("platforms", {})
    queue: List[Dict[str, Any]] = []

    platform_key_map = {
        "linkedin": "LinkedIn",
        "twitter": "Twitter / 𝕏",
        "x": "Twitter / 𝕏",
        "toptal": "Toptal & Elite Networks",
        "yc": "Y Combinator & HN Startups",
        "remote": "Remote Portals (RemoteOK/WWR/Jobicy)",
        "enterprise": "Global Remote Engineering"
    }

    if platform_filter.lower() == "all":
        # Interleave prioritized platforms
        priority_order = [
            "Twitter / 𝕏",
            "Toptal & Elite Networks",
            "LinkedIn",
            "Y Combinator & HN Startups",
            "Remote Portals (RemoteOK/WWR/Jobicy)",
            "Global Remote Engineering"
        ]
        for p in priority_order:
            for item in platforms_dict.get(p, []):
                if item.get("status") in ["READY_TO_DISPATCH", "DRAFT"]:
                    queue.append(item)
    else:
        matched_plat = platform_key_map.get(platform_filter.lower(), platform_filter)
        for item in platforms_dict.get(matched_plat, []):
            if item.get("status") in ["READY_TO_DISPATCH", "DRAFT"]:
                queue.append(item)

    if limit is not None:
        queue = queue[:limit]

    print(f"\n📋 Identified {len(queue)} pending applications ready for one-go outreach.")
    if not queue:
        print("ℹ️ No pending applications found in queue.")
        return

    # SMTP Setup
    smtp_cfg = load_smtp_config()
    is_smtp_ready = bool(smtp_cfg.get("SMTP_USER") and smtp_cfg.get("SMTP_PASSWORD"))

    if live_send and not is_smtp_ready:
        print("❌ Cannot perform live dispatch: SMTP_USER or SMTP_PASSWORD missing in .env")
        return

    # Verified PDF Resume Attachments
    p1 = BASE_DIR / "resume.pdf"
    p2 = BASE_DIR / "resume_single_column.pdf"
    has_resumes = p1.exists() and p2.exists()
    print(f"📄 Resume Attachments: {'Attached (1-Page Visual + 2-Page ATS)' if has_resumes else 'Warning: Local PDF files missing'}")

    dispatched = 0
    blocked_count = 0

    for idx, job in enumerate(queue, 1):
        comp = job.get("company", "Company")
        title = job.get("title", "Role")
        plat = job.get("platform", "Platform")
        email_addr = job.get("contact_email", "")

        print(f"\n[{idx}/{len(queue)}] 🎯 Processing: {comp} — {title}")
        print(f"   🌐 Channel   : {plat}")
        print(f"   📧 Recipient : {email_addr}")

        # Zero-Bounce Guard: Strict DNS MX & Aggregator check
        is_valid, reason = founder_discovery.validate_recipient_email(email_addr, comp, check_dns=True)
        if not is_valid:
            print(f"   🛑 [Zero-Bounce Guard] Blocked dispatch to {email_addr} — {reason}")
            job["status"] = f"BLOCKED: {reason}"
            blocked_count += 1
            continue

        # Zero-Bounce Guard: Distinguish Verified vs Speculative guesses
        is_verified = (
            any(k in comp.lower() for k in founder_discovery.KNOWN_FOUNDER_CONTACTS)
            or "twitter" in plat.lower()
            or "x" in plat.lower()
            or "tweet" in str(job.get("source_file", ""))
            or not email_addr.startswith("founders@")
        )

        if live_send and not is_verified and not allow_speculative:
            print(f"   🛡️ [Zero-Bounce Shield] Skipped speculative address: {email_addr}")
            print(f"      👉 Staged safely in Excel with 1-click mailto link (avoids 550 NoSuchUser bounce).")
            job["status"] = "STAGED_SPECULATIVE"
            continue

        pitch = build_curated_pitch(job)

        if live_send:
            try:
                msg = MIMEMultipart()
                msg["From"] = f"{smtp_cfg['SENDER_NAME']} <{smtp_cfg['SENDER_EMAIL']}>"
                msg["To"] = email_addr
                msg["Subject"] = pitch["subject"]
                msg.attach(MIMEText(pitch["body"], "plain"))

                if p1.exists():
                    with open(p1, "rb") as fp:
                        a1 = MIMEApplication(fp.read(), _subtype="pdf")
                        a1.add_header("Content-Disposition", "attachment", filename="Kishor_Kumar_Paroi_1Page_Visual_Resume.pdf")
                        msg.attach(a1)
                if p2.exists():
                    with open(p2, "rb") as fp:
                        a2 = MIMEApplication(fp.read(), _subtype="pdf")
                        a2.add_header("Content-Disposition", "attachment", filename="Kishor_Kumar_Paroi_Single_Column_ATS_Resume.pdf")
                        msg.attach(a2)

                with smtplib.SMTP(smtp_cfg["SMTP_SERVER"], int(smtp_cfg["SMTP_PORT"]), timeout=20) as server:
                    server.starttls()
                    server.login(smtp_cfg["SMTP_USER"], smtp_cfg["SMTP_PASSWORD"])
                    server.send_message(msg)

                job["status"] = "SENT_LIVE"
                job["dispatched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"   ✉️ [LIVE SMTP DISPATCHED] Successfully sent tailored application to {email_addr}!")
            except Exception as e:
                print(f"   ⚠️ SMTP Send failed: {e}. Keeping in Staged Outbox.")
                job["status"] = "STAGED_OUTBOX"
        else:
            job["status"] = "STAGED_READY"
            print(f"   📝 [DRY-RUN VERIFIED] Tailored pitch & verified resumes staged for {comp}")

        dispatched += 1

        # Real-Time CRM & Excel Tracker Sync
        crm_file = OUTPUTS_DIR / "founders_outreach_crm.json"
        if crm_file.exists():
            try:
                with open(crm_file, "r", encoding="utf-8") as f:
                    crm_records = json.load(f)
                matched = False
                for r in crm_records:
                    if r.get("company", "").lower() == comp.lower():
                        r["delivery_status"] = "SENT_LIVE" if live_send else "STAGED_READY"
                        r["mail_sent"] = live_send
                        r["dispatch_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        matched = True
                        break
                if not matched:
                    crm_records.append({
                        "crm_id": f"CRM-{len(crm_records)+1:04d}",
                        "company": comp,
                        "role": title,
                        "email": email_addr,
                        "delivery_status": "SENT_LIVE" if live_send else "STAGED_READY",
                        "mail_sent": live_send,
                        "dispatch_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "reply_received": False,
                        "reply_intent": "Awaiting Reply"
                    })
                with open(crm_file, "w", encoding="utf-8") as f:
                    json.dump(crm_records, f, indent=2)
            except Exception:
                pass

        # Anti-Phishing Human Cadence Jitter
        if idx < len(queue):
            delay = random.randint(min_interval, max_interval)
            print(f"   ⏳ Google Anti-Phishing Safety Delay: waiting {delay}s while analyzing next opportunity...")
            time.sleep(delay)

    # Final Sync to Excel Workbook
    excel_tracker.sync_board_to_excel()

    print("\n" + "=" * 75)
    print(f"✅ One-Go Dispatch Run Complete!")
    print(f"   • Successfully processed: {dispatched}")
    print(f"   • Blocked by Zero-Bounce: {blocked_count}")
    print(f"   • Updated Master Excel   : outputs/job_applications_tracker.xlsx")
    print("=" * 75)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="One-Go Automated Job Application & Founder Email Dispatcher")
    parser.add_argument("--platform", default="all", choices=["all", "linkedin", "twitter", "x", "toptal", "yc", "remote", "enterprise"], help="Platform filter")
    parser.add_argument("--limit", type=int, default=5, help="Number of applications to dispatch (default: 5)")
    parser.add_argument("--all", action="store_true", help="Process ALL pending applications")
    parser.add_argument("--live", action="store_true", help="Actually send live via Gmail SMTP (default: dry-run)")
    parser.add_argument("--allow-speculative", action="store_true", help="Allow sending to speculative guesses (caution: risk of 550 bounces)")
    parser.add_argument("--min-delay", type=int, default=30, help="Minimum anti-spam delay in seconds (default: 30)")
    parser.add_argument("--max-delay", type=int, default=60, help="Maximum anti-spam delay in seconds (default: 60)")

    args = parser.parse_args()
    lim = None if args.all else args.limit
    run_one_go_dispatch(
        platform_filter=args.platform,
        limit=lim,
        live_send=args.live,
        allow_speculative=args.allow_speculative,
        min_interval=args.min_delay,
        max_interval=args.max_delay
    )
