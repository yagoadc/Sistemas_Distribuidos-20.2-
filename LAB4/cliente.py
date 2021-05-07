import sys
import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

# Cria um socket 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tenta uma conexão
def conectaAoServidor ():
    server = (HOST, PORT)
    sock.connect(server)


# Envia de mesagem para o servidor
def envia(mensagem):
    tamanho = len(mensagem) 
    while tamanho >0:            
        enviado = sock.send(bytes(mensagem, 'utf-8'))
        tamanho=tamanho-enviado

# Cada cliente cria uma thread para ficar escutando o servidor, caso receba alguma mensagem
def threadEscutaServer():
    while True:
        try:
            msg = sock.recv(2048)
            print(msg.decode("utf-8"))
            if (msg.decode("utf-8") == "out"):   
                break
        except:
            print("Erro ao receber uma mensagem!")
            
def main():   
    try:
        conectaAoServidor()       
    except:
        print("Não foi possível se conectar ao servidor!")
        return 

    # Thread do cliente (parte passiva) que ficará escutando servidor.
    cliente = threading.Thread(target=threadEscutaServer)
    cliente.start()

    while True:
        entrada = input()
        if entrada=="out":
            envia(entrada)
            cliente.join()
            sock.close()     
            sys.exit()
        elif entrada:
            envia(entrada)

main()