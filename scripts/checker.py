import asyncio
import aiohttp
import time
import json
import os
from datetime import datetime

# Core seed list for programmatic scale
CORE_SEEDS = [
    "google", "youtube", "facebook", "amazon", "wikipedia", "instagram", "reddit",
    "twitter", "x", "yahoo", "whatsapp", "netflix", "linkedin", "openai", "bing",
    "microsoft", "twitch", "github", "pinterest", "ebay", "aliexpress", "canva",
    "tiktok", "fandom", "imdb", "cloudflare", "spotify", "duckduckgo", "quora",
    "wordpress", "medium", "adobe", "apple", "roblox", "paypal", "vimeo", "dropbox",
    "salesforce", "walmart", "zoom", "archive", "tumblr", "booking", "cnn", "bbc",
    "nytimes", "gitlab", "namecheap", "hostinger", "godaddy", "vercel", "netlify",
    "stripe", "shopify", "wix", "squarespace", "bitbucket", "docker", "coursera",
    "udemy", "stackoverflow", "envato", "fiverr", "upwork", "freelancer",
    "kickstarter", "indiegogo", "producthunt", "techcrunch", "theverge", "wired"
]

TLDS = [".com", ".net", ".org", ".io", ".co", ".ai"]

# Generate full multi-TLD target list
DOMAINS_TO_CHECK = [f"{seed}{tld}" for seed in CORE_SEEDS for tld in TLDS]

async def inspect_domain(session, domain):
    url = f"https://{domain}" if not domain.startswith("http") else domain
    clean_domain = domain.replace("https://", "").replace("http://", "").strip("/")
    
    result = {
        "domain": clean_domain,
        "status": "Offline / Expired / Unreachable",
        "status_code": None,
        "response_time_ms": None,
        "server": "Unknown",
        "tech_stack": [],
        "last_checked": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    start_time = time.time()
    try:
        async with session.get(url, timeout=8, allow_redirects=True) as response:
            latency = round((time.time() - start_time) * 1000, 2)
            result["status"] = "Online" if response.status < 400 else "Issues Detected"
            result["status_code"] = response.status
            result["response_time_ms"] = latency
            
            headers = response.headers
            result["server"] = headers.get("Server", "Hidden/CDN")
            
            techs = []
            if "cf-ray" in headers or "cloudflare" in result["server"].lower():
                techs.append("Cloudflare")
            if "X-Powered-By" in headers:
                techs.append(headers["X-Powered-By"])
            if "ghs" in headers.get("Via", "").lower():
                techs.append("GitHub Pages")
            
            result["tech_stack"] = techs

    except Exception as e:
        latency = round((time.time() - start_time) * 1000, 2)
        result["status"] = "Offline / Expired / Unreachable"
        result["response_time_ms"] = latency
        result["error"] = str(e)

    return result

async def main():
    # Set concurrent TCP connection limit for higher speed
    connector = aiohttp.TCPConnector(limit=30)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [inspect_domain(session, d) for d in DOMAINS_TO_CHECK]
        results = await asyncio.gather(*tasks)

    os.makedirs("data", exist_ok=True)
    with open("data/site_status.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Successfully inspected {len(results)} domain permutations!")

if __name__ == "__main__":
    asyncio.run(main())