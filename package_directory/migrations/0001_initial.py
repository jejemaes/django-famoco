# Generated by Django 2.0 on 2019-12-11 09:14

from django.db import migrations, models
import django.utils.timezone
import package_directory.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apk_file', models.FileField(upload_to=package_directory.models.app_directory_path)),
                ('package_name', models.CharField(max_length=42)),
                ('package_version_code', models.CharField(max_length=10)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de creation')),
                ('description', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'application_android',
                'ordering': ['package_name'],
            },
        ),
    ]