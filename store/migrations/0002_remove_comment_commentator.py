# Generated by Django 4.0.4 on 2022-05-08 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='commentator',
        ),
    ]