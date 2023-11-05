import re
import flaskr.simpleBool as simpleBool


def parseBoolExpression(bool_exp, variables):
    bool_exp = re.sub("!", "! ", bool_exp)
    for v in variables:
        simpleBool.interpretation[v] = False
    res = simpleBool.boolExpr.parseString(bool_exp)

    return res
    #success = "PASS" if bool(res) == True else "FAIL"
    #print(bool_exp, "\n", res, "=", bool(res), "\n", success, "\n")

def parseOrderingExpression(order_exp):
    no_white = re.sub(r"\s+","", order_exp)
    return re.split("<", no_white)

print(parseBoolExpression("p || !q", ["p", "q"]))
