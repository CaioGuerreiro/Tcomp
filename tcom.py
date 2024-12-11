import pandas as pd

# Função para ler o arquivo e organizar os dados
def parse_nfa(file_path):
    nfa = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Processar estados (Q)
    states_line = [line for line in lines if line.startswith("Q:")][0]  
    states = states_line.split(":")[1].strip().split(", ")
    
    # Inicializar o NFA com estados e alfabeto
    for state in states:
        nfa[state] = {}
    
    # Processar alfabeto (A)
    alphabet_line = [line for line in lines if line.startswith("A:")][0]
    alphabet = alphabet_line.split(":")[1].strip().split(", ")
    
    for state in nfa:
        for symbol in alphabet:
            nfa[state][symbol] = []  # Inicializar todas as transições como listas vazias
    
    # Processar transições (T)
    transitions_line = [line for line in lines if line.startswith("T:")][0]
    transitions_index = lines.index(transitions_line) + 1
    transitions = lines[transitions_index:]
    for transition in transitions:
        if "->" in transition:
            left, right = transition.split(" -> ")
            state, symbol = left.split(",")
            state, symbol = state.strip(), symbol.strip()
            destinations = right.strip().split(", ")
            nfa[state][symbol].extend(destinations)
    
    # Processar estado inicial (q0)
    initial_line = [line for line in lines if "inicial" in line][0]
    initial_state = initial_line.split(":")[1].strip()
    
    # Processar estados finais (F)
    final_line = [line for line in lines if line.startswith("F:")][0]
    final_states = final_line.split(":")[1].strip().split(", ")
    
    # Processar palavra (w)
    word_line = [line for line in lines if line.startswith("w:")][0]
    word = word_line.split(":")[1].strip()
    
    return nfa, states, alphabet, initial_state, final_states, word

# Função para converter NFA em DFA
def nfa_to_dfa(nfa, alphabet, initial_state, final_states):
    # Inicializar estruturas do DFA
    dfa = {}
    dfa_states = []
    dfa_final_states = []
    queue = []
    
    # Estado inicial do DFA é o conjunto que contém apenas o estado inicial da NFA
    start_state = initial_state  # Usando o nome do estado inicial diretamente (sem vírgula)
    queue.append(start_state)
    dfa_states.append(start_state)
    dfa[start_state] = {}

    # Processar a fila de estados
    while queue:
        current_state = queue.pop(0)
        dfa[current_state] = {}
        
        # Para cada símbolo do alfabeto
        for symbol in alphabet:
            # Determinar os estados alcançáveis a partir do estado atual
            next_states = set()
            for substate in current_state.split():
                if substate in nfa and symbol in nfa[substate]:
                    next_states.update(nfa[substate][symbol])
            
            # Criar o novo estado (conjunto de estados da NFA) como uma string
            next_state = " ".join(sorted(next_states))  # Juntando os estados com espaço
            
            # Adicionar transição no DFA
            dfa[current_state][symbol] = [next_state]
            
            # Se o novo estado não estiver no DFA, adicionar à fila
            if next_state not in dfa_states:
                dfa_states.append(next_state)
                queue.append(next_state)
    
    # Determinar os estados finais do DFA
    for dfa_state in dfa_states:
        if any(state in final_states for state in dfa_state.split()):
            dfa_final_states.append(dfa_state)
    
    # Adicionar estado morto para garantir transições completas
    dead_state = "D"  # Estado morto representado por uma string vazia
    if dead_state not in dfa:
        dfa[dead_state] = {symbol: dead_state for symbol in alphabet}
    for state in dfa:
        for symbol in alphabet:
            if symbol not in dfa[state]:
                dfa[state][symbol] = dead_state

    return dfa, dfa_final_states

# def reverse(dfa):
#     dfa[state][symbol]


# Caminho do arquivo
file_path = "input.txt"

# Processar o arquivo
nfa, states, alphabet, initial_state, final_states, word = parse_nfa(file_path)

# Exibir o NFA
print("\nNFA:")
print(nfa)

# Converter NFA em DFA
dfa, dfa_final_states = nfa_to_dfa(nfa, alphabet, initial_state, final_states)

# Exibir o DFA
print("\nDFA:")
print(dfa)

# Exibir estados finais do DFA
print("\nFinal states of DFA:", dfa_final_states)

# Exibir tabelas
print("\nNFA Table:")
nfa_table = pd.DataFrame(nfa)
print(nfa_table.transpose())

print("\nDFA Table:")
dfa_table = pd.DataFrame(dfa)
print(dfa_table.transpose())

# Verificar se a palavra é aceita pelo DFA
current_state = initial_state
for symbol in word:
    if symbol in dfa[current_state]:
        current_state = dfa[current_state][symbol][0]
    else:
        current_state = ""
        break

if current_state in dfa_final_states:
    print(f"\nThe word '{word}' is accepted by the DFA.")
else:
    print(f"\nThe word '{word}' is not accepted by the DFA.")
