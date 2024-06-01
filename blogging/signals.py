from blogging.models import (
    Blog,
    TopicBlogMapping
)
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
import re
from bs4 import BeautifulSoup


@receiver(pre_save, sender=Blog)
def before_blog_saved(sender, instance: Blog, **kwargs):
    instance.title_slug = slugify(instance.title)
    soup = BeautifulSoup(instance.content, 'html.parser')
    
    text = soup.get_text()

    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text = re.sub(r'&nbsp;', ' ', cleaned_text)
    cleaned_text = re.sub(r'\r\n', ' ', cleaned_text)
    
    instance.total_read_time = round(len(cleaned_text.split()) / 200)


@receiver(post_save, sender=Blog)
def after_blog_saved(sender, instance: Blog, created: bool, **kwargs):
    if created:
        pass
    else:
        if not instance.active:
            for topic_blog_mapping in TopicBlogMapping.objects.filter(blog=instance):
                topic_blog_mapping.topic.total_blogs -= 1
                topic_blog_mapping.topic.save()


@receiver(post_save, sender=TopicBlogMapping)
def before_topic_blog_mapping_saved(sender, instance: Blog, created: bool, **kwargs):
    if created:
        pass
    else:
        pass

    for topic_blog_mapping in TopicBlogMapping.objects.filter(active=True): # TODO: Definitely need a better approach here
        topic_blog_mapping.topic.total_blogs = TopicBlogMapping.objects.filter(topic=topic_blog_mapping.topic, blog__active=True).count()
        topic_blog_mapping.topic.save()