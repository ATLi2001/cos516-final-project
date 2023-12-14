import re
import flaskr.simpleBool as simpleBool
#import wtforms import Form, StringField, validators
import itertools


#interp
# for k, v in interp.items():
#        simpleBool.interpretation[k] = v
#    res = simpleBool.parseExpression(bool_exp)
    
#    simpleBool.interpretation = {} 

def parseBoolExpression(bool_exp):
    bool_exp = re.sub("!", "! ", bool_exp)
    return simpleBool.Formula(bool_exp)

def parseOrderingExpression(order_exp):
    no_white = re.sub(r"\s+","", order_exp)
    return re.split("<", no_white)

def createInterpretations(vars):
    result_list = []
    for p in itertools.product([True, False], repeat=len(vars)):
        table = dict(map(lambda i,j : (i,j) , vars, p))
        result_list.append(table)
    return result_list