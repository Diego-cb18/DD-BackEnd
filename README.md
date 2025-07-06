# 🧠 Backend Drowsiness Detection

Este es el backend del sistema de detección de somnolencia para conductores, desarrollado con Django REST Framework. Permite recibir reportes JSON generados desde dispositivos Raspberry Pi, almacenar los datos en una base de datos PostgreSQL, y gestionarlos desde un dashboard web.

---

## 🚀 Características

- API REST para recepción de reportes de somnolencia
- Procesamiento automático de campos como gravedad, estado y eventos críticos
- Soporte para subida de archivos JSON con campos personalizados
- Listado y actualización de reportes (estado "Revisado")
- Compatibilidad con Docker
- Conexión a base de datos PostgreSQL externa (ej. RDS)

---

## 🐳 Despliegue con Docker

### 1. Clonar el repositorio

```bash
git clone https://github.com/Diego-cb18/DD-BackEnd.git
cd DD-BackEnd
