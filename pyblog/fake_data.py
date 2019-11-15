
# We want to populate our site with some fake data
# First step: Add users

class User:

    def __init__(self, username, email):
        # Check if username already exist
        # Check if email is valid

        self.username = username
        self.email    = email

users = []
# Create a lot of random users
for name in ('john', 'nick', 'charles', 'zoe', 'tesfit', 'awet', 'reuven', 'michael','avner'):
    fake_mail = "{}@gmail.com".format(name)
    user      = User(name, fake_mail)
    users.append(user)
