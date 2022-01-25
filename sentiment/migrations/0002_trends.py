# Generated by Django 4.0.1 on 2022-01-21 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='trends',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trend_1', models.CharField(blank=True, max_length=30, null=True)),
                ('trend_2', models.CharField(blank=True, max_length=30, null=True)),
                ('trend_3', models.CharField(blank=True, max_length=30, null=True)),
                ('trend_4', models.CharField(blank=True, max_length=30, null=True)),
                ('trend_5', models.CharField(blank=True, max_length=30, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]