# Generated by Django 3.1.7 on 2021-03-04 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_api', '0012_db_global_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_project',
            name='user_id',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
