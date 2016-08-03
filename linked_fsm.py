from state import State

class Linked_FSM(object):

    def connect(self, source_state, dest_state, char):
        if char in self.terminals:
            source_state.set_transition(dest_state, char)
        else:
            return False
    
    def __init__(self, start_accepting, terminals=set()):
        self.start = State('START_STATE', start_accepting, transitions={})
        
        self.all_states = set()
        self.all_states.add(self.start)

        self.inhabited_states = set()
        self.inhabited_states.add(self.start)

        self.dead_state = State('DEAD', False)
        
        self.terminals = terminals
        for terminal in terminals:
            self.connect(self.dead_state, self.dead_state, terminal)

    def get_start_state(self):
        return self.start

    def set_start_state(self, state):
        self.get_inhabited_states().discard(self.start)
        self.start = state
        self.get_inhabited_states().add(self.start)
    
    def get_all_states(self):
        return self.all_states

    def get_inhabited_states(self):
        return self.inhabited_states

    def is_empty(self):
        return len(self.all_states) == 0

    def create_state(self, identifier, is_accepting, transitions):
        state = State(identifier, is_accepting, transitions)
        self.all_states.add(state)
        return state

    def in_accepting_state(self):
        return any([state.is_accepting() for state in self.inhabited_states])

    def process_character(self, char):
        destinations = set()
        if char not in self.terminals or self.dead_state in self.inhabited_states:
            destinations.add(self.dead_state)
            
        for state in self.inhabited_states:
            if char in state.get_transitions().keys():
                for next_state in state.get_next(char):
#                    print('{} takes {} to {}'.format(char, state.get_identifier(), next_state.get_identifier()))
                    destinations.add(next_state)

            if '\0' in state.get_transitions().keys():
                for next_state in state.get_next('\0'):
#                    print('\0 takes {} to {}'.format(state.get_identifier(), next_state.get_identifier()))
                    destinations.add(next_state)

        self.inhabited_states = destinations
