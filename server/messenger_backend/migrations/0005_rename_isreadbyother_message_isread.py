# Generated by Django 3.2.4 on 2022-04-04 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messenger_backend', '0004_auto_20220401_2039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='isReadByOther',
            new_name='isRead',
        ),
    ]