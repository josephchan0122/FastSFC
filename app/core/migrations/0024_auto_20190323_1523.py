# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20190323_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='ref',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
