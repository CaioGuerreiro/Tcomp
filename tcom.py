import pandas as pd

#Função que lê o arquivo e organiza os dados
def ler_afn(caminho_arquivo):
    afn = {}
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    
    #Processar estados (Q)
    linha_estados = [linha for linha in linhas if linha.startswith("Q:")][0]  
    estados = linha_estados.split(":")[1].strip().split(", ")
    
    for estado in estados:
        afn[estado] = {}
    
    #Processar alfabeto (A)
    linha_alfabeto = [linha for linha in linhas if linha.startswith("A:")][0]
    alfabeto = linha_alfabeto.split(":")[1].strip().split(", ")
    
    for estado in afn:
        for simbolo in alfabeto:
            afn[estado][simbolo] = []
    
    #Processar transições (T)
    linha_transicoes = [linha for linha in linhas if linha.startswith("T:")][0]
    indice_transicoes = linhas.index(linha_transicoes) + 1
    transicoes = linhas[indice_transicoes:]
    for transicao in transicoes:
        if "->" in transicao:
            esquerda, direita = transicao.split(" -> ")
            estado, simbolo = esquerda.split(",")
            estado, simbolo = estado.strip(), simbolo.strip()
            destinos = direita.strip().split(", ")
            afn[estado][simbolo].extend(destinos)
    
    #Processar estado inicial (q0)
    linha_inicial = [linha for linha in linhas if "inicial" in linha][0]
    estado_inicial = linha_inicial.split(":")[1].strip()
    
    #Processar estados finais (F)
    linha_finais = [linha for linha in linhas if linha.startswith("F:")][0]
    estados_finais = linha_finais.split(":")[1].strip().split(", ")
    
    #Processar palavra (w)
    linha_palavra = [linha for linha in linhas if linha.startswith("w:")][0]
    palavra = linha_palavra.split(":")[1].strip()
    
    return afn, estados, alfabeto, estado_inicial, estados_finais, palavra

#Função para converter AFN em AFD
def afn_para_afd(afn, alfabeto, estado_inicial, estados_finais):
    afd = {}
    estados_afd = []
    estados_finais_afd = []
    fila = []
    estado_inicial_afd = estado_inicial
    fila.append(estado_inicial_afd)
    estados_afd.append(estado_inicial_afd)
    afd[estado_inicial_afd] = {}

    #Processar a fila de estados
    while fila:
        estado_atual = fila.pop(0)
        afd[estado_atual] = {}
        
        #Para cada símbolo do alfabeto
        for simbolo in alfabeto:
            proximos_estados = set()
            for subestado in estado_atual.split():
                if subestado in afn and simbolo in afn[subestado]:
                    proximos_estados.update(afn[subestado][simbolo])
            
            #Criar o novo estado (conjunto de estados da AFN) como uma string
            proximo_estado = " ".join(sorted(proximos_estados))
            
            #Adicionar transição no AFD
            afd[estado_atual][simbolo] = [proximo_estado]
            
            #Se o novo estado não estiver no AFD, adicionar à fila
            if proximo_estado not in estados_afd:
                estados_afd.append(proximo_estado)
                fila.append(proximo_estado)
    
    #Determinar os estados finais do AFD
    for estado_afd in estados_afd:
        if any(estado in estados_finais for estado in estado_afd.split()):
            estados_finais_afd.append(estado_afd)

    return afd, estados_finais_afd, estado_inicial_afd

def reverso_afd(afd, estado_inicial, estados_finais, alfabeto):
    # Inicializar o AFD reverso com os mesmos estados e alfabeto
    afd_reverso = {estado: {simbolo: [] for simbolo in alfabeto} for estado in afd}
    
    # Inverter as transições
    for estado, transicoes in afd.items():
        for simbolo, destinos in transicoes.items():
            if not isinstance(destinos, list):
                destinos = [destinos]  # Garantir que destinos seja uma lista
            for destino in destinos:
                if destino not in afd_reverso:
                    afd_reverso[destino] = {simbolo: [] for simbolo in alfabeto}
                afd_reverso[destino][simbolo].append(estado)
    
    # Criar um novo estado inicial único no reverso
    novo_estado_inicial = "novo_estado_inicial"
    afd_reverso[novo_estado_inicial] = {simbolo: [] for simbolo in alfabeto}
    
    # Adicionar transições epsilon para os antigos estados finais
    for estado_final in estados_finais:
        if "epsilon" not in afd_reverso[novo_estado_inicial]:
            afd_reverso[novo_estado_inicial]["epsilon"] = []
        afd_reverso[novo_estado_inicial]["epsilon"].append(estado_final)
    
    # Determinar os novos estados finais (o antigo estado inicial)
    estados_finais_reverso = [estado_inicial]

    return afd_reverso, novo_estado_inicial, estados_finais_reverso




#Função para descobrir o complemento do AFD
def complemento_afd(afd, estados, estados_finais):
    #Determinar os estados não finais
    estados_nao_finais = [estado for estado in estados if estado not in estados_finais]
    
    #O complemento do DFA usa os estados não finais como novos estados finais
    estados_finais_complemento = estados_nao_finais
    return afd, estados_finais_complemento


#Caminho do arquivo
caminho_arquivo = "input.txt"

afn, estados, alfabeto, estado_inicial, estados_finais, palavra = ler_afn(caminho_arquivo)

print("\nAFN:")
print(afn)

#Converter AFN em AFD
afd, estados_finais_afd, estado_inicial_afd = afn_para_afd(afn, alfabeto, estado_inicial, estados_finais)

#Invertendo AFD
afd_reverso, estado_inicial_reverso, estados_finais_reverso = reverso_afd(afd, estado_inicial, estados_finais, alfabeto) 
print("\nAFD INVERTIDO")
print(afd_reverso)

#Complemento AFD
afd_complemento, estados_finais_complemento = complemento_afd(afd, estados, estados_finais)
print("\nAFD COMPLEMENTO")
print(afd_complemento)
print("\nEstados finais: ")
print(estados_finais_complemento)

#Exibir o AFD
print("\nAFD:")
print(afd)

#Exibir estados finais do AFD
print("\nEstados finais do AFD:", estados_finais_afd)

#Exibir tabelas
print("\nTabela AFN:")
tabela_afn = pd.DataFrame(afn)
print(tabela_afn.transpose())

print("\nTabela AFD:")
tabela_afd = pd.DataFrame(afd)
print(tabela_afd.transpose())

#Verificar se a palavra é aceita pelo AFD
estado_atual = estado_inicial
for simbolo in palavra:
    if simbolo in afd[estado_atual]:
        estado_atual = afd[estado_atual][simbolo][0]
    else:
        estado_atual = ""
        break

if estado_atual in estados_finais_afd:
    print(f"\nA palavra '{palavra}' é aceita pelo AFD.")
else:
    print(f"\nA palavra '{palavra}' não é aceita pelo AFD.")
