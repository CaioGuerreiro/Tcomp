import pandas as pd

nfa = {}
n = int(input("number of states: "))
t = int (input("number of transitions: "))

for i in range(n):
    state = input("state name: ")
    nfa[state] = {}
    for j in range(t):
        path = input ("path: ")
        print(f"Enter end state from state {state} travelling through path {path}: ")
        reaching_state = [x for x in input().split()]
        nfa[state][path] = reaching_state

print("\nNFA :\n")
print(nfa)
print("\nPrinting NFA table: ")
nfa_table = pd.DataFrame(nfa)
print(nfa_table.transpose())

print("Enter final state of NFA: ")
nfa_final_state = [x for x in input().split()]

new_states_list = []
dfa = {}
keys_list = list(nfa.keys()) #aqui deu problema
path_list = list(nfa[keys_list[0]].keys())

dfa[keys_list[0]] = {}
for y in range(t):
    var = "".join(nfa[keys_list[0]][path_list[y]])
    dfa[keys_list[0]][path_list[y]] = var
    if var not in keys_list:
        new_states_list.append(var)
        keys_list.append(var)

while len(new_states_list) != 0:
    current_state = new_states_list[0]
    dfa[current_state] = {}
    for path in path_list:
        temp = []
        for state in current_state:
            temp += nfa[state][path]
        new_state = "".join(sorted(set(temp)))
        dfa[current_state][path] = new_state
        if new_state not in keys_list:
            new_states_list.append(new_state)
            keys_list.append(new_state)
    new_states_list.remove(current_state)


print("\nDFA: \n")
print(dfa)
print("\nPrinting DFA table")
dfa_table = pd.DataFrame(dfa)
print(dfa_table.transpose())

dfa_states_list = list(dfa.keys())
dfa_final_states = []
for x in dfa_states_list:
    for i in x:
        if i in nfa_final_state:
            dfa_final_states.append(x)
            break

print("\n Final states of the DFA are : ", dfa_final_states)
