// Nocodesquare Worker.
// Serves the static site from site/, and handles GitHub sign-in for the admin at /admin:
//   /api/auth      -> sends the browser to GitHub to approve access
//   /api/callback  -> GitHub returns here; we swap the one-time code for a token and hand it to the admin window
// Needs GITHUB_CLIENT_ID (in wrangler.jsonc) and GITHUB_CLIENT_SECRET (a secret set in the Cloudflare dashboard).
// Only GitHub accounts with write access to the repository can actually change anything.

const STATE_COOKIE = 'ncs_oauth_state';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/auth') return startAuth(url, env);
    if (url.pathname === '/api/callback') return finishAuth(request, url, env);
    return env.ASSETS.fetch(request);
  },
};

function startAuth(url, env) {
  if (!env.GITHUB_CLIENT_ID) return text('Sign-in is not set up yet: GITHUB_CLIENT_ID is missing.', 500);
  const state = crypto.randomUUID();
  const github = new URL('https://github.com/login/oauth/authorize');
  github.searchParams.set('client_id', env.GITHUB_CLIENT_ID);
  github.searchParams.set('redirect_uri', `${url.origin}/api/callback`);
  github.searchParams.set('scope', 'repo,user');
  github.searchParams.set('state', state);
  return new Response(null, {
    status: 302,
    headers: {
      Location: github.toString(),
      'Set-Cookie': `${STATE_COOKIE}=${state}; Path=/api; HttpOnly; Secure; SameSite=Lax; Max-Age=600`,
      'Cache-Control': 'no-store',
    },
  });
}

async function finishAuth(request, url, env) {
  const code = url.searchParams.get('code');
  const state = url.searchParams.get('state');
  const cookie = (request.headers.get('Cookie') || '').match(new RegExp(`${STATE_COOKIE}=([^;]+)`));
  if (!code || !state || !cookie || cookie[1] !== state) {
    return reply(url.origin, 'error', { message: 'Sign-in expired or was interrupted. Close this window and try again.' });
  }
  if (!env.GITHUB_CLIENT_SECRET) {
    return reply(url.origin, 'error', { message: 'Sign-in is not set up yet: GITHUB_CLIENT_SECRET is missing.' });
  }
  const res = await fetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json', 'User-Agent': 'nocodesquare-admin' },
    body: JSON.stringify({
      client_id: env.GITHUB_CLIENT_ID,
      client_secret: env.GITHUB_CLIENT_SECRET,
      code,
      redirect_uri: `${url.origin}/api/callback`,
    }),
  });
  const data = await res.json().catch(() => ({}));
  if (!data.access_token) {
    return reply(url.origin, 'error', { message: data.error_description || 'GitHub did not approve the sign-in.' });
  }
  return reply(url.origin, 'success', { token: data.access_token, provider: 'github' });
}

// The admin opens sign-in in a pop-up. This page tells the admin window the result, then closes.
// Messages only go to this site's own origin, never anywhere else.
function reply(origin, status, payload) {
  const message = `authorization:github:${status}:${JSON.stringify(payload)}`;
  const safe = JSON.stringify(message).replace(/</g, '\\u003c');
  const html = `<!doctype html><meta charset="utf-8"><title>Signing in…</title>
<p style="font:16px system-ui;padding:24px">${status === 'success' ? 'Signed in. You can close this window.' : 'Sign-in failed. Close this window and try again.'}</p>
<script>
(function () {
  var origin = ${JSON.stringify(origin)};
  if (!window.opener) return;
  window.addEventListener('message', function handshake(e) {
    if (e.origin !== origin) return;
    window.removeEventListener('message', handshake);
    window.opener.postMessage(${safe}, origin);
    setTimeout(function () { window.close(); }, 400);
  });
  window.opener.postMessage('authorizing:github', origin);
})();
</script>`;
  return new Response(html, {
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'no-store',
      'Set-Cookie': `${STATE_COOKIE}=; Path=/api; HttpOnly; Secure; SameSite=Lax; Max-Age=0`,
      'Content-Security-Policy': "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'",
    },
  });
}

function text(body, status) {
  return new Response(body, { status, headers: { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store' } });
}
