# Generated by Django 4.2.1 on 2023-06-26 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='カテゴリ名')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='タグ名')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='タイトル')),
                ('text', models.TextField(verbose_name='内容')),
                ('author', models.CharField(max_length=10, verbose_name='書いた人')),
                ('image', models.ImageField(blank=True, default='images/noimage.png', upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogsite.category', verbose_name='カテゴリ')),
                ('tag', models.ManyToManyField(blank=True, to='blogsite.tag', verbose_name='タグ')),
            ],
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(verbose_name='IPアドレス')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogsite.topic', verbose_name='記事')),
            ],
            options={
                'unique_together': {('topic', 'ip')},
            },
        ),
    ]
