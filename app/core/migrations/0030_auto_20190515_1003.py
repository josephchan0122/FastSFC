# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20190513_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='cached',
            field=models.SmallIntegerField(default=0, db_index=True, choices=[(0, b'Not started'), (1, b'Started'), (2, b'Success'), (3, b'Error')]),
        ),
        migrations.AlterField(
            model_name='document',
            name='indexed',
            field=models.SmallIntegerField(default=0, db_index=True, choices=[(0, b'Not started'), (1, b'Started'), (2, b'Success'), (3, b'Error')]),
        ),
        migrations.AlterField(
            model_name='document',
            name='parsed',
            field=models.SmallIntegerField(default=0, db_index=True, choices=[(0, b'Not started'), (1, b'Started'), (2, b'Success'), (3, b'Error')]),
        ),
    ]
