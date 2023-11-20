# simpleBool.py
#
# Example of defining a boolean logic parser using
# the operatorGrammar helper method in pyparsing.
#
# In this example, parse actions associated with each
# operator expression will "compile" the expression
# into BoolXXX class instances, which can then
# later be evaluated for their boolean value.
#
# Copyright 2006, by Paul McGuire
# Updated 2013-Sep-14 - improved Python 2/3 cross-compatibility
# Updated 2021-Sep-27 - removed Py2 compat; added type annotations
#
# Edited by Kenny Poor

from typing import Callable, Iterable

from pyparsing import infix_notation, opAssoc, Keyword, Word, alphas, ParserElement, exceptions

ParserElement.enablePackrat()

# define classes to be built at parse time, as each matching
# expression type is parsed
interpretation = {}
class BoolOperand:
    def __init__(self, t):
        self.label = t[0]
        try:
            self.value = eval(t[0], interpretation)
        except NameError as e:
            self.value = False

    def __bool__(self) -> bool:
        return self.value

    def __str__(self) -> str:
        return self.label

    __repr__ = __str__


class BoolNot:
    def __init__(self, t):
        self.arg = t[0][1]

    def __bool__(self) -> bool:
        v = bool(self.arg)
        return not v

    def __str__(self) -> str:
        return "~" + str(self.arg)

    __repr__ = __str__


class BoolBinOp:
    repr_symbol: str = ""
    eval_fn: Callable[
        [Iterable[bool]], bool
    ] = lambda _: False

    def __init__(self, t):
        self.args = t[0][0::2]

    def __str__(self) -> str:
        sep = " %s " % self.repr_symbol
        return "(" + sep.join(map(str, self.args)) + ")"

    def __bool__(self) -> bool:
        return self.eval_fn(bool(a) for a in self.args)


class BoolAnd(BoolBinOp):
    repr_symbol = "&"
    eval_fn = all


class BoolOr(BoolBinOp):
    repr_symbol = "|"
    eval_fn = any


# define keywords and simple infix notation grammar for boolean
# expressions
TRUE = Keyword("True")
FALSE = Keyword("False")
NOT = Keyword("!")
AND = Keyword("&&")
OR = Keyword("||")
boolOperand = TRUE | FALSE | Word(alphas, max=1)
boolOperand.set_parse_action(BoolOperand).set_name("bool_operand")

# define expression, based on expression operand and
# list of operations in precedence order
boolExpr = infix_notation(
    boolOperand,
    [
        (NOT, 1, opAssoc.RIGHT, BoolNot),
        (AND, 2, opAssoc.LEFT, BoolAnd),
        (OR, 2, opAssoc.LEFT, BoolOr),
    ],
).set_name("boolean_expression")

boolOperand2 = TRUE | FALSE | Word(alphas, max=1)

boolExpr2 = infix_notation(
    boolOperand2,
    [
        (NOT, 1, opAssoc.RIGHT, BoolNot),
        (AND, 2, opAssoc.LEFT, BoolAnd),
        (OR, 2, opAssoc.LEFT, BoolOr),
    ],
).set_name("boolean_expression")


def parseExpression(bool_exp):
    try:
        res = boolExpr.parseString(bool_exp, parseAll=True)
        res2 = boolExpr2.parseString(bool_exp, parseAll=True)
    except (exceptions.ParseException, NameError) as e:
        res = None
    print("hi", res2[0])
    return res

if __name__ == "__main__":
    p = True
    q = False
    r = True
    tests = [
        ("p", True),
        ("q", False),
        ("! p", False),
        #("p and q", False),
        #("p and not q", True),
        #("not not p", True),
        #("not(p and q)", True),
        #("q or not p and r", False),
        #("q or not p or not r", False),
        #("q or not (p and r)", False),
        #("p or q or r", True),
        #("p or q or r and False", True),
        #("(p or q or r) and False", False),
    ]

    #print("p =", p)
    #print("q =", q)
    #print("r =", r)
    print()
    for test_string, expected in tests:
        res = boolExpr.parseString(test_string, parseAll=True)[0]
        print("\n\n") 
        print(type(res), res)
        print("\n\n") 
        success = "PASS" if bool(res) == expected else "FAIL"
        print(test_string, "\n", res, "=", bool(res), "\n", success, "\n")
