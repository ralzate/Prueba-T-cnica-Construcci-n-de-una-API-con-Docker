# Usar una imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY ./app /app

# Instalar las dependencias
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy requests

# Exponer el puerto 8000
EXPOSE 8000

# Ejecutar la aplicación FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]