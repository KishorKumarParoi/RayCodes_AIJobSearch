#!/usr/bin/env python3
"""
Hyper-Irresistible Recruiter & Founder Outreach Engine with 15 Verified Projects
Architected for:
  - 3-5 Second Attention Span Shortlisting
  - Radical Risk Inversion: "2-Week Free Production Trial on your toughest bottleneck" + "Immediate Assessment Test"
  - 'Jack of All Trades, Master of Many' positioning (Compiler/SIMD -> AI RAG -> Lakehouse -> 3D WebGL)
  - 1-Click WhatsApp Direct Chat & Calendly 15-Minute Zoom Booking Integration
  - Deep Dynamic Project Mapping across all 15 Production Projects from Master Resume & GitHub README
"""

import sys
import re
import urllib.parse
from typing import Dict, List, Any, Tuple

# All 15 Verified Flagship Projects from Master Resume & GitHub README
ALL_15_PROJECTS = {
    "1_ZOMATO_LAKEHOUSE": {
        "id": 1,
        "title": "Zomato AI Lakehouse & Multimodal Dispute Platform",
        "url": "https://github.com/KishorKumarParoi/zomato-analysis",
        "stack": "Snowflake • PySpark Delta Lake • dbt SCD-2 • Feast Feature Store • Computer Vision Anti-Fraud",
        "metric": "Ingested 35M+ orders (2.3 GB); slashed warehouse compute by 42% ($18K/mo); neutralized refund dispute fraud by 68% ($1.2M saved).",
        "tags": ["lakehouse", "spark", "pyspark", "snowflake", "delta lake", "dbt", "data", "etl", "feast", "computer vision", "redis", "kafka", "debezium"]
    },
    "2_HYBRID_ANIME_LLMOPS": {
        "id": 2,
        "title": "Hybrid Anime Intelligence & Continuous LLMOps Platform",
        "url": "https://github.com/KishorKumarParoi/Hybrid-Anime-Recommender",
        "stack": "Polyglot Mesh (Rust SIMD / Go 1.24 / FastAPI) • Dynamic Multi-LoRA vLLM • RSLoRA Flywheel",
        "metric": "Sub-0.5ms vector scoring via Rust SIMD (50x speedup over Python); 68% GPU cost reduction with vLLM Multi-LoRA continuous batching; NDCG@10 = 0.94.",
        "tags": ["rust", "simd", "vllm", "lora", "fine-tuning", "llmops", "go", "fastapi", "kafka", "inference", "gpu", "recommendation"]
    },
    "3_ENTERPRISE_AI_SECURITY": {
        "id": 3,
        "title": "Enterprise AI Security & Production Agentic RAG Platform",
        "url": "https://github.com/KishorKumarParoi/AI_Security_Production_App",
        "stack": "Zero-Trust AI Gateway • NVIDIA NeMo Guardrails • LangGraph • FastMCP • BotShield WAF",
        "metric": "Sub-35ms Hybrid RAG (Qdrant + BM25 + FlashRank ONNX); blocked 95%+ prompt injections (Microsoft PyRIT); saved $8.4K/mo (42%) via semantic similarity caching.",
        "tags": ["rag", "agent", "langgraph", "security", "guardrails", "nemo", "fastmcp", "hitl", "llm", "genai", "waf", "qdrant", "onnx"]
    },
    "4_SMART_MANUFACTURING": {
        "id": 4,
        "title": "Smart Manufacturing Industrial AI & Multi-Cloud MLOps",
        "url": "https://github.com/KishorKumarParoi/smart-manufacturing",
        "stack": "Rust Edge SIMD • PyTorch Autoencoders • GKE / K3s CNCF • ArgoCD GitOps • TensorRT INT8",
        "metric": "Sub-20ms PyTorch CNN defect classification; reduced defect escape by 31% ($420K annual scrap savings); automated 12-stage ArgoCD GitOps CI/CD.",
        "tags": ["manufacturing", "edge", "rust", "simd", "pytorch", "argocd", "gitops", "k8s", "kubernetes", "gke", "tensorrt", "mlops"]
    },
    "5_NEXUS_AI_LAKEHOUSE": {
        "id": 5,
        "title": "Nexus-AI: Enterprise Multi-Cloud Lakehouse & Autonomous Agent Mesh",
        "url": "https://github.com/KishorKumarParoi/Nexus_AI",
        "stack": "Medallion Lakehouse (Bronze-Silver-Gold) • 5-Agent LangGraph Mesh • DuckDB • Terraform",
        "metric": "5-agent LangGraph mesh accelerated analytics turnaround by 82%; DuckDB compressed dashboard query latencies from 4.5s to <120ms across AWS, GCP, and Azure.",
        "tags": ["lakehouse", "duckdb", "langgraph", "agent", "agents", "terraform", "aws", "gcp", "azure", "multi-cloud", "nl2sql"]
    },
    "6_ADVANCED_AI_CHATBOT": {
        "id": 6,
        "title": "Advanced AI Chatbot: Enterprise Autonomous Agent & HITL Platform",
        "url": "https://github.com/KishorKumarParoi/Advanced_AI_Chatbot_Project",
        "stack": "LangGraph Cyclic State Machine • FastMCP • HITL Financial Gating • BotShield WAF",
        "metric": "Multi-turn thread persistence with dynamic rollbacks; FastMCP approval gates on transactions >$50; <12ms semantic caching saving $3.2K/mo.",
        "tags": ["chatbot", "conversational", "langgraph", "fastmcp", "hitl", "agent", "agents", "waf", "qdrant", "redis"]
    },
    "7_DATA_AGENT_BI": {
        "id": 7,
        "title": "Data Agent: Multi-Agent Business Intelligence & Self-Healing SQL",
        "url": "https://github.com/KishorKumarParoi/Data-Agent",
        "stack": "Hierarchical LangGraph Mesh • Self-Healing SQL LLM Judge • ReAct ETL Sandbox",
        "metric": "96.2% query routing accuracy; LLM security judge auto-heals 89% of initial SQL errors and intercepts 100% of injection attacks; cuts pipeline cycles by 75%.",
        "tags": ["data agent", "sql", "nl2sql", "langgraph", "bi", "etl", "react", "pandas", "analytics", "agent"]
    },
    "8_NETWORK_SECURITY_ETL": {
        "id": 8,
        "title": "Advanced Network Security Medallion Lakehouse & Distributed ML",
        "url": "https://github.com/KishorKumarParoi/Advanced_ETL_Project",
        "stack": "Azure Data Factory (ADF v2) • ADLS Gen2 • Databricks Spark • Synapse CETAS • Sub-4ms ML",
        "metric": "Processes 1.4B security logs with dynamic partition pruning and Z-Order clustering; containerized ONNX inference reduced p99 latency by 11.8x.",
        "tags": ["azure", "databricks", "spark", "adls", "synapse", "etl", "lakehouse", "security", "distributed", "onnx"]
    },
    "9_AWS_SAGEMAKER_MLOPS": {
        "id": 9,
        "title": "AWS SageMaker End-to-End MLOps Pipeline & Governance Platform",
        "url": "https://github.com/KishorKumarParoi/Aws-Sagemaker",
        "stack": "SageMaker Pipelines (DAG) • Managed Spot Training • Model Registry • DataCaptureConfig",
        "metric": "Automated SageMaker DAG with Managed Spot training slashing costs by 70%; autoscaling serverless endpoints sustaining 2,500 req/s with automated drift alerts.",
        "tags": ["sagemaker", "aws", "mlops", "pipeline", "spot", "model registry", "drift", "governance", "kms"]
    },
    "10_REALTIME_MLOPS_KSERVE": {
        "id": 10,
        "title": "Cloud-Native Real-Time MLOps: KServe, AWS ECS Fargate & Kubernetes",
        "url": "https://github.com/KishorKumarParoi/realtime-mlops",
        "stack": "KServe v1beta1 • AWS ECS Fargate • Kubernetes • Modular Terraform IaC • Trivy CVE",
        "metric": "Scale-to-zero serverless inference cutting idle compute spend by 65%; 90/10 canary traffic routing with automated Prometheus latency rollbacks (>25ms).",
        "tags": ["kserve", "kubernetes", "k8s", "ecs", "fargate", "terraform", "mlops", "serving", "serverless", "devops"]
    },
    "11_RUST_GIT_ENGINE": {
        "id": 11,
        "title": "Core Systems Engineering: Rust Git Engine & POSIX Terminal Shell",
        "url": "https://github.com/KishorKumarParoi/codecrafters-git-rust",
        "stack": "Rust 1.85 Bare-Metal • SHA-1 DAG Graph • SIMD Zlib Decompression • Zero-Copy I/O",
        "metric": "Matches C Git performance with 100% memory safety; zero-copy packfile parsing via memmap2 (<14MB RSS); 10M fuzz test iterations with zero crash.",
        "tags": ["rust", "systems", "git", "posix", "compiler", "simd", "low-level", "zero-copy", "performance"]
    },
    "12_USER_SURVIVAL_MLOPS": {
        "id": 12,
        "title": "User Survival Prediction & MLOps Infrastructure Platform",
        "url": "https://github.com/KishorKumarParoi/User-Survival-Prediction",
        "stack": "Astro Airflow DAGs • Redis Low-Latency Feature Store • Alibi Detect KS Drift • Prometheus & Grafana",
        "metric": "Automated Airflow ETL to Redis Feature Store (<2ms retrieval); continuous Kolmogorov-Smirnov drift alarms; 88.9% holdout accuracy model.",
        "tags": ["airflow", "redis", "feature store", "drift", "prometheus", "grafana", "mlops", "classification"]
    },
    "13_KOOMAI_VIDEO_AI": {
        "id": 13,
        "title": "Koom-AI: Enterprise Video Intelligence & Workspace Platform",
        "url": "https://github.com/KishorKumarParoi/koom-ai",
        "stack": "Next.js 16 App Router • Manifest V3 Chrome Extension • WebRTC SVC Media Engine • Stripe Connect",
        "metric": "Sub-120ms glass-to-glass latency across 50,000+ recording minutes; 20-agent LangGraph copilot mesh; $24K MRR enterprise pilot adoption.",
        "tags": ["webrtc", "video", "fullstack", "next.js", "chrome extension", "streaming", "startup", "founder", "audio"]
    },
    "14_REINVENT_3D_PLATFORM": {
        "id": 14,
        "title": "re:invent: Interactive 3D Platform & Real-Time Visitor Telemetry",
        "url": "https://github.com/KishorKumarParoi/re-invent",
        "stack": "React 19.2 • Three.js • GSAP 3.13 • Rolldown Vite • Supabase PostgreSQL Telemetry",
        "metric": "60 FPS custom WebGL spatial camera choreography; live visitor telemetry engine with anti-tamper rate limiting serving global analytics in <100ms.",
        "tags": ["three.js", "webgl", "3d", "react", "gsap", "frontend", "vite", "supabase", "graphics"]
    },
    "15_MACOS_TAHOE_PORTFOLIO": {
        "id": 15,
        "title": "macOS Tahoe: Interactive Apple Silicon OS Portfolio in React & GSAP",
        "url": "https://github.com/KishorKumarParoi/macos-portofolio",
        "stack": "React 19 • GSAP Draggable • Minimax AI Chess Engine • Fire Particle Terminal • ATS Resume",
        "metric": "Full desktop OS recreation with fluid window stacking, minimax computer AI chess engine, interactive CLI particle terminal, and sub-100ms Edge CDN delivery.",
        "tags": ["react", "frontend", "macos", "os", "chess", "minimax", "gsap", "desktop", "ui", "ux"]
    }
}


