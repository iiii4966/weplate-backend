# Generated by Django 2.2.4 on 2019-08-28 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelTable(
            name='comment',
            table='commemts',
        ),
    ]