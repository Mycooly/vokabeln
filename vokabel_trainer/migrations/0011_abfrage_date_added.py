# Generated by Django 3.2.7 on 2021-09-24 09:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vokabel_trainer', '0010_abfrage'),
    ]

    operations = [
        migrations.AddField(
            model_name='abfrage',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
