# Generated by Django 4.2.7 on 2025-03-20 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_alter_template_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='status',
            field=models.CharField(choices=[('pending_l1', 'Pending L1 Approval'), ('approved_l1', 'Approved by L1'), ('rejected_l1', 'Rejected by L1'), ('approved_l2', 'Approved by L2'), ('rejected_l2', 'Rejected by L2')], default='pending_l1', max_length=20),
        ),
    ]
