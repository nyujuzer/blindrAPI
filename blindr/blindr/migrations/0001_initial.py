# Generated by Django 4.1.2 on 2023-10-10 06:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DisplayModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('gender', models.IntegerField(validators=[django.core.validators.MaxValueValidator(3)])),
                ('preferences', models.IntegerField(validators=[django.core.validators.MaxValueValidator(4)])),
                ('bio', models.CharField(max_length=255)),
                ('age', models.DateField()),
                ('longitude', models.CharField(blank=True, max_length=10, null=True)),
                ('latitude', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='hobbiesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hobby', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MatchesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('userId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('maxdist', models.IntegerField(blank=True, null=True)),
                ('maxAge', models.IntegerField(blank=True, null=True)),
                ('currentLikes', models.ManyToManyField(blank=True, to='blindr.displaymodel')),
            ],
        ),
        migrations.CreateModel(
            name='VideoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='videos')),
                ('title', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='blindr.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='ThumbnailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.ImageField(upload_to='thumbnails')),
                ('relatedvideo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_video', to='blindr.videomodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='blindr.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='blindr.matchesmodel')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blindr.usermodel')),
            ],
        ),
        migrations.AddField(
            model_name='matchesmodel',
            name='user_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='one', to='blindr.usermodel'),
        ),
        migrations.AddField(
            model_name='matchesmodel',
            name='user_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='two', to='blindr.usermodel'),
        ),
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isProfilePic', models.BooleanField()),
                ('image', models.ImageField(upload_to='img')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blindr.usermodel')),
            ],
        ),
        migrations.AddField(
            model_name='displaymodel',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blindr.usermodel'),
        ),
        migrations.AddField(
            model_name='displaymodel',
            name='hobbies',
            field=models.ManyToManyField(to='blindr.hobbiesmodel'),
        ),
    ]