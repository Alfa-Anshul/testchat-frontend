from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature

app = FastAPI()
SECRET = "nexus-anervea-secret-2025"
SIGNER = URLSafeTimedSerializer(SECRET)
USERS = {"aniket": "Password@123"}

def get_user(request: Request):
    try:
        return SIGNER.loads(request.cookies.get("session",""), max_age=86400)
    except BadSignature:
        return None

LOGIN_HTML = r"""
<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>NexusChat — Sign in</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{min-height:100vh;background:#0d1117;color:#e6edf3;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Inter',Helvetica,Arial,sans-serif;font-size:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px}
.logo-wrap{margin-bottom:16px}
.logo-wrap svg{fill:#e6edf3;width:48px;height:48px}
.card{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:24px;width:100%;max-width:340px}
.card h1{font-size:24px;font-weight:300;color:#e6edf3;text-align:center;margin-bottom:16px;letter-spacing:-.5px}
.field-label{display:block;font-size:14px;font-weight:600;color:#e6edf3;margin-bottom:6px}
.field{width:100%;background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:5px 12px;color:#e6edf3;font-size:14px;line-height:20px;outline:none;transition:border-color .15s,box-shadow .15s;margin-bottom:16px;height:32px;font-family:inherit}
.field:focus{border-color:#388bfd;box-shadow:0 0 0 3px rgba(56,139,253,.3)}
.field::placeholder{color:#484f58}
.btn{width:100%;background:#238636;border:1px solid rgba(240,246,252,.1);border-radius:6px;padding:5px 16px;color:#fff;font-size:14px;font-weight:500;font-family:inherit;cursor:pointer;transition:background .15s;height:32px;line-height:20px}
.btn:hover{background:#2ea043}
.error{background:rgba(248,81,73,.1);border:1px solid rgba(248,81,73,.4);border-radius:6px;padding:8px 16px;font-size:13px;color:#f85149;margin-bottom:16px;display:flex;align-items:center;gap:8px}
.sub-card{margin-top:16px;border:1px solid #30363d;border-radius:6px;padding:16px;max-width:340px;width:100%;text-align:center;font-size:12px;color:#8b949e}
.sub-card a{color:#58a6ff;text-decoration:none}
</style></head><body>
<div class="logo-wrap">
  <svg height="48" viewBox="0 0 16 16" width="48" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
</div>
<div class="card">
  <h1>Sign in</h1>
  ERROR_PLACEHOLDER
  <form method="post" action="/login">
    <label class="field-label" for="u">Username or email address</label>
    <input class="field" id="u" name="username" type="text" autocomplete="username" required autofocus/>
    <label class="field-label" for="p">Password</label>
    <input class="field" id="p" name="password" type="password" autocomplete="current-password" required/>
    <button class="btn" type="submit">Sign in</button>
  </form>
</div>
<div class="sub-card">NexusChat &mdash; Powered by <a href="#">Anervea AI</a></div>
</body></html>
"""

