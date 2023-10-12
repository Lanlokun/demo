# Generated by Django 3.2.17 on 2023-10-11 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corecode', '0008_remove_participant_access_coupons'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParticipantBulkUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_uploaded', models.DateTimeField(auto_now=True)),
                ('csv_file', models.FileField(upload_to='participants/bulkupload/')),
            ],
        ),
        migrations.AddField(
            model_name='participant',
            name='qr_code_image',
            field=models.ImageField(blank=True, null=True, upload_to='participants'),
        ),
    ]
