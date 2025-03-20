# Generated by Django 4.2.7 on 2025-03-20 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_alter_template_status_delete_analytics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='status',
            field=models.CharField(choices=[('approved_system', 'Approved by System'), ('rejected_system', 'Rejected by System'), ('approved_admin', 'Approved by Admin'), ('rejected_admin', 'Rejected by Admin'), ('approved_l1', 'Approved by L1'), ('rejected_l1', 'Rejected by L1'), ('approved_l2', 'Approved by L2'), ('rejected_l2', 'Rejected by L2')], default='approved_system', max_length=20),
        ),
    ]
