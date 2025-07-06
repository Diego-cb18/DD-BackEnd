from rest_framework import serializers
from .models import DrowsinessReport

class DrowsinessReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrowsinessReport
        fields = '__all__'
