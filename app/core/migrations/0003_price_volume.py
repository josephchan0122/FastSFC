# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_metric_price_timeseries'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='volume',
            field=models.FloatField(null=True),
        ),
    ]
