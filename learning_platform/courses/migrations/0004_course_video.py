# Generated by Django 5.0.7 on 2024-08-07 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_category_course_featured_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='course_videos/'),
        ),
    ]
