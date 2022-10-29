# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField(null=True)),
                ('message', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=0, choices=[(0, b'OK'), (1, b'ERROR')])),
                ('message', models.TextField(null=True)),
            ],
        ),
    ]
