# Generated by Django 3.1.7 on 2021-05-23 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_auto_20210523_1328'),
        ('myarchive', '0017_auto_20210523_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='posts.post'),
        ),
    ]