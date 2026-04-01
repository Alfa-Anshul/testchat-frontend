from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature

app = FastAPI()

SECRET = "nexus-anervea-secret-2025"
SIGNER = URLSafeTimedSerializer(SECRET)
USERS = {"aniket": "Password@123"}

def get_user(request: Request):
    token = request.cookies.get("session")
    if not token:
        return None
    try:
        return SIGNER.loads(token, max_age=86400)
    except BadSignature:
        return None

LOGIN_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>NexusChat — Login</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{min-height:100vh;background:#0a0a0f;color:#e8e8f0;font-family:'Syne',sans-serif;display:flex;align-items:center;justify-content:center;padding:20px}
.bg-grid{position:fixed;inset:0;background-image:linear-gradient(rgba(124,106,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(124,106,255,.04) 1px,transparent 1px);background-size:40px 40px;pointer-events:none}
.glow{position:fixed;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(124,106,255,.12) 0%,transparent 70%);top:-200px;left:50%;transform:translateX(-50%);pointer-events:none}
.card{position:relative;background:#111118;border:1px solid #2a2a3a;border-radius:24px;padding:48px 40px;width:100%;max-width:420px;box-shadow:0 24px 80px rgba(0,0,0,.6),0 0 0 1px rgba(124,106,255,.08)}
.logo-row{display:flex;align-items:center;gap:12px;margin-bottom:32px}
.logo-mark{width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,#7c6aff,#ff6a9e);display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800;color:#fff}
.logo-text{font-size:24px;font-weight:800;letter-spacing:-.5px;background:linear-gradient(90deg,#7c6aff,#ff6a9e);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.tagline{font-size:13px;color:#7070a0;font-family:'DM Mono',monospace;font-weight:300;margin-bottom:32px;padding-bottom:32px;border-bottom:1px solid #2a2a3a}
.field-label{font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#7070a0;margin-bottom:8px;display:block}
.field{width:100%;background:#18181f;border:1px solid #2a2a3a;border-radius:12px;padding:12px 16px;color:#e8e8f0;font-family:'Syne',sans-serif;font-size:14px;outline:none;transition:border-color .2s,box-shadow .2s;margin-bottom:20px}
.field:focus{border-color:#7c6aff;box-shadow:0 0 0 3px rgba(124,106,255,.12)}
.field::placeholder{color:#3a3a5a}
.btn{width:100%;background:linear-gradient(135deg,#7c6aff,#ff6a9e);border:none;border-radius:12px;padding:14px;color:#fff;font-family:'Syne',sans-serif;font-size:15px;font-weight:700;cursor:pointer;transition:all .2s;box-shadow:0 4px 20px rgba(124,106,255,.3);margin-top:4px}
.btn:hover{transform:translateY(-1px);box-shadow:0 8px 28px rgba(124,106,255,.4)}
.error{background:rgba(255,106,158,.08);border:1px solid rgba(255,106,158,.25);border-radius:10px;padding:10px 14px;font-size:13px;color:#ff6a9e;margin-bottom:20px;display:flex;align-items:center;gap:8px}
.footer{text-align:center;margin-top:28px;font-size:11px;color:#3a3a5a;font-family:'DM Mono',monospace}
</style>
</head>
<body>
<div class="bg-grid"></div>
<div class="glow"></div>
<div class="card">
  <div class="logo-row">
    <div class="logo-mark">N</div>
    <span class="logo-text">NexusChat</span>
  </div>
  <p class="tagline">Powered by Anervea AI · Sign in to continue</p>
  ERROR_PLACEHOLDER
  <form method="post" action="/login">
    <label class="field-label" for="u">Username</label>
    <input class="field" id="u" name="username" type="text" placeholder="Enter your username" autocomplete="username" required/>
    <label class="field-label" for="p">Password</label>
    <input class="field" id="p" name="password" type="password" placeholder="Enter your password" autocomplete="current-password" required/>
    <button class="btn" type="submit">Sign In →</button>
  </form>
  <p class="footer">NexusChat · Anervea AI © 2025</p>
</div>
</body>
</html>
"""

CHAT_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>NexusChat — Anervea AI</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0a0a0f;--surface:#111118;--surface2:#18181f;--border:#2a2a3a;--accent:#7c6aff;--accent2:#ff6a9e;--accent3:#6affd4;--text:#e8e8f0;--text-dim:#7070a0;--text-dimmer:#3a3a5a;--user-bubble:#1e1a3a;--bot-bubble:#181822;--font:'Syne',sans-serif;--mono:'DM Mono',monospace;--r:18px;--rs:10px}
html,body{height:100%;background:var(--bg);color:var(--text);font-family:var(--font);overflow:hidden}
::-webkit-scrollbar{width:4px}::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}
.shell{display:flex;height:100vh;width:100vw;overflow:hidden}
.sidebar{width:260px;min-width:260px;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;padding:24px 0 0;transition:transform .3s cubic-bezier(.4,0,.2,1);z-index:100}
.sb-head{display:flex;align-items:center;gap:10px;padding:0 20px 24px;border-bottom:1px solid var(--border)}
.logo-mark{width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:800;color:#fff;flex-shrink:0}
.logo-txt{font-size:20px;font-weight:800;letter-spacing:-.5px;background:linear-gradient(90deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sb-nav{flex:1;padding:16px 12px;display:flex;flex-direction:column;gap:4px}
.nav-btn{display:flex;align-items:center;gap:10px;background:none;border:none;color:var(--text-dim);font-family:var(--font);font-size:14px;font-weight:500;padding:10px 12px;border-radius:var(--rs);cursor:pointer;transition:all .2s;text-align:left;width:100%}
.nav-btn:hover{background:var(--surface2);color:var(--text)}
.nav-btn.active{color:var(--accent);background:rgba(124,106,255,.08)}
.nav-icon{font-size:16px}
.sb-user{padding:16px 20px;border-top:1px solid var(--border)}
.user-row{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.user-av{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px;color:#fff;flex-shrink:0}
.user-name{font-size:13px;font-weight:600;color:var(--text)}
.user-role{font-size:10px;color:var(--text-dimmer);font-family:var(--mono)}
.logout-btn{display:flex;align-items:center;gap:8px;background:none;border:1px solid var(--border);color:var(--text-dim);font-family:var(--font);font-size:12px;font-weight:500;padding:8px 12px;border-radius:var(--rs);cursor:pointer;transition:all .2s;width:100%}
.logout-btn:hover{border-color:var(--accent2);color:var(--accent2)}
.overlay{display:none;position:fixed;inset:0;background:#0009;z-index:90;backdrop-filter:blur(2px)}
.main{flex:1;display:flex;flex-direction:column;min-width:0;background:var(--bg)}
.hdr{display:flex;align-items:center;gap:12px;padding:14px 20px;border-bottom:1px solid var(--border);background:var(--surface);z-index:10}
.menu-btn{display:none;flex-direction:column;gap:4px;background:none;border:none;cursor:pointer;padding:4px}
.menu-btn span{display:block;width:20px;height:2px;background:var(--text-dim);border-radius:2px}
.hdr-info{flex:1;display:flex;align-items:center;gap:10px}
.bot-av{width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;color:#fff;position:relative;flex-shrink:0}
.pulse{position:absolute;bottom:1px;right:1px;width:10px;height:10px;border-radius:50%;background:var(--accent3);border:2px solid var(--surface)}
.bot-name{font-size:15px;font-weight:700;letter-spacing:-.3px}
.bot-status{font-size:11px;color:var(--accent3);font-family:var(--mono);font-weight:300}
.clr-btn{background:none;border:1px solid var(--border);color:var(--text-dim);width:32px;height:32px;border-radius:8px;cursor:pointer;font-size:13px;transition:all .2s}
.clr-btn:hover{color:var(--accent2);border-color:var(--accent2)}
.msgs{flex:1;overflow-y:auto;padding:24px 0}
.msgs-inner{max-width:760px;margin:0 auto;padding:0 20px;display:flex;flex-direction:column;gap:16px}
.msg-row{display:flex;align-items:flex-end;gap:10px;animation:fadeUp .3s ease both}
.msg-row.user{flex-direction:row-reverse}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.av{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;flex-shrink:0;margin-bottom:18px}
.av.bot{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff}
.av.usr{background:var(--surface2);border:1px solid var(--border);color:var(--text-dim)}
.msg-content{max-width:75%;display:flex;flex-direction:column;gap:4px}
.bubble{padding:12px 16px;border-radius:var(--r);font-size:14px;line-height:1.65;word-break:break-word}
.bubble.bot{background:var(--bot-bubble);border:1px solid var(--border);border-bottom-left-radius:4px;color:var(--text)}
.bubble.usr{background:var(--user-bubble);border:1px solid rgba(124,106,255,.2);border-bottom-right-radius:4px;color:var(--text)}
.bubble strong{color:var(--accent);font-weight:600}
.bubble code{font-family:var(--mono);font-size:12px;background:rgba(124,106,255,.1);padding:2px 6px;border-radius:4px;color:var(--accent3)}
.msg-time{font-size:10px;color:var(--text-dimmer);font-family:var(--mono);padding:0 4px}
.msg-time.r{text-align:right}
.typing-row{display:flex;align-items:flex-end;gap:10px;animation:fadeUp .2s ease both}
.typing-bubble{background:var(--bot-bubble);border:1px solid var(--border);border-radius:var(--r);border-bottom-left-radius:4px;padding:14px 18px;display:flex;gap:5px;align-items:center}
.dot{width:6px;height:6px;background:var(--accent);border-radius:50%;animation:bounce 1.2s infinite ease-in-out}
.dot:nth-child(2){animation-delay:.2s}.dot:nth-child(3){animation-delay:.4s}
@keyframes bounce{0%,80%,100%{transform:translateY(0);opacity:.4}40%{transform:translateY(-6px);opacity:1}}
.suggestions{display:flex;flex-wrap:wrap;gap:8px;padding:0 20px 16px;max-width:760px;margin:0 auto;width:100%}
.chip{background:var(--surface2);border:1px solid var(--border);color:var(--text-dim);font-family:var(--font);font-size:12px;font-weight:500;padding:7px 14px;border-radius:50px;cursor:pointer;transition:all .2s}
.chip:hover{border-color:var(--accent);color:var(--accent);background:rgba(124,106,255,.06)}
.input-area{padding:16px 20px 20px;border-top:1px solid var(--border);background:var(--surface);display:flex;flex-direction:column;align-items:center;gap:6px}
.input-box{display:flex;align-items:flex-end;gap:10px;width:100%;max-width:760px;background:var(--surface2);border:1px solid var(--border);border-radius:var(--r);padding:10px 10px 10px 16px;transition:border-color .2s}
.input-box:focus-within{border-color:var(--accent)}
#inp{flex:1;background:none;border:none;color:var(--text);font-family:var(--font);font-size:14px;resize:none;outline:none;line-height:1.5;max-height:120px;min-height:22px}
#inp::placeholder{color:var(--text-dimmer)}
.send-btn{width:36px;height:36px;flex-shrink:0;border-radius:10px;background:var(--border);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--text-dim);transition:all .2s}
.send-btn svg{width:16px;height:16px}
.send-btn.on{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;box-shadow:0 4px 16px rgba(124,106,255,.35)}
.send-btn.on:hover{transform:scale(1.07)}
.hint{font-size:11px;color:var(--text-dimmer);font-family:var(--mono);font-weight:300}
@media(max-width:700px){.sidebar{position:fixed;left:0;top:0;bottom:0;transform:translateX(-100%)}.sidebar.open{transform:translateX(0)}.overlay{display:block}.menu-btn{display:flex}}
</style>
</head>
<body>
<div class="shell">
  <aside class="sidebar" id="sb">
    <div class="sb-head"><div class="logo-mark">N</div><span class="logo-txt">Nexus</span></div>
    <nav class="sb-nav">
      <button class="nav-btn active"><span class="nav-icon">💬</span>Chat</button>
      <button class="nav-btn" onclick="clearChat()"><span class="nav-icon">🗑</span>Clear Chat</button>
    </nav>
    <div class="sb-user">
      <div class="user-row">
        <div class="user-av" id="uav">A</div>
        <div><div class="user-name" id="uname">aniket</div><div class="user-role">Anervea AI</div></div>
      </div>
      <form method="post" action="/logout">
        <button class="logout-btn" type="submit">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          Sign Out
        </button>
      </form>
    </div>
  </aside>
  <div class="overlay" id="ov" onclick="closeSb()"></div>
  <main class="main">
    <header class="hdr">
      <button class="menu-btn" onclick="toggleSb()"><span></span><span></span><span></span></button>
      <div class="hdr-info">
        <div class="bot-av"><span>N</span><div class="pulse"></div></div>
        <div><div class="bot-name">Nexus</div><div class="bot-status">Online · Anervea AI</div></div>
      </div>
      <button class="clr-btn" onclick="clearChat()">✕</button>
    </header>
    <div class="msgs" id="msgs"><div class="msgs-inner" id="feed"></div></div>
    <div class="suggestions" id="chips"></div>
    <div class="input-area">
      <div class="input-box">
        <textarea id="inp" rows="1" placeholder="Message Nexus..." oninput="onInput()" onkeydown="onKey(event)"></textarea>
        <button class="send-btn" id="sbtn" onclick="send()" disabled>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2L11 13"/><path d="M22 2L15 22L11 13L2 9L22 2Z"/></svg>
        </button>
      </div>
      <p class="hint">Enter to send · Shift+Enter for new line</p>
    </div>
  </main>
</div>
<script>
(function(){
  var m=document.cookie.match(/uname=([^;]+)/);
  if(m){var n=decodeURIComponent(m[1]);var el=document.getElementById('uname');if(el)el.textContent=n;var av=document.getElementById('uav');if(av)av.textContent=n.charAt(0).toUpperCase();}
})();
var SUGG=['What can you help me with?','Tell me about Anervea AI','How does competitive intelligence work?','What is AlfaKinetic?'];
var RES={anervea:"Anervea AI builds intelligent platforms that transform how organizations understand their competitive landscape.",competitive:"Competitive intelligence involves gathering, analyzing, and acting on information about competitors, markets, and industry trends.",intelligence:"Competitive intelligence involves gathering, analyzing, and acting on information about competitors, markets, and industry trends.",alfakinetic:"AlfaKinetic is Anervea\u2019s flagship CI platform \u2014 it synthesizes signals from multiple data sources into actionable insights for pharma and life sciences.",alfa:"AlfaKinetic is Anervea\u2019s flagship CI platform for pharma and life sciences.",help:"I\u2019m Nexus, your AI assistant by Anervea. I can help with competitive intelligence, research, and strategic insights.",data:"I can analyze data patterns, summarize research, and provide strategic recommendations.",analyze:"I can analyze data patterns, summarize research, and provide strategic recommendations."};
var FB=["I\u2019m Nexus by Anervea. Ask me about markets, competitors, or industry trends.","Great question! I\u2019m here to assist around the clock.","Could you clarify that? I want to give you the most precise answer.","I can help with competitive intelligence, research summaries, and strategic insights."];
function fmt(t){return t.replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>').replace(/`(.*?)`/g,'<code>$1</code>');}
function ts(){return new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});}
function addMsg(r,t){var u=r==='user';var row=document.createElement('div');row.className='msg-row '+(u?'user':'bot');row.innerHTML=(u?'':'<div class="av bot"><span>N</span></div>')+'<div class="msg-content"><div class="bubble '+(u?'usr':'bot')+'">'+fmt(t)+'</div><div class="msg-time '+(u?'r':'')+'">'+ts()+'</div></div>'+(u?'<div class="av usr"><span>U</span></div>':'');document.getElementById('feed').appendChild(row);scroll();if(u)document.getElementById('chips').style.display='none';}
function showTyp(){var e=document.createElement('div');e.className='typing-row';e.id='typ';e.innerHTML='<div class="av bot"><span>N</span></div><div class="typing-bubble"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>';document.getElementById('feed').appendChild(e);scroll();}
function hideTyp(){var e=document.getElementById('typ');if(e)e.remove();}
function scroll(){var m=document.getElementById('msgs');m.scrollTop=m.scrollHeight;}
function reply(t){var l=t.toLowerCase();for(var k in RES){if(l.indexOf(k)>=0)return RES[k];}return FB[Math.floor(Math.random()*FB.length)];}
function send(t){var inp=document.getElementById('inp');var msg=(t||inp.value).trim();if(!msg)return;addMsg('user',msg);inp.value='';onInput();showTyp();setTimeout(function(){hideTyp();addMsg('bot',reply(msg));},1100+Math.random()*900);inp.focus();}
function onInput(){var inp=document.getElementById('inp');var btn=document.getElementById('sbtn');var has=inp.value.trim().length>0;btn.disabled=!has;btn.className='send-btn'+(has?' on':'');inp.style.height='auto';inp.style.height=Math.min(inp.scrollHeight,120)+'px';}
function onKey(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();}}
function clearChat(){document.getElementById('feed').innerHTML='';addMsg('bot','Chat cleared. Start a new conversation!');document.getElementById('chips').style.display='none';closeSb();}
function toggleSb(){document.getElementById('sb').classList.toggle('open');}
function closeSb(){document.getElementById('sb').classList.remove('open');}
addMsg('bot','Hello! I am **Nexus**, your intelligent AI assistant by Anervea. How can I help you today?');
var chips=document.getElementById('chips');
SUGG.forEach(function(s){var b=document.createElement('button');b.className='chip';b.textContent=s;b.onclick=function(){send(s);};chips.appendChild(b);});
</script>
</body>
</html>
"""

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    if not get_user(request):
        return RedirectResponse('/login', status_code=302)
    return HTMLResponse(content=CHAT_HTML)

@app.get('/login', response_class=HTMLResponse)
async def login_get(request: Request):
    if get_user(request):
        return RedirectResponse('/', status_code=302)
    return HTMLResponse(content=LOGIN_HTML.replace('ERROR_PLACEHOLDER', ''))

@app.post('/login')
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if USERS.get(username) == password:
        token = SIGNER.dumps(username)
        resp = RedirectResponse('/', status_code=302)
        resp.set_cookie('session', token, httponly=True, max_age=86400, samesite='lax')
        resp.set_cookie('uname', username, max_age=86400, samesite='lax')
        return resp
    error = '<div class="error"><span>⚠️</span> Invalid username or password.</div>'
    return HTMLResponse(content=LOGIN_HTML.replace('ERROR_PLACEHOLDER', error), status_code=401)

@app.post('/logout')
async def logout():
    resp = RedirectResponse('/login', status_code=302)
    resp.delete_cookie('session')
    resp.delete_cookie('uname')
    return resp

@app.get('/{full_path:path}', response_class=HTMLResponse)
async def catch_all(request: Request, full_path: str):
    if not get_user(request):
        return RedirectResponse('/login', status_code=302)
    return HTMLResponse(content=CHAT_HTML)
