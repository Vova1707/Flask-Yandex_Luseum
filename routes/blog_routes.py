from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from db_session import create_session
from models.blog import BlogPost
from models.users import User

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

@blog_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_blog_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        session = create_session()
        user = session.query(User).get(current_user.id)
        blog_post = BlogPost(title=title, content=content)
        blog_post.author = user
        session.add(blog_post)
        session.commit()
        return redirect(url_for('index'))

    return render_template('blog/create.html')

@blog_bp.route('/<int:post_id>')
def view_blog_post(post_id):
    session = create_session()
    post = session.query(BlogPost).get(post_id)
    if not post:
        flash('Запись не найдена.', 'danger')
        return redirect(url_for('index'))
    return render_template('blog/view.html', post=post)

@blog_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_blog_post(post_id):
    session = create_session()
    post = session.query(BlogPost).get(post_id)
    if not post:
        flash('Запись не найдена.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if title and content:
            post.title = title
            post.content = content
            session.commit()
            flash('Запись успешно обновлена!', 'success')
            return redirect(url_for('blog.view_blog_post', post_id=post.id))
        else:
            flash('Заголовок и содержимое обязательны.', 'danger')

    return render_template('blog/edit.html', post=post)