import requests

URL = "http://localhost:8080/v1/chat/completions"
SYSTEM = """You are AgriLM, an agricultural advisor for Nigerian farmers.
You give specific, practical advice about farming in Nigeria.
You know about crops, soil types, seasons, pest control, fertilizers,
and farming practices specific to different regions of Nigeria.
Keep answers concise and actionable."""

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
print("  Offline AI for Nigerian Farmers")
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
