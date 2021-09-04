# Generated by Django 2.2.8 on 2021-09-01 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210825_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(choices=[(1, 'Создан'), (2, 'Удален'), (3, 'Изменен'), (4, 'Выдан'), (5, 'Принят')])),
                ('doc_name', models.CharField(max_length=500)),
                ('doc_id', models.IntegerField()),
                ('doc_instance_unique_number', models.CharField(max_length=500)),
                ('who_use', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=1200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
