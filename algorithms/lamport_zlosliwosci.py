from algorithms.operations_batch import OperationsBatch
from algorithms.lamport_algorithm import LamportIterAlgorithm
from graph import Graph
from vertex import Vertex
import random

class LamportZlosliwosci(LamportIterAlgorithm):
    
      def __init__(self, graph):
          
          super().__init__(graph=graph)