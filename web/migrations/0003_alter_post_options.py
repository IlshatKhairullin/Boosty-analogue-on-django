# Generated by Django 4.1.1 on 2022-10-02 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_authorinfo_img'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-publish',)},
        ),
    ]