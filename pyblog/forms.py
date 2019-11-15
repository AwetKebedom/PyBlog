import flask_wtf
import wtforms
from wtforms import validators as valid

class Signup(flask_wtf.FlaskForm):

    username            = wtforms.StringField("Username", validators=[valid.DataRequired(message="Username can't be empty")])
    email               = wtforms.StringField("Email", validators=[valid.DataRequired(), valid.Email()])
    password            = wtforms.PasswordField("Password", validators=[valid.DataRequired()])
    password_confirm    = wtforms.PasswordField("Confirm password", validators=[valid.DataRequired(),
                                                                                                                                                                    valid.EqualTo('password')])

    age                 = wtforms.IntegerField("Age", validators=[valid.DataRequired(message="Age can't be empty")])
    city                = wtforms.StringField("City", validators=[])

    submit              = wtforms.SubmitField("Sign up")

class SignIn(flask_wtf.FlaskForm):

    username            = wtforms.StringField("Username", validators=[valid.DataRequired(message="Username can't be empty")])
    password            = wtforms.PasswordField("Password", validators=[valid.DataRequired()])
    submit              = wtforms.SubmitField("Sign In")

class NewPost(flask_wtf.FlaskForm):

    title               = wtforms.StringField("title", validators=[valid.DataRequired(message="Field can't be empty")])
    content             = wtforms.StringField("Content", validators=[valid.DataRequired(message="Field can't be empty")])

    submit              = wtforms.SubmitField("Post")

class ContactUs(flask_wtf.FlaskForm):

    subject             = wtforms.StringField('Subject', validators=[valid.DataRequired(message="Field can't be empty")])
    first_name          = wtforms.StringField('First Name')
    last_name           = wtforms.StringField('Last Name')
    content             = wtforms.TextAreaField('Comment')
    submit              = wtforms.SubmitField("Submit")

class CreateCv(flask_wtf.FlaskForm):

    #Personal Details
    first_name          = wtforms.StringField('First Name')
    last_name           = wtforms.StringField('Last Name')
    email               = wtforms.StringField('Email')

    #Work Experiences
    company_name        = wtforms.StringField('Company Name')
    job_title           = wtforms.StringField('Job Title', validators=[valid.DataRequired(message="Field can't be empty")])
    work_explanation    =  wtforms.TextAreaField('Description')
    # Start and End
    date_from           = wtforms.DateTimeField('Start',format='%Y-%m-%d', validators=[])
    to                  = wtforms.DateTimeField('To',format='%Y-%m-%d', validators=[])

    #Education
    school              = wtforms.StringField('School')
    degree              = wtforms.StringField('Degree')
    #Start and End
    Edu_start           = wtforms.DateTimeField('Start',format='%Y-%m-%d', validators=[])
    Edu_end             = wtforms.DateTimeField('End',format='%Y-%m-%d', validators=[])
    city                = wtforms.StringField('City')
    degree_explanation  = wtforms.TextAreaField('Description')


    submit              = wtforms.SubmitField("Create")


class PasswordResetRequest(flask_wtf.FlaskForm):
    mail                = wtforms.StringField("Email", validators=[valid.DataRequired(), valid.Email()])
    submit              = wtforms.SubmitField("Request password reset")

class PasswordReset(flask_wtf.FlaskForm):
    password            = wtforms.StringField("Password", validators=[valid.DataRequired()])
    password_confirm    = wtforms.StringField("Confirm password", validators=[valid.EqualTo('password')])

    submit              = wtforms.SubmitField("Request password reset")


