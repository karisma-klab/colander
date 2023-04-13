# Generated by Django 3.2.18 on 2023-03-18 15:22

import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_entityrelation_attributes'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackendCredentials',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier.', primary_key=True, serialize=False)),
                ('backend', models.CharField(default='', max_length=512, verbose_name='backend identifier')),
                ('last_usage', models.DateTimeField(default=django.utils.timezone.now)),
                ('credentials', django.contrib.postgres.fields.hstore.HStoreField(default=dict)),
            ],
            options={
                'ordering': ['last_usage'],
                'unique_together': {('backend', 'credentials')},
            },
        ),
    ]