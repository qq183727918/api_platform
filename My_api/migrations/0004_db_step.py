# Generated by Django 3.1.7 on 2021-02-26 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_api', '0003_db_cases'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Case_id', models.CharField(max_length=10, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('index', models.IntegerField(null=True)),
                ('api_method', models.CharField(max_length=10, null=True)),
                ('api_url', models.CharField(max_length=1000, null=True)),
                ('api_host', models.CharField(max_length=100, null=True)),
                ('api_header', models.CharField(max_length=1000, null=True)),
                ('api_body_method', models.CharField(max_length=10, null=True)),
                ('api_body', models.CharField(max_length=10, null=True)),
                ('get_path', models.CharField(max_length=500, null=True)),
                ('get_zz', models.CharField(max_length=500, null=True)),
                ('assert_zz', models.CharField(max_length=500, null=True)),
                ('assert_qz', models.CharField(max_length=500, null=True)),
                ('assert_path', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]
