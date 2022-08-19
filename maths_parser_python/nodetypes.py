class TreeNode:
    def eval(self, env={}): pass
    def __str__(self): pass
    def __repr__(self): return str(self)


class BinaryOperator(TreeNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.symbol} {self.right})"


class UnaryOperator(TreeNode):
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return f"({self.symbol}{self.arg})"


class Add(BinaryOperator):
    symbol = '+'

    def eval(self, env={}):
        return self.left.eval(env) + self.right.eval(env)


class Subtract(BinaryOperator):
    symbol = '-'

    def eval(self, env={}):
        return self.left.eval(env) - self.right.eval(env)


class Mult(BinaryOperator):
    symbol = '*'

    def eval(self, env={}):
        return self.left.eval(env) * self.right.eval(env)


class Div(BinaryOperator):
    symbol = '/'

    def eval(self, env={}):
        return self.left.eval(env) / self.right.eval(env)


class Negate(UnaryOperator):
    symbol = '-'

    def eval(self, env={}):
        return -self.arg.eval(env)


class Identifier(TreeNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def eval(self, env):
        return env[self.value]


class Integer(TreeNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def eval(self, env={}):
        return int(self.value)
