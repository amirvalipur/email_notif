# Generated by Django 4.2.7 on 2023-11-22 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_options_remove_useremail_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='message',
            field=models.TextField(blank=True, default='', null=True, verbose_name='متن'),
        ),
    ]
