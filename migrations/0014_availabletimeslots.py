# Generated by Django 4.2.4 on 2023-09-09 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0013_alter_booknow_ubookingtime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Availabletimeslots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availabletime', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]