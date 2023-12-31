# Generated by Django 3.2.2 on 2023-11-10 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, null=True)),
                ('subjectid', models.IntegerField(null=True)),
                ('about', models.CharField(max_length=500, null=True)),
                ('outcomes', models.CharField(max_length=500, null=True)),
                ('level', models.CharField(max_length=1, null=True)),
                ('instructorid', models.IntegerField(null=True)),
                ('agegroup', models.CharField(max_length=1, null=True)),
                ('language', models.CharField(max_length=1, null=True)),
                ('duration', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timeframe', models.IntegerField(null=True)),
                ('certificate', models.CharField(max_length=1, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=13)),
                ('objectives', models.CharField(max_length=500, null=True)),
                ('eligibility', models.CharField(max_length=500, null=True)),
                ('status', models.CharField(max_length=1, null=True)),
            ],
            options={
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='CourseLesson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, null=True)),
                ('courseid', models.IntegerField(null=True)),
                ('type', models.CharField(max_length=1, null=True)),
                ('medialurl', models.CharField(max_length=100, null=True)),
                ('moduleid', models.IntegerField(null=True)),
                ('sequence', models.IntegerField(null=True)),
                ('duration', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(max_length=1, null=True)),
            ],
            options={
                'db_table': 'courselesson',
            },
        ),
        migrations.CreateModel(
            name='CourseMedia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('courseid', models.IntegerField(null=True)),
                ('type', models.CharField(max_length=1, null=True)),
                ('mediaurl', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'coursemedia',
            },
        ),
        migrations.CreateModel(
            name='CourseModule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sequence', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('courseid', models.IntegerField(null=True)),
                ('assesment', models.CharField(max_length=1, null=True)),
                ('duration', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=1, null=True)),
            ],
            options={
                'db_table': 'coursemodule',
            },
        ),
        migrations.CreateModel(
            name='CourseRating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('registrationid', models.IntegerField(null=True)),
                ('courseid', models.IntegerField(null=True)),
                ('comments', models.CharField(max_length=500, null=True)),
                ('rating', models.IntegerField(null=True)),
                ('dateofrating', models.DateTimeField(null=True)),
                ('instructorid', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'courserating',
            },
        ),
        migrations.CreateModel(
            name='CourseRegistration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('registrationid', models.IntegerField(null=True)),
                ('courseid', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=1, null=True)),
            ],
            options={
                'db_table': 'courseregistration',
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('about', models.CharField(max_length=500, null=True)),
                ('experience', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=1, null=True)),
            ],
            options={
                'db_table': 'instructor',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('registrationid', models.IntegerField(null=True)),
                ('courseid', models.IntegerField(null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reference', models.CharField(max_length=100, null=True)),
                ('paymod', models.CharField(max_length=20, null=True)),
                ('paydate', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'payment',
            },
        ),
        migrations.CreateModel(
            name='question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('registrationid', models.IntegerField(null=True)),
                ('courseid', models.IntegerField(null=True)),
                ('question', models.CharField(max_length=100, null=True)),
                ('answer', models.CharField(max_length=100, null=True)),
                ('lessonid', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=1, null=True)),
            ],
            options={
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=100, null=True)),
                ('lastname', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('password', models.CharField(max_length=20, null=True)),
                ('country', models.CharField(max_length=2, null=True)),
                ('agegroup', models.IntegerField(null=True)),
                ('profilepicurl', models.CharField(max_length=100, null=True)),
                ('dateregistered', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=1, null=True)),
            ],
            options={
                'db_table': 'registration',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(max_length=1, null=True)),
            ],
            options={
                'db_table': 'subject',
            },
        ),
    ]
