from django.core.mail import send_mail
from django.conf import settings

from mysite.celery import app
from web.models import Comment


@app.task
def send_comment_notification(post_comment_id: int):
    post_comment = Comment.objects.get(id=post_comment_id)
    post = post_comment.post

    text = f"К посту {post.title} был оставлен комментарий: \n{post_comment.body}"

    send_mail(
        "Новый комментарий",
        text,
        settings.DEFAULT_FROM_EMAIL,
        [post.author.email],
    )
