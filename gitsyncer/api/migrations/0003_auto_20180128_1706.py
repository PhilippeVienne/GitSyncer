# Generated by Django 2.0.1 on 2018-01-28 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180128_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mirror',
            name='ssh_key',
        ),
        migrations.AddField(
            model_name='repository',
            name='ssh_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.SSHKey'),
        ),
    ]
