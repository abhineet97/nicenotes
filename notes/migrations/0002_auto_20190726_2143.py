# Generated by Django 2.2.3 on 2019-07-26 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="note",
            old_name="author",
            new_name="owner",
        ),
    ]
