import requests
import os
from rag import get_context

URL = "http://localhost:8080/v1/chat/completions"

prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
with open(prompt_path, "r") as f:
    SYSTEM = f.read()

history = [{"role": "system", "content": SYSTEM}]

def ask(question):
    context = get_context(question)
    if context:
        enriched = context + "\n\n" + question
    else:
        enriched = question
    
    history.append({"role": "user", "content": enriched})
    
    response = requests.post(URL, json={
        "messages": history,
        "max_tokens": 256,
        "temperature": 0.7,
    })
    data = response.json()
    answer = data["choices"][0]["message"]["content"]
    
    history.append({"role": "assistant", "content": answer})
    return answer

print("=" * 50)
print("  AgriLM - Nigerian Agricultural Advisor")
print("  Offline AI · No Internet Required")
print("  Powered by Qwen2.5-3B + Nigerian Agri Knowledge Base")
print("  Type 'quit' to exit | 'clear' to reset")
print("=" * 50)

while True:
    question = input("\nFarmer: ")
    if question.lower() in ["quit", "exit", "q"]:
        print("Goodbye! Happy farming!")
        break
    if question.lower() == "clear":
        history = [{"role": "system", "content": SYSTEM}]
        print("Conversation cleared.")
        continue
    if not question.strip():
        continue
    print("\nAgriLM:", ask(question))
