# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20151103_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='date',
            field=models.DateTimeField(null=True, db_index=True),
        ),
    ]
