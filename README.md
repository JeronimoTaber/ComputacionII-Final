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