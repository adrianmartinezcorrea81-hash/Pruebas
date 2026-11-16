
# Load Tester para Formularios (Next.js Server Actions)

Este script de Python realiza pruebas de carga controladas y legítimas contra formularios desarrollados con Server Actions de Next.js. Simula envíos concurrentes para comprobar si el servidor y la base de datos soportan picos de tráfico y si las protecciones contra spam (Rate Limit / 429) están funcionando correctamente.

## 📋 Requisitos Previos

Necesitas tener Python instalado. Antes de ejecutar el script, instala la única dependencia necesaria]:

bash: 

pip install requests



## 🔍 Paso 1: Cómo obtener el `NEXT_ACTION_ID` (¡Importante!)

En Next.js, los formularios que usan Server Actions no envían los datos a una URL normal (como `/api/submit`), sino que usan un código identificador único generado en cada *build*. **Si la web se vuelve a desplegar (deploy), este ID cambiará y el script fallará.**

Para conseguir el ID actual:

1. Abre la página web donde está el formulario.
2. Abre las herramientas de desarrollador del navegador (pulsa **F12** o clic derecho -> Inspeccionar).
3. Ve a la pestaña **Network** (Red).
4. Rellena el formulario manualmente y dale a enviar.
5. En la lista de peticiones de red, busca una petición de tipo **POST** (normalmente tiene el nombre de la ruta, ej: `cuestionario`).
6. Haz clic en ella y ve a la sección **Request Headers** (Cabeceras de la petición).
7. Busca la cabecera llamada `Next-Action`. Copia su valor (es un código alfanumérico largo).

## ⚙️ Paso 2: Configurar el Script

Abre el archivo `test_formularios.py` y modifica las siguientes variables en la sección de CONFIGURACIÓN:

* **`URL_OBJETIVO`**: La URL exacta donde está el formulario.


* **`NEXT_ACTION_ID`**: Pega aquí el código que has copiado en el Paso 1.


* **`PETICIONES_TOTALES`**: Número de veces que se enviará el formulario. Empieza con algo bajo (ej. 30) y sube gradualmente.


* **`HILOS_SIMULTANEOS`**: Cuántos envíos se hacen a la vez (concurrencia).


* **`EMAIL_DE_VERIFICACION`**: Pon tu email real aquí. Solo la última petición de todas se enviará usando este correo para que puedas comprobar visualmente si te llega el correo de confirmación de la app web.



## 🚀 Paso 3: Ejecutar la prueba

Lanza el script desde tu terminal:

```bash
python test_formularios.py

```

Verás un registro en tiempo real mostrando las peticiones exitosas (200/201), las que han sido bloqueadas por el servidor (429 Rate Limited - esto es buena señal de seguridad) y los fallos de red.

## 🧹 Limpieza Post-Test

El script genera datos aleatorios, pero todos los nombres empiezan por el prefijo `TEST_LOAD_` (ejemplo: `TEST_LOAD_54321`).

Cuando termines tus pruebas, ve a tu base de datos y filtra por los nombres que empiecen por `TEST_LOAD_` para borrar toda la basura generada por el test fácilmente.

```

```
