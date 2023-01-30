# Generated by Django 3.2.15 on 2023-01-13 12:09

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20230112_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='case',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='core_actor_related', related_query_name='core_actors', to='core.case'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detectionrule',
            name='case',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='core_detectionrule_related', related_query_name='core_detectionrules', to='core.case'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='threat',
            name='case',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='core_threat_related', related_query_name='core_threats', to='core.case'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='case',
            name='es_prefix',
            field=models.CharField(default='vdpjwzsuhj9spmql', editable=False, max_length=16),
        ),
        migrations.AlterField(
            model_name='event',
            name='first_seen',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 13, 12, 9, 29, 751373, tzinfo=utc), help_text='First time the event has occurred.'),
        ),
        migrations.AlterField(
            model_name='event',
            name='last_seen',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 13, 12, 9, 29, 751407, tzinfo=utc), help_text='First time the event has occurred.'),
        ),
        migrations.AlterField(
            model_name='observable',
            name='es_prefix',
            field=models.CharField(default='7ikejzfa0wsvlnz1', editable=False, max_length=16),
        ),
        migrations.AlterField(
            model_name='piroguedump',
            name='analysis_index',
            field=models.CharField(default='roatmhcg5zr4cdoy', help_text='Elasticsearch index storing the analysis.', max_length=64),
        ),
    ]