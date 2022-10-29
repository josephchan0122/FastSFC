# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_documentcategory_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentcategory',
            name='type',
            field=models.CharField(default=b'other', max_length=200, null=True),
        ),
    ]
