# Generated by Django 2.2.4 on 2019-08-29 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0007_auto_20190829_2250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user_id',
            new_name='user',
        ),
    ]
