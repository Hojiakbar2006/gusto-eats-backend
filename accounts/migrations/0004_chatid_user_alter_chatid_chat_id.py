# Generated by Django 5.0.1 on 2024-03-03 14:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_chatid_chat_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatid',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chatid',
            name='chat_id',
            field=models.SmallIntegerField(),
        ),
    ]
