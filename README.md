# App-Jing
## Local
### Backend
Todo lo relacionado al backend en Django y la API REST se encuentra en la carpeta `backend`.

Para iniciar:
1) Crear ambiente virtual.
2) Instalar requisitos (desde la carpeta `backend`).
```
pip install -r requirements.txt
```
3) Hacer y aplicar migraciones.
```
python manage.py makemigrations
python manage.py migrate
```
4) Iniciar servidor.
```
python manage.py runserver
```
5) Por defecto, el backend se iniciará en `http://localhost:8000/`. La API se encuentra en `http://localhost:8000/api/`.
### Frontend
El frontend en React se encuentra en la carpeta `frontend`.

Para iniciar:
1) Instalar dependencias (desde la carpeta `frontend`).
```
npm install
```
2) Iniciar servidor.
```
npm start
```
3) Por defecto, el frontend se iniciará en `http://localhost:3000/`.

---

## Deploy
El servidor del DCC es `jing.dcc.uchile.cl`, en el puerto 221. Solicitar acceso en Sistemas.

Para el backend, se deben definir las siguientes variables de entorno en el sistema operativo:
```
JING_ALLOWED_HOSTS="jing.dcc.uchile.cl"
JING_CORS_ORIGIN_WHITELIST="https://jing.dcc.uchile.cl"
```

Luego, para iniciar se debe hacer con el siguiente comando:
```
python manage.py runserver 0:8000
```

El frontend se inicia igual que en local, pero se debe crear un archivo `.env` en la carpeta `frontend` con el siguiente contenido:
```
REACT_APP_API_URL=https://jing.dcc.uchile.cl/api
```

---
## Otros

El proyecto original se encuentra íntegro en la carpeta `app_jing`, a modo de referencia. Funciona de manera completamente independiente y es seguro correrlo y borrarlo.