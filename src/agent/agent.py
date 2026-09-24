from ollama import Client
from tools.calculator import Calculator

class Agent:

    def __init__(self):
        self.calculator = Calculator()
        self.client = Client()
        
    def ask(self, question):

        messages = [
        {
            "role": "user",
            "content": question,
        }
    ]

        answer = self.client.chat(
            model="qwen3:4b",
            messages=messages,
            tools=self.tools
    )

        messages.append(answer.message)
        
        tool_call = answer.message.tool_calls[0]

        expression = tool_call.function.arguments["expression"]

        result = self.calculator.calculate(expression)
        
        messages.append({
            "role": "tool",
            "tool_name": "calculator",
            "content": str(result)
})
        answer = self.client.chat(
            model="qwen3:4b",
            messages=messages
    )

        return answer["message"]["content"]
    
    tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Realiza cálculos matemáticos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Expressão matemática a ser calculada."
                    }
                },
                "required": ["expression"]
            }
        }
    }
]