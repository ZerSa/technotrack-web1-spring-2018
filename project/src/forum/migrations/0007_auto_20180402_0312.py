# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-02 03:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_topic_is_archive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Topic', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Тема'),
        ),
    ]