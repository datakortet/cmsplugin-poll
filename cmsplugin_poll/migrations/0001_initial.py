# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(max_length=200, verbose_name='choice')),
                ('votes', models.IntegerField(default=0, verbose_name='votes')),
            ],
            options={
                'verbose_name': 'Choice',
                'verbose_name_plural': 'Choices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=300, verbose_name='question')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('close_date', models.DateTimeField(null=True, verbose_name='date closed')),
            ],
            options={
                'ordering': ('-pub_date',),
                'db_table': 'cmsplugin_poll_poll',
                'verbose_name': 'Poll',
                'verbose_name_plural': 'Polls',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PollPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin', on_delete=models.CASCADE)),
                ('poll', models.ForeignKey(verbose_name='Poll to display', to='cmsplugin_poll.Poll', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Poll plugin',
                'verbose_name_plural': 'Poll plugins',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(verbose_name='poll', to='cmsplugin_poll.Poll', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
