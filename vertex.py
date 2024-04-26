from tkinter import Label


class Vertex:

    is_faulty = False
    # current_decision = True
    memory_bank = []

    def __init__(self, position: (float, float), node_id: int, is_faulty: bool = False, current_choice: bool = False, memory: int = [], node: Label = None, trust_level: float = 1.0):
        self.position = position
        self.node_id = node_id
        self.is_faulty = is_faulty
        self.current_choice = current_choice
        self.memory = memory
        self.node = node
        self.trust_level = trust_level
        
    def __str__(self):
        return "Node id: " + str(self.node_id) + "\nIs Faulty: " + str(self.is_faulty) + "\nCurrent Choice: " + str(self.current_choice) + "\nMemory: " + str(self.memory)
   
    def set_trust_level(self, level):
        self.trust_level = level

    def get_trust_level(self):
        return self.trust_level

    def get_node(self):
        return self.node

    def get_memory(self):
        return self.memory

    def get_node_id(self):
        return self.node_id

    def get_is_faulty(self):
        return self.is_faulty

    def get_current_choice(self):
        return self.current_choice
    
    def get_current_choice_sim(self): # if faulty, return opposite
        if self.is_faulty:
            return not self.current_choice
        else:
            return self.current_choice

    def set_memory(self, memory):
        self.memory = memory

    def set_nodeID(self, nodeID):
        self.nodeID = nodeID

    def set_node(self, node):
        self.node = node

    def set_is_faulty(self, is_faulty):
        self.is_faulty = is_faulty

    def set_current_choice(self, current_choice):
        self.current_choice = current_choice

    def add_memory(self, command):
        if not isinstance(command, tuple):
            command = (command, 1.0)
        self.memory.append(command)
    def clear_memory(self):
        self.memory = []
    '''
    def choose_majority(self):
        if self.memory.count(True) > self.memory.count(False):
            self.current_choice = True
        else:
            self.current_choice = False
    '''
    def choose_majority(self):
        true_count = sum(1 for op, _ in self.memory if op)
        false_count = len(self.memory) - true_count
        self.current_choice = true_count > false_count

    def choose_majority_with_tie_breaker(self, king_opinion, condition):
        if self.memory.count(True) > self.memory.count(False):
            self.current_choice = True
        elif self.memory.count(True) < self.memory.count(False):
            self.current_choice = False
        else:
            self.current_choice = king_opinion
        if self.memory.count(True) + self.memory.count(False) < condition:
            self.current_choice = king_opinion
   
    def choose_majority_weighted(self):
        opinion_weight = 0

        for opinion, trust in self.memory:
            if opinion:
                opinion_weight += trust
            else:
                opinion_weight -= trust
        self.current_choice = opinion_weight > 0

    def copy(self):
        return Vertex(self.position, self.node_id, self.is_faulty, self.current_choice, self.memory, self.node)
