from algorithms.operations_batch import OperationsBatch
from graph import Graph
from vertex import Vertex
#jeśli v.is_faulty, zwraca fałszywą opinie

class KingAlgorithm:
  def __init__(self, graph):
    self.phase = 0
    self.numberOfPhases = 0
    self.isFinished = False
    self.graph = graph
    self.raport = []

  def isFinished(self):
    return self.checkIsFinished()

  def getIsFinishedProperty(self):
    return self.isFinished

  def checkIsFinished(self):
    if self.phase == self.numberOfPhases:
      self.isFinished = True

  def firstRound(self):
    print("First round")
    self.cleanKnowledge()
    firstOperationsBatch_set_opinion = OperationsBatch('set_opinion')
    firstOperationsBatch_send = OperationsBatch('send')
    for v in self.graph.vertices:
      vOpinion = v.get_current_choice_sim()
      v.add_memory(vOpinion)
      firstOperationsBatch_send.add(f'Sender;vertex:{v.node_id},opinion:{v.get_current_choice()}')
      u_neighbours = self.graph.get_node_neighbours(v.node_id)
      for u_id in u_neighbours:
        u = self.graph.get_node_by_id(u_id)
        firstOperationsBatch_send.add(f'Send;{v.node_id},{u.node_id},opinion:{v.get_current_choice_sim()}') # if faulty, send opposite
        opinion = v.get_current_choice_sim()
        u.add_memory(opinion)
      
    self.raport.append(firstOperationsBatch_send)
    for v in self.graph.vertices:
      v.choose_majority()
      firstOperationsBatch_set_opinion.add(f'Set_opinion;vertex:{v.node_id},opinion:{v.get_current_choice()}')

    self.raport.append(firstOperationsBatch_set_opinion)

  def secondRound(self):
    print("Second round")
    king = self.graph.vertices[self.phase-1 % len(self.graph.vertices)]
    condition = len(self.graph.vertices) // 2 + self.allowedNumberOfTraitors()
    secondOperationBatch_log = OperationsBatch('log')
    secondOperationBatch_set_opinion = OperationsBatch('set_opinion')
    secondOperationBatch_log.add(f'runda: {self.phase + 1}, królem jest węzeł {king.node_id}')
    king_neighbours = self.graph.get_node_neighbours(king.node_id)
    for v_id in king_neighbours:
      v = self.graph.get_node_by_id(v_id)
      kingOpinion = king.get_current_choice_sim() # if faulty, send opposite
      v.choose_majority_with_tie_breaker(kingOpinion, condition)
      secondOperationBatch_set_opinion.add(f'Set_opinion;vertex:{v.node_id},opinion:{v.current_choice}')
    self.raport.append(secondOperationBatch_log)
    self.raport.append(secondOperationBatch_set_opinion)
   
  def cleanKnowledge(self):
    for vertex in self.graph.vertices:
      vertex.clear_memory()

  def allowedNumberOfTraitors(self):
    return int((len(self.graph.vertices) / 4.0) - 1)

  def checkForConsensus(self):
    opinions = []
    resultOperationsBatch = OperationsBatch('log')
    for vertex in self.graph.vertices:
      opinions.append(vertex.get_current_choice()) # real opinion
    first_opinion = opinions[0]
    if all(opinion == first_opinion for opinion in opinions):
      print("Consensus")
      resultOperationsBatch.add(f'Konsensus został osiągnięty, decyzja {first_opinion}')
      self.raport.append(resultOperationsBatch)
      return True, self.raport
    else:
      print("No consensus")
      resultOperationsBatch.add(f'Konsensus nie został osiągnięty')
      self.raport.append(resultOperationsBatch)
      return False, self.raport
      
  
  def runAlgorithm(self, graph, numberOfPhases):
    self.numberOfPhases = min(numberOfPhases, len(graph.vertices))
    self.graph = graph
    startOperationBatch = OperationsBatch('log')
    startOperationBatch.add(f'Rozpoczęcie algorytmu króla, {self.numberOfPhases} rund')
    self.raport.append(startOperationBatch)
    self.firstRound()
    self.secondRound()
    self.phase += 1
    while not self.isFinished:
      self.firstRound()
      self.secondRound()
      self.phase += 1
      self.checkIsFinished()
    print("Finished, now to check for consensus")
    result = self.checkForConsensus()
    return result