def score_project_relevance(project: Dict[str, Any], query_text: str) -> int:
    query_lower = query_text.lower()
    score = 0
    # Match tags
    for tag in project.get("tags", []):
        if tag in query_lower:
            score += 10
    # Match title & stack words
    title_words = project.get("title", "").lower().split()
    for w in title_words:
        if len(w) > 3 and w in query_lower:
            score += 5
    stack_words = project.get("stack", "").lower().split()
    for w in stack_words:
        if len(w) > 3 and w in query_lower:
            score += 4
    return score


def select_curated_project_suite(job_title: str, job_snippet: str = "") -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Intelligently scores all 15 projects against the target role and selects:
      - 4 Best-Matched Core Architecture Proofs (with direct GitHub repo links & verified metrics)
      - 3 High-Impact Cross-Domain Feats (demonstrating breadth & founder execution)
    """
    search_context = f"{job_title} {job_snippet}".lower()

    scored = []
    for key, p in ALL_15_PROJECTS.items():
        relevance = score_project_relevance(p, search_context)
        scored.append((relevance, p))

    # Sort descending by relevance
    scored.sort(key=lambda x: x[0], reverse=True)

    # Top 4 matched projects
    matched = [item[1] for item in scored[:4]]

    # Ensure baseline flagship projects are represented if relevance is low
    matched_ids = {p["id"] for p in matched}
    fallback_priority = [3, 2, 1, 13]  # AI Security, vLLM/Rust, Zomato, KoomAI
    for fid in fallback_priority:
        if len(matched) < 4:
            cand = next((p for p in ALL_15_PROJECTS.values() if p["id"] == fid), None)
            if cand and cand["id"] not in matched_ids:
                matched.append(cand)
                matched_ids.add(cand["id"])

    # 3 Distinct Cross-Domain Projects outside the top 4
    cross = []
    cross_candidates = [
        ALL_15_PROJECTS["13_KOOMAI_VIDEO_AI"],
        ALL_15_PROJECTS["11_RUST_GIT_ENGINE"],
        ALL_15_PROJECTS["14_REINVENT_3D_PLATFORM"],
        ALL_15_PROJECTS["15_MACOS_TAHOE_PORTFOLIO"],
        ALL_15_PROJECTS["4_SMART_MANUFACTURING"],
        ALL_15_PROJECTS["10_REALTIME_MLOPS_KSERVE"]
    ]
    for c in cross_candidates:
        if c["id"] not in matched_ids:
            cross.append(c)
        if len(cross) >= 3:
            break

    return matched, cross


def generate_curated_cold_email(company: str, role_title: str, recipient_email: str, snippet: str = "") -> Dict[str, str]:
    matched_projs, cross_projs = select_curated_project_suite(role_title, snippet)

    matched_text = "\n".join([
        f"  {idx}. {p['title']}\n     🔗 Repository: {p['url']}\n     ⚙️ Stack: {p['stack']}\n     📈 Impact: {p['metric']}"
        for idx, p in enumerate(matched_projs, 1)
    ])

    cross_text = "\n".join([
        f"  • {p['title']}: {p['url']}\n    ↳ {p['metric']}"
        for p in cross_projs
    ])

    subject = f"Solving low-latency AI & Agent Infrastructure for {company} — Kishor Kumar Paroi"

    body = f"""Hi {company} Founding & Engineering Team,

