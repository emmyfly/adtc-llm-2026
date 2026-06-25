import requests
import os

URL = "http://localhost:8080/v1/chat/completions"

prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
with open(prompt_path, "r") as f:
    SYSTEM = f.read()

def ask(question):
    response = requests.post(URL, json={
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": question},
        ],
        "max_tokens": 256,
        "temperature": 0.7,
    })
    data = response.json()
    return data["choices"][0]["message"]["content"]

print("=" * 50)
print("  AgriLM - Nigerian Agricultural Advisor")
print("  Offline AI · No Internet Required")
print("  Powered by Qwen2.5-3B on llama.cpp")
print("  Type 'quit' to exit")
print("=" * 50)

while True:
    question = input("\nFarmer: ")
    if question.lower() in ["quit", "exit", "q"]:
        print("Goodbye! Happy farming!")
        break
    if not question.strip():
        continue
    print("\nAgriLM:", ask(question))
