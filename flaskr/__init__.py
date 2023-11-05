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
    return render_template('hello.html')
    return 'Hello, World!'
  
  @app.route('/', methods=('GET', 'POST'))
  def create():
    if request.method == 'POST':
        ordering = request.form.get('ordering', '')
        encoding = request.form.get('encoding', '')
        #content = request.form['ordering']
        var = parse_utils.parseOrderingExpression(ordering)
        encoding = parse_utils.parseBoolExpression(encoding, var)
        print(encoding)
        print(encoding[0])
        print(bool(encoding[0]))
    



  return app
