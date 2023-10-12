# Generated by Django 4.0.6 on 2023-04-15 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_person_gotorder_delivery_qty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distributedorder',
            name='distributed_to',
        ),
        migrations.AddField(
            model_name='distributedorder',
            name='person',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='order.person'),
            preserve_default=False,
        ),
    ]