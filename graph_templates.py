import numpy as np

graphs = {
  'K2': np.array([[50, 50], [250, 250]]),
  'K3': np.array([[150, 50], [50, 250], [250, 250]]),
  'K4': np.array([[50, 50], [50, 250], [250, 250], [250, 50]]),
  'K5': np.array([[150, 50], [260, 120], [230, 250], [70, 250], [40, 120]]),
  'K6': np.array([[100, 50], [100, 250], [200, 250], [200, 50], [260, 150], [40, 150]]),
  'K7': np.array([[200, 50], [260, 120], [230, 200], [150, 250], [70, 200], [40, 120], [100, 50]]),
  'K8': np.array([[105, 50], [50,105], [50, 195], [105, 250], [250, 195], [195, 250], [195, 50], [250, 105]]),
  'K3,3': np.array([[[50, 50], [50, 175], [50, 300]], [[250, 50], [250, 175], [250, 300]]]),
  'K5,5': np.array([[[50, 50], [50, 175], [50, 300], [50, 425], [50, 550]], [[250, 50], [250, 175], [250, 300], [250, 425], [250, 550]]]),
  'K3,5': np.array([[[50, 50], [50, 300], [50, 550], [-1, -1], [-1, -1]], [[250, 50], [250, 175], [250, 300], [250, 425], [250, 550]]]),
  'Planes': np.array([[[50, 50], [300, 50], [500, 50],[600, 50], [650, 50]], [[100, 450], [225, 450], [350, 450], [440, 450], [-1, -1]]]),
  'Journalist': np.array([[300, 300]] + [[300 + 250 * np.cos(2*np.pi*i/5), 300 + 250 * np.sin(2*np.pi*i/5)] for i in range(5)]),
  'Pairwise Comparison': np.array([[300 + 250 * np.cos(2*np.pi*i/7), 300 + 250 * np.sin(2*np.pi*i/7)] for i in range(7)]),
}

def generate_positions(graph, scale: (float, float)): # type: ignore arg type
  #TODO brać pod uwagę window width i height i alutomatycznie skalować i centrować
  positions = graphs[graph].copy().astype('float64')
  max_x, max_y = 0, 0
  if positions.ndim == 2:
    for vertex in positions:
      if vertex[0] > max_x:
        max_x = vertex[0]
      if vertex[1] > max_y:
        max_y = vertex[1]
  elif positions.ndim == 3:
    for v0 in positions:
      for vertex in v0:
        if vertex[0] > max_x:
          max_x = vertex[0]
        if vertex[1] > max_y:
          max_y = vertex[1]

  width, height = scale
  scale_x = (width - 75)/max_x
  scale_y = (height - 75)/max_y

  positions *= min(scale_x, scale_y)
  positions = positions.astype('int32')
  '''
  for i in range(len(positions)):
    
    if type(positions[i]) == list:
      for j in range(len(positions[i])):
        positions[i][j] *= scale
    else:
      positions[i][0] *= scale
      positions[i][1] *= scale
    '''
  return positions
