class FormulaError(Exception):
    """Base class for formula errors"""
    pass

class InvalidFormatError(FormulaError):
    pass

class UnknownVariableError(FormulaError):
    pass

class DivisionByZeroError(FormulaError):
    pass

class UnsupportedOperatorError(FormulaError):
    pass


class Calculator:
    def __init__(self):
        self.variables = {}

    def assign(self, var, value):
        self.variables[var] = value

    def evaluate(self, expression):
        try:
            parts = expression.split()
            if len(parts) == 3:
                left, op, right = parts
                left_val = self.get_value(left)
                right_val = self.get_value(right)

                if op == "+":
                    return left_val + right_val
                elif op == "-":
                    return left_val - right_val
                elif op == "*":
                    return left_val * right_val
                elif op == "/":
                    if right_val == 0:
                        raise DivisionByZeroError("Division by zero")
                    return left_val / right_val
                elif op == "%":
                    if right_val == 0:
                        raise DivisionByZeroError("Modulo by zero")
                    return left_val % right_val
                else:
                    raise UnsupportedOperatorError(f"Unsupported operator: {op}")
            else:
                raise InvalidFormatError("Invalid formula format")
        except FormulaError as e:
            return type(e).__name__

    def get_value(self, token):
        if token.isdigit() or self.is_float(token):
            return float(token)
        elif token in self.variables:
            return self.variables[token]
        else:
            raise UnknownVariableError(f"Unknown variable: {token}")

    def is_float(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False


# ---------------- SAMPLE INTERACTIVE INPUT ----------------
calc = Calculator()

inputs = [
    "x = 20",
    "y = 5",
    "x + y",
    "x / 0",
    "z + 10",
    "3 ** 2",
    "quit"
]

for line in inputs:
    if line == "quit":
        break
    elif "=" in line:
        var, val = line.split("=")
        calc.assign(var.strip(), float(val.strip()))
    else:
        print(calc.evaluate(line))
