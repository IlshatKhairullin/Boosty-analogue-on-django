from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from mysite.celery import app
from web.models import Comment


@app.task
def send_comment_notification(post_comment_id: int, link_to_post: str):
    post_comment = Comment.objects.get(id=post_comment_id)
    post = post_comment.post

    rendered = render_to_string(
        "web/emails/comment_notification.html",
        {
            "user_name": post.author.username,
            "link_to_post": link_to_post,
            "post_title": post.title,
            "comment_text": post_comment.body,
        },
    )

    send_mail("Новый комментарий", "", settings.DEFAULT_FROM_EMAIL, [post.author.email], html_message=rendered)
