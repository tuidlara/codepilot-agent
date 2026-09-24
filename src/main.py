from agent.agent import Agent

agent = Agent()

question = "Quanto é (15 + 5) * 3?"

answer = agent.ask(question)

print(answer)