# porta de entrada do programa

from tools.calculator import Calculator

calculator = Calculator()

print(calculator.execute("-2 + 3"))
print(calculator.execute("-2 * 5"))
print(calculator.execute("(-2 + 5) * 3"))