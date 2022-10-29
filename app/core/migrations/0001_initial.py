# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticker', models.CharField(max_length=10, null=True)),
                ('full_name', models.CharField(max_length=200, null=True)),
                ('short_name', models.CharField(max_length=200, null=True)),
                ('website', models.URLField(null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(null=True)),
                ('url', models.URLField(null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('size', models.IntegerField(null=True)),
                ('filetype', models.CharField(max_length=20, null=True, choices=[(b'PDF', b'PDF'), (b'HTML', b'HTML'), (b'HTM', b'HTM'), (b'PPT', b'PPT'), (b'DOC', b'DOC'), (b'Multiple', b'Multiple')])),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Document Categories',
            },
        ),
        migrations.CreateModel(
            name='DocumentCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actual_count', models.IntegerField(null=True)),
                ('our_count', models.IntegerField(null=True)),
                ('company', models.ForeignKey(to='core.Company')),
            ],
            options={
                'verbose_name_plural': 'Document Counts',
            },
        ),
        migrations.CreateModel(
            name='DocumentSubcategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1000, null=True)),
            ],
            options={
                'verbose_name_plural': 'Document Subcategories',
            },
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=20, null=True)),
                ('full_name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='cat',
            field=models.ForeignKey(to='core.DocumentCategory', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='company',
            field=models.ForeignKey(to='core.Company', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='subcat',
            field=models.ForeignKey(to='core.DocumentSubcategory', null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='exchange',
            field=models.ForeignKey(to='core.Exchange', null=True),
        ),
    ]
