# coding=utf-8
from __future__ import division
import imp
import sys
from os import listdir
from os.path import isfile, join







def main():
  #util = imp.load_source('*', '/home/guillermo/Maestría/Tesis/evolving networks/util.py')  

  foo = imp.load_source('*', '/homedtic/gsantamaria/home/Tesis/evolving networks/network_generator.py')  

  fileName = "network.net"
  network = foo.Network("European Congress")
  network.importFromTSVFile(fileName)

  network.getNodeById(0)
  
 #  mainComponent = network.getCleanedLargestConnectedComponent()
  mainComponent = network


  mainComponent.importPslPottsNetwork("/homedtic/gsantamaria/home/Tesis/europeanCongress/community_results/psl_potts_6.comm")
  mainComponent.importGenericAttribute("political_parties.txt","political-parties")
  for node in mainComponent.nodes:
   if len(node.attributes)<1:
     print node.nodeId
  network.exportToGraphMlFile("gephi_network.graphml")
#  balancedEdges =  mainComponent.checkBalanceByAttribute("psl-potts")
#  reportFile = file("community_results/results_"+str(sys.argv[1]),"w")
#  parametersFile = file("comm_params.txt","r")
#  actualLine = parametersFile.readlines()[int(sys.argv[1])]
#  actualLine = actualLine.strip()
#  numberOfCommunities = actualLine.split("\t")[0]
#  firstVertices = actualLine.split("\t")[1]
'''
  reportFile.write("Number of stablished communties: " + numberOfCommunities+"\n")
  reportFile.write("First vertices: ")
  for vertex in firstVertices.split(" "):
    reportFile.write(" ")
    reportFile.write(str(vertex))
  reportFile.write("\n")
  reportFile.write("Number of balanced edges: " + str(balancedEdges)+"\n")
  reportFile.write("Number of unbalanced edges: " + str(mainComponent.getNumberOfEdges()-balancedEdges)+"\n")
  reportFile.write("Proportion of balanced edges: " + str(float(balancedEdges)/float(mainComponent.getNumberOfEdges()))+"\n")
  reportFile.write("Proportion of unbalanced edges: " + str(float(mainComponent.getNumberOfEdges()-balancedEdges)/float(mainComponent.getNumberOfEdges()))+"\n")
  reportFile.write("\n")
'''
if __name__ == "__main__":
    main()
    
