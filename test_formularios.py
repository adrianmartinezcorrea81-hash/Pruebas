

import requests
import concurrent.futures
import time
import random
import threading
from datetime import datetime, timezone


URL_OBJETIVO = "https://delego-fitness.vercel.app/cuestionario"
PETICIONES_TOTALES = 300       
HILOS_SIMULTANEOS = 50         


NEXT_ACTION_ID = "40dfd125b24342d7e28de6821a03c99c8f45327c2d"

sesion = requests.Session()
lock = threading.Lock()
exitosas = 0
fallidas = 0
rate_limited = 0



EMAIL_DE_VERIFICACION = "amazonprimeparalel@gmail.com"


def generar_payload(es_verificacion=False):
    numero = random.randint(1000, 99999)
    fecha_actual = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

    email = EMAIL_DE_VERIFICACION if es_verificacion else f"test.load.{numero}@example.com"
    nombre = f"TEST_LOAD_VERIFICACION_{numero}" if es_verificacion else f"TEST_LOAD_{numero}"

    return [{
        "contact": {
            
            "firstName": nombre,
            "lastName": "Pruebas",
            "phone": f"+34 600 {random.randint(100, 999)} {random.randint(100, 999)}",
            "email": email,
        },
        "plan": None,
        "profile": {
            "age": random.randint(18, 50),
            "weight": random.randint(60, 90),
            "height": random.randint(160, 190),
            "gender": random.choice(["male", "female"]),
            "goal": ["lose-weight"],
        },
        "training": {
            "experienceLevel": random.choice(["beginner", "intermediate"]),
            "trainingLocation": "gym",
            "equipment": [],
        },
        "health": {
            "healthConditions": "Ninguna",
            "injuries": "Ninguna",
            "dietaryRestrictions": "Ninguna",
        },
        "submittedAt": fecha_actual,
    }]


def enviar_formulario(id_peticion):
    global exitosas, fallidas, rate_limited
    
    es_ultima = (id_peticion == PETICIONES_TOTALES - 1)
    datos = generar_payload(es_verificacion=es_ultima)

    cabeceras = {
        
        "Content-Type": "text/plain;charset=UTF-8",
        "Next-Action": NEXT_ACTION_ID,
        
        "User-Agent": "LoadTest-DelegoFitness/1.0 (contacto: tu-email@ejemplo.com)",
    }

    try:
        
        import json
        respuesta = sesion.post(
            URL_OBJETIVO,
            data=json.dumps(datos),
            headers=cabeceras,
            timeout=10,
        )

        with lock:
            if respuesta.status_code in (200, 201):
                exitosas += 1
                etiqueta = " <-- ESTA ES LA DE VERIFICACIÓN, revisa tu email" if es_ultima else ""
                print(f"[+] {id_peticion} OK ({respuesta.status_code}){etiqueta}")
            elif respuesta.status_code == 429:
                rate_limited += 1
                print(f"[!] {id_peticion} Rate limited (429) - tu servidor está protegiéndose, es buena señal")
            else:
                fallidas += 1
                print(f"[-] {id_peticion} Fallo ({respuesta.status_code}) - {respuesta.text[:80]}")

    except Exception as e:
        with lock:
            fallidas += 1
        print(f"[!] {id_peticion} Error de conexión: {e}")


def main():
    print(f"Iniciando test de carga contra {URL_OBJETIVO}")
    print(f"Peticiones: {PETICIONES_TOTALES} | Hilos: {HILOS_SIMULTANEOS}\n")

    inicio = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=HILOS_SIMULTANEOS) as ejecutor:
        list(ejecutor.map(enviar_formulario, range(PETICIONES_TOTALES)))
    duracion = time.time() - inicio

    print("\n" + "=" * 40)
    print("RESULTADOS DEL TEST DE CARGA")
    print("=" * 40)
    print(f"Tiempo total:      {duracion:.2f} s")
    print(f"Peticiones/seg:    {PETICIONES_TOTALES / duracion:.2f}")
    print(f"Exitosas:          {exitosas}")
    print(f"Rate limited (429):{rate_limited}")
    print(f"Fallidas:          {fallidas}")
    print("=" * 40)
    print("\nRecuerda: borra de tu base de datos los registros con firstName")
    print("que empiece por 'TEST_LOAD_' para no dejar basura de prueba.")


if __name__ == "__main__":
    main()