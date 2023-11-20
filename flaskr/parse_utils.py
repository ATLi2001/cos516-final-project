import re
import flaskr.simpleBool as simpleBool
#import wtforms import Form, StringField, validators
import itertools



def parseBoolExpression(bool_exp, interp):
    bool_exp = re.sub("!", "! ", bool_exp)
    for k, v in interp.items():
        simpleBool.interpretation[k] = v
    res = simpleBool.parseExpression(bool_exp)
    
    simpleBool.interpretation = {} 

    return res

def parseOrderingExpression(order_exp):
    no_white = re.sub(r"\s+","", order_exp)
    return re.split("<", no_white)

def createInterpretations(vars):
    result_list = []
    for p in itertools.product([True, False], repeat=len(vars)):
        result_list.append(dict(zip(vars, p)))
    return result_list