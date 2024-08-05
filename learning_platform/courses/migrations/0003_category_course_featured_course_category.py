# Generated by Django 5.0.7 on 2024-08-04 08:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_favorites'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='courses.category'),
        ),
    ]