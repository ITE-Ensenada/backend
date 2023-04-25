# menu

Aqui van las instrucciones pa echar a andar este proyecto

primero instala el archivo de requierements

> pip install -r requirements.txt

lo mejor es hacerlo todo en un virtual enviroment

para arrancar esto tienes que irte a tu directorio del venv y hacer lo siguiente (Desde windows)

> venv\Scripts\activate

una vez aqui te va a salir algo como

> (venv) Directorio:

Muy bien, ahora pa correr esto tienes que usar el comando

> python main.py

## BataDase

Un detallote es que aveces se cierra automaticamente despues de meter el psswrd en el comandline, la cosa es que el puerto del MYSQL esta apagado, deberas inicializarlo pq sino obviamente no va a jalar

Esto en windows es:

Task Manager > Services > Open Services

Una vez aqui busca el proceso "MYSQL${numerodelpuertoasignado}", en mi caso es MYSQL72
Anyway, puedes dar click en x proceso y presionar "m" en el teclado para que te lleve directamente hasta las M y buscar ahi
Ahora despues de seleccionarlo, a la derecha debe salir el Start service y ya estaria listo
Ahora al abrir el Commandline no deberia cerrarse despues de ingresar el pswrd

las imagenes se guardan en BASE64

## Tareilla pa

importar el hashlib
