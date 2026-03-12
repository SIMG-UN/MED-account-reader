# MED-account-reader
Proyecto para ayudante financiero que lee correos de gastos de bancos, los parsea, guarda y que, por medio de LLM local, permite responder preguntas sobre gastos/ingresos y cruzar contextos que dé el usuario

Algunas de las carpetas:

1. connection: Directorio con todo el contenido relacionado a conexiones y requests para acceder a información del correo. Se necesita llenar las credenciales en el .yaml con los datos propios para verificar! El archivo **conection_test.py** se basa en estas credenciales y busca en el INBOX del correo todos los correos enviados por Bancolombia y muestra el último.