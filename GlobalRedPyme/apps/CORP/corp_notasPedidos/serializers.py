from rest_framework import serializers

from apps.CORP.corp_notasPedidos.models import FacturasEncabezados, FacturasDetalles

from datetime import datetime
from django.utils import timezone

# Actualizar factura
class FacturasDetallesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = FacturasDetalles
       	fields = '__all__'

class FacturasSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    detalles = FacturasDetallesSerializer(many=True,allow_empty=False)
    class Meta:
        model = FacturasEncabezados
       	fields = '__all__'
    
    def update(self, instance, validated_data):
        detalles_database = {detalle.id: detalle for detalle in instance.detalles.all()}
        detalles_actualizar = {item['id']: item for item in validated_data['detalles']}

        # Actualiza la factura cabecera
        instance.__dict__.update(validated_data) 
        instance.save()

        # Eliminar los detalles que no esté incluida en la solicitud de la factura detalles
        for detalle in instance.detalles.all():
            if detalle.id not in detalles_actualizar:
                detalle.delete()

        # Crear o actualizar instancias de detalles que se encuentran en la solicitud de factura detalles
        for detalle_id, data in detalles_actualizar.items():
            detalle = detalles_database.get(detalle_id, None)
            if detalle is None:
                data.pop('id')
                FacturasDetalles.objects.create(**data)
            else:
                now = timezone.localtime(timezone.now())
                data['updated_at'] = str(now)
                FacturasDetalles.objects.filter(id=detalle.id).update(**data)

        return instance

# Listar las facturas cabecera
class FacturasListarSerializer(serializers.ModelSerializer):
    detalles = FacturasDetallesSerializer(many=True,allow_empty=False)
    class Meta:
        model = FacturasEncabezados
       	fields = '__all__'

    def to_representation(self, instance):
            data = super(FacturasListarSerializer, self).to_representation(instance)
            # Quitar los credito de la factura
            credito = str(data.pop('credito'))
            data.update({"credito": credito})
            # Quitar los empresaComercial de la factura
            empresaComercial = str(data.pop('empresaComercial'))
            data.update({"empresaComercial": empresaComercial})
            # Quitar los detalles de la factura
            detalles = data.pop('detalles')
            articulos = ''
            for detalle in detalles:
                articulos += detalle['articulo'] + ','
            data.update({"detalles": articulos})
            return data

# Listar las facturas cabecera tabla
class FacturasListarTablaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturasEncabezados
       	fields = ['id','numeroFactura','created_at','canal','numeroProductosComprados','total']

# Crear factura
class DetallesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturasDetalles
       	fields = '__all__'

class FacturaSerializer(serializers.ModelSerializer):
    detalles = DetallesSerializer(many=True,allow_empty=False)
    class Meta:
        model = FacturasEncabezados
       	fields = '__all__'

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        facturaEncabezado = FacturasEncabezados.objects.create(**validated_data)
        if facturaEncabezado.numeroFactura is not None:
            facturaEncabezado.numeroFactura = facturaEncabezado.id + 1
            facturaEncabezado.save()
        else:
            facturaEncabezado.numeroFactura = 1
            facturaEncabezado.save()
        for detalle_data in detalles_data:
            FacturasDetalles.objects.create(facturaEncabezado=facturaEncabezado, **detalle_data)
        return facturaEncabezado

    def to_representation(self, instance):
        data = super(FacturaSerializer, self).to_representation(instance)
        # Quitar los credito de la factura
        credito = str(data.pop('credito'))
        data.update({"credito": credito})
        # Quitar los empresaComercial de la factura
        empresaComercial = str(data.pop('empresaComercial'))
        data.update({"empresaComercial": empresaComercial})
        return data


# Actualizar factura
class FacturasDetallesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = FacturasDetalles
       	fields = '__all__'

class FacturasSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    detalles = FacturasDetallesSerializer(many=True,allow_empty=False)
    class Meta:
        model = FacturasEncabezados
       	fields = '__all__'
    
    def update(self, instance, validated_data):
        detalles_database = {detalle.id: detalle for detalle in instance.detalles.all()}
        detalles_actualizar = {item['id']: item for item in validated_data['detalles']}

        # Actualiza la factura cabecera
        instance.__dict__.update(validated_data) 
        instance.save()

        # Eliminar los detalles que no esté incluida en la solicitud de la factura detalles
        for detalle in instance.detalles.all():
            if detalle.id not in detalles_actualizar:
                detalle.delete()

        # Crear o actualizar instancias de detalles que se encuentran en la solicitud de factura detalles
        for detalle_id, data in detalles_actualizar.items():
            detalle = detalles_database.get(detalle_id, None)
            if detalle is None:
                data.pop('id')
                FacturasDetalles.objects.create(**data)
            else:
                now = timezone.localtime(timezone.now())
                data['updated_at'] = str(now)
                FacturasDetalles.objects.filter(id=detalle.id).update(**data)

        return instance

    def to_representation(self, instance):
        data = super(FacturasSerializer, self).to_representation(instance)
        # Quitar los credito de la factura
        credito = str(data.pop('credito'))
        data.update({"credito": credito})
        # Quitar los empresaComercial de la factura
        empresaComercial = str(data.pop('empresaComercial'))
        data.update({"empresaComercial": empresaComercial})
        return data