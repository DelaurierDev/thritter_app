from flask_app import app
from flask import render_template, redirect,request,session,flash
from flask_app.models.post import Post
from flask_app.models.user import User

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

@app.route('/posts/edit/<id>')
def edit_post(id):
    if 'user_id' not in session:
        flash('Must Login')
        return redirect('/')
    return render_template('edit.html', post = Post.getPostByPostID({'id': id}))

@app.route('/posts/update', methods = ['POST'])
def update_post():
    redirecturl = f'/posts/edit/{request.form["id"]}'
    if not Post.validatepost(request.form):
        return redirect(redirecturl)
    
    data = {
        'id': request.form['id'],
        'post_contents' : request.form['post_content'],
        'post_title' : request.form['post_title']
    }
    Post.edit(data)
    return redirect('/mypage')

@app.route('/posts/delete/<id>')
def delete_post(id):
    if 'user_id' not in session:
        flash('Must Login')
        return redirect('/')
    Post.delete({'id' : id})
    return redirect('/mypage')

@app.route("/page/<id>")
def userPage(id):
    if 'user_id' not in session:
        flash('Must Login')
        return redirect('/')
    return render_template("page.html", posts = Post.getpostsbyuserid({"id" : id}), user = User.get_by_id({"id" : id}))