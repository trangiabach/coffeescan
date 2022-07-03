# Generated by Django 4.0.5 on 2022-06-18 14:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_alter_location_options_location_coffee_desc_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tags',
            new_name='Tag',
        ),
        migrations.CreateModel(
            name='SideImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(default='')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='side_images', to='locations.location')),
            ],
            options={
                'ordering': ('date_added',),
            },
        ),
    ]
