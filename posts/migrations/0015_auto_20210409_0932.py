# Generated by Django 3.1.7 on 2021-04-09 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20210409_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, height_field='720', null=True, upload_to='uploads/', verbose_name='image', width_field='1280'),
        ),
    ]