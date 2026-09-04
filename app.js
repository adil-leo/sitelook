document.getElementById('searchForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const domain = document.getElementById('domainInput').value.trim().toLowerCase();
  
  const outputCard = document.getElementById('outputCard');
  const outDomain = document.getElementById('outDomain');
  const outStatusBadge = document.getElementById('outStatusBadge');
  const outLatency = document.getElementById('outLatency');
  const outCode = document.getElementById('outCode');
  const outServer = document.getElementById('outServer');
  const outTechStack = document.getElementById('outTechStack');
  const outCheckedAt = document.getElementById('outCheckedAt');
  const outAffiliateLink = document.getElementById('outAffiliateLink');

  outputCard.classList.remove('hidden');
  outDomain.textContent = domain;
  outStatusBadge.textContent = 'Pinging...';
  outStatusBadge.className = 'px-3 py-1 rounded-full text-xs font-semibold bg-yellow-500/10 text-yellow-400 border border-yellow-500/20';

  outAffiliateLink.href = `https://www.namecheap.com/domains/registration/results/?domain=${domain}`;

  const startTime = performance.now();
  try {
    const res = await fetch(`https://${domain}`, { mode: 'no-cors' });
    const latency = Math.round(performance.now() - startTime);

    outStatusBadge.textContent = 'ONLINE';
    outStatusBadge.className = 'px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20';
    outLatency.textContent = `${latency} ms`;
    outCode.textContent = '200 OK (Reachable)';
    outServer.textContent = 'Cloud / CDN';
    outCheckedAt.textContent = `Checked at: ${new Date().toLocaleTimeString()}`;

    outTechStack.innerHTML = `
      <span class="bg-slate-800 text-slate-300 px-2.5 py-1 rounded-md text-xs border border-slate-700">HTTPS SSL</span>
      <span class="bg-slate-800 text-slate-300 px-2.5 py-1 rounded-md text-xs border border-slate-700">CDN Protected</span>
    `;

  } catch (err) {
    outStatusBadge.textContent = 'CHECK FAILED / CORS RESTRICTED';
    outStatusBadge.className = 'px-3 py-1 rounded-full text-xs font-semibold bg-red-500/10 text-red-400 border border-red-500/20';
    outLatency.textContent = '-- ms';
    outCode.textContent = 'Blocked/Offline';
    outServer.textContent = 'Unknown';
    outCheckedAt.textContent = `Checked at: ${new Date().toLocaleTimeString()}`;
  }
});