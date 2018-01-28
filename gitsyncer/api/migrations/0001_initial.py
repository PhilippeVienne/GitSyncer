# Generated by Django 2.0.1 on 2018-01-28 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mirror',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.URLField(verbose_name='origine')),
                ('destination', models.URLField(verbose_name='destination')),
                ('enabled', models.BooleanField(default=True, verbose_name='activé')),
                ('last_sync', models.DateTimeField(blank=True, null=True, verbose_name='dernière synchronisation')),
            ],
        ),
    ]