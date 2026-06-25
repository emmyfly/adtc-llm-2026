import requests
import time

URL = "http://localhost:8080/v1/chat/completions"
SYSTEM = "You are AgriLM, an agricultural advisor for Nigerian farmers. Give specific, practical advice."

def ask_llm(question, max_tokens=128):
    start = time.time()
    response = requests.post(URL, json={
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": question},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    })
    elapsed = time.time() - start
    data = response.json()
    answer = data["choices"][0]["message"]["content"]
    return {"question": question, "answer": answer, "time_seconds": round(elapsed, 2)}

questions = [
    "What crops grow best in Lagos Nigeria during rainy season?",
    "What is the best soil type for growing cassava in Nigeria?",
    "How do I prevent tomato blight during rainy season?",
    "When should I plant maize in southwestern Nigeria?",
    "What organic fertilizers work for yam farming?",
]

print("=== AgriLM 3B Benchmark ===\n")

results = []
for q in questions:
    r = ask_llm(q)
    results.append(r)
    print(f"Q: {r['question']}")
    print(f"A: {r['answer'][:400]}")
    print(f"Time: {r['time_seconds']}s\n")

avg_time = sum(r["time_seconds"] for r in results) / len(results)
print(f"=== Average response time: {avg_time:.2f}s ===")
print(f"=== Model: Qwen2.5-3B Q4_K_M ===")
