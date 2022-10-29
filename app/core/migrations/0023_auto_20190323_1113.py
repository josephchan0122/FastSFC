# -*- coding: utf-8 -*-


from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_documentcategory_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='meta',
            field=jsonfield.fields.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='ref',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
