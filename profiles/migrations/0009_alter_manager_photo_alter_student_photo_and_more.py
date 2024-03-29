# Generated by Django 4.2.6 on 2023-10-30 08:27

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_remove_manager_polymorphic_ctype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='photo',
            field=models.ImageField(default='img/default_profile.png', upload_to=profiles.models.get_upload_name),
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(default='img/default_profile.png', upload_to=profiles.models.get_upload_name),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='photo',
            field=models.ImageField(default='img/default_profile.png', upload_to=profiles.models.get_upload_name),
        ),
    ]
