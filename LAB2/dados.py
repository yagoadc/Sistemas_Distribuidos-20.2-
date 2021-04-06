####### LAB 2 - Sistemas Distribuidos ###########

# Alunos:
#        Rodrigo Passos - 115196299
#        Yago Alves - 115212477

##################################################
# Camada de dados
def openFile(path):
    try:
        arq = open(path, 'r', encoding="utf-8")
        return arq.readlines()
    except:
        raise Exception("Não foi possivel abrir o arquivo")
