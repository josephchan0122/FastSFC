# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151029_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentcategory',
            name='type',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
