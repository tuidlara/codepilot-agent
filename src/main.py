#porta de entrada do programa

from agent.agent import Agent

agent = Agent()

question = "Analise o calculator.py e procure possíveis problemas no código."

print(agent.ask(question))