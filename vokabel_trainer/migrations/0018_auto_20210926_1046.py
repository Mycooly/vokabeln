# Generated by Django 3.2.7 on 2021-09-26 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vokabel_trainer', '0017_alter_abfrage_reihenfolge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abfrage',
            name='reihenfolge',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='liste',
            name='file',
            field=models.FileField(default='default.txt', upload_to=''),
        ),
    ]
