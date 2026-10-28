#!/usr/bin/env python3
"""
Dual-Channel Dispatcher & Dual-Resume Attachment Engine
Handles two distinct channels with custom attachments and body templates:
  Channel 1: 'FOUNDER' -> Founder-to-Founder consulting pitch, portfolio links + BOTH RESUMES ATTACHED.
  Channel 2: 'COMPANY' -> Formal Job Application, tailored Cover Letter + BOTH RESUMES ATTACHED.

Attachments Included in EVERY Email:
  1. Kishor_Kumar_Paroi_1Page_ATS_Resume.pdf (Minimalist 1-Page ATS-100 Format)
  2. Kishor_Kumar_Paroi_Comprehensive_Portfolio_Resume.pdf (Detailed Deep-Dive Architecture Resume)
"""

import sys
import os
import smtplib
import imaplib
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent

RESUME_1PAGE_PATH = ROOT_DIR / "simple_resume.pdf"
RESUME_FULL_PATH = ROOT_DIR / "full_comprehensive_resume.pdf"

sys.path.insert(0, str(BASE_DIR / "scripts"))
import founder_discovery
import founders_crm
import email_drafter
import fact_guard
import tracker
import excel_tracker
import continuous_batch_accumulator


def load_mail_credentials():
    env_file = BASE_DIR / ".env"
    cfg = {
        "SMTP_SERVER": "smtp.gmail.com",
        "SMTP_PORT": "587",
        "IMAP_SERVER": "imap.gmail.com",
        "SMTP_USER": "",
        "SMTP_PASSWORD": "",
        "SENDER_NAME": "Kishor Kumar Paroi"
    }
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k in cfg:
                        cfg[k] = v
    return cfg


def craft_founder_cold_email(company: str, role_title: str, recipient_email: str) -> Dict[str, str]:
    """Elite cold outreach pitch referencing BOTH attached resumes."""
    subject = f"{role_title} (Remote) @ {company} — AI Systems Architect & Founder Background"

    body = f"""Hi {company} Founding & Engineering Team,

I've been following {company}'s trajectory and saw your open {role_title} role. Given your mission, I wanted to reach out directly.

I am a Remote AI Systems Architect, former Startup Founder (KoomAI — enterprise video intelligence), and Forward Deployed AI Engineer (phi0.ai Europe / RUET CSE). I specialize in production GenAI inference, high-scale agent orchestration, and distributed cloud systems:

• Sub-35ms Hybrid RAG & Re-ranking: Engineered hybrid dense/sparse vector pipelines (Qdrant + BM25) with local FlashRank ONNX re-ranking, delivering high concurrency under strict latency budgets.
• 24/7 Autonomous Multi-Agent Mesh: Built production agentic loops with LangGraph and local open models (NVIDIA Nemotron-70B, Gemma-2) protected by programmatic zero-hallucination fact guards and NeMo guardrails.
• High-Throughput Inference & Fine-Tuning: Hands-on fine-tuning (QLoRA, RSLoRA, DPO), vLLM / TensorRT-LLM serving, and Rust 1.85 SIMD edge pre-filters reducing compute latency by over 40%.
• Enterprise Big Data & Cloud Native: Production lakehouse pipelines across Databricks, Snowflake, PySpark, Kafka, and Azure Synapse, deployed on AWS EKS / GCP GKE with ArgoCD GitOps and zero-trust DevSecOps.

I have attached both versions of my resume for your convenience:
1. 1-Page Minimalist ATS Resume (quick overview)
2. Comprehensive Architecture & Portfolio Dossier (deep technical breakdown)

Live Systems & Verification:
• Interactive macOS Portfolio: https://kishor.tech (3D Experience: https://3d.kishor.tech)
• Open Codebase & Blueprints: https://github.com/KishorKumarParoi
• Startup Platform: https://koom.kishor.tech

Would you be open to a brief 15-minute introductory call next week to explore how I can help accelerate your engineering roadmap?

Best regards,

Kishor Kumar Paroi
AI Systems Architect & Founder @ KoomAI
B.Sc. in Computer Science & Engineering (RUET)
Email: kishor.ruet.cse@gmail.com | Phone: +880 1724-714156
LinkedIn: https://linkedin.com/in/kishor-kumar-paroi-b06344166
"""
    return {
        "to": recipient_email,
        "subject": subject,
        "body": body
    }


