from flaskr.bdd import BDD
from flaskr.robdd import ROBDD

import os
import re
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
  def homepage():
    return render_template('input.html', count="nothing", url="")
  
  @app.route('/', methods=('GET', 'POST'))
  def create():
    global count, max_count, orig_img, adjust_bool

    def displayResult():
      adjust_str = "_adjust" if adjust_bool else ""
      adjust_button = "Revert Adjust" if adjust_bool else "Adjust Nodes"
      img = "/" + orig_img + "(" + str(count) + ")" + adjust_str + ".png"
      cnt_str = str(count) + "/" + str(max_count)
      print(adjust_button, adjust_bool)
      return render_template('result.html', count = cnt_str, url=img, adjust=adjust_button)

    if request.method == 'POST':
      ordering = request.form.get('ordering', '')
      encoding = request.form.get('encoding', '')
        ## should strip trailing and leading spaces and add space
      encoding = re.sub("!", "! ", encoding.strip())
      button_val = request.form.get('submit_button')
      adjust_val = request.form.get('adjust')
      

      if button_val == 'Next':
        if count < max_count:
          count = count + 1

      if button_val == 'Previous':
        if count > 1: 
          count -= 1

      if adjust_val:
        adjust_bool = not adjust_bool


      if not button_val and not adjust_val:
       #user submitted formula 
        parse_utils.cleanImages("static/images")
        var = parse_utils.parseOrderingExpression(ordering)
        formula = parse_utils.parseBoolExpression(encoding)

        bdd = BDD(var, formula)

        robdd = ROBDD(bdd)

        robdd.curr_robdd.visualize(manual_readjust=False)
        robdd.curr_robdd.visualize(manual_readjust=True)
        max_count = 1
        
        while(robdd.next()):
          robdd.curr_robdd.visualize(manual_readjust=False)
          robdd.curr_robdd.visualize(manual_readjust=True)
          max_count += 2

        count = 1
        orig_img = os.path.join('static', 'images', re.sub("\s+", '_', encoding))
        adjust_bool = False
      print(button_val, adjust_val)
      return displayResult()

  return app
