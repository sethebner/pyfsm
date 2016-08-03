from linked_fsm import Linked_FSM
from tokenizer import Tokenizer

import re
import sys

'''

Two well-formed statements allowed:

initial_state -> final_state :: {terminals}
[variable] :: value

'''

LHS = 0 # left hand side index
RHS = 1 # right hand side index
TERMINALS = 2 # terminals index

DEBUG_MODE_ON = False
def debug_print(s):
    if DEBUG_MODE_ON:
        print(s)

def str_to_bool(s):
    ans = False
    if s.lower() in ['true']:
        ans = True
    elif s.lower() in ['false']:
        ans = False
    else:
        raise ValueError('Could not determine truth value')
    return ans
    
def main():
    '''    
    terminals = ['a', 'b', '\0']
    fsm = Linked_FSM(False, terminals)

    input_string = 'aaa'

    q1 = fsm.create_state('q1', True)

    fsm.connect(fsm.get_start_state(), fsm.get_start_state(), 'a')
    fsm.connect(fsm.get_start_state(), q1, 'b')
#    fsm.connect(fsm.get_start_state(), q1, '\0')
    fsm.connect(q1, q1, 'a')
    fsm.connect(q1, q1, 'b')
    '''

    if len(sys.argv) < 2:
        sys.exit()
        
    t = Tokenizer()
    tokens = t.tokenize(sys.argv[1])

    '''
    Move this to a Parser class
    -Ensure each line has a LHS, RHS
    -Return state_names(set), state_accepting(dict), terminals(set), start_accepting(bool), input_string(str)
    '''
    
    input_string = ''
    start_accepting = False
    start_state_name = ''
    terminals = set()
    terminal_regex = '|'.join(map(re.escape, ['{', '}']))
    state_names = set()
    state_accepting = {}
    debug_print(tokens)
    for token in tokens:
        if token[LHS].lower() == '[input]':
            input_string = token[RHS]
#        elif token[LHS].lower().startswith('[-') and token[LHS].lower().endswith(']'):
#            start_accepting = str_to_bool(token[RHS])    
        elif token[LHS].lower() == '[terminals]':
            terminals = re.split(terminal_regex, token[RHS])
            terminals = list(filter(None, terminals))
            terminals = terminals[0].split()
            terminals = set(terminals)
        elif token[LHS].lower().startswith('[') and token[LHS].lower().endswith(']'):
            tab = str.maketrans('[]', '  ')
            temp_state_name = token[LHS].translate(tab)
            temp_state_name = temp_state_name.strip()
            if temp_state_name.startswith('-'):
                temp_state_name = temp_state_name[1:]
                start_state_name = temp_state_name
            state_names.add(temp_state_name)
#            debug_print('Token line: token is {}, token[LHS] is {}, token[RHS] is {}'.format(token, token[LHS], token[RHS]))
            state_accepting[temp_state_name] = str_to_bool(token[RHS])
        else:
            state_names.add(token[LHS])
            state_names.add(token[RHS])
            
    debug_print('Input string: {}'.format(input_string))
    debug_print('START state is accepting: {}'.format(start_accepting))
    debug_print('Terminals: {}'.format(terminals))
    debug_print('States: {}'.format(state_names))
    '''^^^'''

    fsm = Linked_FSM(start_accepting, terminals)

    # create states based on state_names (fsm.create_state)
    states = {}
    debug_print('state_accepting.keys(): {}'.format(state_accepting.keys()))
    for state_name in state_accepting.keys():
        states[state_name] = fsm.create_state(state_name, state_accepting[state_name], transitions = {})

    # connect states based on statements (fsm.connect)
    debug_print('states.keys(): {}'.format(states.keys()))
    for token in tokens:
        if token[LHS] in states.keys() and token[RHS] in states.keys():
            for terminal in token[TERMINALS].split():
                fsm.connect(states[token[LHS]], states[token[RHS]], terminal)
#                print('{} connected to {} by {}'.format(states[token[LHS]].get_identifier(), states[token[RHS]].get_identifier(), terminal))

    fsm.set_start_state(states[start_state_name])
    print([s.to_string() for s in fsm.get_inhabited_states()])

    for char in input_string:
        print('Processing {}.'.format(char))
        fsm.process_character(char)
        print('Now in state(s): {}'.format([s.to_string() for s in fsm.get_inhabited_states()]))
        print('We are{} accepting'.format('' if fsm.in_accepting_state() else ' not'))

    print('INPUT{} ACCEPTED'.format('' if fsm.in_accepting_state() else ' NOT'))
    
if __name__ == '__main__':
    main()
