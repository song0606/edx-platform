# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0012_sociallink'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseEntitlement',
            fields=[
                ('root_course', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True, null=True)),
                ('enroll_end_date', models.DateTimeField()),
                ('mode', models.CharField(default=b'audit', max_length=100)),
                ('is_active', models.BooleanField(default=1)),
                ('enrollment_course', models.ForeignKey(to='student.CourseEnrollment', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