I've been tracking {company}'s trajectory and wanted to reach out directly regarding your {role_title} needs.

I am an AI Systems Architect & Forward Deployed Engineer (Founder @ KoomAI, B.Sc. CSE from RUET, Merit Rank 483rd in Bangladesh). I specialize in high-throughput, sub-millisecond distributed AI systems and zero-trust autonomous agent meshes:

🚀 PROUD FLAGSHIP STARTUP: KoomAI (https://koom.kishor.tech)
Architected an enterprise 20-agent autonomous mesh serving as a one-stop freelancer powerhouse:
• Sub-120ms glass-to-glass WebRTC high-performance video communication & neural transcription.
• Autonomous agentic job hunter, automated candidate briefing & ATS resume tailor.
• NotebookLLM-grade deep research synthesis, multimodal document arbitration, and instant global escrow payouts.
• 24/7 personal executive assistant mesh sustaining 50,000+ recording minutes.
• 🔗 Repository: https://github.com/KishorKumarParoi/koom-ai

⚡ 4 TARGET ARCHITECTURE PROOFS (Matched to {role_title}):
{matched_text}

🌐 CROSS-DOMAIN SYSTEMS BREADTH (Proving 'Master of Many'):
{cross_text}

📚 COMPLETE 15-PROJECT PRODUCTION INDEX & CURRICULUM:
• Master GitHub Technical Showcase (All 15 Projects): https://github.com/KishorKumarParoi#1-flagship-technical-projects-1---15
• 38-Module AI Systems Engineering Blueprints: https://github.com/KishorKumarParoi/AI-Engineering
• 1-Page Visual Resume (PDF): https://kishor.tech/resume.pdf
• 2-Page ATS Dossier (PDF): https://kishor.tech/resume_single_column.pdf
• 3D Interactive Spatial Platform: https://3d.kishor.tech
• 3D Cyber Hacker Cockpit: https://hacker.kishor.tech

═════════════════════════════════════════════════════════════════
📅 1-CLICK INSTANT CALL (15-MIN ZOOM) OR DIRECT WHATSAPP:
═════════════════════════════════════════════════════════════════
• Calendar (Instant Zoom): https://calendly.com/kishor-ruet-cse/15min
• WhatsApp Direct 1-Click Message: https://wa.me/8801724714156?text=Hi%20Kishor,%20I%20saw%20your%20pitch%20for%20{urllib.parse.quote(company)}

I have attached both my 1-Page Visual Resume (resume.pdf) and 2-Page Single-Column ATS Resume (resume_single_column.pdf) for immediate review.

Looking forward to taking your technical assessment or tackling a 2-week backlog bottleneck this week.

Warm regards,

Kishor Kumar Paroi
Principal AI Systems Architect | Founder @ KoomAI
B.Sc. in Computer Science & Engineering (RUET)
Email: kishor.ruet.cse@gmail.com | WhatsApp: +8801724714156
LinkedIn: https://linkedin.com/in/kishor-kumar-paroi-b06344166
"""

    mailto_params = urllib.parse.urlencode({"subject": subject, "body": body}, quote_via=urllib.parse.quote)
    mailto_url = f"mailto:{recipient_email}?{mailto_params}"

    return {
        "to": recipient_email,
        "subject": subject,
        "body": body,
        "mailto_url": mailto_url,
        "matched_projects": matched_projs,
        "cross_projects": cross_projs
    }


if __name__ == "__main__":
    print(f"Loaded all {len(ALL_15_PROJECTS)} verified projects!")
    sample = generate_curated_cold_email("Anthropic", "Senior vLLM & LLMOps Systems Engineer", "founders@anthropic.com", "High-throughput inference on GPU clusters with vLLM, Rust and LangGraph agents")
    print(f"Generated Subject: {sample['subject']}\n")
    print("--- SAMPLE PITCH PREVIEW ---")
    print(sample["body"][:1200] + "\n...")
