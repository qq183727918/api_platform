# Generated by Django 3.1.7 on 2021-03-02 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_api', '0007_db_step_public_header'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=100, null=True)),
                ('des', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
