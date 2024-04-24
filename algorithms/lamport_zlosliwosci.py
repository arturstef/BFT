from algorithms.operations_batch import OperationsBatch
from algorithms.lamport_algorithm import LamportIterAlgorithm
from graph import Graph
from vertex import Vertex
import random

class LamportZlosliwosci(LamportIterAlgorithm):
    
      def __init__(self, graph):
          
          super().__init__(graph=graph)


      def runAlgorithm(self, graph, depth = 1,failure_rate_func=None):
          if not failure_rate_func is None:
              self.faliure_rate(graph=graph, depth = 1, failure_rate_func = failure_rate_func)

          else:
              super().runAlgorithm(graph = graph, depth = 1)



      def faliure_rate(self, graph, depth=1, failure_rate_func=None):
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
