# Generated by Django 3.1.7 on 2021-05-23 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_auto_20210523_1328'),
        ('myarchive', '0006_auto_20210523_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='posts.post'),
        ),
    ]
