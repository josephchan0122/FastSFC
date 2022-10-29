# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20190324_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='ticker_alt',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='short_alt_name',
            field=models.CharField(max_length=100, unique=True, null=True, db_index=True),
        ),
    ]
