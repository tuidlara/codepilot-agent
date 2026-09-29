#porta de entrada do programa

from agent.agent import Agent

agent = Agent()

question = "Analise o calculator.py. Verifique especificamente o tratamento de divisão por zero."

print(agent.ask(question))