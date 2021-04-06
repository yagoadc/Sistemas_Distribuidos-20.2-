####### LAB 2 - Sistemas Distribuidos ###########

# Alunos:
#        Rodrigo Passos - 115196299
#        Yago Alves - 115212477

##################################################

# Camada de processamento

from dados import openFile
import os
import sys
import re
import string


def processa_dados(lista_nomes):
    resposta = ""  # Variavel que vai receber a resposta para o cliente
    # Percorrendo a lista de nomes de arquivos
    for name in lista_nomes:
        dicionario = {}  # Inicia um dicionario que vai receber o par palavra:numero_de_ocorrecias
        # Retira os espaços do inicio e do final do nome
        name = name.strip(" ")

        if name:
            # Marca na resposta que a partir dessa linha, tudo abaixo será sobre o arquivo em name
            resposta += name+":\n"

        try:
            # É feito um acesso a camada de dados - Verifica existencia e retorna o conteudo do arquivo
            conteudo = openFile(name)
        except Exception:  # Caso não seja possível a leitura do arquivo, insiro essa informacao na resposta
            resposta += f"\tO arquivo {name} não foi encontrado\n"
            continue

        # Camada de processamento - criando um dicionario com as palavras e salvando o numeros de ocorrencias das palavras.
        for linha in conteudo:
            if linha:
                linha = linha.lower()  # Tudo para minusculo
                # Retira os espaços do inicio e do final da linha
                linha = linha.strip(" ")
                linha = linha.strip("\n")  # Remove o pula linha
                linha = re.compile('[%s]' % re.escape(
                    string.punctuation)).sub("", linha)  # Revome os caracteres de pontução
                # Separa cada palavra da linha e salva na lista
                palavras = linha.split(" ")
                for p in palavras:
                    if p:
                        # Se a palvra já estiver no dicionario, contabiliza mais um no valor de ocorrencias
                        if p in list(dicionario):
                            dicionario[p] = dicionario[p] + 1
                        else:  # Se não, é adicionado um novo par palavra:numero_ocerrencias
                            dicionario[p] = 1
        # Reorganiza o dicionario de forma decrescente pelo valor de numero de ocerrencias
        dicionario = sorted(
            dicionario.items(),  key=lambda x: x[1], reverse=True)

        # Descobre a quantidade de palavras descobertas
        tamanho_max = len(dicionario)
        if tamanho_max >= 10:
            # Pega as 10 mais ocorridas.
            mais_ocorridos = zip(range(0, 10), dicionario)
        else:
            # Menor que 10 palavras, pega todas as palavras descobertas.
            mais_ocorridos = zip(range(0, tamanho_max), dicionario)

        # Preparando a resposta para o cliente
        for i, tupla in mais_ocorridos:  # Pega a tupla palavra:numero_de_ocorrencias e salva na string de resposta
            resposta += "\t"+tupla[0]+": "+str(tupla[1])+"\n"

        resposta += "\n"  # Pula linha no final da respota
    return resposta
