import socket 
import select 
import sys 
import threading

HOST = ""
PORT = 5000

# lista que vai receber os cliente conectados ( varialvel compartilha entre as threads)
clientes_ativos = [] 

# lock para tratar variaveis compartilhadas entre as threads
lock = threading.Lock()

# define a lista de I/O de interesse (jah inclui a entrada padrao)
entradas = [sys.stdin]

# cria socket para o servidor 
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def iniciaServidor():
    '''Cria um socket de servidor e o coloca em modo de espera por conexoes
    Saida: o socket criado'''
    # cria o socket
    # Internet( IPv4 + TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # vincula a localizacao do servidor
    sock.bind((HOST, PORT))

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

    return clisock, endr

def envia(msg, conn): # Envia mensagem para algum cliente
    tamanho = len(msg)
    while tamanho >0:
        enviado = conn.send(bytes(msg, 'utf-8')) 
        tamanho=tamanho-enviado


def entrou_ou_saiu (msg): # Faz um broadcast de um aviso sobre um usuario que entrou ou saiu da sala.
    lock.acquire()
    for cliente in clientes_ativos:
        sock_c = cliente["sock_cliente"]    
        envia(msg,sock_c)
    lock.release()

def remove(user): # Retira algum cliente da lista dos ativos e informa a todos na sala sobre sua saida.
    lock.acquire()
    clientes_ativos.remove(user)
    lock.release()
    user["sock_cliente"].close()
    print(user["name"] + '-> encerrou')
    msg = user["name"] + '-> Saiu da sala '
    entrou_ou_saiu(msg)

def tratraRequisicao(mensagem, conn, flag, usr):
    if flag==1: # Envia a lista de usuarios ativos
        try:
            indice=1
            lock.acquire()
            for usuario in clientes_ativos:
                user_sock = usuario["sock_cliente"]
                if user_sock != conn: # Se não for a conexão do usuario que pediu a requisição
                    mensagem=mensagem+str(indice)+":  "+usuario["name"]+"\n"
                    indice+=1
                else:
                    mensagem=mensagem+str(indice)+": (Você)"+"\n"
                    indice+=1
            envia(mensagem, conn)
            lock.release()
        except:
            envia("Erro ao obter lista de ativos!", conn)  
    elif flag==2: # Busca o destinatario na lista de ativos e envia a mensagem  
        indice_destinatario = mensagem.split(':', 1)[0].strip() # Pega o indice do usuario destino
        msg = mensagem.split(':', 1)[1].strip() # Pega o conteudo da mensagem
        lock.acquire()
        c = clientes_ativos[int(indice_destinatario)-1] # Pega o usuario destinatario
        sock_c = c["sock_cliente"] # Socket do destinatario 
        msg= usr["name"]+":" + "\n    "+msg # Prepara a string da mensagem 
        envia(msg,sock_c)
        lock.release()      
    elif flag==3: # Faz um broadcast
        lock.acquire()
        for cliente in clientes_ativos:
            sock_c = cliente["sock_cliente"]
            if sock_c != conn: # Se não for a conexão do usuario origem
                msg= usr["name"]+":" + "\n    "+mensagem # Prepara a string da mensagem
                envia(msg,sock_c)
        lock.release()

# Apos aceitar conexão. Recebe o username do cliente e o insere na lista de ativos. 
def criaUsuario (conn, addr): 

    conn.send(bytes("Bem vindo ao chat do DCC!\nDigite seu nome:", 'utf-8')) # Pede um username para o cliente            
    username = conn.recv(2048).decode("utf-8") # Recebe o username

    #Cria uma instacia de usuario para cada nova conexão
    new_user = {}
    new_user["name"] = username
    new_user["sock_cliente"] = conn
    new_user["endereco"] = addr

    # registra a novo usuario
    lock.acquire()
    clientes_ativos.append(new_user) # Add na lista de clientes
    lock.release()

    return new_user

def atendeRequisicao(conn, addr):

    user = criaUsuario(conn, addr)
    print (user["name"]+" "+addr[0]+" conectado")
    entrou_ou_saiu(user["name"] + '-> Entrou da sala\n') # Informo que entrei na sala para todos os clientes ativos

    # Passa algumas intruções para o novo cleinte
    men1 = "Para saber se há usuarios ativos, digite lista\n"
    men2 = "Para enviar mensagem privada, digite numero_posição_na_lista_usuario:conteudo_da_mensagem\n"
    men3 = "Para enviar mensagem para todos na sala, digite all\n"
    men4 = "Para sair da sala e finalizar, digite out"
    conn.send(bytes(men1+men2+men3+men4, 'utf-8'))

    while True: 
        try: 
            # Recebe requisição
            mensagem = conn.recv(2048) 
            if mensagem: 
                msg_decode = mensagem.decode("utf-8")
                print(user["name"] + " " + msg_decode)
                if msg_decode == "lista": # Flag 1 - lista de clientes ativos
                    tratraRequisicao("", conn, 1, user)   
                elif msg_decode == "all": # Flag 3 - Envia mensagem para todos usuarios ativos na sala
                    conn.send(bytes("Digite a mensagem:", 'utf-8')) 
                    res = conn.recv(2048)
                    res_decode = res.decode("utf-8")
                    tratraRequisicao(res_decode, conn, 3, user)            
                elif msg_decode == "out": # Encerra a conexação do cliente
                    lock.acquire()
                    envia("out", conn) # Envia sinal para a thread do lado cliente terminar.
                    lock.release()
                    remove(user)
                    break
                else: # Flag 2 - Envia mensagem para um destinatario 
                    tratraRequisicao(msg_decode, conn, 2, user)
            else: # Se algum problema no recebimento da requisição, envia as intruções novamente
                conn.send(bytes(men1+men2+men3+men4, 'utf-8'))
        except: 
            conn.send(bytes("Problema ao enviar! Tente novamanete.","utf-8")) 
            continue

def main():
    '''Inicializa e implementa o loop principal do servidor'''
    print("Iniciando servidor.")
    server_sock = iniciaServidor()
    clientes_threads =[] # lista com a threads de cada cliente conectado
    print("Digite out, para finalizar servidor.")
    print("Pronto para receber conexoes...")
    while True: 
        leitura, escrita, excecao = select.select(entradas, [], [])
        for pronto in leitura:
            if pronto == server_sock:           
                # Aceita conexão com algum cliente requisitado 
                conn, addr = aceitaConexao(server_sock)
                # Cria thread que ficara responsavél pelas requisições do cliente
                cliente = threading.Thread(target=atendeRequisicao, args=(conn, addr))
                cliente.start()
                clientes_threads.append(cliente)                  
            elif pronto == sys.stdin:
                cmd = input()
                if cmd == 'out': #Para finalizar o servidor
                    print("Recuso novas conexões e esperos as ativas terminarem")
                    for c in clientes_threads: #aguarda todas as threads terminarem
                        c.join()
                    print("Encerrando.")
                    server_sock.close()     
                    sys.exit()
main()