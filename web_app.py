from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests
import os
import subprocess
import tempfile

from rag import get_context
from preprocessor import preprocess
from image_classifier import classify_image

LLM_URL = "http://localhost:8080/v1/chat/completions"
WHISPER_CLI = os.path.expanduser("~/adtc-llm/whisper.cpp/build/bin/whisper-cli")
WHISPER_MODEL = os.path.expanduser("~/adtc-llm/whisper.cpp/models/ggml-base.bin")

prompt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_prompt.txt")
with open(prompt_path, "r") as f:
    SYSTEM = f.read()

HTML = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")).read()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML.encode())

    def do_POST(self):
        if self.path == "/ask":
            length = int(self.headers["Content-Length"])
            body = json.loads(self.rfile.read(length))
            question = body["question"]
            question = preprocess(question)
            history = body.get("history", [])
            if not history:
                history = [{"role": "system", "content": SYSTEM}]
            context = get_context(question)
            enriched = (context + "\n\n" + question) if context else question
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
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"answer": answer, "history": history}).encode())

        elif self.path == "/transcribe":
            length = int(self.headers["Content-Length"])
            raw = self.rfile.read(length)
            
            boundary = self.headers["Content-Type"].split("boundary=")[1].encode()
            parts = raw.split(b"--" + boundary)
            audio_data = None
            for part in parts:
                if b"audio" in part and b"\r\n\r\n" in part:
                    audio_data = part.split(b"\r\n\r\n", 1)[1].rstrip(b"\r\n--")
                    break
            
            if not audio_data:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"text": "No audio received"}).encode())
                return
            
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
                tmp.write(audio_data)
                webm_path = tmp.name
            
            wav_path = webm_path.replace(".webm", ".wav")
            subprocess.run(
                ["ffmpeg", "-y", "-i", webm_path, "-ar", "16000", "-ac", "1", wav_path],
                capture_output=True, timeout=10
            )
            os.unlink(webm_path)
            
            result = subprocess.run(
                [WHISPER_CLI, "-m", WHISPER_MODEL, "-f", wav_path, "--no-timestamps", "-t", "4"],
                capture_output=True, text=True, timeout=30
            )
            os.unlink(wav_path)
            
            text = result.stdout.strip()
            text = text.replace("[BLANK_AUDIO]", "").strip()
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"text": text}).encode())
        elif self.path == "/classify":
            length = int(self.headers["Content-Length"])
            raw = self.rfile.read(length)

            boundary = self.headers["Content-Type"].split("boundary=")[1].encode()
            parts = raw.split(b"--" + boundary)
            image_data = None
            question = ""
            for part in parts:
                if b"image" in part and b"\r\n\r\n" in part:
                    image_data = part.split(b"\r\n\r\n", 1)[1].rstrip(b"\r\n--")
                if b"question" in part and b"\r\n\r\n" in part:
                    question = part.split(b"\r\n\r\n", 1)[1].rstrip(b"\r\n--").decode()

            if not image_data:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"text": "No image received"}).encode())
                return

            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                tmp.write(image_data)
                img_path = tmp.name

            label, confidence = classify_image(img_path)
            os.unlink(img_path)

            diagnosis = f"Plant disease identified: {label} (confidence: {confidence:.0%})"
            if question:
                question = preprocess(question)
                enriched = f"{diagnosis}\n\nFarmer asks: {question}"
            else:
                enriched = f"{diagnosis}\nPlease advise the farmer on treatment and prevention."

            context = get_context(label)
            if context:
                enriched = context + "\n\n" + enriched

            history = [{"role": "system", "content": SYSTEM}]
            history.append({"role": "user", "content": enriched})
            response = requests.post(LLM_URL, json={
                "messages": history,
                "max_tokens": 256,
                "temperature": 0.7,
            })
            data = response.json()
            answer = data["choices"][0]["message"]["content"]

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"diagnosis": label, "confidence": f"{confidence:.0%}", "answer": answer}).encode())


    def log_message(self, format, *args):
        pass

print("AgriLM Web UI running at http://localhost:5001")
print("Make sure llama-server is running on port 8080")
HTTPServer(("", 5001), Handler).serve_forever()
