# Generated by Django 4.2.6 on 2023-10-30 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0009_alter_manager_photo_alter_student_photo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField()),
                ('due_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('content', models.TextField()),
                ('media', models.FileField(blank=True, null=True, upload_to='lesson/<django.db.models.fields.CharField>')),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.month')),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.student')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='students',
            field=models.ManyToManyField(through='lesson.Progress', to='profiles.student'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='week',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lesson.week'),
        ),
        migrations.CreateModel(
            name='HomeworkSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('grade', models.PositiveIntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.homework')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.student')),
            ],
        ),
        migrations.AddField(
            model_name='homework',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.lesson'),
        ),
    ]
