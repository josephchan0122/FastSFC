# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1000, null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(null=True)),
                ('open', models.FloatField(null=True)),
                ('high', models.FloatField(null=True)),
                ('low', models.FloatField(null=True)),
                ('close', models.FloatField(null=True)),
                ('adj_close', models.FloatField(null=True)),
                ('company', models.ForeignKey(to='core.Company', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Timeseries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(max_length=1000, null=True)),
                ('date_from', models.DateTimeField(null=True)),
                ('date_to', models.DateTimeField(null=True)),
                ('value', models.FloatField(null=True)),
                ('company', models.ForeignKey(to='core.Company', null=True)),
                ('document', models.ForeignKey(to='core.Document', null=True)),
                ('metric', models.ForeignKey(to='core.Metric')),
            ],
        ),
    ]
