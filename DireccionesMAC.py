import subprocess #Modelo para utilizar comandos
import json #Modulo para escribir y leer json 
import re #Modelo para trabajar con expresiones regulares

def leer_maquinas(archivo):
    maquinas = {}
    with open(archivo, "r", encoding="utf-8") as f: #abre el archivo en modo lectura (r)
        contenido = f.read()
        #findall busca coincidencias en el archivo
        bloques = re.findall(r"([0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2})\s+\(hex\)\s+(.*)", contenido) 
        for mac, nombre in bloques:
            nombre = nombre.strip()
            maquinas[mac.upper()] = nombre  
    return maquinas

#Usamos el comando arp -a y capturamos la salida que tenga 
resultado = subprocess.run(["arp", "-a"], capture_output=True, text=True)

# Si el proceso se cumplio returncode sera 0, sino se manda un error con stderr
if resultado.returncode != 0:
    print("Error al ejecutar el comando 'arp -a':", resultado.stderr)
    exit(1)

#Se procesa la salida del comando
dispositivos = [] #Diccionario 
for linea in resultado.stdout.splitlines(): #Se divide la salida en lineas individuales 
    # Se busca coincidencias con search y la expresion regular en cada linea
    coincidencia = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]+)\s+(\w+)", linea)
    # Si las encuentra se hace lo siguiente
    if coincidencia:
        ip = coincidencia.group(1)  # Direccion IP
        mac = coincidencia.group(2)  # Direccion MAC completa
        digitos = "-".join(mac.split("-")[:3]).upper()  # Tomar los primeros tres grupos y los hace mayusculas
        # Agregar los datos al diccionario
        dispositivos.append({"ip": ip, "mac": mac, "digitos": digitos})

# Leer el archivo maquinas.txt y crear un diccionario de maquinas
maquinas = leer_maquinas("maquinas.txt")

# Buscar el nombre de la maquina para cada dispositivo
for dispositivo in dispositivos:
    digitos = dispositivo["digitos"]
    if digitos in maquinas:
        dispositivo["maquina"] = maquinas[digitos]
    else:
        dispositivo["maquina"] = "Desconocido"  # Si no se encuentra en el archivo

# Guardar los datos en un archivo JSON
with open("dispositivos.json", "w") as archivo_json:
    json.dump(dispositivos, archivo_json, indent=4)

print("Datos guardados en 'dispositivos.json'.")

# Escribir los resultados en un archivo de texto (solo dispositivos con maquina conocida)
with open("resultados.txt", "w", encoding="utf-8") as archivo_txt: #Se abre el txt en modo escritura w
    for dispositivo in dispositivos:
        if dispositivo["maquina"] != "Desconocido":
            archivo_txt.write(f"IP: {dispositivo['ip']} --- MAC: {dispositivo['mac']} --- Máquina: {dispositivo['maquina']}\n")

print("Resultados guardados en 'resultados.txt'.")