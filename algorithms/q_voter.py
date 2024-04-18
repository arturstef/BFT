from algorithms.operations_batch import OperationsBatch
import random
import math

class QVoterModel:
  def __init__(self, graph):
    self.graph = None
    self.selectedAgent = None
    self.algorithmPhase = "Send"
    self.probabilityType = "Linear" # funkcja probabilistyczna liniowa
    self.q = 0
    self.maxTime = 0
    self.time = 0
    self.isFinished = False
    self.raport = []
  
  def runAlgorithm(self, graph, time = 3, q = 2, probability = "Linear"):
    print("Running Q-Voter algorithm")
    startOperationBatch_log = OperationsBatch('log')
    startOperationBatch_log.add(f'Rozpoczęcie algorytmu QVoter, z parametrami time: {time}, q: {q}')
    self.raport.append(startOperationBatch_log)
    self.graph = graph
    self.maxTime = time
    self.q = q
    self.probabilityType = probability
    self.time = 0
    self.isFinished = False


    while not self.isFinished:
      print("Step " + str(self.time))
      self.step()
    
    print("Algorithm finished")
    return self.checkForConsensus()

  def step(self):
    if self.algorithmPhase == "Send":
      self.algorithmPhase = "Choose"
      return self.sendOpinions()
    elif self.algorithmPhase == "Choose":
      self.algorithmPhase = "Send"
      stepReport = self.makeDecision()
      self.time += 1
      self.checkIsFinished()
      return stepReport

  def sendOpinions(self):
    nextOperationsBatch_send = OperationsBatch('send')
    nextOperationsBatch_log = OperationsBatch('log')
    agentIndex = random.randint(0, len(self.graph.vertices) - 1)
    self.selectedAgent = self.graph.vertices[agentIndex]
    agentNeighbours = self.getNeighbours(self.selectedAgent)
    nextOperationsBatch_log.add(f'Agent {self.selectedAgent.node_id} został wybrany do otrzymania opinii od {len(agentNeighbours)} sąsiadów')
    for neighbour in agentNeighbours:
      opinion = neighbour.get_current_choice_sim() # if faulty, send opposite
      self.selectedAgent.add_memory(opinion)
      nextOperationsBatch_send.add(f'Sender;vertex:{neighbour.node_id},opinion:{opinion}')
      nextOperationsBatch_send.add(f'Send;{neighbour.node_id},{self.selectedAgent.node_id},opinion:{opinion}')
    self.raport.append(nextOperationsBatch_send)
    self.raport.append(nextOperationsBatch_log)


  def makeDecision(self):
    if self.shouldAcceptNeighboursOpinion() or self.neighborsConsensus():
      nextOperationsBatch_set_opinion = OperationsBatch('set_opinion')
      self.selectedAgent.choose_majority()
      nextOperationsBatch_set_opinion.add(f'Set_opinion;vertex:{self.selectedAgent.node_id},opinion:{self.selectedAgent.get_current_choice()}')
      self.raport.append(nextOperationsBatch_set_opinion)

    self.selectedAgent.clear_memory()

  def shouldAcceptNeighboursOpinion(self):
    return len(self.selectedAgent.get_memory()) <= 1 or self.checkProbability()

  def isFinished(self):
    return self.isFinished

  def getIsFinishedProperty(self):
    return self.isFinished

  def checkIsFinished(self):
    if self.time == self.maxTime:
      self.isFinished = True

  def getNeighbours(self, vertex):
    neigh = []
    for v_id in self.graph.get_node_neighbours(vertex.node_id):
      neigh.append(self.graph.get_node_by_id(v_id))
    selectedNeighbours = random.sample(neigh, self.q)
    return selectedNeighbours

  def neighborsConsensus(self):
    for opinion in self.selectedAgent.get_memory():
      if opinion != self.selectedAgent.get_current_choice():
        return False
    return True
  
  def checkProbability(self):
    return random.random() <= self.getProbability()

  def getProbability(self):
    if self.probabilityType == "Linear":
      return 0.5 + 0.5 * (self.time / self.maxTime) # modified to be in linear range [0.5, 1]
    elif self.probabilityType == "Boltzmann":
      return math.sqrt(self.time / self.maxTime)
    else:
      raise ValueError("Probability for " + self.probabilityType + " is not defined")
    
  def checkForConsensus(self):
    finalOpersBatch = OperationsBatch('log')
    for v in self.graph.vertices:
      if v.get_current_choice() != self.graph.vertices[0].get_current_choice():
        print("No consensus")
        finalOpersBatch.add(f'Konsensus nie osiągnięty')
        self.raport.append(finalOpersBatch)
        return False, self.raport
    print("Consensus")
    finalOpersBatch.add(f'Konsensus został osiągnięty, decyzja: {self.graph.vertices[0].get_current_choice()}')
    self.raport.append(finalOpersBatch)
    return True, self.raport
  
class QVoterStepReport:
  def __init__(self):
    self.roles = {}

  def fillRoles(self, agent, neighbours):
    for v in self.graph.vertices():
      if v == agent:
        self.roles[v] = "VOTER"
      elif neighbours is not None and v in neighbours:
        self.roles[v] = "NEIGHBOUR"
      else:
        self.roles[v] = "NONE"

  def getRoles(self):
    return self.roles