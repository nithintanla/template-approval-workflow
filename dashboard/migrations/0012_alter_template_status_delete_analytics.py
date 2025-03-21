# Generated by Django 4.2.7 on 2025-03-13 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_alter_template_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='status',
            field=models.CharField(choices=[('approved_system', 'Approved by System'), ('rejected_system', 'Rejected by System'), ('approved_admin', 'Approved by Admin'), ('rejected_admin', 'Rejected by Admin')], default='approved_system', max_length=20),
        ),
        migrations.DeleteModel(
            name='Analytics',
        ),
    ]