CHAT_HTML = r"""
<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>NexusChat — Anervea AI</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0d1117;--surface:#161b22;--surface2:#21262d;--surface3:#30363d;
  --border:#30363d;--border-muted:#21262d;
  --accent:#1f6feb;--accent-hover:#388bfd;--accent-fg:#58a6ff;
  --success:#238636;--success-hover:#2ea043;
  --text:#e6edf3;--text-2:#8b949e;--text-3:#484f58;
  --user-bubble:#1c2128;--bot-bubble:#161b22;
  --font:-apple-system,BlinkMacSystemFont,'Segoe UI','Inter',Helvetica,Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace;
  --r:6px;
}
html,body{height:100%;background:var(--bg);color:var(--text);font-family:var(--font);font-size:14px;overflow:hidden;-webkit-font-smoothing:antialiased}
::-webkit-scrollbar{width:8px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:var(--surface3);border-radius:6px;border:2px solid var(--bg)}
.shell{display:flex;height:100vh;width:100vw;overflow:hidden}
.sidebar{width:256px;min-width:256px;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;transition:transform .25s ease;z-index:100}
.sb-head{display:flex;align-items:center;gap:8px;padding:16px;border-bottom:1px solid var(--border-muted)}
.logo-icon{width:32px;height:32px;border-radius:var(--r);background:var(--surface2);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.logo-icon svg{fill:var(--text);width:18px;height:18px}
.logo-txt{font-size:14px;font-weight:600;color:var(--text)}
.logo-badge{margin-left:auto;background:var(--success);color:#fff;font-size:10px;font-weight:600;padding:1px 6px;border-radius:20px}
.sb-sec{padding:16px 16px 4px;font-size:12px;font-weight:600;color:var(--text-2);text-transform:uppercase;letter-spacing:.04em}
.sb-nav{flex:1;padding:4px 8px;display:flex;flex-direction:column;gap:1px}
.nav-btn{display:flex;align-items:center;gap:8px;background:none;border:none;color:var(--text-2);font-family:var(--font);font-size:14px;padding:6px 8px;border-radius:var(--r);cursor:pointer;transition:background .12s,color .12s;text-align:left;width:100%}
.nav-btn:hover{background:var(--surface2);color:var(--text)}
.nav-btn.active{background:var(--surface2);color:var(--text);font-weight:600}
.nav-btn svg{width:16px;height:16px;flex-shrink:0;fill:currentColor;opacity:.8}
.sb-div{border-top:1px solid var(--border-muted);margin:8px 0}
.sb-user{padding:12px 16px;border-top:1px solid var(--border-muted);display:flex;flex-direction:column;gap:10px}
.user-row{display:flex;align-items:center;gap:8px}
.user-av{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#1f6feb,#388bfd);display:flex;align-items:center;justify-content:center;font-weight:600;font-size:13px;color:#fff;flex-shrink:0;border:2px solid var(--surface3)}
.user-name{font-size:14px;font-weight:600;color:var(--text);line-height:1.2}
.user-handle{font-size:12px;color:var(--text-2)}
.logout-btn{display:flex;align-items:center;gap:6px;background:none;border:1px solid var(--border);color:var(--text-2);font-family:var(--font);font-size:12px;padding:4px 10px;border-radius:var(--r);cursor:pointer;transition:all .12s;width:100%;height:28px}
.logout-btn:hover{background:var(--surface2);color:var(--text);border-color:var(--accent-hover)}
.logout-btn svg{width:14px;height:14px;fill:currentColor;opacity:.7}
.overlay{display:none;position:fixed;inset:0;background:rgba(1,4,9,.8);z-index:90}
.main{flex:1;display:flex;flex-direction:column;min-width:0;background:var(--bg)}
.hdr{display:flex;align-items:center;gap:12px;padding:0 16px;height:48px;border-bottom:1px solid var(--border);background:var(--surface);z-index:10;flex-shrink:0}
.menu-btn{display:none;flex-direction:column;gap:4px;background:none;border:none;cursor:pointer;padding:4px;color:var(--text-2)}
.menu-btn svg{width:16px;height:16px;fill:currentColor}
.hdr-info{flex:1;display:flex;align-items:center;gap:8px}
.hdr-av{width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,#1f6feb,#388bfd);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;color:#fff;flex-shrink:0;border:1px solid var(--surface3);position:relative}
.online-dot{position:absolute;bottom:0;right:0;width:8px;height:8px;border-radius:50%;background:#3fb950;border:1.5px solid var(--surface)}
.hdr-name{font-size:14px;font-weight:600;color:var(--text)}
.hdr-sub{font-size:12px;color:var(--text-2)}
.icon-btn{background:none;border:1px solid var(--border);color:var(--text-2);width:28px;height:28px;border-radius:var(--r);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .12s}
.icon-btn:hover{background:var(--surface2);color:var(--text);border-color:var(--accent-hover)}
.icon-btn svg{width:14px;height:14px;fill:currentColor}
.msgs{flex:1;overflow-y:auto;padding:16px 0}
.msgs-inner{max-width:800px;margin:0 auto;padding:0 16px;display:flex;flex-direction:column;gap:4px}
.date-sep{display:flex;align-items:center;gap:8px;margin:12px 0 4px;color:var(--text-2);font-size:12px}
.date-sep::before,.date-sep::after{content:'';flex:1;border-top:1px solid var(--border-muted)}
.msg-row{display:flex;align-items:flex-start;gap:8px;padding:2px 0;animation:fadeIn .15s ease}
.msg-row.user{flex-direction:row-reverse}
@keyframes fadeIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
.av{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:11px;flex-shrink:0;margin-top:4px}
.av.bot{background:linear-gradient(135deg,#1f6feb,#388bfd);color:#fff;border:1px solid var(--surface3)}
.av.usr{background:var(--surface2);border:1px solid var(--border);color:var(--text-2)}
.msg-content{max-width:calc(100% - 80px);display:flex;flex-direction:column;gap:2px}
.msg-meta{display:flex;align-items:baseline;gap:6px;margin-bottom:2px}
.msg-meta .mname{font-size:13px;font-weight:600;color:var(--text)}
.msg-meta .mtime{font-size:11px;color:var(--text-3)}
.msg-row.user .msg-meta{flex-direction:row-reverse}
.bubble{display:inline-block;padding:8px 12px;border-radius:2px 12px 12px 12px;font-size:14px;line-height:1.6;word-break:break-word;color:var(--text);max-width:100%}
.bubble.bot{background:var(--bot-bubble);border:1px solid var(--border);border-top-left-radius:2px}
.bubble.usr{background:#1c2128;border:1px solid #30363d;border-top-right-radius:2px;border-top-left-radius:12px}
.bubble strong{color:var(--accent-fg);font-weight:600}
.bubble code{font-family:var(--mono);font-size:12px;background:var(--surface2);padding:1px 5px;border-radius:4px;color:#e3b341;border:1px solid var(--border-muted)}
.typing-row{display:flex;align-items:flex-start;gap:8px;padding:2px 0;animation:fadeIn .15s ease}
.typing-bubble{background:var(--bot-bubble);border:1px solid var(--border);border-radius:2px 12px 12px 12px;padding:10px 14px;display:flex;gap:4px;align-items:center}
.dot{width:6px;height:6px;background:var(--text-2);border-radius:50%;animation:bounce 1.4s infinite ease-in-out}
.dot:nth-child(2){animation-delay:.16s}.dot:nth-child(3){animation-delay:.32s}
@keyframes bounce{0%,60%,100%{transform:translateY(0);opacity:.4}30%{transform:translateY(-5px);opacity:1}}
.suggestions{display:flex;flex-wrap:wrap;gap:6px;padding:8px 16px 12px;max-width:800px;margin:0 auto;width:100%}
.chip{background:var(--surface2);border:1px solid var(--border);color:var(--text-2);font-family:var(--font);font-size:12px;padding:4px 12px;border-radius:20px;cursor:pointer;transition:all .12s}
.chip:hover{border-color:var(--accent-hover);color:var(--text)}
.input-wrap{padding:12px 16px 16px;border-top:1px solid var(--border);background:var(--surface);display:flex;flex-direction:column;align-items:center;gap:6px}
.input-row{display:flex;align-items:flex-end;gap:8px;width:100%;max-width:800px;background:var(--bg);border:1px solid var(--border);border-radius:var(--r);padding:8px 8px 8px 12px;transition:border-color .15s,box-shadow .15s}
.input-row:focus-within{border-color:var(--accent-hover);box-shadow:0 0 0 3px rgba(56,139,253,.15)}
#inp{flex:1;background:none;border:none;color:var(--text);font-family:var(--font);font-size:14px;resize:none;outline:none;line-height:1.5;max-height:120px;min-height:20px}
#inp::placeholder{color:var(--text-3)}
.send-btn{width:28px;height:28px;flex-shrink:0;border-radius:var(--r);background:var(--success);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#fff;transition:all .12s;opacity:.4}
.send-btn svg{width:14px;height:14px;fill:currentColor}
.send-btn.on{opacity:1}
.send-btn.on:hover{background:var(--success-hover)}
.hint{font-size:11px;color:var(--text-3);font-family:var(--mono)}
@media(max-width:768px){.sidebar{position:fixed;left:0;top:0;bottom:0;transform:translateX(-100%)}.sidebar.open{transform:translateX(0)}.overlay{display:block}.menu-btn{display:flex}}
</style></head><body>
<div class="shell">
  <aside class="sidebar" id="sb">
    <div class="sb-head">
      <div class="logo-icon"><svg viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg></div>
      <span class="logo-txt">NexusChat</span>
      <span class="logo-badge">AI</span>
    </div>
    <p class="sb-sec">Navigation</p>
    <nav class="sb-nav">
      <button class="nav-btn active">
        <svg viewBox="0 0 16 16"><path d="M2.5 2.75a.25.25 0 0 1 .25-.25h10.5a.25.25 0 0 1 .25.25v7.5a.25.25 0 0 1-.25.25h-6.5a.75.75 0 0 0-.53.22L4 12.44V10.5a.75.75 0 0 0-.75-.75H2.75a.25.25 0 0 1-.25-.25Zm.25-1.75A1.75 1.75 0 0 0 1 2.75v7.5c0 .966.784 1.75 1.75 1.75H3v1.94a.75.75 0 0 0 1.28.53l2.345-2.344H13.25A1.75 1.75 0 0 0 15 10.25v-7.5A1.75 1.75 0 0 0 13.25 1Z"/></svg>
        Chat
      </button>
      <button class="nav-btn" onclick="clearChat()">
        <svg viewBox="0 0 16 16"><path d="M11 1.75V3h2.25a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1 0-1.5H5V1.75C5 .784 5.784 0 6.75 0h2.5C10.216 0 11 .784 11 1.75ZM4.496 6.675l.66 6.6a.25.25 0 0 0 .249.225h5.19a.25.25 0 0 0 .249-.225l.66-6.6a.75.75 0 0 1 1.492.149l-.66 6.6A1.748 1.748 0 0 1 10.595 15h-5.19a1.75 1.75 0 0 1-1.741-1.575l-.66-6.6a.75.75 0 1 1 1.492-.15ZM6.5 1.75V3h3V1.75a.25.25 0 0 0-.25-.25h-2.5a.25.25 0 0 0-.25.25Z"/></svg>
        Clear chat
      </button>
    </nav>
    <div class="sb-div"></div>
    <div class="sb-user">
      <div class="user-row">
        <div class="user-av" id="uav">A</div>
        <div><div class="user-name" id="uname">aniket</div><div class="user-handle">Anervea AI</div></div>
      </div>
      <form method="post" action="/logout">
        <button class="logout-btn" type="submit">
          <svg viewBox="0 0 16 16"><path d="M2 2.75C2 1.784 2.784 1 3.75 1h2.5a.75.75 0 0 1 0 1.5h-2.5a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h2.5a.75.75 0 0 1 0 1.5h-2.5A1.75 1.75 0 0 1 2 13.25Zm10.44 4.5-1.97-1.97a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215l3.25 3.25a.75.75 0 0 1 0 1.06l-3.25 3.25a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734l1.97-1.97H6.75a.75.75 0 0 1 0-1.5Z"/></svg>
          Sign out
        </button>
      </form>
    </div>
  </aside>
  <div class="overlay" id="ov" onclick="closeSb()"></div>
  <main class="main">
    <header class="hdr">
      <button class="menu-btn" onclick="toggleSb()"><svg viewBox="0 0 16 16"><path d="M1 2.75A.75.75 0 0 1 1.75 2h12.5a.75.75 0 0 1 0 1.5H1.75A.75.75 0 0 1 1 2.75Zm0 5A.75.75 0 0 1 1.75 7h12.5a.75.75 0 0 1 0 1.5H1.75A.75.75 0 0 1 1 7.75ZM1.75 12h12.5a.75.75 0 0 1 0 1.5H1.75a.75.75 0 0 1 0-1.5Z"/></svg></button>
      <div class="hdr-info">
        <div class="hdr-av"><span>N</span><div class="online-dot"></div></div>
        <div><div class="hdr-name">Nexus</div><div class="hdr-sub">Active now · Anervea AI</div></div>
      </div>
      <button class="icon-btn" onclick="clearChat()" title="Clear">
        <svg viewBox="0 0 16 16"><path d="M11 1.75V3h2.25a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1 0-1.5H5V1.75C5 .784 5.784 0 6.75 0h2.5C10.216 0 11 .784 11 1.75ZM4.496 6.675l.66 6.6a.25.25 0 0 0 .249.225h5.19a.25.25 0 0 0 .249-.225l.66-6.6a.75.75 0 0 1 1.492.149l-.66 6.6A1.748 1.748 0 0 1 10.595 15h-5.19a1.75 1.75 0 0 1-1.741-1.575l-.66-6.6a.75.75 0 1 1 1.492-.15ZM6.5 1.75V3h3V1.75a.25.25 0 0 0-.25-.25h-2.5a.25.25 0 0 0-.25.25Z"/></svg>
      </button>
    </header>
    <div class="msgs" id="msgs"><div class="msgs-inner" id="feed"></div></div>
    <div class="suggestions" id="chips"></div>
    <div class="input-wrap">
      <div class="input-row">
        <textarea id="inp" rows="1" placeholder="Message Nexus..." oninput="onInput()" onkeydown="onKey(event)"></textarea>
        <button class="send-btn" id="sbtn" onclick="send()" disabled>
          <svg viewBox="0 0 16 16"><path d="M.989 8 .064 2.68a1.342 1.342 0 0 1 1.85-1.462l13.402 5.744a1.13 1.13 0 0 1 0 2.076L1.913 14.782a1.343 1.343 0 0 1-1.85-1.463L.99 8Zm.603-5.378.93 4.78h5.795a.75.75 0 0 1 0 1.5H2.522l-.93 4.78L13.496 8Z"/></svg>
        </button>
      </div>
      <p class="hint">Return to send &middot; Shift+Return for new line</p>
    </div>
  </main>
</div>
<script>
(function(){var m=document.cookie.match(/uname=([^;]+)/);if(m){var n=decodeURIComponent(m[1]);var el=document.getElementById('uname');if(el)el.textContent=n;var av=document.getElementById('uav');if(av)av.textContent=n.charAt(0).toUpperCase();}})();
var SUGG=['What can you help me with?','Tell me about Anervea AI','How does competitive intelligence work?','What is AlfaKinetic?'];
var RES={anervea:"Anervea AI builds intelligent platforms that transform how organizations understand their competitive landscape.",competitive:"Competitive intelligence involves gathering, analyzing, and acting on information about competitors, markets, and industry trends.",intelligence:"Competitive intelligence involves gathering, analyzing, and acting on information about competitors, markets, and industry trends.",alfakinetic:"AlfaKinetic is Anervea\u2019s flagship CI platform \u2014 synthesizing signals from multiple data sources into actionable insights for pharma and life sciences.",alfa:"AlfaKinetic is Anervea\u2019s flagship CI platform for pharma and life sciences.",help:"I\u2019m Nexus, your AI assistant by Anervea. I can help with competitive intelligence, research, and strategic insights.",data:"I can analyze data patterns, summarize research, and provide strategic recommendations.",analyze:"I can analyze data patterns and provide strategic recommendations."};
var FB=["I\u2019m Nexus by Anervea. Ask me about markets, competitors, or industry trends.","Great question! I\u2019m here to help. What would you like to know?","Could you clarify that? I want to give you the most precise answer.","I can help with competitive intelligence, research summaries, and strategic insights."];
function fmt(t){return t.replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>').replace(/`(.*?)`/g,'<code>$1</code>');}
function ts(){return new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});}
function uname(){return(document.getElementById('uname')||{textContent:'You'}).textContent;}
function addMsg(r,t){
  var u=r==='user';
  var row=document.createElement('div');row.className='msg-row '+(u?'user':'bot');
  row.innerHTML='<div class="av '+(u?'usr':'bot')+'"><span>'+(u?uname().charAt(0).toUpperCase():'N')+'</span></div>'+
    '<div class="msg-content"><div class="msg-meta"><span class="mname">'+(u?uname():'Nexus')+'</span><span class="mtime">'+ts()+'</span></div>'+
    '<div class="bubble '+(u?'usr':'bot')+'">'+fmt(t)+'</div></div>';
  document.getElementById('feed').appendChild(row);scroll();
  if(u)document.getElementById('chips').style.display='none';
}
function showTyp(){var e=document.createElement('div');e.className='typing-row';e.id='typ';e.innerHTML='<div class="av bot"><span>N</span></div><div class="typing-bubble"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>';document.getElementById('feed').appendChild(e);scroll();}
function hideTyp(){var e=document.getElementById('typ');if(e)e.remove();}
function scroll(){var m=document.getElementById('msgs');m.scrollTop=m.scrollHeight;}
function reply(t){var l=t.toLowerCase();for(var k in RES){if(l.indexOf(k)>=0)return RES[k];}return FB[Math.floor(Math.random()*FB.length)];}
function send(t){var inp=document.getElementById('inp');var msg=(t||inp.value).trim();if(!msg)return;addMsg('user',msg);inp.value='';onInput();showTyp();setTimeout(function(){hideTyp();addMsg('bot',reply(msg));},1000+Math.random()*800);inp.focus();}
function onInput(){var inp=document.getElementById('inp');var btn=document.getElementById('sbtn');var has=inp.value.trim().length>0;btn.disabled=!has;btn.className='send-btn'+(has?' on':'');inp.style.height='auto';inp.style.height=Math.min(inp.scrollHeight,120)+'px';}
function onKey(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();}}
function clearChat(){document.getElementById('feed').innerHTML='';var sep=document.createElement('div');sep.className='date-sep';sep.textContent=new Date().toLocaleDateString([],{weekday:'long',month:'long',day:'numeric'});document.getElementById('feed').appendChild(sep);addMsg('bot','Chat cleared. Start a new conversation!');document.getElementById('chips').style.display='none';closeSb();}
function toggleSb(){document.getElementById('sb').classList.toggle('open');}
function closeSb(){document.getElementById('sb').classList.remove('open');}
var sep=document.createElement('div');sep.className='date-sep';sep.textContent=new Date().toLocaleDateString([],{weekday:'long',month:'long',day:'numeric'});document.getElementById('feed').appendChild(sep);
addMsg('bot','Hello! I am **Nexus**, your AI assistant by Anervea. How can I help you today?');
var chips=document.getElementById('chips');SUGG.forEach(function(s){var b=document.createElement('button');b.className='chip';b.textContent=s;b.onclick=function(){send(s);};chips.appendChild(b);});
</script></body></html>
"""

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    if not get_user(request): return RedirectResponse('/login', status_code=302)
    return HTMLResponse(content=CHAT_HTML)

