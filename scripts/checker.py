import asyncio
import aiohttp
import time
import json
import os
from datetime import datetime

async def inspect_domain(session, domain):
    url = f"https://{domain}" if not domain.startswith("http") else domain
    clean_domain = domain.replace("https://", "").replace("http://", "").strip("/")
    
    result = {
        "domain": clean_domain,
        "status": "Offline",
        "status_code": None,
        "response_time_ms": None,
        "server": "Unknown",
        "tech_stack": [],
        "last_checked": datetime.utcnow().isoformat() + "Z"
    }

    start_time = time.time()
    try:
        async with session.get(url, timeout=10, allow_redirects=True) as response:
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
        result["status"] = "Offline"
        result["error"] = str(e)

    return result

async def main():
    domains_to_check = ["google.com", "github.com", "amazon.com", "wordpress.org"]
    
    async with aiohttp.ClientSession() as session:
        tasks = [inspect_domain(session, d) for d in domains_to_check]
        results = await asyncio.gather(*tasks)

    os.makedirs("data", exist_ok=True)
    with open("data/site_status.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"Successfully checked {len(results)} domains!")

if __name__ == "__main__":
    asyncio.run(main())