# Generated by Django 5.0.6 on 2024-05-21 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_contacto_avisos_alter_contacto_tipo_consulta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='obra',
            name='id',
        ),
        migrations.AlterField(
            model_name='obra',
            name='id_obra',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]