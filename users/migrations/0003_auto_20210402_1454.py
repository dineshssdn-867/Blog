# Generated by Django 3.1.7 on 2021-04-02 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_category_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='person-icon-blue-7560.png', null=True, upload_to='users'),
        ),
    ]
