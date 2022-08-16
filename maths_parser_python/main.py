# region node types

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

# endregion


expr = Add(Integer(7), Mult(Integer(5), Integer(2)))
assert str(expr) == "(7 + (5 * 2))"
assert expr.eval() == 17


# todo: multi-character tokens (for identifiers and numbers)
class Lexer:
    def __init__(self, string: str):
        self._string = string + '\0'
        self._index = -1
        self._nextToken = None
        self.scanToken()

    def scanToken(self) -> None:
        self._index += 1
        if self._index < len(self._string):
            self._nextToken = self._string[self._index]
            # skip whitespace
            if self._nextToken == ' ':
                self.scanToken()

    def next(self) -> str:
        return self._nextToken


# here's our grammar:
# E -> T{+|- T}
# T -> F{*|/ F}
# F -> ID | INTEGER | (E) | -F

# for reference, here's an example grammar that might work for boolean algebra.
# E -> T{+|. E}
# T -> F
# F -> ID | 0 | 1 | (E) | ~F

# the parsing functions will read tokens and return the tree that they build.
class Parser:
    def parse(self, lexer: Lexer) -> TreeNode:
        a = self._parseExpr(lexer)
        assert lexer.next() == '\0'
        return a

    def _parseExpr(self, lexer: Lexer) -> TreeNode:
        a = self._parseTerm(lexer)
        if a is None:
            return None

        while 1:
            if lexer.next() == '+':
                lexer.scanToken()

                b = self._parseTerm(lexer)
                if b is None:
                    return None

                a = Add(a, b)
                if a is None:
                    return None
            elif lexer.next() == '-':
                lexer.scanToken()

                b = self._parseTerm(lexer)
                if b is None:
                    return None

                a = Subtract(a, b)
                if a is None:
                    return None
            else:
                return a

    def _parseTerm(self, lexer: Lexer) -> TreeNode:
        a = self._parseFactor(lexer)
        if a is None:
            return None

        while 1:
            if lexer.next() == '*':
                lexer.scanToken()

                b = self._parseFactor(lexer)
                if b is None:
                    return None

                a = Mult(a, b)
                if a is None:
                    return None
            elif lexer.next() == '/':
                lexer.scanToken()

                b = self._parseFactor(lexer)
                if b is None:
                    return None

                a = Div(a, b)
                if a is None:
                    return None
            else:
                return a

    def _parseFactor(self, lexer: Lexer) -> TreeNode:
        if self.is_identifier(lexer.next()):
            a = Identifier(lexer.next())
            lexer.scanToken()
            return a
        elif self.is_integer(lexer.next()):
            a = Integer(lexer.next())
            lexer.scanToken()
            return a
        elif lexer.next() == '(':
            lexer.scanToken()

            a = self._parseExpr(lexer)
            if a is None:
                return None

            if lexer.next() == ')':
                lexer.scanToken()
                return a
            else:
                return None
        elif lexer.next() == '-':
            lexer.scanToken()

            a = self._parseFactor(lexer)
            if a is None:
                return None

            return Negate(a)
        else:
            return None

    def is_digit(self, char: str) -> bool:
        return char >= '0' and char <= '9'

    def is_integer(self, string: str) -> bool:
        for c in string:
            if not self.is_digit(c):
                return False
        return True

    def is_letter(self, char: str) -> bool:
        return (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z')

    def is_identifier(self, string: str) -> bool:
        if not self.is_letter(string[0]):
            return False

        for c in string[1:]:
            if not self.is_letter(c) and not self.is_integer(c):
                return False
        return True


parser = Parser()

lexer_one = Lexer("(7 + (5 * 2))")
tree_one = parser.parse(lexer_one)

assert str(tree_one) == "(7 + (5 * 2))"
assert tree_one.eval() == 17

lexer_two = Lexer("6 + (-4 + (3*x+7) * y * 9 / (4 + 3))")
tree_two = parser.parse(lexer_two)
assert str(tree_two) == "(6 + ((-4) + (((((3 * x) + 7) * y) * 9) / (4 + 3))))"
assert tree_two.eval({'x': 7, 'y': 2}) == 74.0

tree_three = Add(Identifier('x'), Mult(Integer(5), Integer(2)))
assert str(tree_three) == "(x + (5 * 2))"
assert tree_three.eval({'x': 12}) == 22
