# Generated by Django 3.1.7 on 2021-04-02 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_comment'),
        ('users', '0004_auto_20210402_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='category_like',
            field=models.ManyToManyField(default='Category', to='posts.Category'),
        ),
    ]
