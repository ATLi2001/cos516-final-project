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

from pyparsing import infix_notation, opAssoc, Keyword, Word, alphanums, ParserElement, exceptions

ParserElement.enablePackrat()

interp = {}
class Formula:
    def __init__(self, formula):
        self.label = formula

    def __str__(self) -> str:
        return self.label

    def evaluate(self, table):
        # define keywords and simple infix notation grammar for boolean
        # expressions
        TRUE = Keyword("True")
        FALSE = Keyword("False")
        NOT = Keyword("!")
        AND = Keyword("&&")
        OR = Keyword("||")
        boolOperand = TRUE | FALSE | Word(alphanums)
        boolOperand.add_condition(self.parseVars, message = "Not all variables are included in the ordering.", fatal = True)
        boolOperand.add_parse_action(BoolOperand).set_name("bool_operand")


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

        try:
            global interp
            interp = table
            res = bool(boolExpr.parseString(self.label, parseAll=True)[0])
        except (exceptions.ParseException, NameError, exceptions.ParseFatalException ) as e:
            print(e)
            if(type(e) == exceptions.ParseFatalException):
                print("Not apparently")
            res = None
        return res

    def parseVars(self, t):
        return t[0] in list(interp.keys())
# define classes to be built at parse time, as each matching
# expression type is parsed

class BoolOperand:
    def __init__(self, t):
        self.label = t[0]
        try:
            self.value = eval(t[0], interp)
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
    # print()
    # for test_string, expected in tests:
    #     res = boolExpr.parseString(test_string, parseAll=True)[0]
    #     print("\n\n") 
    #     print(type(res), res)
    #     print("\n\n") 
    #     success = "PASS" if bool(res) == expected else "FAIL"
    #     print(test_string, "\n", res, "=", bool(res), "\n", success, "\n")
