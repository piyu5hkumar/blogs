from django.db import connection
from utils.helper import dictfetchall
from blogging.models import Blog, Like, LikeBlogMapping
from blog_users.models import User


def get_active_topics_and_total_blogs():
    with connection.cursor() as cursor:
        query = f'''
            SELECT
                name,
                total_blogs
            FROM
                blogging_topic
            WHERE
                active = 1
                AND total_blogs > 0
        '''
    
        # print(query)
        cursor.execute(query)
        return dictfetchall(cursor)
    

def get_active_blogs_wrt_topic(topic_name):
    with connection.cursor() as cursor:
        query = f'''
            SELECT
                blog.title, 
                blog.total_likes,
                blog.total_read_time,
                blog.total_comments,
                blog.created_at,
                blog.title_slug,
                topic.name topic_name
            FROM 
                blogging_topic topic
                JOIN blogging_topicblogmapping topicblogmapping ON topicblogmapping.topic_id = topic.id
                JOIN blogging_blog blog ON blog.id = topicblogmapping.blog_id
            WHERE
                topic.active
                AND topicblogmapping.active
                AND blog.active
                AND topic.name = '{topic_name}'
            ORDER BY
                blog.created_at DESC
        '''
    
        # print(query)
        cursor.execute(query)
        return dictfetchall(cursor)


def like_a_blog(blog: Blog, user:User):
    like = Like.objects.filter(user=user).first()
    if not like:
        like = Like()
        like.user = user
        like.save()

    like_blog_mapping = LikeBlogMapping.objects.filter(like=like, blog=blog).first()
    if not like_blog_mapping:
        like_blog_mapping = LikeBlogMapping()
        like_blog_mapping.like = like
        like_blog_mapping.blog = blog
        like_blog_mapping.save()

        blog.total_likes += 1
        blog.save()
