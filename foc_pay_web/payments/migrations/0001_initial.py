# Generated by Django 3.2.10 on 2021-12-12 09:20

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('status', model_utils.fields.StatusField(choices=[('created', 'Created'), ('paid', 'Paid'), ('credited', 'Credited'), ('declined', 'Declined'), ('error', 'Error'), ('cancelled', 'Cancelled')], default='created', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('payment_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('payer_alias', models.CharField(max_length=20)),
                ('amount', models.CharField(max_length=10)),
                ('machine', models.CharField(blank=True, choices=[('', 'None'), ('focumama', 'Focumama'), ('drickomaten', 'Drickomaten')], default='', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
