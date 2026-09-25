from ollama import Client
from tools.calculator import Calculator
from tools.file_reader import FileReader
from tools.project_explorer import ProjectExplorer
from tools.code_searcher import CodeSearcher


class Agent:

    def __init__(self):
        self.calculator = Calculator()
        self.client = Client()
        self.file_reader = FileReader()
        self.project_explorer = ProjectExplorer()
        self.code_searcher = CodeSearcher()

        self.tool_handlers = {
            "calculator": self.calculator,
            "file_reader": self.file_reader,
            "project_explorer": self.project_explorer,
            "code_searcher": self.code_searcher,
        }

    def ask(self, question):

        # prompt ajustado
        messages = [
            {
                "role": "system",
                "content": "Você é um agente para auxiliar o usuário. Responda usando seu próprio conhecimento quando puder. Use as ferramentas disponíveis somente quando forem necessárias.",
            },
            {
                "role": "user",
                "content": question,
            },
        ]

        answer = self.client.chat(model="qwen3:4b", messages=messages, tools=self.tools)

        messages.append(answer.message)

        while answer.message.tool_calls:

            for tool_call in answer.message.tool_calls:

                tool_name = tool_call.function.name
                tool = self.tool_handlers[tool_name]

                arguments = tool_call.function.arguments

                try:
                    if arguments:
                        # pega o primeiro argumento enviado pela ferramenta
                        argument = next(iter(arguments.values()))
                        result = tool.execute(argument)
                    else:
                        result = tool.execute()
                except ValueError as error:
                    result = str(error)

                messages.append(
                    {"role": "tool", "tool_name": tool_name, "content": str(result)}
                )
            answer = self.client.chat(
                model="qwen3:4b", messages=messages, tools=self.tools
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
                            "description": "Expressão matemática a ser calculada.",
                        }
                    },
                    "required": ["expression"],
                },
            },
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
                            "description": "Caminho do arquivo que deve ser lido.",
                        }
                    },
                    "required": ["file_path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "project_explorer",
                "description": "Lista os arquivos do projeto para entender sua estrutura.",
                "parameters": {"type": "object", "properties": {}, "required": []},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "code_searcher",
                "description": "Procura um texto ou termo nos arquivos do projeto e retorna onde ele foi encontrado.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Texto ou termo que deve ser procurado no projeto.",
                        }
                    },
                    "required": ["pattern"],
                },
            },
        },
    ]
