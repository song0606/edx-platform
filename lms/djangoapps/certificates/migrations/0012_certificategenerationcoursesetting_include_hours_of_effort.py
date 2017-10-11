# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0011_certificatetemplate_alter_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificategenerationcoursesetting',
            name='include_hours_of_effort',
            field=models.BooleanField(default=True, help_text='Include estimated time to complete the course in the certificate rendering context. This attribute will only be displayed in certificates when there exists a template that includes Hours of Effort.'),
        ),
    ]
