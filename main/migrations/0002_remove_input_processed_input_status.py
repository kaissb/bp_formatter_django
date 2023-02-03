# Generated by Django 4.1.6 on 2023-02-03 00:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="input",
            name="processed",
        ),
        migrations.AddField(
            model_name="input",
            name="status",
            field=models.CharField(
                choices=[("0", "Uploaded"), ("1", "Processing"), ("2", "Done")],
                default="0",
                max_length=10,
            ),
        ),
    ]