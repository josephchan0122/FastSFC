# -*- coding: utf-8 -*-


from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20190323_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='industry',
            name='industry_group',
        ),
        migrations.AddField(
            model_name='company',
            name='meta',
            field=jsonfield.fields.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='industry',
            name='code',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='industry',
            name='subsector',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='industry',
            name='supersector',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='industry',
            name='industry',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='industry',
            name='sector',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
