# Generated by Django 4.0.4 on 2022-05-18 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymbo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='date_ended',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
