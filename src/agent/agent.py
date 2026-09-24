from ollama import Client
from tools.calculator import Calculator

class Agent:

    def __init__(self):
        self.calculator = Calculator()
        self.client = Client()
        
    def ask(self, question):

        messages = [
        {
            "role": "system",
            "content": "Você é um agente para auxiliar o usuário. Responda usando seu próprio conhecimento quando puder. Use as ferramentas disponíveis somente quando forem necessárias."
        },
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
        
        if answer.message.tool_calls:
            
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
        else:
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