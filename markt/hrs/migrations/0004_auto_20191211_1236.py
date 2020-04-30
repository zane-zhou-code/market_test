# Generated by Django 2.2.5 on 2019-12-11 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrs', '0003_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='regdate',
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=32, verbose_name='用户密码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='tel',
            field=models.IntegerField(max_length=20, verbose_name='手机号'),
        ),
    ]