@app.get('/login', response_class=HTMLResponse)
async def login_get(request: Request):
    if get_user(request): return RedirectResponse('/', status_code=302)
    return HTMLResponse(content=LOGIN_HTML.replace('ERROR_PLACEHOLDER', ''))

@app.post('/login')
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if USERS.get(username) == password:
        token = SIGNER.dumps(username)
        resp = RedirectResponse('/', status_code=302)
        resp.set_cookie('session', token, httponly=True, max_age=86400, samesite='lax')
        resp.set_cookie('uname', username, max_age=86400, samesite='lax')
        return resp
    err = '<div class="error"><svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" style="flex-shrink:0"><path d="M6.457 1.047c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0 1 14.082 15H1.918a1.75 1.75 0 0 1-1.543-2.575Zm1.763.707a.25.25 0 0 0-.44 0L1.698 13.132a.25.25 0 0 0 .22.368h12.164a.25.25 0 0 0 .22-.368Zm.53 3.996v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"/></svg> Incorrect username or password.</div>'
    return HTMLResponse(content=LOGIN_HTML.replace('ERROR_PLACEHOLDER', err), status_code=401)

@app.post('/logout')
async def logout():
    resp = RedirectResponse('/login', status_code=302)
    resp.delete_cookie('session'); resp.delete_cookie('uname')
    return resp

@app.get('/{full_path:path}', response_class=HTMLResponse)
async def catch_all(request: Request, full_path: str):
    if not get_user(request): return RedirectResponse('/login', status_code=302)
    return HTMLResponse(content=CHAT_HTML)
