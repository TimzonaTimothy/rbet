# Generated by Django 3.0.5 on 2022-02-06 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='code',
            field=models.CharField(blank=True, default='2hGodriQ', max_length=8, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='account',
            name='recommended_by',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
