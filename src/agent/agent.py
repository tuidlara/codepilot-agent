from ollama import Client

class Agent:

    def __init__(self):
        self.client = Client()
        
    def ask(self, question):
        answer = self.client.chat(
     model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

        return answer["message"]["content"]