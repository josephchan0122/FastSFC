# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20190625_0615'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='cached_url',
            field=models.URLField(null=True),
        ),
    ]
