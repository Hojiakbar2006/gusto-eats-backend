# Generated by Django 5.0.1 on 2024-02-22 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_chatid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatid',
            name='chat_id',
            field=models.SmallIntegerField(max_length=10),
        ),
    ]