# Generated by Django 3.1.13 on 2021-11-09 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_auto_20211109_0518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='ask_type',
            field=models.CharField(choices=[('public', 'public'), ('limited', 'limited')], default='public', max_length=7),
        ),
    ]
