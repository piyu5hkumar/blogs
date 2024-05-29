from django.db import models
from utils.abstract_models import BaseModel
from blog_users.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify



class Blog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    title_slug = models.SlugField(null=True, unique=True, blank=True)
    content = RichTextUploadingField()
    total_likes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title


@receiver(pre_save, sender=Blog)
def set_title_slug(sender, instance: Blog, **kwargs):
    instance.title_slug = slugify(instance.title)


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    parent_comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)
    total_comments = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Topic(BaseModel):
    name = models.CharField(max_length=100)
    total_blogs = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.name


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


class TopicBlogMapping(BaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
