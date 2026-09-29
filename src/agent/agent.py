from ollama import Client
from tools.calculator import Calculator
from tools.file_reader import FileReader
from tools.project_explorer import ProjectExplorer
from tools.code_searcher import CodeSearcher


# orquestrador do projeto
class Agent:

    def __init__(self):
        self.calculator = Calculator()
        self.client = Client()
        self.file_reader = FileReader()
        self.project_explorer = ProjectExplorer()
        self.code_searcher = CodeSearcher()

        # ferramentas (tools)
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
                "content": """
Você é um agente de desenvolvimento de software.

Ajude o usuário a entender e trabalhar com o projeto atual.

Ferramentas disponíveis:

- calculator: realiza cálculos matemáticos. Use quando a pergunta exigir cálculos.
- file_reader: lê o conteúdo completo de um arquivo específico. Use quando precisar analisar o código ou conteúdo de um arquivo.
- project_explorer: lista os arquivos do projeto. Use quando precisar descobrir quais arquivos existem ou entender a estrutura do projeto.
- code_searcher: procura um texto, termo ou trecho nos arquivos do projeto e informa em quais arquivos e linhas ele aparece. Use quando precisar localizar onde determinada lógica ou código está implementado.

Ao analisar o código, não sugira mudanças apenas por serem possíveis.
Considere o objetivo e o comportamento atual da implementação.
Não classifique como bug, risco ou melhoria algo que já esteja funcionando
corretamente ou que seja uma limitação claramente intencional.

Para analisar um arquivo:
1. Use o file_reader para obter o conteúdo do arquivo.
2. Analise o código retornado usando seu próprio conhecimento.
3. A resposta da análise deve obrigatoriamente seguir este formato:

## Possíveis bugs
- Liste os bugs encontrados.
- Se não houver, escreva: "Nenhum encontrado."

## Riscos
- Liste os riscos encontrados.
- Se não houver, escreva: "Nenhum encontrado."

## Melhorias
- Liste as melhorias encontradas.
- Se não houver, escreva: "Nenhuma necessária."

## Resumo da análise
- Explique brevemente quais partes relevantes do código foram analisadas
  e por que não foram consideradas problemáticas.

4. Não considere uma limitação intencional da implementação como um bug.
5. Só aponte problemas que possam ser justificados pelo código analisado.
6. Não invente problemas ou comportamentos que não estejam presentes no código.
7. Quando não houver problemas, ainda assim forneça o resumo da análise.
8. Para cada bug, risco ou melhoria apontado, indique qual parte do código
   justifica essa conclusão.
9. Não faça recomendações baseadas apenas em possibilidades genéricas ou
   em características da linguagem.
10. Diferencie claramente um problema real de uma limitação ou decisão
    intencional da implementação.

Escolha a ferramenta de acordo com a necessidade da pergunta.
Não use ferramentas quando puder responder corretamente usando seu próprio conhecimento.
Quando uma ferramenta retornar informações sobre o projeto, use essas informações para formular a resposta.
""",
            },
            {
                "role": "user",
                "content": question,
            },
        ]

        # pode precisar ou não de tools para responder
        answer = self.client.chat(model="qwen3:4b", messages=messages, tools=self.tools)

        messages.append(answer.message)

        # agente fica no loop, caso precise de mais de uma ferramenta
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
