from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_approvalsettings_analytics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='approval_status',
        ),
    ]
