# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20151122_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dashboard',
            name='charts',
        ),
        migrations.DeleteModel(
            name='Pipeline',
        ),
        migrations.DeleteModel(
            name='Chart',
        ),
        migrations.DeleteModel(
            name='Dashboard',
        ),
    ]
