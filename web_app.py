from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import requests
import os
from rag import get_context

LLM_URL = "http://localhost:8080/v1/chat/completions"

prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
with open(prompt_path, "r") as f:
    SYSTEM = f.read()

HTML = """<!DOCTYPE html>
<html>
<head>
<title>AgriLM - Nigerian Agricultural Advisor</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, sans-serif; background: #f0f4f0; height: 100vh; display: flex; flex-direction: column; }
.header { background: #1a5c2e; color: white; padding: 16px; text-align: center; }
.header h1 { font-size: 20px; }
.header p { font-size: 12px; opacity: 0.8; }
.chat { flex: 1; overflow-y: auto; padding: 16px; }
.msg { margin: 8px 0; padding: 12px 16px; border-radius: 12px; max-width: 85%; line-height: 1.5; }
.user { background: #1a5c2e; color: white; margin-left: auto; text-align: right; }
.bot { background: white; border: 1px solid #ddd; }
.bot pre { white-space: pre-wrap; font-family: inherit; }
.input-area { padding: 12px; background: white; border-top: 1px solid #ddd; display: flex; gap: 8px; }
.input-area input { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; }
.input-area button { padding: 12px 24px; background: #1a5c2e; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
.loading { color: #888; font-style: italic; }
.badge { display: inline-block; background: #e8f5e9; color: #1a5c2e; padding: 2px 8px; border-radius: 4px; font-size: 11px; margin-top: 4px; }
</style>
</head>
<body>
<div class="header">
    <h1>AgriLM</h1>
    <p>Offline AI Agricultural Advisor for Nigerian Farmers</p>
    <span class="badge">No Internet Required</span>
</div>
<div class="chat" id="chat">
    <div class="msg bot">Welcome! I am AgriLM, your agricultural advisor. Ask me anything about farming in Nigeria. I work completely offline.<br><br>Try: "What crops grow best in Lagos during rainy season?"</div>
</div>
<div class="input-area">
    <input type="text" id="input" placeholder="Ask about farming..." autofocus>
    <button onclick="send()">Ask</button>
</div>
<script>
const chat = document.getElementById('chat');
const input = document.getElementById('input');
let history = [];

input.addEventListener('keypress', e => { if(e.key==='Enter') send(); });

async function send() {
    const q = input.value.trim();
    if(!q) return;
    input.value = '';
    
    chat.innerHTML += '<div class="msg user">' + q + '</div>';
    chat.innerHTML += '<div class="msg bot loading" id="loading">Thinking...</div>';
    chat.scrollTop = chat.scrollHeight;
    
    try {
        const res = await fetch('/ask', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({question: q, history: history})
        });
        const data = await res.json();
        history = data.history;
        document.getElementById('loading').remove();
        chat.innerHTML += '<div class="msg bot"><pre>' + data.answer + '</pre></div>';
    } catch(e) {
        document.getElementById('loading').remove();
        chat.innerHTML += '<div class="msg bot">Error connecting to model. Make sure llama-server is running.</div>';
    }
    chat.scrollTop = chat.scrollHeight;
}
</script>
</body>
</html>"""

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML.encode())
    
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))
        
        question = body['question']
        history = body.get('history', [])
        
        if not history:
            history = [{"role": "system", "content": SYSTEM}]
        
        context = get_context(question)
        enriched = (context + "\\n\\n" + question) if context else question
        history.append({"role": "user", "content": enriched})
        
        response = requests.post(LLM_URL, json={
            "messages": history,
            "max_tokens": 256,
            "temperature": 0.7,
        })
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        history.append({"role": "assistant", "content": answer})
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"answer": answer, "history": history}).encode())
    
    def log_message(self, format, *args):
        pass

print("AgriLM Web UI running at http://localhost:5001")
print("Make sure llama-server is running on port 8080")
HTTPServer(('', 5001), Handler).serve_forever()
