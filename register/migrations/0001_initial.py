# Generated by Django 4.0.3 on 2023-06-05 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='source/images/user/08.jpg', upload_to='image/person/')),
                ('firstname', models.CharField(blank=True, max_length=50, null=True)),
                ('lastname', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, choices=[('1', 'Erkak'), ('2', 'Ayol')], max_length=50, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=25, null=True)),
                ('balance', models.IntegerField(default=0)),
            ],
        ),
    ]