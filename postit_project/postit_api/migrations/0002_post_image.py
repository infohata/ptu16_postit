# Generated by Django 4.2.6 on 2023-10-25 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postit_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='posts/img', verbose_name='image'),
        ),
    ]
