# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_price_volume'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='period',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='metric',
            name='synonyms',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
