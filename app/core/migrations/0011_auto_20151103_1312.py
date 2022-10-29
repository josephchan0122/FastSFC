# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20151103_1303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='alt_name',
            new_name='full_alt_name',
        ),
        migrations.AddField(
            model_name='company',
            name='short_alt_name',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
