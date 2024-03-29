# Generated by Django 2.2.4 on 2019-09-06 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_auto_20190904_1055'),
        ('user', '0003_auto_20190906_1610'),
        ('comments', '0004_comment_deleted_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='Restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.Restaurant'),
        ),
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='deleted',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.User'),
            preserve_default=False,
        ),
    ]
