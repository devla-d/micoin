# Generated by Django 3.2 on 2021-05-07 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investors', '0011_alter_account_ref_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='ref_code',
            field=models.CharField(blank=True, default='153', max_length=50, null=True),
        ),
    ]