import re
import flaskr.simpleBool as simpleBool


def parseBoolExpression(bool_exp, interp):
    bool_exp = re.sub("!", "! ", bool_exp)
    for k, v in interp.items():
        simpleBool.interpretation[k] = v
    res = simpleBool.boolExpr.parseString(bool_exp)
    simpleBool.interpretation = {} 

    return res

def parseOrderingExpression(order_exp):
    no_white = re.sub(r"\s+","", order_exp)
    return re.split("<", no_white)
