from app import create_app, db, cli
from app.models import User, Post, Notification, Message, Task, Comment, Role


app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'Role': Role,'User':User, 'Post':Post, 'Message': Message, 'Notification': Notification, 'Task':Task, 'Comment': Comment}
