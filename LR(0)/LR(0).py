def LR0():
    regulations = [
        "S->AA", "A->aA", "A->b"
    ]

    N = {'S', 'A'}
    T = {'a', 'b', '$'}

    s = "aabb"
    action = [{} for _ in range(6)]
    goto = [{} for _ in range(6)]

    def formTable():
        action_table = {
            0: {'a': 's3', 'b': 's4'},
            1: {'a': 's3', 'b': 's4', '$': 'r3'},
            2: {'$': 'acc'},
            3: {'a': 's3', 'b': 's4'},
            4: {'$': 'r2', 'a': 'r2', 'b': 'r2'},
            5: {'$': 'r1', 'a': 'r1', 'b': 'r1'},
        }


        goto_table = {
            0: {'S': 1, 'A': 2},
            3: {'A': 5},
        }

        for state, actions in action_table.items():
            action[state].update(actions)
        
        for state, gotos in goto_table.items():
            goto[state].update(gotos)

    formTable()

    stateStack = [0]
    symbleStack = ['']
    buffer = s + '$'
    p = 0

    while True:
        S = stateStack[-1]
        a = buffer[p]
        
        action_entry = action[S].get(a, '')

        print(f"Current state: {S}, current symbol: {a}")
        
        if action_entry.startswith('s'):
            num = int(action_entry[1:])
            symbleStack.append(a)
            stateStack.append(num)
            p += 1
            print(f"Shift: moved to state {num}, symbol stack: {symbleStack}, state stack: {stateStack}")
        elif action_entry.startswith('r'):
            index = int(action_entry[1:]) - 1
            left, right = regulations[index].split("->")
            for _ in right:
                stateStack.pop()
                symbleStack.pop()
            S = stateStack[-1]
            symbleStack.append(left)
            stateStack.append(goto[S][left])
            print(f"Reduce: used rule {regulations[index]}, symbol stack: {symbleStack}, state stack: {stateStack}")
        elif action_entry == 'acc':
            print("Accept: the input string is successfully parsed.")
            return
        else:
            print("Error: invalid symbol or state.")
            return
        
        print(f"State Stack: {stateStack}")
        print(f"Symbol Stack: {symbleStack}\n")

LR0()
