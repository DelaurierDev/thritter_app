from flask_app import app
from flask import render_template, redirect,request,session,flash
from flask_app.models.post import Post

@app.route('/posts/save', methods = ['POST'])
def save_post():
    if 'user_id' not in session:
        flash('Must Login')
        return redirect('/')
    if not Post.validatepost(request.form):
        return redirect('/dashboard')
    data = {
        'post_title': request.form['post_title'],
        'post_content': request.form['post_content'],
        'user_id': session['user_id']
    }
    Post.savepost(data)
    return redirect('/dashboard')