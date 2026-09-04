import json
import os
from datetime import datetime

# Domain URL of your site
BASE_URL = "https://adil-leo.github.io/sitelook"

def generate_sitemap():
    if not os.path.exists("data/site_status.json"):
        print("data/site_status.json not found! Skipping sitemap creation.")
        return

    with open("data/site_status.json", "r") as f:
        domains_data = json.load(f)

    today = datetime.utcnow().strftime("%Y-%m-%d")

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    # Add homepage
    xml_lines.append(f"""  <url>
    <loc>{BASE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>""")

    # Add programmatic status pages
    for item in domains_data:
        domain = item['domain']
        page_url = f"{BASE_URL}/status/{domain}.html"
        xml_lines.append(f"""  <url>
    <loc>{page_url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.8</priority>
  </url>""")

    xml_lines.append('</urlset>')

    sitemap_content = "\n".join(xml_lines)

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    print(f"sitemap.xml successfully generated with {len(domains_data) + 1} URLs!")

if __name__ == "__main__":
    generate_sitemap()