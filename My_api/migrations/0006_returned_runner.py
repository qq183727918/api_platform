# Generated by Django 3.1.7 on 2021-04-30 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_api', '0005_usertoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='Returned',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apis_id', models.IntegerField(blank=True)),
                ('extract_path', models.TextField(blank=True)),
                ('extract_re', models.TextField(blank=True)),
                ('expected', models.TextField(blank=True)),
                ('assert_re', models.TextField(blank=True)),
                ('assert_path', models.TextField(blank=True)),
                ('mock_res', models.TextField(blank=True)),
                ('is_delete', models.IntegerField()),
            ],
            options={
                'db_table': 'returned',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Runner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('is_gunzip', models.IntegerField()),
                ('user_id', models.CharField(max_length=255)),
                ('created_time', models.DateTimeField()),
                ('is_delete', models.IntegerField()),
            ],
            options={
                'db_table': 'runner',
                'managed': False,
            },
        ),
    ]
