export default async function handler(req, res) {
  const target = process.env.TUNNEL_URL || 'http://localhost:5001';
  const originalUrl = req.headers['x-vercel-rewrite'] || req.url;
  const reqPath = originalUrl.replace('/api/proxy', '');
  const url = target + reqPath;

  try {
    const headers = { 'cookie': req.headers.cookie || '' };
    if (req.headers['content-type'])
      headers['content-type'] = req.headers['content-type'];

    const opts = {
      method: req.method,
      headers,
      redirect: 'manual',
    };

    if (req.method !== 'GET' && req.method !== 'HEAD') {
      opts.body = await new Promise(r => { let d=''; req.on('data',c=>d+=c); req.on('end',()=>r(d)); });
    }

    const resp = await fetch(url, opts);
    let body = await resp.text();

    const ct = resp.headers.get('content-type') || '';
    if (ct.includes('text/html')) {
      body = body.replace(/(href|src|action)=(["'])\//g, (m,p1,p2) => `${p1}=${p2}/api/proxy/`);
    }

    const sc = resp.headers.get('set-cookie');
    if (sc) res.setHeader('set-cookie', sc);

    const loc = resp.headers.get('location');
    if (loc) {
      if (loc.startsWith('/')) res.setHeader('location', '/api/proxy' + loc);
      else res.setHeader('location', loc);
    }

    resp.headers.forEach((v, k) => {
      if (!['set-cookie','location','content-encoding','transfer-encoding'].includes(k))
        res.setHeader(k, v);
    });

    res.status(resp.status).send(body);
  } catch (e) {
    res.status(502).send(`<h1>Admin Offline</h1><p>Start: bash start_admin.sh</p>`);
  }
}
