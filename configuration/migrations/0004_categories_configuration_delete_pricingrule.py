# Generated by Django 5.0.3 on 2024-05-20 16:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0003_pricingrule_remove_configuration_proprietaire_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorie', models.CharField(choices=[('Classe A', 'classe A'), ('Classe B', 'classe B'), ('Classe C', 'classe C'), ('Classe VIP', 'VIP')], max_length=150)),
                ('prix_enfant', models.FloatField(default=0.0)),
                ('prix_adulte', models.FloatField(default=0.0)),
                ('proprietaire', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Categorie',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('telephone', models.CharField(blank=True, max_length=100)),
                ('adresse', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='Logo')),
                ('date_ajout', models.DateField(auto_now=True)),
                ('proprietaire', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='PricingRule',
        ),
    ]