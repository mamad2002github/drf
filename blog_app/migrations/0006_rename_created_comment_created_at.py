# Generated by Django 5.1.3 on 2024-12-11 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0005_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='created',
            new_name='created_at',
        ),
    ]
