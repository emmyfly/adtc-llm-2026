#!/bin/bash
echo "========================================"
echo "  AgriLM - Nigerian Agricultural Advisor"
echo "  Offline AI · No Internet Required"
echo "========================================"

MODEL="models/qwen2.5-3b-instruct-q4_k_m.gguf"
if [ ! -f "$MODEL" ]; then
    echo "Model not found. Download it:"
    echo "wget https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf -P models/"
    exit 1
fi

echo "Starting model server..."
./llama.cpp/build/bin/llama-server -m "$MODEL" --port 8080 &
SERVER_PID=$!
sleep 15
echo "Model loaded."

echo ""
echo "Choose interface:"
echo "  1. Web Browser (recommended)"
echo "  2. Terminal"
read -p "Select (1/2): " choice

if [ "$choice" = "1" ]; then
    echo "Opening web interface at http://localhost:5000"
    python3 web_app.py
else
    python3 agrilm.py
fi

kill $SERVER_PID
