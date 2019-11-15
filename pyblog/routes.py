from pyblog import fake_data
from pyblog import app, db, login_mngr, message_handler
from pyblog import forms, models, mail
import flask
import datetime
import flask_login
from werkzeug import security
import flask_mail
import jwt


@app.route('/')
@app.route('/home')
def homepage():
    if flask_login.current_user.is_anonymous:
        d = datetime.datetime.now()
        current_date = "{}/{}/{}".format(d.day, d.month, d.year)

        return flask.render_template("home.jin", today_date=current_date)
    else:
        return flask.redirect(flask.url_for('user_profile', user_id=flask_login.current_user.id))


@flask_login.login_required
@app.route("/contact", methods=("GET", "POST"))
def contact():
    form = forms.ContactUs()

    if flask.request.method == "GET":
        return flask.render_template('contact.jin', form=form)

    if form.validate_on_submit():
        user = models.User.query.filter_by(email=flask_login.current_user.email).first()
        message_handler.send_mail(subject=form.subject.data,
                                  recipients=['awetkebedom@gmail.com'],
                                  sender=user.email,
                                  html_body=form.content.data)

        return flask.redirect(flask.url_for('homepage'))


@app.route('/users')
def users_list():
    all_users = models.User.query.all()
    for user in all_users:
        if flask_login.current_user.is_authenticated and user.id == flask_login.current_user.id:
            all_users.remove(user)

    return flask.render_template('users_list.jin',
                                 users=all_users)


@app.route('/user_profile/<user_id>')
def user_profile(user_id):
    found = models.User.query.get(user_id)

    if found:
        user_posts = found.posts
        return flask.render_template('user_profile.jin', user=found, posts=user_posts)
    else:
        return flask.redirect(flask.url_for('homepage'))


@app.route("/sign_in", methods=('GET', 'POST'))
def signin():
    form = forms.SignIn()
    if flask.request.method == "GET":
        return flask.render_template('signin.jin', signinform=form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = models.User.check_signin(username, password)
        if user:
            flask.flash("{} logged in !".format(username))
            flask_login.login_user(user)
        else:
            flask.flash("Invalid username/password combination")
            return flask.redirect(flask.url_for('signin'))

    else:
        flask.flash("Invalid form!")
        return flask.render_template('signin.jin', signinform=form)
    return flask.redirect(flask.url_for('homepage'))


@app.route("/sign_up", methods=('GET', 'POST'))
def signup():
    form = forms.Signup()

    if flask.request.method == "GET":  # STATE 1: The user requests only the html content
        return flask.render_template("signup.jin", signupform=form)

    else:  # STATE 2: The user already saw the page and filled the content

        if form.validate_on_submit():  # STATE 2a: The form is valid

            # Create a user
            user = models.User()
            user.name = form.username.data
            user.age = form.age.data
            user.email = form.email.data
            user.city = form.city.data

            user.add_password(form.password.data)

            user.add_to_db()

            flask.flash("Welcome, " + form.username.data)
            return flask.redirect(flask.url_for('homepage'))

        else:  # STATE 2b: The form is invalid
            flask.flash("Invalid form")
            return flask.render_template("signup.jin", signupform=form)


@app.route("/sign-out")
def signout():
    # log the user out
    flask_login.logout_user()

    # Redirect somewhere
    return flask.redirect(flask.url_for('homepage'))


@flask_login.login_required
@app.route("/new-post", methods=("GET", "POST"))
def newpost():
    form = forms.NewPost()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        # Create a post
        post = models.Post()

        # Add attributes
        post.title = title
        post.content = content

        # Link to a user
        post.author = flask_login.current_user

        # Retrieve and add tags
        post.add_tags_from_content()

        flask.flash("{} Added a post".format(flask_login.current_user.name))
        # Save
        db.session.commit()

        return flask.redirect(flask.url_for("homepage"))
    return flask.render_template("new_post.jin", form=form)


@app.route('/search/by-tag/<tag>')
def tag_search(tag):
    # Retrieve tag object
    tag_obj = models.Tag.query.filter_by(name=tag)
    if not tag_obj:
        return flask.redirect(flask.url_for('homepage'))
    tag_obj = tag_obj[0]
    associated_posts = tag_obj.posts
    associated_posts.sort(key=lambda p: p.pub_date, reverse=True)

    return flask.render_template('search_result.jin', posts=associated_posts)


@app.route('/search/by-tag', methods=["POST"])
def bridge_tag():
    tag = flask.request.form['searched_text']
    return flask.redirect(flask.url_for('tag_search', tag=tag))


# @app.route("/messages")
# def message():
#
#     message_handler.send_mail(subject='HELLO WORLD',
#                     recipients=['eyal@chocron.eu'],
#                     sender=app.config["MAIL_USERNAME"],
#                     html_body=flask.render_template('messages.jin'))
#
#     return flask.redirect(flask.url_for('homepage'))


@app.route("/send-email")
def send_mail_to_everyone():
    msg = flask_mail.Message(subject="Hello",
                             sender=app.config.get("MAIL_USERNAME"),
                             recipients=["eyal@chocron.eu"],
                             body="Hello Eyal")
    mail.send(msg)
    return flask.redirect(flask.url_for('homepage'))


@flask_login.login_required
@app.route("/cv", methods=["GET", "POST"])
def create_cv():
    form = forms.CreateCv()

    if flask.request.method == "GET":
        return flask.render_template('create_cv.jin', form=form)

    if form.validate_on_submit():
        return flask.render_template('cv_template.jin', form=form)
    return flask.redirect(flask.url_for('homepage'))

@app.route("/reset-password", methods=['GET', 'POST'])
def password_reset_request():
    form = forms.PasswordResetRequest()
    if flask.request.method == 'GET':
        return flask.render_template('password_reset_request.jin', form=form)
    else:
        # Retrieve user
        user = models.User.query.filter_by(email=form.mail.data).first()
        if not user:
            return flask.redirect(flask.url_for('homepage'))

        # Create a token
        payload = {
            'user_id': user.id,
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'])
        # Send this token by mail
        txt_content = 'Hi, to reset your password, follow this link:{}'.format(
            flask.url_for('password_reset_handler', token=token, _external=True)
        )
        link = flask.url_for('password_reset_handler', token=token)

        message_handler.send_mail(
            sender=app.config['MAIL_USERNAME'],
            receivers=[form.mail.data],
            subject='Reset password',
            txt_content=txt_content,
            html_content=flask.render_template('mail_reset_password.jin', link=link)
        )

        return flask.redirect(flask.url_for('homepage'))


@app.route('/reset-password/<token>')
def password_reset_handler(token):
    decrypted_token = jwt.decode(token, app.config['SECRET_KEY'])
    user_id = decrypted_token['user_id']
    user = models.User.query.get(user_id).first()
    if user:
        form = forms.PasswordReset()
        if flask.request.method == 'GET':
            return flask.render_template('password_request.jin', form=form)
        else:
            user.add_password(form.password.data)
            flask.flash('Password changed !')

    return flask.redirect(flask.url_for('homepage'))
