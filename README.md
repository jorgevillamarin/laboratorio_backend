1)primero que nada, active el entorno virtual para python con el siguiente comando:
    .\venv\Scripts\Activate 

2)elimine el archivo "test.db" para evitar conflictos con la base de datos. esta se creara automaticamente al iniciar el servidor

3)instale los requerimientos y librerias con las cuales funciona el proyecto con el siguiente comando:
  pip install -r requirements.txt

4)abra una terminal en la raiz del proyecto e inicie el servidor con el siguiente comando:
  uvicorn main:app --reload

5)dirigase al puerto 8000 de su localhost para que su navegador le diga si se conecto correctamente el backend

6) acceda a la documentacion automatica, agregando a su ruta local, la siguiente direccion: 
   http://127.0.0.1:8000/docs