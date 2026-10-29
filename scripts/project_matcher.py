#!/usr/bin/env python3
"""
Hyper-Irresistible Recruiter & Founder Outreach Engine
Architected for:
  - 3-5 Second Attention Span Shortlisting
  - Radical Risk Inversion: "2-Week Free Production Trial on your toughest bottleneck" + "Immediate Assessment Test"
  - 'Jack of All Trades, Master of Many' positioning (Compiler/SIMD -> AI RAG -> Lakehouse -> 3D WebGL)
  - One-Click 15-Minute Calendly / Zoom Booking Integration
  - Deep Dynamic Project Mapping (2-3 Core AI/Systems Matches + 2-3 Surprising Cross-Domain Feats)
"""

import sys
import re
import urllib.parse
from typing import Dict, List, Any, Tuple

# Full Spectrum Portfolio from Kishor's Master Resume & Architect Journey
ALL_PROJECTS = {
    # Core AI & Systems Matches
    "AGENTIC_RAG": {
        "title": "Enterprise AI Security & Production Agentic RAG Platform",
        "url": "https://github.com/KishorKumarParoi/AI_Security_Production_App",
        "category": "core_ai",
        "metric": "Sub-35ms Hybrid RAG (Dense HNSW + BM25 + FlashRank ONNX) + 5 concurrent LangGraph cyclic agents with FastMCP tool execution. Reduced LLM token bills by $18K/mo."
    },
    "LLMOPS_VLLM": {
        "title": "Hybrid Anime Intelligence & Continuous LLMOps Platform",
        "url": "https://github.com/KishorKumarParoi/Hybrid-Anime-Recommender",
        "category": "core_ai",
        "metric": "Low-latency continuous batching with vLLM & dynamic multi-LoRA switching (<30ms). High-throughput Rust 1.85 & Go gRPC gateways delivering 3.8x throughput on >32K contexts."
    },
    "LAKEHOUSE_SPARK": {
        "title": "Zomato AI Lakehouse & Real-time MLOps Platform",
        "url": "https://github.com/KishorKumarParoi/zomato-analysis",
        "category": "core_ai",
        "metric": "35M+ records Medallion Lakehouse with PySpark, Delta Lake, Snowflake, and Feast Feature Store (<10ms point-in-time lookup for online inference)."
    },
    "EDGE_SIMD": {
        "title": "Smart Manufacturing Edge AI & Vibration Defect Platform",
        "url": "https://github.com/KishorKumarParoi",
        "category": "core_ai",
        "metric": "Rust 1.85 SIMD edge pre-filters cutting compute latency by >40% + sub-20ms PyTorch CNN defect vision saving $420K annually in scrap waste."
    },
    # Surprising Cross-Domain Feats (Proving "Jack of All Trades, Master of Many")
    "FOUNDER_KOOMAI": {
        "title": "KoomAI — Asynchronous Video Intelligence Platform (Live Startup)",
        "url": "https://koom.kishor.tech",
        "category": "cross_domain",
        "metric": "Solo-built full-stack startup: WebRTC SVC media engine (<120ms latency), Electron desktop app, Chrome Extension, Next.js 16, and AWS S3/CloudFront CDN."
    },
    "GRAPHICS_3D": {
        "title": "3D Interactive WebGL Spatial Universe",
        "url": "https://3d.kishor.tech",
        "category": "cross_domain",
        "metric": "60 FPS custom physics and shader rendering using Three.js & React Three Fiber — combining deep systems optimization with spatial interactive design."
    },
    "RUST_GIT": {
        "title": "Git Engine Built from Scratch in Rust",
        "url": "https://github.com/KishorKumarParoi",
        "category": "cross_domain",
        "metric": "Implemented custom SHA-1 content-addressable storage, tree delta hashing, and zlib compression protocols with zero third-party dependencies."
    },
    "AI_SECURITY": {
        "title": "Defense-in-Depth AI Security Gateway & PyRIT Red-Teaming",
        "url": "https://github.com/KishorKumarParoi/AI_Security_Production_App",
        "category": "cross_domain",
        "metric": "NVIDIA NeMo Guardrails, autonomous PII scrubbing, BotShield WAF, and automated adversarial jailbreak evaluation."
    }
}


