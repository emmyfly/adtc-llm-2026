#!/bin/bash
echo "Starting AgriLM - Offline Agricultural Advisor"
echo "Loading model... (this takes about 15 seconds)"

MODEL="models/qwen2.5-3b-instruct-q4_k_m.gguf"
if [ ! -f "$MODEL" ]; then
    echo "Model not found. Download it first:"
    echo "wget https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf -P models/"
    exit 1
fi

./llama.cpp/build/bin/llama-server -m "$MODEL" --port 8080 &
SERVER_PID=$!
sleep 15

echo "Server ready. Starting advisor..."
python3 agrilm.py

kill $SERVER_PID
