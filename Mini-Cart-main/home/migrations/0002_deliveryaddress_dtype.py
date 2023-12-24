from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryaddress',
            name='dtype',
            field=models.CharField(default='Home', max_length=30),  # Replace 'Home' with your desired default value
            preserve_default=False,
        ),
    ]
