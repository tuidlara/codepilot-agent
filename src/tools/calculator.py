import ast
import operator


class Calculator:

    def calculate(self, expression):
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv
        }

        tree = ast.parse(expression, mode="eval")

        return self._calculate_node(tree.body, allowed_operators)

    def _calculate_node(self, node, allowed_operators):

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = self._calculate_node(node.left, allowed_operators)
            right = self._calculate_node(node.right, allowed_operators)

            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("Não é possível dividir por zero.")

            return allowed_operators[type(node.op)](left, right)

        raise ValueError("Expressão contém operação não permitida.")