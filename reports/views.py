from .serializers import DrowsinessReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DrowsinessReport
import json
from datetime import datetime
from django.utils.timezone import make_aware
from pytz import timezone
import random

def generar_dato_aleatorio():
    nombres = ["Diego", "Juan", "Luis", "Carlos"]
    apellidos = ["Pérez", "García", "Ramírez", "Campos"]
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    return nombre, apellido

def generar_placa():
    letras = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    numeros = ''.join(random.choices("0123456789", k=3))
    return f"{letras}-{numeros}"

GRAVEDAD_PRIORIDAD = {
    "parpadeo prolongado": 1,
    "microsueño leve": 2,
    "microsueño moderado": 3,
    "microsueño profundo": 4
}

def calcular_gravedad(eventos):
    gravedad_mayor = 0
    for evento in eventos:
        for clave, prioridad in GRAVEDAD_PRIORIDAD.items():
            if clave in evento.lower():
                gravedad_mayor = max(gravedad_mayor, prioridad)
    if gravedad_mayor >= 3:
        return "Grave"
    elif gravedad_mayor == 2 or gravedad_mayor == 1:
        return "Moderado"
    return "Leve" if eventos else "Desconocida"

class ReportUploadView(APIView):
    def post(self, request):
        try:
            json_file = request.FILES.get('json')
            json_data = json.load(json_file)

            conductor = json_data["conductor"]
            reporte = json_data["reporte_somnolencia"]

            nombre, apellido = generar_dato_aleatorio()
            first_name = conductor.get("nombre") or nombre
            last_name = conductor.get("apellidos") or apellido
            dni = conductor.get("dni") or str(random.randint(10000000, 99999999))
            telefono = conductor.get("telefono") or f"9{random.randint(100000000, 999999999)}"
            placa = conductor.get("placa") or generar_placa()
            tipo_vehiculo = conductor.get("tipo_vehiculo") or random.choice(["Bus", "Camión", "Minibús"])

            gravedad = calcular_gravedad(reporte["eventos_criticos"])
            lima_tz = timezone("America/Lima")
            generated_at = lima_tz.localize(datetime.strptime(json_data["fecha_generacion"], "%Y-%m-%d %H:%M:%S"))

            mac_address = json_data.get("mac_address")
            if not mac_address:
                mac_address = request.META.get("REMOTE_ADDR", "desconocido")

            report = DrowsinessReport.objects.create(
                mac_address=mac_address,
                first_name=first_name,
                last_name=last_name,
                dni=dni,
                phone=telefono,
                vehicle_type=tipo_vehiculo,
                plate=placa,
                blink_count=reporte["parpadeos"],
                yawn_count=reporte["bostezos"],
                nod_count=reporte["cabeceos"],
                critical_events=reporte["eventos_criticos"],
                video_names=reporte["videos"],
                url_videos=reporte.get("url_videos", []),
                generated_at=generated_at,
                estado="No revisado",
                gravedad=gravedad
            )

            return Response({"status": "ok", "report_id": report.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ReportListView(APIView):
    def get(self, request):
        reports = DrowsinessReport.objects.all().order_by('-generated_at')
        serializer = DrowsinessReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MarkAsReviewedView(APIView):
    def patch(self, request, pk):
        try:
            report = DrowsinessReport.objects.get(pk=pk)
            report.estado = "Revisado"
            report.save()
            return Response({"status": "updated"}, status=status.HTTP_200_OK)
        except DrowsinessReport.DoesNotExist:
            return Response({"error": "Reporte no encontrado"}, status=status.HTTP_404_NOT_FOUND)
