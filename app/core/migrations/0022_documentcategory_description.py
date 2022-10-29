# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20190318_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentcategory',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
