# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20190317_0646'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebsiteDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(to='core.Company', null=True)),
            ],
        ),
    ]
