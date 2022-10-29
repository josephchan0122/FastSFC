# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20190423_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentcount',
            name='cache_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='documentcount',
            name='index_count',
            field=models.IntegerField(null=True),
        ),
    ]
