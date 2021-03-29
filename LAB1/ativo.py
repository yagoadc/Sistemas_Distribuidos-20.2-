####### LAB 1 - Sistemas Distribuidos ###########

# Alunos:   
#        Rodrigo Passos - 115196299
#        Yago Alves - 115212477

##################################################

# Exemplo basico socket (lado ativo)

import socket

HOST = 'localhost' # maquina onde esta o par passivo
PORTA = 5000        # porta que o par passivo esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o par passivo
sock.connect((HOST, PORTA)) 

#decisao = input(" Digite 0 para sair ou 1 para enviar mensagem")
#if(decisao == 1):
print('Digite uma mensagem qualquer. Para encerrar,apenas digite out.')
mensg = input('Entre com a mensagem: ')

while mensg != 'out':
    # envia uma mensagem para o par conectado
    sock.sendto(mensg.encode('utf-8'), (HOST, PORTA))

    #espera a resposta do par conectado (chamada pode ser BLOQUEANTE)
    msg = sock.recv(1024) # argumento indica a qtde maxima de bytes da mensagem

    # imprime a mensagem recebida
    print(str(msg,  encoding='utf-8'))

    mensg = input('Entre com a mensagem: ') 

# encerra a conexao
sock.close() 
