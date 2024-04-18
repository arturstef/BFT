class OperationsBatch:
  def __init__(self, title = ''):
    self.operations = []
    self.title = title

  def add(self, operation):
    self.operations.append(operation)

  def remove(self, operation):
    self.operations.remove(operation)
  
  def get_operations(self):
    return self.operations
  
  def get_title(self):
    return self.title
  
  def set_title(self, title):
    self.title = title
