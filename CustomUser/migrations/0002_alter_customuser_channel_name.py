# Generated by Django 5.0 on 2023-12-26 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='channel_name',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]