# Generated by Django 2.2.4 on 2019-08-31 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('user_email', models.EmailField(max_length=100, unique=True)),
                ('user_password', models.CharField(max_length=100)),
                ('user_fav_food', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]