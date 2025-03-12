from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_remove_template_approval_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='templatestatus',
        ),
    ]