def select_curated_project_suite(job_title: str, job_snippet: str = "") -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """Selects 2-3 matched core projects + 2 surprising cross-domain projects."""
    blob = f"{job_title} {job_snippet}".lower()
    
    # 1. Matched Core Projects
    matched = []
    if any(k in blob for k in ["rag", "agent", "llm", "genai", "security", "guardrail"]):
        matched.append(ALL_PROJECTS["AGENTIC_RAG"])
    if any(k in blob for k in ["vllm", "inference", "quantization", "fine-tuning", "lora", "serving", "mlops"]):
        matched.append(ALL_PROJECTS["LLMOPS_VLLM"])
    if any(k in blob for k in ["data", "spark", "lakehouse", "snowflake", "databricks", "etl", "kafka", "dbt"]):
        matched.append(ALL_PROJECTS["LAKEHOUSE_SPARK"])
    if any(k in blob for k in ["rust", "simd", "c++", "systems", "edge", "hardware", "performance"]):
        matched.append(ALL_PROJECTS["EDGE_SIMD"])

    # Guarantee at least 2 matched
    if len(matched) < 2:
        for p in [ALL_PROJECTS["AGENTIC_RAG"], ALL_PROJECTS["LAKEHOUSE_SPARK"], ALL_PROJECTS["LLMOPS_VLLM"]]:
            if p not in matched:
                matched.append(p)
            if len(matched) >= 3:
                break
    matched = matched[:3]

    # 2. Outside Expertise / Cross-Domain Projects
    outside = []
    for p_key in ["FOUNDER_KOOMAI", "GRAPHICS_3D", "RUST_GIT", "AI_SECURITY"]:
        candidate = ALL_PROJECTS[p_key]
        if candidate not in matched:
            outside.append(candidate)
        if len(outside) >= 2:
            break

    return matched, outside


def generate_curated_cold_email(company: str, role_title: str, recipient_email: str, snippet: str = "") -> Dict[str, str]:
    matched_projs, cross_projs = select_curated_project_suite(role_title, snippet)

    matched_text = "\n".join([
        f"  ▶ {p['title']} ({p['url']})\n    ↳ {p['metric']}" for p in matched_projs
    ])

    cross_text = "\n".join([
        f"  ✦ {p['title']} ({p['url']})\n    ↳ {p['metric']}" for p in cross_projs
    ])

    calendly_link = "https://calendly.com/kishor-ruet-cse/15min"

    subject = f"{role_title} (Remote) @ {company} — 2-Week Free Sprint / Technical Assessment"

    body = f"""Hi {company} Founding & Engineering Team,

I've been tracking {company}'s trajectory and noticed your open {role_title} role. Rather than sending a standard boilerplate application, I want to cut straight to what moves the needle:

I am a Remote AI Systems Architect & Founder (RUET CSE Alum). People often label me a "Jack of all trades, master of none" — until they see me write a sub-35ms SIMD pre-filter in Rust, build a 35M-row Lakehouse, train an LLM with RSLoRA, and ship a 3D WebGL engine in the same sprint. I believe in 2026, the highest-leverage engineers are full-stack generalists who can dive deep into compilers and distributed systems without missing a beat.

Here is my direct offer to {company}:
1. ZERO-RISK 2-WEEK SPRINT: Give me your team's most frustrating technical backlog item or bottleneck. I will build and ship it for 2 weeks at zero financial cost or obligation.
2. IMMEDIATE TECHNICAL ASSESSMENT: If you have a rigorous coding or systems take-home test, send it over immediately. I will complete and return production-ready code with tests within 24 hours.

═════════════════════════════════════════════════════════════════
🎯 2-3 ARCHITECTURES DIRECTLY MATCHING THIS ROLE:
═════════════════════════════════════════════════════════════════
{matched_text}

═════════════════════════════════════════════════════════════════
⚡ 2-3 CROSS-DOMAIN PROOFS OF WORK (BEYOND THE JOB SCOPE):
═════════════════════════════════════════════════════════════════
{cross_text}

═════════════════════════════════════════════════════════════════
📅 1-CLICK INSTANT CALL (15-MIN ZOOM):
═════════════════════════════════════════════════════════════════
Book directly on my calendar: {calendly_link}
(Pick any slot that fits your schedule — Zoom link is generated instantly).

Interactive Systems & Resumes:
• macOS Desktop Portfolio: https://kishor.tech
• 3D WebGL Universe: https://3d.kishor.tech
• 1-Page Visual Resume: resume.pdf (Attached for immediate 4-second human review)
• Comprehensive Single-Column ATS Dossier: resume_single_column.pdf (Attached for full technical depth)

Looking forward to taking your assessment test or solving your backlog this week.

Warm regards,

Kishor Kumar Paroi
Remote AI Systems Architect & Founder @ KoomAI
B.Sc. in Computer Science & Engineering (RUET)
Email: kishor.ruet.cse@gmail.com | Phone: +880 1724-714156
LinkedIn: https://linkedin.com/in/kishor-kumar-paroi-b06344166
"""
    mailto_params = urllib.parse.urlencode({"subject": subject, "body": body}, quote_via=urllib.parse.quote)
    mailto_url = f"mailto:{recipient_email}?{mailto_params}"

    return {
        "to": recipient_email,
        "subject": subject,
        "body": body,
        "calendly_url": calendly_link,
        "mailto_url": mailto_url
    }


