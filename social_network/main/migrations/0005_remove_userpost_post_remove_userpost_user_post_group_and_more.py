# Generated by Django 4.2.1 on 2023-05-29 22:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_userpost_postlike_postcomment_grouppost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpost',
            name='post',
        ),
        migrations.RemoveField(
            model_name='userpost',
            name='user',
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.group'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='GroupPost',
        ),
        migrations.DeleteModel(
            name='UserPost',
        ),
    ]
