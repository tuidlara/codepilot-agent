from ollama import Client
from tools.calculator import Calculator
from tools.file_reader import FileReader

class Agent:

    def __init__(self):
        self.calculator = Calculator()
        self.client = Client()
        self.file_reader = FileReader()
        
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
            
            for tool_call in answer.message.tool_calls:

                tool_name = tool_call.function.name
            
                if tool_name == "calculator":
                    expression = tool_call.function.arguments["expression"]
                    result = self.calculator.calculate(expression)

                elif tool_name == "file_reader":
                    file_path = tool_call.function.arguments["file_path"]
                    result = self.file_reader.read(file_path)
        
                messages.append({
                    "role": "tool",
                    "tool_name": tool_name,
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
    },
    {
        "type": "function",
        "function": {
            "name": "file_reader",
            "description": "Lê o conteúdo de um arquivo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Caminho do arquivo que deve ser lido."
                    }
                },
                "required": ["file_path"]
            }
        }
    }
]