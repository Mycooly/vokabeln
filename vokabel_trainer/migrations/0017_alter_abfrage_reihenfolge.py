# Generated by Django 3.2.7 on 2021-09-26 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vokabel_trainer', '0016_alter_liste_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abfrage',
            name='reihenfolge',
            field=models.CharField(default='default.txt', max_length=10000),
        ),
    ]
