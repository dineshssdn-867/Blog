# Generated by Django 3.1.7 on 2021-04-28 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0022_auto_20210428_1159'),
        ('myarchive', '0005_archive'),
    ]

    operations = [
        migrations.AddField(
            model_name='archive',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='posts.post'),
        ),
    ]
