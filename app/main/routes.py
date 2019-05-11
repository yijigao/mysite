from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app, send_from_directory, abort
from flask_login import current_user, login_required, AnonymousUserMixin
from flask_babel import _, get_locale
from app import db
from app.main.forms import EditProfileForm, PostForm, SearchForm, MessageForm, CommentForm
from app.models import User, Post, Message, Notification, Comment
from app.main import bp
import os
import moment



@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())

# @bp.route('/favicon.ico', methods=['GET', 'POST'])
# def favicon():
#     return send_from_directory(os.path.join(current_app.root_path, 'static'), 'favicon.ico')

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('动态发布成功！')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    posts = pagination.items
    # next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    # prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Home', form=form, posts=posts, pagination=pagination)

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    posts = pagination.items
    # next_url = url_for('main.explore', page=posts.next_num) \
    #     if posts.has_next else None
    # prev_url = url_for('main.explore', page=posts.prev_num) \
    #     if posts.has_prev else None
    return render_template('index.html', title='随便看看',
                           posts=posts, pagination=pagination)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config["POSTS_PER_PAGE"], False)
    # next_url = url_for('main.user', username=user.username, page=posts.next_num) if posts.has_next else None
    # prev_url = url_for('main.user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, pagination=pagination)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('你的更改已保存！')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='编辑个人资料',
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'用户名{username}没找到！')
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('你不能关注你自己')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f'你关注了{username}!')
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'用户名{username}没找到！')
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('你不能取消关注你自己')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'你不再关注{username}!')
    return redirect(url_for('main.user', username=username))



# @bp.route('/search')
# @login_required
# def search():
#     if not g.search_form.validate():
#         return redirect(url_for("main.explore"))
#     page = request.args.get('page', 1, type=int)
#     posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
#     next_url = url_for('main.search', q=g.search_form.q.data, page=page+1) if total > page*current_app.config['POSTS_PER_PAGE'] else None
#     prev_url = url_for('main.search', q=g.search_form.q.data, page=page+1) if page > 1 else None
#     return render_template("search.html", title='Search', posts=posts, next_url=next_url, prev_url=prev_url)


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.message.data)
        db.session.add(msg)
        user.add_notification('未读私信', user.new_messages())
        db.session.commit()
        flash('私信发送成功！')
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title='Send Message', form=form, recipient=recipient)

@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('未读私信', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    pagination = current_user.messages_received.order_by(Message.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for('main.messages', page=messages.next_num) if messages.has_next else None
    # prev_url = url_for("main.messages", page=messages.prev_num) if messages.has_prev else None
    messages = pagination.items
    return render_template('messages.html', messages=messages, pagination=pagination)

@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])

@bp.route('/export_posts')
@login_required
def export_posts():
    if current_user.get_task_in_progress('export_posts'):
        flash('一项导出任务正在执行..')
    else:
        current_user.launch_task('export_posts', 'Exporting posts...')
        db.session.commit()
    return redirect(url_for('main.user', username=current_user.username))

@bp.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author: # and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.post.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been update.')
        return redirect(url_for('main.post', id=post.id))
    form.post.data = post.body
    return render_template('edit_post.html', form=form)






@bp.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit(): #and current_user.can(Permission.COMMENT):
        comment = Comment(body=form.body.data, post=post, author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('评论发布成功~')
        return redirect(url_for('main.post', id=post.id, page=-1))
    page = request.args.get('page', 1 , type=int)
    if page == -1:
        page = (post.comments.count() - 1) // current_app.config['POSTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form, comments=comments, pagination=pagination)

@bp.route('/delete_post/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    post.isvalid = False
    db.session.add(post)
    db.session.commit()
    return redirect(url_for("main.index"))