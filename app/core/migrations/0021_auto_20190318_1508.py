# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_websitedocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentcategory',
            name='name',
            field=models.CharField(default='Default', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='documentcategory',
            name='type',
            field=models.CharField(default=b'other', max_length=200, db_index=True),
        ),
    ]
