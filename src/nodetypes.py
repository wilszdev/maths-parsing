from copy import copy


class TreeNode:
    def eval(self, env={}): pass
    def simplify(self): return self
    def __str__(self): pass
    def __repr__(self): return str(self)


class BinaryOperator(TreeNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.symbol} {self.right})"

    def simplify(self):
        s_self = copy(self)
        s_self.left = self.left.simplify()
        s_self.right = self.right.simplify()

        if (
            isinstance(s_self.left, (Integer, Float))
            and isinstance(s_self.right, (Integer, Float))
        ):
            if (
                isinstance(s_self.left, (Integer))
                and isinstance(s_self.right, (Integer))
            ):
                return Integer(s_self.eval())
            return Float(s_self.eval())

        return s_self


class UnaryOperator(TreeNode):
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return f"({self.symbol}{self.arg})"

    def simplify(self):
        s_self = copy(self)
        s_self.arg = self.arg.simplify()

        if isinstance(s_self.arg, (Integer, Float)):
            return Float(s_self.eval())

        return s_self


class Add(BinaryOperator):
    symbol = '+'

    def eval(self, env={}):
        return self.left.eval(env) + self.right.eval(env)

    def simplify(self):
        s_self = copy(self)
        s_self.left = self.left.simplify()
        s_self.right = self.right.simplify()

        if (
            isinstance(s_self.left, (Integer, Float))
            and isinstance(s_self.right, (Integer, Float))
        ):
            if (
                isinstance(s_self.left, (Integer))
                and isinstance(s_self.right, (Integer))
            ):
                return Integer(s_self.eval())
            return Float(s_self.eval())

        return s_self


class Subtract(BinaryOperator):
    symbol = '-'

    def eval(self, env={}):
        return self.left.eval(env) - self.right.eval(env)

    def simplify(self):
        s_self = copy(self)
        s_self.left = self.left.simplify()
        s_self.right = self.right.simplify()

        if (
            isinstance(s_self.left, (Integer, Float))
            and isinstance(s_self.right, (Integer, Float))
        ):
            if (
                isinstance(s_self.left, (Integer))
                and isinstance(s_self.right, (Integer))
            ):
                return Integer(s_self.eval())
            return Float(s_self.eval())

        return s_self


class Mult(BinaryOperator):
    symbol = '*'

    def eval(self, env={}):
        return self.left.eval(env) * self.right.eval(env)

    def simplify(self):
        s_self = copy(self)
        s_self.left = self.left.simplify()
        s_self.right = self.right.simplify()

        if (
            isinstance(s_self.left, (Integer, Float))
            and isinstance(s_self.right, (Integer, Float))
        ):
            if (
                isinstance(s_self.left, (Integer))
                and isinstance(s_self.right, (Integer))
            ):
                return Integer(s_self.eval())
            return Float(s_self.eval())

        return s_self


class Div(BinaryOperator):
    symbol = '/'

    def eval(self, env={}):
        return self.left.eval(env) / self.right.eval(env)

    def simplify(self):
        s_self = copy(self)
        s_self.left = self.left.simplify()
        s_self.right = self.right.simplify()

        if (
            isinstance(s_self.left, (Integer, Float))
            and isinstance(s_self.right, (Integer, Float))
        ):
            if (
                isinstance(s_self.left, (Integer))
                and isinstance(s_self.right, (Integer))
                and s_self.left.value % s_self.right.value == 0
            ):
                return Integer(int(s_self.eval()))
            return Float(s_self.eval())

        return s_self


class Negate(UnaryOperator):
    symbol = '-'

    def eval(self, env={}):
        return -self.arg.eval(env)

    def simplify(self):
        s_self = copy(self)
        s_self.arg = self.arg.simplify()

        if isinstance(s_self.arg, Integer):
            return Integer(s_self.eval())

        if isinstance(s_self.arg, Float):
            return Float(s_self.eval())

        return s_self


class Identifier(TreeNode):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def eval(self, env):
        return env[self.value]


class Integer(TreeNode):
    def __init__(self, value):
        if isinstance(value, int):
            self.value = value
            self.raw = str(value)
        elif isinstance(value, str):
            self.raw = value
            self.value = int(value)
        else:
            raise ValueError("`value` should be int or str.")

    def __str__(self):
        return f"{self.raw}"

    def eval(self, env={}):
        return self.value


class Float(TreeNode):
    def __init__(self, value):
        if isinstance(value, float):
            self.value = value
            self.raw = str(value)
        elif isinstance(value, str):
            self.raw = value
            self.value = float(value)
        else:
            raise ValueError("`value` should be float or str.")

    def __str__(self):
        return f"{self.raw}"

    def eval(self, env={}):
        return self.value