def craft_company_formal_application(company: str, role_title: str, recipient_email: str) -> Dict[str, str]:
    """Formal ATS job application referencing BOTH attached resumes."""
    subject = f"Application: {role_title} (Remote) — Kishor Kumar Paroi"

    body = f"""Dear {company} Hiring Team,

I am writing to formally submit my application for the {role_title} (Remote) position at {company}.

With extensive experience as a Principal AI Systems Architect, former Startup Founder (KoomAI), and Forward Deployed AI Engineer (phi0.ai Europe), I specialize in building and deploying mission-critical, low-latency AI and data architectures.

Key qualifications aligned with this role:
1. Sub-35ms Hybrid RAG & Re-ranking: Engineered dense/sparse vector pipelines (Qdrant + BM25) with local FlashRank ONNX cross-encoder re-ranking under strict SLA constraints.
2. Production Multi-Agent Systems: Architected 24/7 autonomous LangGraph agent workflows powered by local open models (NVIDIA Nemotron-70B, Gemma-2) and verified by programmatic Fact Guard rails.
3. High-Throughput Inference & Scale: Production fine-tuning (QLoRA, RSLoRA, DPO), vLLM / TensorRT-LLM serving, and Rust 1.85 SIMD edge pre-filters reducing compute latency by >40%.
4. Distributed Big Data & Lakehouse Scale: Designed enterprise Medallion lakehouses across Databricks, Snowflake, PySpark, Delta Lake, and Kafka on AWS EKS / GCP GKE with ArgoCD GitOps.

I have attached both versions of my credentials for your review:
1. Kishor_Kumar_Paroi_1Page_ATS_Resume.pdf — Concise 1-page ATS-formatted resume.
2. Kishor_Kumar_Paroi_Comprehensive_Portfolio_Resume.pdf — Full technical history and systems breakdown.

Verified architectures and open-source systems: https://github.com/KishorKumarParoi and https://kishor.tech.

Thank you for your consideration. I look forward to the possibility of discussing how my technical background can support {company}'s goals.

Sincerely,

Kishor Kumar Paroi
AI Systems Architect & Founder @ KoomAI
B.Sc. in Computer Science & Engineering (RUET)
Email: kishor.ruet.cse@gmail.com | Phone: +880 1724-714156
LinkedIn: https://linkedin.com/in/kishor-kumar-paroi-b06344166
"""
    return {
        "to": recipient_email,
        "subject": subject,
        "body": body
    }


def send_dual_channel_email(
    channel: str, # 'FOUNDER' or 'COMPANY'
    company: str,
    role_title: str,
    recipient_email: str,
    send_live: bool = False
) -> Dict[str, Any]:
    cfg = load_mail_credentials()

    if channel == "FOUNDER":
        draft = craft_founder_cold_email(company, role_title, recipient_email)
        target_folder = "Career-AI/Founders-Outreach"
    else: # COMPANY
        draft = craft_company_formal_application(company, role_title, recipient_email)
        target_folder = "Career-AI/Company-Applications"

    # Fact Guard Audit
    gt_sources = fact_guard.load_candidate_sources(BASE_DIR)
    audit = fact_guard.verify_text(draft["body"], gt_sources)
    if not audit.get("verified", True):
        return {"status": "FLAGGED", "error": "Fact Guard verification failed"}

    if not send_live:
        return {
            "status": "STAGED",
            "channel": channel,
            "company": company,
            "recipient": recipient_email,
            "subject": draft["subject"],
            "body": draft["body"],
            "attachments": ["simple_resume.pdf", "full_comprehensive_resume.pdf"],
            "folder": target_folder
        }

    # Live Dispatch via SMTP with BOTH Resume Attachments
    try:
        msg = MIMEMultipart()
        msg["From"] = f"{cfg['SENDER_NAME']} <{cfg['SMTP_USER']}>"
        msg["To"] = recipient_email
        msg["Subject"] = draft["subject"]
        msg.attach(MIMEText(draft["body"], "plain"))

        # Attachment 1: 1-Page ATS Resume
        if RESUME_1PAGE_PATH.exists():
            with open(RESUME_1PAGE_PATH, "rb") as f:
                attach1 = MIMEApplication(f.read(), _subtype="pdf")
                attach1.add_header("Content-Disposition", "attachment", filename="Kishor_Kumar_Paroi_1Page_ATS_Resume.pdf")
                msg.attach(attach1)

        # Attachment 2: Comprehensive Architecture Resume
        if RESUME_FULL_PATH.exists():
            with open(RESUME_FULL_PATH, "rb") as f:
                attach2 = MIMEApplication(f.read(), _subtype="pdf")
                attach2.add_header("Content-Disposition", "attachment", filename="Kishor_Kumar_Paroi_Comprehensive_Portfolio_Resume.pdf")
                msg.attach(attach2)

        # 1. Send SMTP
        with smtplib.SMTP(cfg["SMTP_SERVER"], int(cfg["SMTP_PORT"]), timeout=15) as s:
            s.starttls()
            s.login(cfg["SMTP_USER"], cfg["SMTP_PASSWORD"])
            s.send_message(msg)

        # 2. Append to specific Gmail Label via IMAP
        try:
            with imaplib.IMAP4_SSL(cfg["IMAP_SERVER"], 993) as imap:
                imap.login(cfg["SMTP_USER"], cfg["SMTP_PASSWORD"])
                imap.append(target_folder, '\\Seen', imaplib.Time2Internaldate(time.time()), msg.as_bytes())
        except Exception as e:
            print(f"Notice: IMAP label append note ({target_folder}): {e}")

        print(f"✉️ [SENT {channel}] Delivered to {company} ({recipient_email}) with BOTH RESUMES -> Saved to Gmail '{target_folder}'")
        return {"status": "DELIVERED", "channel": channel, "recipient": recipient_email}
    except Exception as e:
        print(f"❌ Error sending {channel} email to {recipient_email}: {e}")
        return {"status": "ERROR", "error": str(e)}


if __name__ == "__main__":
    print("Testing Dual-Channel Dispatcher with Both Resumes...")
    f_res = send_dual_channel_email("FOUNDER", "RemoteTech", "AI Architect", "founders@remotetech.com", send_live=False)
    print("Founder Staged Subject:", f_res["subject"])
    print("Attachments:", f_res.get("attachments"))
    c_res = send_dual_channel_email("COMPANY", "RemoteTech", "AI Architect", "jobs@remotetech.com", send_live=False)
    print("Company Staged Subject:", c_res["subject"])
    print("Attachments:", c_res.get("attachments"))
