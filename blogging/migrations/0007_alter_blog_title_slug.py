# Generated by Django 5.0.6 on 2024-05-29 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0006_blog_title_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title_slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
