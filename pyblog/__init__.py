#################################################
#######                                   #######
#######             __INIT__.PY           #######
#######                                   ####### 
#################################################

import flask
import flask_sqlalchemy
import flask_migrate
import flask_login
import os
import flask_mail

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'reuvenkey'

# Define the path of the database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+ os.path.join(os.path.dirname(__file__), 'pyblog.db')

# Create a database object
db  = flask_sqlalchemy.SQLAlchemy(app)

# Create migration object
migrate = flask_migrate.Migrate(app, db)

# Create a login manager object
login_mngr = flask_login.LoginManager(app)


#create a mail manager object

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config["MAIL_USE_SSL"] = False
app.config['MAIL_USERNAME'] ="awetkebedom@gmail.com"
app.config["MAIL_PASSWORD"] ="muluekebedom"


mail = flask_mail.Mail(app)



from pyblog import routes, models
