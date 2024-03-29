# Generated by Django 4.2.9 on 2024-02-24 18:58

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_userprofile_active_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=django_resized.forms.ResizedImageField(crop=None, default='avatars/default.png', force_format=None, keep_meta=True, quality=-1, scale=None, size=[300, 300], upload_to='avatars/'),
        ),
    ]
