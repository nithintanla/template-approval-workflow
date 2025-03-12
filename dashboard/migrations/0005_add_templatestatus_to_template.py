from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_approvalsettings_analytics'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='templatestatus',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
