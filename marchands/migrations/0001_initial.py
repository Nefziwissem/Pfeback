# Generated by Django 5.0.6 on 2024-08-04 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Marchand',
            fields=[
                ('id_marchand', models.AutoField(primary_key=True, serialize=False)),
                ('nom_marchand', models.CharField(max_length=100)),
                ('type_machine', models.CharField(max_length=100)),
                ('quantite', models.PositiveIntegerField()),
                ('emplacement', models.CharField(max_length=255)),
                ('date_entretien', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Fille',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='marchands.marchand')),
            ],
        ),
    ]
