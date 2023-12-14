from flaskr.bdd import BDD
from flaskr.robdd import ROBDD

import os
import flaskr.parse_utils as parse_utils
from flask import Flask, render_template, request, flash, redirect, url_for



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
  )

  if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass
  # a simple page that says hello
  @app.route('/')
  def hello():
    return render_template('input.html')
    return 'Hello, World!'
  
  @app.route('/', methods=('GET', 'POST'))
  def create():
    if request.method == 'POST':
      ordering = request.form.get('ordering', '')
      encoding = request.form.get('encoding', '')
      var = parse_utils.parseOrderingExpression(ordering)
      formula = parse_utils.parseBoolExpression(encoding)

      bdd = BDD(var, formula)

      robdd = ROBDD(bdd)
      while(robdd.next()):
        robdd.curr_robdd.visualize()
      
        # ordering = request.form.get('ordering', '')
        # encoding = request.form.get('encoding', '')
        # #content = request.form['ordering']
        # var = parse_utils.parseOrderingExpression(ordering)
        # formula = parse_utils.parseBoolExpression(encoding)
        # truth_list = parse_utils.createInterpretations(var)

        # encode_list = []
        # output = ""
        # for table in truth_list:
        #   table2 = table.copy()
        #   encode = formula.evaluate(table2)
        #   if not encode:
        #     return redirect(url_for('create'))
        #   else:
        #     encode_list.append(encode)
        #     output += str(table) + " "
        
        # bool_list = [bool(enc[0]) for enc in encode_list]
        # output += str(bool_list)


        
    return bdd.level_order()


  return app
