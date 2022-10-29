# -*- coding: utf-8 -*-


from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20151118_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('meta', jsonfield.fields.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('inputs', jsonfield.fields.JSONField(null=True)),
                ('schedule', jsonfield.fields.JSONField(null=True)),
            ],
        ),
    ]
