from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
mydb = 'thritter'

#creating user class object
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['firstname']
        self.last_name = data['lastname']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #Creating a class method to save users into the database when they create a user
    @classmethod
    def save_user(cls,data):
        query = 'INSERT INTO users (created_at, updated_at, firstname, lastname, email, password, username) VALUES (NOW(), NOW(), %(fname)s, %(lname)s, %(email)s,%(password)s,%(username)s);'
        return connectToMySQL(mydb).query_db(query,data)
    
    #This is a class method used to find a user by email in the database to login.
    @classmethod
    def get_by_email(cls, data):
        query = '''
        SELECT *
        FROM users
        WHERE email = %(email)s;
        '''
        result = connectToMySQL(mydb).query_db(query,data)

        if len(result) < 1:
            return False
        return cls(result[0])
    
    #A Method used to find the user by username so they can login from that as well.
    @classmethod
    def get_by_username(cls,data):
        query = '''
        SELECT *
        FROM users
        WHERE username = %(username)s'''

        result = connectToMySQL(mydb).query_db(query,data)

        if len(result) < 1:
            return False
        return cls(result[0])
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if not str.isalpha(user['fname']):
            flash('First name must be letters only')
            is_valid = False
        if not str.isalpha(user['lname']):
            flash('Last name must be letters only')
            is_valid = False
        if len(user['fname']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['lname']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['username']) <3:
            flash("Usename must be at least 3 characters.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be 8 characters or greater.")
            is_valid = False
        if user['password'] != user['confpassword']:
            flash("Passwords do not match!")
            is_valid = False
        return is_valid
