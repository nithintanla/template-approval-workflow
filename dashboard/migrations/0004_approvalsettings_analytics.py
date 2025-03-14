# Generated by Django 4.2.7 on 2025-03-12 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_create_agent_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rejection_keywords', models.TextField(help_text='Enter keywords separated by commas. Templates containing these words will be rejected.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Approval Settings',
                'verbose_name_plural': 'Approval Settings',
            },
        ),
        migrations.CreateModel(
            name='Analytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.IntegerField(default=0)),
                ('responses', models.IntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.template')),
            ],
            options={
                'verbose_name_plural': 'Analytics',
            },
        ),
    ]
