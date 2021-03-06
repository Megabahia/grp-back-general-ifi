# Generated by Django 3.1.7 on 2022-02-22 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mdp_productos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FichaTecnicaProductos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=150)),
                ('nombreAtributo', models.CharField(max_length=255)),
                ('valor', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdp_productos.productos')),
            ],
        ),
    ]
