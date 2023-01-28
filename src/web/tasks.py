from mysite.celery import app
from web.models import Comment


@app.task
def send_comment_notification(post_comment_id: int):
    post_comment = Comment.objects.get(id=post_comment_id)
    post = post_comment.post
    print(f"Уведомление отправлено автору {post.author} поста {post}")
