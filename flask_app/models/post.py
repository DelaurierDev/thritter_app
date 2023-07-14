from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
mydb = 'thritter'

class Post:
    def __init__(self ,data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#creating a class method to save the posts to the db
    @classmethod
    def savepost(cls, data):
        query = 'INSERT INTO posts (created_at, updated_at, post_title, post_contents, user_id) VALUES (NOW(),NOW(),%(post_title)s,%(post_content)s,%(user_id)s);'
        return connectToMySQL(mydb).query_db(query,data)
    
#creating a method to validate the post information
    @classmethod
    def validatepost(self, post):
        is_valid=True
        if len(post['post_title']) < 5:
            flash('Title must be at least 5 characters.')
            is_valid = False
        if len(post['post_content']) < 1:
            flash('Content must not be empty')
            is_valid = False
        if len(post['post_content'])> 245:
            flash('Content must be less that 245 characters')
            is_valid = False
        return is_valid