def generate_curated_cover_letter(company: str, role_title: str, recipient_email: str, snippet: str = "") -> Dict[str, str]:
    matched_projs, cross_projs = select_curated_project_suite(role_title, snippet)

    matched_text = "\n".join([
        f"• {p['title']}: {p['metric']} ({p['url']})" for p in matched_projs
    ])

    cross_text = "\n".join([
        f"• {p['title']}: {p['metric']} ({p['url']})" for p in cross_projs
    ])

    subject = f"Application: {role_title} (Remote) — Kishor Kumar Paroi"

    body = f"""Dear {company} Hiring Team,

Please accept this formal application for the {role_title} (Remote) position at {company}.

I bring a unique hybrid engineering perspective: I am an AI Systems Architect, former Startup Founder (KoomAI), and Forward Deployed AI Engineer (phi0.ai Europe / RUET CSE). In a technology landscape moving at lightning speed, my value is being a true polyglot problem-solver — bridging low-level hardware performance (Rust SIMD), cutting-edge AI inference (vLLM, LangGraph), enterprise lakehouses (Databricks, PySpark), and intuitive interfaces.

Why I am ready to prove this immediately:
• Proof of Work: I am eager to take your technical assessment test immediately, with 24-hour turnaround.
• Risk-Inverted Trial: I welcome the opportunity to tackle a high-priority 2-week backlog feature to demonstrate production execution before any long-term commitment.

Key Production Architectures Aligned to {company}:
{matched_text}

Diverse Technical Capabilities Outside Core Scope:
{cross_text}

Interactive Proofs & Live Architectures:
• macOS Desktop Portfolio: https://kishor.tech
• 3D WebGL Spatial Platform: https://3d.kishor.tech
• Codebase Blueprints: https://github.com/KishorKumarParoi
• One-Click 15-Minute Sync: https://calendly.com/kishor-ruet-cse/15min

Both my Single-Column ATS Resume (resume_single_column.pdf — optimized for 100% linear portal parsing) and 1-Page Visual Resume (resume.pdf) are provided. Thank you for your consideration, and I look forward to taking your assessment test.

Sincerely,

Kishor Kumar Paroi
AI Systems Architect & Founder @ KoomAI
B.Sc. in Computer Science & Engineering (RUET)
Email: kishor.ruet.cse@gmail.com | Phone: +880 1724-714156
LinkedIn: https://linkedin.com/in/kishor-kumar-paroi-b06344166
"""
    mailto_params = urllib.parse.urlencode({"subject": subject, "body": body}, quote_via=urllib.parse.quote)
    mailto_url = f"mailto:{recipient_email}?{mailto_params}"

    return {
        "to": recipient_email,
        "subject": subject,
        "body": body,
        "mailto_url": mailto_url
    }


if __name__ == "__main__":
    sample = generate_curated_cold_email("Anthropic", "Senior Systems Engineer", "founders@anthropic.com", "Distributed inference with Rust and Python")
    print("Subject:", sample["subject"])
    print("\nBody Snippet:\n", sample["body"][:1200])
