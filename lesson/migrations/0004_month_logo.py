# Generated by Django 4.2.6 on 2023-10-30 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0003_alter_homework_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='month',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='lesson/<django.db.models.fields.related.ForeignKey>/months/'),
        ),
    ]