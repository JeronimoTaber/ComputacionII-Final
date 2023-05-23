# ComputacionII-Final
## Funcionalidades a agregar:
2) definir max jugadores
2) Conexion a chatGPT
3) implementacion de colas de mensajes


NO ESTA MANDANDO EN MENSAJE DE FORMA SINCRONA


celery -A tasks worker --loglevel=infoclear

python3 server/server.py 
python3 client/client.py -n
python3 client/client.py -r 
python3 client/client.py -p 45281


TAREAS:
MANEJO DE ERRORES
QUE NO SEA HARDCODEADO EL 127 EN ASYNCIO
Que pueda usar IPV6 (Cuando arranque levantar socket ipv4 y ipv6 si esta disponible)
REvisar que accedan de distinas ips
Grabar ejecucion que funcione
ARMAR GARAFICO DE LA ESTRUCTURA
