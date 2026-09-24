from agent.agent import Agent

agent = Agent()

question = "Leia o arquivo src/teste.txt e depois calcule 25 * 4."

print(agent.ask(question))