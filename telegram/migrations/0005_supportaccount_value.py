# Generated by Django 4.2 on 2024-06-16 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0004_alter_telegramchannels_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportaccount',
            name='value',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
