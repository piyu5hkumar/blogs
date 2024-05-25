from django.db import models
from utils.abstract_models import BaseModel
from blog_users.models import User

class Blog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    total_likes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    parent_comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)
    total_comments = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


#### Mappings ###


class CommentBlogMapping(BaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class LikeBlogMapping(BaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)


class LikeCommentMapping(BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)



