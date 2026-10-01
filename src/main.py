# porta de entrada do programa

from agent.agent import Agent

agent = Agent()

question = "Encontre no projeto onde está implementado o Calculator e depois me explique como ele trata divisão por zero."

response = agent.ask(question)

print(response)