# Generated by Django 5.0.6 on 2024-05-20 21:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_empleado_edad_alter_obra_descripcion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=254)),
                ('tipo_consulta', models.IntegerField(choices=[(0, 'Consulta'), (1, 'Reclamo'), (2, 'Sugerencia'), (3, 'Felicitaciones')])),
                ('mensaje', models.TextField()),
                ('avisos', models.BooleanField()),
            ],
        ),
        migrations.AlterField(
            model_name='empleado',
            name='genero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.tipogenero'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.tipoempleado'),
        ),
        migrations.AlterField(
            model_name='obra',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.tipoobra'),
        ),
    ]
