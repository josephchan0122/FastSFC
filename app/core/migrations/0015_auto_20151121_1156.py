# -*- coding: utf-8 -*-


from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_dashboard_pipeline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('meta', jsonfield.fields.JSONField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='dashboard',
            name='meta',
        ),
        migrations.AddField(
            model_name='dashboard',
            name='charts',
            field=models.ManyToManyField(to='core.Chart'),
        ),
    ]
