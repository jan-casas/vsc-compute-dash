# Use the official Python image from Docker Hub
FROM python:3.11

# Copy all files from the current directory to the current directory in the container
COPY . .

# Establece el directorio de trabajo en el contenedor Docker
# WORKDIR /Dash-Energia

# Instala los paquetes de Python especificados en el archivo requirements.txt
RUN pip install -r requirements.txt

# Expone el puerto 5000 en el contenedor Docker
EXPOSE 80

# app2.py is the name of the file that contains the code for the app
CMD ["python", "main.py"]