# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20190515_1003'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='watchlist',
            unique_together=set([('company', 'user')]),
        ),
    ]
