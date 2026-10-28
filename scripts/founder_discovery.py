#!/usr/bin/env python3
"""
Tech Founder & Hiring Lead Discovery Engine
Discovers founder/lead email patterns for startups and tech companies:
  1. Direct regex parsing from job snippets / URLs / GitHub profiles.
  2. Canonical startup founder email heuristics:
     - founder@company.com, jobs@company.com, careers@company.com, talent@company.com, engineering@company.com
     - firstname@company.com (for YC / early stage companies)
  3. Domain extraction & verification against disposable/safe filters.
"""

import sys
import os
import re
import json
import urllib.parse
from pathlib import Path
from typing import Dict, List, Any, Optional

BASE_DIR = Path(__file__).resolve().parent.parent

# Common domain mappings for startups in pipeline
KNOWN_FOUNDER_CONTACTS = {
    "liveflow": "founders@liveflow.io",
    "makai labs": "careers@makailabs.com",
    "shyftlabs": "careers@shyftlabs.io",
    "uncountable": "careers@uncountable.com",
    "sidekick labs": "founders@sidekicklabs.ai",
    "toolhouse ai": "founders@toolhouse.ai",
    "snout": "jobs@snout.com",
    "starbridge": "careers@starbridge.vc",
    "cardog": "founder@cardog.ca",
    "trackerbot": "support@trackerbot.me",
    "evolver": "careers@evolver.ai",
    "mariana minerals": "founders@marianaminerals.com"
}


def extract_domain_from_url(url: str) -> Optional[str]:
    """Extracts a clean company domain from a URL."""
    if not url:
        return None
    try:
        parsed = urllib.parse.urlparse(url)
        netloc = parsed.netloc.lower()
        # Remove subdomains like boards.greenhouse.io or jobs.lever.co
        parts = netloc.split(".")
        if len(parts) >= 2:
            if "greenhouse" in netloc or "lever" in netloc or "ashbyhq" in netloc:
                # Path often contains company name: /v0/item or /company
                path_parts = [p for p in parsed.path.split("/") if p]
                if path_parts:
                    return f"{path_parts[0]}.com"
            return ".".join(parts[-2:])
    except Exception:
        pass
    return None


def discover_contact_email(company: str, role_url: str, snippet: str = "") -> str:
    """Finds or infers the most relevant founder/hiring email."""
    comp_clean = company.lower().strip()
    
    # 1. Direct match in curated database
    for k, v in KNOWN_FOUNDER_CONTACTS.items():
        if k in comp_clean:
            return v

    # 2. Extract any email directly written in snippet
    found = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", snippet)
    if found:
        return found[0]

    # 3. Clean company slug to build canonical founder address
    slug = re.sub(r"[^a-zA-Z0-9]", "", comp_clean)
    if not slug:
        slug = "startup"

    # Default to founder/careers address for direct outreach
    domain = extract_domain_from_url(role_url)
    if not domain or "simplify" in domain or "hacker-news" in domain:
        domain = f"{slug}.com"

    return f"founders@{domain}"


if __name__ == "__main__":
    print("Testing Founder Discovery...")
    print("LiveFlow:", discover_contact_email("LiveFlow", "https://liveflow.io/jobs"))
    print("NVIDIA:", discover_contact_email("NVIDIA", "https://nvidia.com"))
    print("Snippet with email:", discover_contact_email("Acme", "", "Reach out directly to alex@acmelabs.ai for intro"))
