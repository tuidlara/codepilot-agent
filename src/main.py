from ollama import Client

client = Client()

question = "Explique de forma concisa o que é inteligência artificial."

answer = client.chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "user",
            "content": question
        }
    ]
)

print(answer["message"]["content"])