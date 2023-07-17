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

    @staticmethod
    def getallposts():
        query = '''
        SELECT *
        FROM posts
        LEFT JOIN users on users.id = posts.user_id'''
        results = connectToMySQL(mydb).query_db(query)
        results2 = results[::-1]
        return results2
    
    @classmethod
    def getpostsbyuserid(cls, id):
        posts = []
        query = '''
        SELECT * FROM posts
        WHERE user_id = %(id)s'''
        results = connectToMySQL(mydb).query_db(query,id)
        for row in results:
            posts.append(row)
        posts2 = posts[::-1]
        return posts2
    
    @classmethod
    def getPostByPostID(cls, id):
        query= '''
        SELECT *
        FROM posts
        WHERE id = %(id)s;
        
        '''
        results = connectToMySQL(mydb).query_db(query,id)
        return results[0]
    
    @classmethod
    def edit(cls, id):
        query = '''
        UPDATE posts
        SET post_title = %(post_title)s,
        post_contents = %(post_contents)s,
        updated_at = NOW()
        WHERE id = %(id)s;
        '''
        return connectToMySQL(mydb).query_db(query, id)
    
    @classmethod
    def delete(cls, id):
        query = '''
        DELETE FROM posts
        WHERE id = %(id)s;
        '''
        return connectToMySQL(mydb).query_db(query,id)

