# Generated by Django 3.2.3 on 2021-06-09 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=128, verbose_name='标题')),
                ('content', models.TextField(default='', verbose_name='内容')),
                ('visit', models.IntegerField(default=0, verbose_name='浏览量')),
                ('host', models.CharField(max_length=32, verbose_name='主办方')),
                ('image', models.CharField(default=None, max_length=256, null=True, verbose_name='图片')),
                ('from_time', models.DateTimeField(verbose_name='开始时间')),
                ('to_time', models.DateTimeField(verbose_name='结束时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(default=None, null=True, verbose_name='删除时间')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('delete_time', models.DateTimeField(default=None, null=True, verbose_name='删除时间')),
            ],
        ),
    ]