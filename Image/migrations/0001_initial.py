# Generated by Django 4.1 on 2023-09-03 11:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='图片')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新日期')),
            ],
            options={
                'verbose_name': 'ExternalImage',
            },
        ),
    ]