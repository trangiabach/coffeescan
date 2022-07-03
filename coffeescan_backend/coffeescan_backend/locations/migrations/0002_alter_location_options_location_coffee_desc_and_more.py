# Generated by Django 4.0.5 on 2022-06-18 12:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('date_added',)},
        ),
        migrations.AddField(
            model_name='location',
            name='coffee_desc',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='location',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='location',
            name='location',
            field=models.CharField(default=django.utils.timezone.now, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='space_desc',
            field=models.TextField(default=''),
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='locations.location')),
            ],
            options={
                'ordering': ('date_added',),
            },
        ),
    ]