# Generated by Django 5.0.4 on 2024-08-30 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='comment',
            field=models.CharField(help_text='Maximum 20 words.', max_length=20),
        ),
    ]
