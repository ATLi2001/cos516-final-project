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
  encoding = ""
  img_dir = ""
  count = 0

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
    return render_template('input.html', name="nothing", url="")
    return 'Hello, World!'
  
  @app.route('/', methods=('GET', 'POST'))
  def create():
    global encoding, img_dir, orig_img
    global count
    if request.method == 'POST':
      ordering = request.form.get('ordering', '')
      encoding = request.form.get('encoding', '')
      button_val = request.form.get('submit_button')

      if button_val == 'Next':
        print("Next\n")
        print(count)
        count = count + 1
        img = "/" + orig_img + "(" + str(count) + ").png"
        return render_template('result.html', name = img, url=img)
      elif button_val == 'Previous':
        print("Previous\n")
        print(count)
        if count > 0: 
          count = count - 1

        if count > 0:
          img = "/" + orig_img + "(" + str(count) + ").png"
        else:
          img = "/" + orig_img + ".png"
          
        return render_template('result.html', name = img, url=img)
      else: #user submitted formula 
        ## should strip trailing and leading spaces
        encoding = encoding.strip()
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

        img_dir = os.path.join('static', 'images')

        #debug examine files in dir 
        #files = os.listdir(img_dir)
        #print(files)
        #for file in os.listdir(img_dir):
        #  img_file = os.path.join(img_dir, file)
        #  print(img_file)

        count = 0 #orig_img will not have the (0) label
        orig_img = os.path.join(img_dir, re.sub("\s+", '_', encoding))
        #flask img dir start with root / then with subdirs static/images
        img = "/"+ orig_img + ".png"
        ## end of POST
 
    return render_template('result.html', name = img, url=img)

  return app
