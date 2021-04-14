####### LAB 3 - Sistemas Distribuidos ###########

# Alunos:
#        Rodrigo Passos - 115196299
#        Yago Alves - 115212477

##################################################

# lado servidor: implementação concorrente utilizando threads e na finalização do servidor usando join. 

from processamento import processa_dados
import socket
import select
import sys
import threading

HOST = ''    # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5000  # porta onde chegarao as mensagens para essa aplicacao

# cria um socket para comunicacao
sock = socket.socket()  # valores default: socket.AF_INET, socket.SOCK_STREAM

# define a lista de I/O de interesse (jah inclui a entrada padrao)
entradas = [sys.stdin]
# armazena as conexoes ativas. Recurso compartilhado por threads.
conexoes = {}
# lock para acesso do dicionario 'conexoes'
lock = threading.Lock()


def iniciaServidor():
    '''Cria um socket de servidor e o coloca em modo de espera por conexoes
    Saida: o socket criado'''
    # cria o socket
    # Internet( IPv4 + TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # vincula a localizacao do servidor
    sock.bind((HOST, PORTA))

    # coloca-se em modo de espera por conexoes
    sock.listen(5)

    # configura o socket para o modo nao-bloqueante
    sock.setblocking(False)

    # inclui o socket principal na lista de entradas de interesse
    entradas.append(sock)

    return sock


def aceitaConexao(sock):
    '''Aceita o pedido de conexao de um cliente
    Entrada: o socket do servidor
    Saida: o novo socket da conexao e o endereco do cliente'''

    # estabelece conexao com o proximo cliente
    clisock, endr = sock.accept()

    # registra a nova conexao
    lock.acquire()
    conexoes[clisock] = endr
    lock.release()

    return clisock, endr


def atendeRequisicoes(clisock, endr):
    '''Recebe mensagens com uma lista de nomes de arquivos .txt e as envia de volta para o cliente uma mensagem no formato string contendo as 10 palavras mais ocorredas em cada arquivo (ate o cliente finalizar)
    Entrada: socket da conexao e endereco do cliente
    Saida: '''
    while True:
        try:
            print('Esperando mensagem de'+str(endr)+'...')
            # argumento indica a qtde maxima de dados
            msg = clisock.recv(1024)
            if not msg:
                lock.acquire()
                # retira o cliente da lista de conexoes ativas
                del conexoes[clisock]
                lock.release()
                clisock.close()  # encerra a conexao com o cliente
                print('Encerrando conexão.')
                print(str(endr) + '-> encerrou')
                clisock.close()
                return
            else:
                # Separa o nome dos arquivo por virgula e salva em uma lista
                msg = msg.decode("utf-8").split(',')
                print('Recebi essa lista de nomes de arquivos: ' + str(msg))
                # A partir daqui é feito o acesso para a camada de processamento
                print('Processando...')
                res = processa_dados(msg)
                # Envio dos dados
                print('Enviando resposta para '+str(endr))
                clisock.send(bytes(res, 'utf-8'))
        except:
            # Caso aconteça algum erro, o servidor comunica o problema pede novamente o arquivo
            clisock.send(
                bytes("Tivemos algum problema, tente novamente", 'utf-8'))


def main():
    '''Inicializa e implementa o loop principal do servidor'''
    print("Iniciando servidor.")
    sock = iniciaServidor()
    print('Para encerrar servidor, apenas digite out')
    print('Para saber se há conexões, apenas digite hist')
    clientes =[] #threads ativas
    print("Pronto para receber conexoes...")
    while True:
        # espera por qualquer entrada de interesse
        leitura, escrita, excecao = select.select(entradas, [], [])
        # tratar todas as entradas prontas
        for pronto in leitura:
            if pronto == sock:  # pedido novo de conexao
                clisock, endr = aceitaConexao(sock)
                print('Conectado com: ', endr)
                # cria nova thread para atender o cliente
                cliente = threading.Thread(
                    target=atendeRequisicoes, args=(clisock, endr))
                cliente.start()
                clientes.append(cliente)
            elif pronto == sys.stdin:  # entrada padrao
                cmd = input()
                if cmd == 'out':
                    for c in clientes: #aguarda todas as threads terminarem
                        c.join()
                    sock.close()     
                    sys.exit()
                elif cmd == 'hist': #outro exemplo de comando para o servidor
                    print(str(conexoes.values()))

main()
