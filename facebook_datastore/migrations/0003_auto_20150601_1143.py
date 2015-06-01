# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_datastore', '0002_auto_20150212_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebookuserprofile',
            name='about_me',
            field=models.TextField(null=True, blank=True, help_text='needs user_about_me'),
        ),
        migrations.AlterField(
            model_name='facebookuserprofile',
            name='birthday',
            field=models.DateField(null=True, blank=True, help_text='needs user_birthday'),
        ),
        migrations.AlterField(
            model_name='facebookuserprofile',
            name='gender',
            field=models.CharField(null=True, max_length=1, choices=[('m', 'Male'), ('f', 'Female')], blank=True),
        ),
        migrations.AlterField(
            model_name='facebookuserprofile',
            name='location_id',
            field=models.TextField(null=True, blank=True, help_text='needs user_location'),
        ),
        migrations.AlterField(
            model_name='facebookuserprofile',
            name='location_name',
            field=models.TextField(null=True, blank=True, help_text='needs user_location'),
        ),
        migrations.AlterField(
            model_name='facebookuserprofile',
            name='relationship_status',
            field=models.TextField(null=True, blank=True, help_text='needs user_relationship'),
        ),
        migrations.AlterField(
            model_name='facebookuserprofile',
            name='website',
            field=models.TextField(null=True, blank=True, help_text='needs user_website'),
        ),
    ]
