# Generated by Django 3.0.4 on 2020-04-10 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sentence',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='translate',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]