# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_company_alt_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='industry',
        ),
        migrations.AddField(
            model_name='company',
            name='industry',
            field=models.ForeignKey(to='core.Industry', null=True),
        ),
    ]
