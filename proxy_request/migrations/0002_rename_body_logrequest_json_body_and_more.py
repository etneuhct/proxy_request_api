# Generated by Django 4.2 on 2023-04-15 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxy_request', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logrequest',
            old_name='body',
            new_name='json_body',
        ),
        migrations.AlterField(
            model_name='logrequest',
            name='exception_message',
            field=models.TextField(default=None),
        ),
    ]
