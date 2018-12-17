from __future__ import division
import pickle
from network_generator import *


def checkBalance(network,communityFileName):
  attrId = communityFileName
  attribute = NodeAttribute(attrId)
  communityFile = open(communityFileName, 'r')
  for line in communityFile:
    line.strip()
    line = line.split(':')
    if len(line)==2:
      nodeId = int(line[0].split('x')[1])
      community = int(line[1].strip())
      if not (type(community)==int):
	print("Wrong parse exception")
      else:
	node = network.getNodeById(nodeId)
	node.addAttribute(attribute,community)
  balancedEdges = network.checkBalanceByAttribute(attrId)
  print "Balanced edges of " + communityFileName + ": " + str(balancedEdges) 
  print "Proportion: " + str(float(balancedEdges)/float(network.getNumberOfEdges()))
  print "--------------------------"


def main():
  
  with open('test.network','rb') as f:
    network = pickle.load(f)
  network.getNodeWithHighestPositiveDegree()
  #checkBalance(network,"testExact.comm")
  #checkBalance(network,"testAprox.comm")
  checkBalance(network,"pottsPsl.comm")
  #checkBalance(network,"pottsPsl.comm")
  #checkBalance(network,"testTestPsl.comm")

if __name__ == "__main__":
    main()