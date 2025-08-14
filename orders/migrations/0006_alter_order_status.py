from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_merge_0003_order_status_0004_order_seen_by_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('paid', 'paid'), ('delivered', 'delivered'), ('canceled', 'canceled')], default='pending', max_length=20),

        ),
    ]
