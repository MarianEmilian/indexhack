# Generated by Django 3.2.1 on 2021-06-15 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_company_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='url',
            field=models.URLField(default=None),
        ),
    ]