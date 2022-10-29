# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20151101_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='short_name',
            field=models.CharField(max_length=200, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='ticker',
            field=models.CharField(max_length=10, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='date',
            field=models.DateTimeField(null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='documentcategory',
            name='type',
            field=models.CharField(default=b'other', max_length=200, null=True, db_index=True),
        ),
    ]
