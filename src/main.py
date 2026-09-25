from agent.agent import Agent

agent = Agent()

question = "Procure no projeto pelo texto 'dividir por zero' e me diga em qual arquivo e linha aparece."

print(agent.ask(question))