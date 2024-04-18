from algorithms.operations_batch import OperationsBatch
from graph import Graph
from vertex import Vertex

# https://medium.com/tronnetwork/an-introduction-to-pbft-consensus-algorithm-11cbd90aaec

class PbftAlgorithm:
  def __init__(self, graph):
    self.client = None
    self.results = []
    self.leader = None
    self.graph = graph
    self.raport = []
    self.phase = ""
    self.i = None

  def isFinished(self):
    return self.checkIsFinished()

  def getIsFinishedProperty(self):
    return self.isFinished

  def checkIsFinished(self): # WRONG
    print(f'results: {self.results}')
    if len(self.results) >= 3:
      return True



  def cleanKnowledge(self):
    for vertex in self.graph.vertices:
      vertex.clear_memory()

  def checkForConsensus(self):
    finalOpersBatch = OperationsBatch('log')
    opinions = []
    for result in self.results:
      opinions.append(result) # real opinion
    first_opinion = opinions[0]
    if all(opinion == first_opinion for opinion in opinions):
      print("Consensus")
      finalOpersBatch.add(f'Konsensus został osiągnięty, decyzja: {first_opinion}, opinie: {opinions}')
      self.raport.append(finalOpersBatch)
      return True, self.raport
    else:
      print("No consensus")
      finalOpersBatch.add(f'Konsensus nie został osiągnięty')
      self.raport.append(finalOpersBatch)
      return False, self.raport
      
  
  def runAlgorithm(self, graph, client_id):
    self.graph = graph
    self.client = self.graph.get_node_by_id(client_id)
    startOperationBatch = OperationsBatch('log')
    startOperationBatch.add(f'Rozpoczęcie algorytmu PBFT')

    self.client.clear_memory()

    neighbors_id = self.graph.get_node_neighbours(self.client.node_id)
    self.i = neighbors_id[0]
    self.raport.append(startOperationBatch)
    while True:
      iterOperationBatch = OperationsBatch('log')
      print(f'request')
      self.request()
      print(f'pre-prepare')
      self.prePrepare()
      print(f'prepare')
      self.prepare()
      print(f'commit')
      self.commit()
      print(f'reply')
      self.reply()
      print('client forms an opinion')
      self.client.choose_majority()
      self.results.append(self.client.get_current_choice())
      iterOperationBatch.add(f'Klient otrzymał opinie: {self.client.memory}, wybiera: {self.client.get_current_choice()}')
      self.raport.append(iterOperationBatch)
      self.client.clear_memory()
      print("Finished, now to check for consensus")
      if self.isFinished():
        result = self.checkForConsensus()
        return result
  
  def request(self):
    self.phase = "request"
    firstOperationsBatch_send = OperationsBatch('send')
    firstOperationsBatch_log = OperationsBatch('log')
    neighbors_id = self.graph.get_node_neighbours(self.client.node_id)
    self.leader = self.graph.get_node_by_id(neighbors_id[self.i - 1])
    client_opinion = self.client.get_current_choice_sim()
    firstOperationsBatch_send.add(f'Sender;vertex:{self.client.node_id},opinion:{self.client.get_current_choice()}')
    firstOperationsBatch_send.add(f'Send;{self.client.node_id},{self.i},opinion:{client_opinion}')
    self.leader.add_memory(client_opinion)
    print(f'i: {self.i}, leader: {self.leader.node_id}')
    firstOperationsBatch_log.add(f'Request: Klient wysyła prośbę do węzła: {self.leader.node_id}')

    self.raport.append(firstOperationsBatch_log)
    self.raport.append(firstOperationsBatch_send)

    self.i = (self.i + 1) % len(neighbors_id)


  def prePrepare(self):
    self.phase = "pre-prepare"
    secondOperationsBatch_send = OperationsBatch('send')
    secondOperationsBatch_log = OperationsBatch('log')
    neighbors_id = self.graph.get_node_neighbours(self.leader.node_id)
    leader_opinion = self.leader.get_current_choice_sim()
    secondOperationsBatch_send.add(f'Sender;vertex:{self.leader.node_id},opinion:{leader_opinion}')
    for neighbor_id in neighbors_id:
      if neighbor_id != self.client.node_id:
        secondOperationsBatch_send.add(f'Send;{self.leader.node_id},{neighbor_id},opinion:{leader_opinion}')
        self.graph.get_node_by_id(neighbor_id).add_memory(leader_opinion)

    secondOperationsBatch_log.add(f'Pre Prepare: Węzeł {self.leader.node_id} wysyła prośbę do reszty węzłów')
    self.raport.append(secondOperationsBatch_log)
    self.raport.append(secondOperationsBatch_send)

  def prepare(self):
    self.phase = "prepare"
    thirdOperationsBatch_send = OperationsBatch('send')
    thirdOperationsBatch_log = OperationsBatch('log')

    #every node except client and leader sends to every node except client
    neighbors_id = self.graph.get_node_neighbours(self.leader.node_id)
    for neighbor_id in neighbors_id:
      if neighbor_id != self.client.node_id:
        thirdOperationsBatch_send.add(f'Sender;vertex:{neighbor_id},opinion:{self.graph.get_node_by_id(neighbor_id).get_current_choice_sim()}')
        for neighbor_id2 in neighbors_id:
          if neighbor_id2 != self.client.node_id and neighbor_id2 != neighbor_id:
            thirdOperationsBatch_send.add(f'Send;{neighbor_id},{neighbor_id2},opinion:{self.graph.get_node_by_id(neighbor_id).get_current_choice_sim()}')
            self.graph.get_node_by_id(neighbor_id2).add_memory(self.graph.get_node_by_id(neighbor_id).get_current_choice_sim())
    
    thirdOperationsBatch_log.add(f'Prepare: Węzły wymieniają wstępną opinię')
    self.raport.append(thirdOperationsBatch_log)
    self.raport.append(thirdOperationsBatch_send)

  def commit(self):
    self.phase = "commit"
    fourthOperationsBatch_send = OperationsBatch('send')
    fourthOperationsBatch_set_opinion = OperationsBatch('set_opinion')
    fourthOperationsBatch_log = OperationsBatch('log')

    #every node except client first sets its opinion from the base, then sends it to every node except client
    neighbors_id = self.graph.get_node_neighbours(self.client.node_id)

    #setting opionion, and resetting the memory table
    for neighbor_id in neighbors_id:
      current_node = self.graph.get_node_by_id(neighbor_id)
      current_node.choose_majority()
      current_node.clear_memory()
      fourthOperationsBatch_set_opinion.add(f'Set_opinion;vertex:{neighbor_id},opinion:{current_node.get_current_choice()}')

    #sending opinion
    for neighbor_id in neighbors_id:
      if neighbor_id != self.client.node_id:
        fourthOperationsBatch_send.add(f'Sender;vertex:{neighbor_id},opinion:{self.graph.get_node_by_id(neighbor_id).get_current_choice_sim()}')
        for neighbor_id2 in neighbors_id:
          if neighbor_id2 != self.client.node_id and neighbor_id2 != neighbor_id:
            fourthOperationsBatch_send.add(f'Send;{neighbor_id},{neighbor_id2},opinion:{self.graph.get_node_by_id(neighbor_id).get_current_choice_sim()}')
            self.graph.get_node_by_id(neighbor_id2).add_memory(self.graph.get_node_by_id(neighbor_id).get_current_choice_sim())

    fourthOperationsBatch_log.add(f'Commit: Węzły wymieniają ostateczną opinię i podejmują decyzję')
    self.raport.append(fourthOperationsBatch_log)
    self.raport.append(fourthOperationsBatch_set_opinion)
    self.raport.append(fourthOperationsBatch_send)

  def reply(self):
    self.phase = "reply"
    fifthOperationsBatch_set_opinion = OperationsBatch('set_opinion')
    fifthOperationsBatch_send = OperationsBatch('send')
    fifthOperationsBatch_log = OperationsBatch('log')

    #every node except client first sets its opinion from the base, then sends it to client
    neighbors_id = self.graph.get_node_neighbours(self.client.node_id)

    #setting opionion, and resetting the memory table
    for neighbor_id in neighbors_id:
      current_node = self.graph.get_node_by_id(neighbor_id)
      current_node.choose_majority()
      current_node.clear_memory()
      fifthOperationsBatch_set_opinion.add(f'Set_opinion;vertex:{neighbor_id},opinion:{current_node.get_current_choice()}')
      
    #sending opinion to client
    for neighbor_id in neighbors_id:
      fifthOperationsBatch_send.add(f'Sender;vertex:{neighbor_id},opinion:{self.graph.get_node_by_id(neighbor_id).get_current_choice_sim()}')
      fifthOperationsBatch_send.add(f'Send;{neighbor_id},{self.client.node_id},opinion:{self.graph.get_node_by_id(neighbor_id).get_current_choice_sim()}')
      self.client.add_memory(self.graph.get_node_by_id(neighbor_id).get_current_choice_sim())
    
    fifthOperationsBatch_log.add(f'Reply: Węzły wysyłają ostateczną opinię do klienta, który wybiera większość i zapisuje')
    self.raport.append(fifthOperationsBatch_log)
    self.raport.append(fifthOperationsBatch_set_opinion)
    self.raport.append(fifthOperationsBatch_send)