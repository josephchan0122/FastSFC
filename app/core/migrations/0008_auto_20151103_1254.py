# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151102_0813'),
    ]

    operations = [
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sector', models.CharField(max_length=1000)),
                ('industry_group', models.CharField(max_length=1000)),
                ('industry', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='industry',
            field=models.ForeignKey(to='core.Industry', null=True),
        ),
    ]
