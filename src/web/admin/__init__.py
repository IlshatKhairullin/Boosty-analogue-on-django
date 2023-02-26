from django.contrib import admin

from web.models import Post, Comment, User
from web.admin.post import PostAdmin
from web.admin.comment import CommentAdmin
from web.admin.user import MyUserAdmin

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, MyUserAdmin)
