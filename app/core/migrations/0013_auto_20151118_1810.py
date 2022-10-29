# -*- coding: utf-8 -*-


from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20151110_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, db_index=True)),
                ('description', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='timeseries',
            old_name='date_to',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='timeseries',
            old_name='date_from',
            new_name='start_date',
        ),
        migrations.RemoveField(
            model_name='metric',
            name='period',
        ),
        migrations.RemoveField(
            model_name='metric',
            name='synonyms',
        ),
        migrations.RemoveField(
            model_name='timeseries',
            name='company',
        ),
        migrations.RemoveField(
            model_name='timeseries',
            name='document',
        ),
        migrations.RemoveField(
            model_name='timeseries',
            name='source',
        ),
        migrations.AddField(
            model_name='metric',
            name='meta',
            field=jsonfield.fields.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='metric',
            name='type',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='timeseries',
            name='type',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='metric',
            name='name',
            field=models.CharField(default='Default', unique=True, max_length=255, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metric',
            name='source',
            field=models.ForeignKey(default=None, to='core.Source', null=True),
        ),
    ]
