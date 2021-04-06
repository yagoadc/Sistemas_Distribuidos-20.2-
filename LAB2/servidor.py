####### LAB 2 - Sistemas Distribuidos ###########

# Alunos:
#        Rodrigo Passos - 115196299
#        Yago Alves - 115212477

##################################################

# lado servidor
from processamento import processa_dados
import socket

HOST = ''    # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5000  # porta onde chegarao as mensagens para essa aplicacao

# cria um socket para comunicacao
sock = socket.socket()  # valores default: socket.AF_INET, socket.SOCK_STREAM

# vincula a interface e porta para comunicacao
sock.bind((HOST, PORTA))

# define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
sock.listen(1)

while True:  # Fica em loop esperando sempre uma nova conexão
    print('Aguardando uma conexão.')
    # aceita a primeira conexao da fila (chamada pode ser BLOQUEANTE)
    # retorna um novo socket e o endereco do par conectado
    novoSock, endereco = sock.accept()
    print('Conectado com: ', endereco)

    while True:
        try:
            # depois de conectar-se, espera uma mensagem (chamada pode ser BLOQUEANTE))
            print('Esperando mensagem...')
            # argumento indica a qtde maxima de dados
            msg = novoSock.recv(2048)
            if not msg:
                print('Encerrando conexão.')
                novoSock.close()
                break
            else:
                # Separa o nome dos arquivo por virgula e salva em uma lista
                msg = msg.decode("utf-8").split(',')
                print('Recebi essa lista de nomes de arquivos: ' + str(msg))

                # A partir daqui é feito o acesso para a camada de processamento
                print('Processando...')
                res = processa_dados(msg)

                # Envio dos dados
                print('Enviando resposta.')
                novoSock.send(bytes(res, 'utf-8'))
        except:
            # Caso aconteça algum erro, o servidor comunica o problema pede novamente o arquivo
            novoSock.send(
                bytes("Tivemos algum problema, tente novamente", 'utf-8'))
