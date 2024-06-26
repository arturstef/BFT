from algorithms.operations_batch import OperationsBatch
from graph import Graph
from vertex import Vertex
import random

class LamportIterAlgorithm:
  def __init__(self, graph):
        self.graph = graph
        self.stack = []
        self.isFinished = False
        self.verticesWithOpinion = []
        self.raport = []

  def runAlgorithm(self, graph, depth=1, failure_rate_func=None):
        self.graph = graph
        if failure_rate_func is None:
            failure_rate_func = lambda x: 0.05 
                
        iteration = 0
        current_failure_rate = failure_rate_func(iteration)
        self.apply_failures(current_failure_rate) 
        
        self.stack = []
        commander = self.graph.vertices[0]
        startOperationBatch = OperationsBatch('log')
        startOperationBatch.add(f'Start of Lamport algorithm, depth {depth}')
        self.raport.append(startOperationBatch)

        lieutenants = [self.graph.get_node_by_id(v_id) for v_id in self.graph.get_node_neighbours(commander.node_id)]
        if self.graph.vertices:
            self.stack.append(StackRecord(commander, [], lieutenants, depth, "SEND"))

        while not self.isFinished:
            iteration += 1
            current_failure_rate = failure_rate_func(iteration)
            print(f'iteration {iteration} failure_rate: {current_failure_rate}')
            vertex_faulty = 0
            for vertex in self.graph.vertices:
                if vertex.is_faulty: vertex_faulty += 1
            print(f'number of faulty nodes: {vertex_faulty}')
            self.apply_failures(current_failure_rate)
            self.om_iter()
            self.checkIsFinished()
        
        return self.checkForConsensus()

  def apply_failures(self, failure_rate):
        """Apply failures based on the current failure rate to each node."""
        for vertex in self.graph.vertices:
            if not vertex.is_faulty and random.random() < failure_rate:
                vertex.is_faulty = True

  def om_iter(self):
    record = self.stack.pop()
    firstOperationsBatch_log = OperationsBatch('log')
    if record.phase == "SEND":
      firstOperationsBatch_send = OperationsBatch('send')
      firstOperationsBatch_set_opinion = OperationsBatch('set_opinion')
      firstOperationsBatch_log.add(f'dowódca: {record.commander.node_id}, zastępcy: {[v.node_id for v in record.lieutenants]}, głębokość stosu: {record.m}')
      for vertex in record.lieutenants:
        commanderOpinion = record.commander.get_current_choice_sim() # if faulty, send opposite
        vertex.add_memory(commanderOpinion)
        firstOperationsBatch_send.add(f'Sender;vertex:{record.commander.node_id},opinion:{commanderOpinion}')
        firstOperationsBatch_send.add(f'Send;{record.commander.node_id},{vertex.node_id},opinion:{commanderOpinion}')
        if vertex not in self.verticesWithOpinion:
          vertex.set_current_choice(record.commander.get_current_choice_sim()) # if faulty, send opposite
          self.verticesWithOpinion.append(vertex)
          firstOperationsBatch_set_opinion.add(f'Set_opinion;vertex:{vertex.node_id},opinion:{vertex.get_current_choice()}')

      if record.m > 0:
        record.previous_commanders.append(record.commander)
        self.stack.append(StackRecord(record.commander, record.previous_commanders.copy(), record.lieutenants, record.m, "CHOOSE"))

        for vertex in record.lieutenants:
          lieutenants = self.getLieutenants(vertex, record.previous_commanders)
          if lieutenants:
            self.stack.append(StackRecord(vertex, record.previous_commanders.copy(), lieutenants, record.m - 1, "SEND"))
      self.raport.append(firstOperationsBatch_send)
      self.raport.append(firstOperationsBatch_set_opinion)

    elif record.phase == "CHOOSE":
      firstOperationsBatch_set_opinion = OperationsBatch('set_opinion')
      for vertex in record.lieutenants:
        vertex.choose_majority()
        firstOperationsBatch_set_opinion.add(f'Set_opinion;vertex:{vertex.node_id},opinion:{vertex.get_current_choice()}')
      self.raport.append(firstOperationsBatch_set_opinion)
    
    self.raport.append(firstOperationsBatch_log)
    self.checkIsFinished()

  def getLieutenants(self, vertex, commanders):
    lieutenants = []
    for v_id in self.graph.get_node_neighbours(vertex.node_id):
      v = self.graph.get_node_by_id(v_id)
      if v not in commanders:
        lieutenants.append(v)
    return lieutenants 

  def step(self):
    if self.stack:
      self.om_iter()
      self.checkIsFinished()

  def isFinished(self):
    return self.checkIsFinished()

  def getIsFinishedProperty(self):
    return self.isFinished

  def checkIsFinished(self):
    if not self.stack:
      self.isFinished = True
      
  def checkForConsensus(self):
    finalOpersBatch = OperationsBatch('log')
    opinions = []
    for vertex in self.graph.vertices:
      opinions.append(vertex.get_current_choice()) # real opinion
    first_opinion = opinions[0]
    if all(opinion == first_opinion for opinion in opinions):
      print("Consensus")
      finalOpersBatch.add(f'Konsensus został osiągnięty, decyzja {first_opinion}')
      self.raport.append(finalOpersBatch)
      return True, self.raport
    else:
      print("No consensus")
      finalOpersBatch.add(f'Konsensus nie został osiągnięty')
      self.raport.append(finalOpersBatch)
      return False, self.raport
    

class StackRecord:
  def __init__(self, commander, previous_commanders, lieutenants, m, phase):
    self.commander = commander
    self.previous_commanders = previous_commanders
    self.lieutenants = lieutenants
    self.m = m
    self.phase = phase
