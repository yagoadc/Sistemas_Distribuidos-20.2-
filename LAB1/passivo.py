####### LAB 1 - Sistemas Distribuidos ###########

# Alunos:   
#        Rodrigo Passos - 115196299
#        Yago Alves - 115212477

##################################################


# Exemplo basico socket (lado passivo)

import socket

HOST = ''    # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5000  # porta onde chegarao as mensagens para essa aplicacao

# cria um socket para comunicacao
sock = socket.socket() # valores default: socket.AF_INET, socket.SOCK_STREAM  

# vincula a interface e porta para comunicacao
sock.bind((HOST, PORTA))

# define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
sock.listen(5) 

# aceita a primeira conexao da fila (chamada pode ser BLOQUEANTE)
novoSock, endereco = sock.accept() # retorna um novo socket e o endereco do par conectado
print ('Conectado com: ', endereco)

while True:
	# depois de conectar-se, espera uma mensagem (chamada pode ser BLOQUEANTE))
	print ('Esperando mensagem...')
	msg = novoSock.recv(1024) # argumento indica a qtde maxima de dados
	if not msg: break 
	#else: print(str(msg,  encoding='utf-8'))

	# envia mensagem de resposta
	print ('Recebi. Enviando resposta.')
	novoSock.send(msg) 

print('Encerrando aplicação. Até a proxima!')
# fecha o socket da conexao
novoSock.close() 

# fecha o socket principal
sock.close() 
