# Generated by Django 4.2.4 on 2023-09-09 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0009_booknow_ubookingstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
            ],
        ),
    ]
