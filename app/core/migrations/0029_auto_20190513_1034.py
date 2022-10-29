# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20190428_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentSummary',
            fields=[
            ],
            options={
                'verbose_name': 'Document Summary',
                'proxy': True,
                'verbose_name_plural': 'Document Summary',
            },
            bases=('core.document',),
        ),
        migrations.AddField(
            model_name='document',
            name='cached',
            field=models.SmallIntegerField(default=0, choices=[(0, b'Not started'), (1, b'Started'), (2, b'Success'), (3, b'Error')]),
        ),
        migrations.AddField(
            model_name='document',
            name='parsed',
            field=models.SmallIntegerField(default=0, choices=[(0, b'Not started'), (1, b'Started'), (2, b'Success'), (3, b'Error')]),
        ),
        migrations.AlterField(
            model_name='document',
            name='filetype',
            field=models.CharField(max_length=20, null=True, choices=[(b'pdf', b'pdf'), (b'html', b'html'), (b'htm', b'htm'), (b'ppt', b'ppt'), (b'doc', b'doc'), (b'Multiple', b'Multiple')]),
        ),
        migrations.AlterField(
            model_name='document',
            name='indexed',
            field=models.SmallIntegerField(default=0, choices=[(0, b'Not started'), (1, b'Started'), (2, b'Success'), (3, b'Error')]),
        ),
    ]
