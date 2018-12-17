# coding=utf-8
import imp
from os import listdir
from os.path import isfile, join







def main():
  #util = imp.load_source('*', '/home/guillermo/Maestría/Tesis/evolving networks/util.py')  

  foo = imp.load_source('*', '/homedtic/gsantamaria/home/Tesis/evolving networks/network_generator.py')  

  fileName = "network.net"
  network = foo.Network("European")
  network.importFromTSVFile(fileName)
  print "The network has " + str(network.getNumberOfEdges()) + " edges"
  mainComponent = network.getCleanedLargestConnectedComponent()
  
  for node in mainComponent.nodes:
    if len(node.inEdges)+len(node.outEdges)==1:
      if len(node.inEdges)>0:
        if list(node.inEdges)[0].coupling == -1:
          print node.nodeId
      else:
         if list(node.outEdges)[0].coupling == -1:
           print node.nodeId

  print "The main component has " + str(mainComponent.getNumberOfEdges())+ " edges"
  print "The main component has " + str(len(mainComponent.nodes)) +" nodes"
  mainComponent.getNodeWithHighestDegree()
  mainComponent.getNodeWithHighestPositiveDegree()
  mainComponent.exportToPslProgram()
if __name__ == "__main__":
    main()
    
