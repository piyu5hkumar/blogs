from django.db import connection
from utils.helper import dictfetchall

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


def get_hot_blogs(total=3):
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
            ORDER BY
                blog.total_likes DESC, 
                blog.total_comments DESC
            LIMIT {total}
        '''
    
        # print(query)
        cursor.execute(query)
        return dictfetchall(cursor)
    


def get_new_blogs(total=3):
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
            ORDER BY
                blog.created_at DESC,
                blog.total_likes DESC, 
                blog.total_comments DESC
            LIMIT {total}
        '''
    
        # print(query)
        cursor.execute(query)
        return dictfetchall(cursor)

