####### LAB 3 - Sistemas Distribuidos ###########

# Alunos:
#        Rodrigo Passos - 115196299
#        Yago Alves - 115212477

##################################################

# lado cliente

import socket

HOST = 'localhost'  # maquina onde esta o par passivo
PORTA = 5000        # porta que o par passivo esta escutando

# cria socket
sock = socket.socket()  # default: socket.AF_INET, socket.SOCK_STREAM

# conecta-se com o par passivo
sock.connect((HOST, PORTA))

while True:
    file = input(
        " Digite o nome do arquivo ou uma lista de arquivos com os nomes separado por virgula\nPara sair da aplicação aperte enter\n")
    if file:
        # Enviando a mensage com os nomes dos arquivos para o servidor
        mensg = bytes(file, 'utf-8')
        sock.sendto(mensg, (HOST, PORTA))

        # Recebendo a mensage com os dados processados no servidor - espera a resposta do par conectado (chamada pode ser BLOQUEANTE)lab1
        resposta = sock.recv(1024)
        if resposta:
            print(resposta.decode("utf-8"))
    else:
        sock.close()
        break
