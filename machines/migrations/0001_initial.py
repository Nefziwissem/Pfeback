# Generated by Django 5.0.6 on 2024-08-02 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id_machine', models.AutoField(primary_key=True, serialize=False)),
                ('nom_machine', models.CharField(max_length=100)),
                ('nom_marchand', models.CharField(max_length=100)),
                ('date_installation', models.DateField()),
                ('date_intervention', models.DateField(null=True)),
                ('date_mise_en_marche', models.DateField()),
            ],
        ),
    ]
