# Generated by Django 3.2.15 on 2022-11-12 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20221112_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='artifact',
            name='extracted_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='observables', to='core.device'),
        ),
    ]