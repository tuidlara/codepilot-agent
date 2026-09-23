from agent.agent import Agent

agent = Agent()

question = "Explique de forma concisa o que é inteligência artificial."

answer = agent.perguntar(question)

print(answer)