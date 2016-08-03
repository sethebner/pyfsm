class State(object):

    def __init__(self, identifier, accepting, transitions={}):
        self.identifier = identifier
        self.accepting = accepting
        self.transitions = transitions

    def get_identifier(self):
        return self.identifier

    def set_identifier(self, identifier):
        self.identifier = identifier
    
    def get_transitions(self):
        return self.transitions

    def set_transition(self, state, char):
        if self.has_transition(state, char):
            return False
        elif char in self.transitions.keys():
            self.transitions[char].append(state)
            return True
        else:
            self.transitions[char] = []
            self.transitions[char].append(state)
            return True
    
    def is_accepting(self):
        return self.accepting

    def set_accepting(self, accepting):
        self.accepting = accepting
    
    def has_transition(self, state, char):
        if char in self.transitions.keys():
            return state in self.transitions[char]
        else:
            return False

    def get_next(self, char):
        if char in self.transitions.keys():
            return self.transitions[char]
        else:
            return None

    def to_string(self):
        return '{}, {}'.format(self.identifier, self.accepting)
        
    def print_node(self):
        print(self.to_string())
