# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-11 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('url', models.CharField(max_length=80)),
                ('CMS', models.CharField(max_length=20, null=True)),
                ('Message_Boards', models.CharField(max_length=20, null=True)),
                ('Database_Managers', models.CharField(max_length=20, null=True)),
                ('Documentation_Tools', models.CharField(max_length=20, null=True)),
                ('Widgets', models.CharField(max_length=20, null=True)),
                ('Ecommerce', models.CharField(max_length=20, null=True)),
                ('Photo_Galleries', models.CharField(max_length=20, null=True)),
                ('Wikis', models.CharField(max_length=20, null=True)),
                ('Hosting_Panels', models.CharField(max_length=20, null=True)),
                ('Analytics', models.CharField(max_length=20, null=True)),
                ('Blogs', models.CharField(max_length=20, null=True)),
                ('Javascript_Frameworks', models.CharField(max_length=20, null=True)),
                ('Issue_Trackers', models.CharField(max_length=20, null=True)),
                ('Video_Players', models.CharField(max_length=20, null=True)),
                ('Comment_Systems', models.CharField(max_length=20, null=True)),
                ('Captchas', models.CharField(max_length=20, null=True)),
                ('Font_Scripts', models.CharField(max_length=20, null=True)),
                ('Web_Frameworks', models.CharField(max_length=20, null=True)),
                ('Miscellaneous', models.CharField(max_length=20, null=True)),
                ('Editors', models.CharField(max_length=20, null=True)),
                ('LMS', models.CharField(max_length=20, null=True)),
                ('Web_Servers', models.CharField(max_length=20, null=True)),
                ('Cache_Tools', models.CharField(max_length=20, null=True)),
                ('Rich_Text_Editors', models.CharField(max_length=20, null=True)),
                ('Javascript_Graphics', models.CharField(max_length=20, null=True)),
                ('Mobile_Frameworks', models.CharField(max_length=20, null=True)),
                ('Programming_Languages', models.CharField(max_length=20, null=True)),
                ('Operating_Systems', models.CharField(max_length=20, null=True)),
                ('Search_Engines', models.CharField(max_length=20, null=True)),
                ('Web_Mail', models.CharField(max_length=20, null=True)),
                ('CDN', models.CharField(max_length=20, null=True)),
                ('Marketing_Automation', models.CharField(max_length=20, null=True)),
                ('Web_Server_Extensions', models.CharField(max_length=20, null=True)),
                ('Databases', models.CharField(max_length=20, null=True)),
                ('Maps', models.CharField(max_length=20, null=True)),
                ('Advertising_Networks', models.CharField(max_length=20, null=True)),
                ('Network_Devices', models.CharField(max_length=20, null=True)),
                ('Media_Servers', models.CharField(max_length=20, null=True)),
                ('Webcams', models.CharField(max_length=20, null=True)),
                ('Printers', models.CharField(max_length=20, null=True)),
                ('Payment_Processors', models.CharField(max_length=20, null=True)),
                ('Tag_Managers', models.CharField(max_length=20, null=True)),
                ('Paywalls', models.CharField(max_length=20, null=True)),
                ('Build_CI_Systems', models.CharField(max_length=20, null=True)),
                ('Control_Systems', models.CharField(max_length=20, null=True)),
                ('Remote_Access', models.CharField(max_length=20, null=True)),
                ('Dev_Tools', models.CharField(max_length=20, null=True)),
                ('Network_Storage', models.CharField(max_length=20, null=True)),
                ('Feed_Readers', models.CharField(max_length=20, null=True)),
                ('Document_Management_Systems', models.CharField(max_length=20, null=True)),
                ('Landing_Page_Builders', models.CharField(max_length=20, null=True)),
                ('Live_Chat', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]