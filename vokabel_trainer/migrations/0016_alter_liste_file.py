# Generated by Django 3.2.7 on 2021-09-26 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vokabel_trainer', '0015_liste_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liste',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
