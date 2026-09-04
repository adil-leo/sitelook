import json
import os

def build_status_page(domain_info):
    domain = domain_info['domain']
    status = domain_info.get('status', 'Unknown')
    latency = domain_info.get('response_time_ms', 'N/A')
    status_code = domain_info.get('status_code', 'N/A')
    server = domain_info.get('server', 'Unknown')
    checked_at = domain_info.get('last_checked', '')

    badge_color = "emerald" if status == "Online" else "red"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Is {domain} Down Right Now? — Real-time Status & Analytics | SiteLook</title>
  <meta name="description" content="Check live uptime status, response latency, server headers, and domain intelligence for {domain}. Is {domain} working or down?">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans">

  <header class="border-b border-slate-800/80 bg-slate-900/50 backdrop-blur py-4 px-6">
    <div class="max-w-5xl mx-auto flex justify-between items-center">
      <a href="../" class="text-2xl font-black bg-gradient-to-r from-cyan-400 via-blue-500 to-indigo-500 bg-clip-text text-transparent">SITELOOK</a>
      <a href="../" class="text-xs text-slate-400 hover:text-cyan-400">← Back to Search</a>
    </div>
  </header>

  <main class="max-w-3xl w-full mx-auto px-4 py-12 flex-1">
    <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 md:p-8 shadow-2xl space-y-6">
      
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center border-b border-slate-800 pb-6 gap-3">
        <div>
          <h1 class="text-2xl md:text-3xl font-extrabold font-mono text-cyan-400">{domain}</h1>
          <p class="text-xs text-slate-500 mt-1">Last inspected: {checked_at}</p>
        </div>
        <span class="px-4 py-1.5 rounded-full text-xs font-bold bg-{badge_color}-500/10 text-{badge_color}-400 border border-{badge_color}-500/20 tracking-wide uppercase">
          {status}
        </span>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-3 gap-4 text-center">
        <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800/60">
          <span class="text-xs text-slate-500 block mb-1">Latency</span>
          <strong class="text-xl font-mono text-slate-200">{latency} ms</strong>
        </div>
        <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800/60">
          <span class="text-xs text-slate-500 block mb-1">HTTP Code</span>
          <strong class="text-xl font-mono text-slate-200">{status_code}</strong>
        </div>
        <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800/60 col-span-2 md:col-span-1">
          <span class="text-xs text-slate-500 block mb-1">Server Type</span>
          <strong class="text-sm font-mono text-slate-200 block truncate">{server}</strong>
        </div>
      </div>

      <!-- Monetization CTA Widget -->
      <div class="bg-gradient-to-r from-blue-900/30 to-indigo-900/30 border border-blue-800/50 rounded-xl p-5 flex flex-col sm:flex-row justify-between items-center gap-4">
        <div>
          <h3 class="text-sm font-bold text-slate-200">Looking to buy or register {domain}?</h3>
          <p class="text-xs text-slate-400">Check registrar details and available domain extensions.</p>
        </div>
        <a href="https://www.namecheap.com/domains/registration/results/?domain={domain}" target="_blank" rel="nofollow" class="px-5 py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:opacity-90 text-white font-semibold text-xs rounded-xl shadow-lg transition shrink-0">
          Check Domain Deals →
        </a>
      </div>

    </div>
  </main>

  <footer class="border-t border-slate-800/80 py-6 text-center text-xs text-slate-500">
    SiteLook Status Engine © 2026 — Automated Web Intelligence
  </footer>

</body>
</html>"""
    return html_content

def main():
    if not os.path.exists("data/site_status.json"):
        print("Data file not found!")
        return

    with open("data/site_status.json", "r") as f:
        domains_data = json.load(f)

    os.makedirs("status", exist_ok=True)

    for item in domains_data:
        domain = item['domain']
        page_html = build_status_page(item)
        file_path = f"status/{domain}.html"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"Generated SEO page: {file_path}")

if __name__ == "__main__":
    main()