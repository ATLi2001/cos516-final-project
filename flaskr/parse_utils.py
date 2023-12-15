import re
import flaskr.simpleBool as simpleBool
#import wtforms import Form, StringField, validators
import os

#interp
# for k, v in interp.items():
#        simpleBool.interpretation[k] = v
#    res = simpleBool.parseExpression(bool_exp)
    
#    simpleBool.interpretation = {} 
def cleanImages(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for filename in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, filename)):
            os.remove(os.path.join(folder, filename))


def parseBoolExpression(bool_exp):
    return simpleBool.Formula(bool_exp)

def parseOrderingExpression(order_exp):
    no_white = re.sub(r"\s+","", order_exp)
    return re.split("<", no_white)