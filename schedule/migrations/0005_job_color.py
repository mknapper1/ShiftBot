# Generated by Django 2.0.6 on 2018-06-23 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20180623_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='color',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]