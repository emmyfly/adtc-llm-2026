#!/bin/bash
~/adtc-llm/llama.cpp/build/bin/llama-server \
  -m ~/adtc-llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf \
  --port 8080 \
  -t 4 \
  -c 512 \
  -b 512 \
  -np 1 \
  --flash-attn on \
  --mlock
