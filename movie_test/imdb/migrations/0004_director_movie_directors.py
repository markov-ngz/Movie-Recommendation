# Generated by Django 4.2.4 on 2023-11-02 08:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("imdb", "0003_delete_person_actor_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Director",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name="movie",
            name="directors",
            field=models.ManyToManyField(to="imdb.director"),
        ),
    ]
