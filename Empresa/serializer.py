
from rest_framework import serializers

from Empresa.models import Establecimiento


class EstablecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establecimiento
        fields = '__all__'


