# Generated by Django 3.1.2 on 2021-03-17 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=100000)),
            ],
        ),
        migrations.CreateModel(
            name='Qa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=100000)),
                ('answer', models.CharField(max_length=100000)),
            ],
        ),
    ]
