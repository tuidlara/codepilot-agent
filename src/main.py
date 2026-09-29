#porta de entrada do programa

from agent.agent import Agent

agent = Agent()

question = "Analise a integração entre agent.py, calculator.py e file_reader.py. Explique como o Agent chama essas duas ferramentas, quais argumentos envia e como os resultados retornam para o Agent."

print(agent.ask(question))