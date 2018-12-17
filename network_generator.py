# coding=utf-8
from __future__ import division
import random
import numpy as np
import math
import pickle
import sys
from random import randint
from os import path
import operator
import copy

#this is a util class
class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

class Node:
  def __init__(self, nodeId):
    self.nodeId = nodeId
    self.outEdges = set()
    self.inEdges = set()
    self.alias = ""
    self.localField = 0
    self.isingCommunityId = 0
    #this dictionary stores custom attributes (the ising community id should be here)
    self.attributes = dict()
  
  def addInEdge(self,inEdge):
    self.inEdges.add(inEdge)
    
  def addOutEdge(self,outEdge):
    self.outEdges.add(outEdges)
    
  def pointsToNode(self,node):
    for edge in self.outEdges:
      if edge.nodeTo == node:
	return True
    return False
  
  def nodeIsPointingToMe(self,node):
    for edge in self.inEdges:
      if edge.nodeFrom == node:
	return True
    return False
  
  def setTentativeIsingCommunity(self,isingCommunityId):
    self.isingCommunityId = isingCommunityId
  
  def setLocalField(self,localField):
    self.localField = localField
    
  def getLocalField(self):
    return self.localField
  
  def addAttribute(self,attribute,value):
    self.attributes[attribute] = value
    
  def getAttributeValueById(self,attrId):
    for attribute in self.attributes:
      if str(attribute.attrId) == str(attrId):
	return self.attributes[attribute]
    return None
  
class NodeAttribute():
  
  def __init__(self, attrId):
    self.attrId = attrId
    
  def setDescription(self,description):
    self.description = description
    
  def setName(self,name):
    self.name = name
    
  def setType(self,attrType):
    self.attrType = attrType
   
class Edge:
  
  def __init__(self, nodeFrom, nodeTo):
    self.nodeFrom = nodeFrom
    self.nodeTo = nodeTo
    self.edgeId = "f"+str(self.nodeFrom.nodeId)+"t"+str(self.nodeTo.nodeId)
    nodeFrom.outEdges.add(self)
    nodeTo.inEdges.add(self)
  
  def setCoupling(self,coupling):
    self.coupling = coupling
    
  def getCoupling(self):
    return self.coupling
   
class Community(object):
  def __init__(self):
    self.inDegreeSequence = list()
    self.outDegreeSequence = list()
    self.containedComunities = list()
    self.nodes = set()
    self.edges = set()
    self.parentCommunity = None
    
  def getNumberOfEdges(self):
    numberOfEdges = 0
    for node in self.nodes:
      for edge in node.outEdges:
	numberOfEdges += 1
    return numberOfEdges
  
  def addContainedCommunity(self,community):
    community.parentCommunity = self
    self.containedComunities.append(community)
    
  def addContainedCommunities(self,numberOfCommunities):
    for i in range(numberOfCommunities):
      community = Community()
      self.addContainedCommunity(community)
    
  def addNode(self,node):
    self.nodes.add(node)
    if self.parentCommunity!=None:
      self.parentCommunity.addNode(node)
    
  def addNodeFromSequence(self):
    node = Node(self.getAndIncrementSequence())
    self.addNode(node)
    return node
  
  def addNodesFromSequence(self,numberOfNodes):
    nodes = set()
    for i in range(numberOfNodes):
      nodes.add(self.addNodeFromSequence())
    return nodes
      
  def getAndIncrementSequence(self):
    if self.parentCommunity == None:
      oldSequence = self.sequence
      self.sequence+=1
      return oldSequence
    else:
      return self.parentCommunity.getAndIncrementSequence()
  
  def findNodeByAlias(self,alias):
    for node in self.nodes:
      if node.alias == alias:
	return node
    return None 
  
  def getNodeByPrefAttachIn(self,offset):
    probability = (len(self.inDegreeSequence))/(len(self.inDegreeSequence)+len(self.nodes)*offset)
    a = np.random.binomial(1, probability, 1)
    if a==1:
      return random.choice(self.inDegreeSequence)
    else:
      return random.choice(list(self.nodes))
    
  def getNodeByPrefAttachOut(self,offset):
    probability = (len(self.outDegreeSequence))/(len(self.outDegreeSequence)+len(self.nodes)*offset)
    a = np.random.binomial(1, probability, 1)
    if a==1:
      return random.choice(self.outDegreeSequence)
    else:
      return random.choice(list(self.nodes))
  
  #this function looks for a node with the given id, if it does not exist, the method creats it
  def getOrCreateNodeById(self,nodeId):
    for node in self.nodes:
      if node.nodeId == nodeId:
	return node
    node = Node(nodeId)
    self.addNode(node)
    return node

  def getNodeWithHighestDegree(self):
    highestDegree = 0
    for node in self.nodes:
      if (len(node.outEdges)+len(node.inEdges))>highestDegree:
	highestDegree = len(node.outEdges)+len(node.inEdges)
	bestNode = node
    #print "Node with highest degree: " + str(bestNode.nodeId) +" with degree "+str(highestDegree)
    return bestNode

  def getNodeWithHighestNegativeDegree(self):
    highestNegativeDegree = 0
    for node in self.nodes:
      negativeEdges = 0
      for edge in node.outEdges:
	if (edge.coupling <0 ):
	  negativeEdges += 1
      for edge in node.inEdges:
	if (edge.coupling <0 ):	
	  negativeEdges += 1
      if (negativeEdges>highestNegativeDegree):
	highestNegativeDegree = negativeEdges
	bestNode = node
    #print "Node with highest degree: " + str(bestNode.nodeId) +" with negative degree "+str(highestNegativeDegree)  
    return bestNode

  def getNodeWithHighestPositiveDegree(self):
    highestPositiveDegree = 0
    for node in self.nodes:
      positiveEdges = 0
      for edge in node.outEdges:
        if (edge.coupling >0 ):
          positiveEdges += 1
      for edge in node.inEdges:
        if (edge.coupling >0 ):
          positiveEdges += 1
      if (positiveEdges>highestPositiveDegree):
        highestPositiveDegree = positiveEdges
        bestNode = node
    #print "Node with highest positive degree: " + str(bestNode.nodeId) +" with positive degree "+str(highestPositiveDegree)
    return bestNode

  def getListOfNodesByPositiveDegree(self):
    degreeByNode=dict()
    for node in self.nodes:
      positiveEdges = 0
      for edge in node.outEdges:
        if (edge.coupling >0 ):
          positiveEdges += 1
      for edge in node.inEdges:
        if (edge.coupling >0 ):
          positiveEdges += 1
      degreeByNode[node.nodeId]=positiveEdges
    degreeByNode=sorted(degreeByNode.items(),key=operator.itemgetter(1),reverse=True)
    return [item[0] for item in degreeByNode]


  def getListOfNodesByNegativeDegree(self):
    degreeByNode=dict()
    for node in self.nodes:
      positiveEdges = 0
      for edge in node.outEdges:
        if (edge.coupling <0 ):
          positiveEdges += 1
      for edge in node.inEdges:
        if (edge.coupling <0 ):
          positiveEdges += 1
      degreeByNode[node.nodeId]=positiveEdges
    degreeByNode=sorted(degreeByNode.items(),key=operator.itemgetter(1),reverse=True)
    return [item[0] for item in degreeByNode]




  def getNodeById(self,nodeId):
    for node in self.nodes:
      if int(node.nodeId) == int(nodeId):
	return node
    print("Any node with id: " + str(nodeId) + " was found")
    return None
  
  def getConnectedComponents(self):
    connectedComponents = list()
    nodesByComponent = [None]*140000
    actualConnectedComponent = -1
    totalNumberOfVertices = 0
    for node in self.nodes:
      if nodesByComponent[node.nodeId] == None:
	numberOfNodes = 0
	actualConnectedComponent += 1
	component = Network(self.networkName+"_C"+str(actualConnectedComponent))
	stack = Stack()
	stack.push(node)
	while not stack.isEmpty():
	  actualNode = stack.pop()
	  if nodesByComponent[actualNode.nodeId]==None:
	    component.addNode(actualNode)
	    numberOfNodes += 1
	    nodesByComponent[actualNode.nodeId] = actualConnectedComponent
	    for edge in actualNode.outEdges:
	      if nodesByComponent[edge.nodeTo.nodeId]==None:
		stack.push(edge.nodeTo)
	    for edge in actualNode.inEdges:
	      if nodesByComponent[edge.nodeFrom.nodeId]==None:
		stack.push(edge.nodeFrom)
	connectedComponents.append(component)	
	totalNumberOfVertices += numberOfNodes
	#print "Connected component "+str(actualConnectedComponent)+" has " + str(numberOfNodes)
		
    print "Number of connected components: " + str(actualConnectedComponent)
    print "Number of nodes: " + str(totalNumberOfVertices)
    return connectedComponents

  def removeLoops(self):
    numberOfLoops = 0
    for node in self.nodes:
      edgesToRemove = set()
      for edge in node.outEdges:
        if node == edge.nodeTo:
          numberOfLoops += 1
          edgesToRemove.add(edge)
      for edge in edgesToRemove:
        node.outEdges.remove(edge)
        node.inEdges.remove(edge)
    print str(numberOfLoops) + " loops removed"

  def removeIncompatibleEdges(self):
    incompatibleEdges = 0
    for node in self.nodes:
      edgesToRemove = set()
      for edge in node.outEdges:
        edges2ToRemove = set()
        for edge2 in edge.nodeTo.outEdges:
          if edge2.nodeTo == node and edge2.coupling*edge.coupling == -1:
            edges2ToRemove.add(edge2)
            edgesToRemove.add(edge)
        for edge2 in edges2ToRemove:
          node.inEdges.remove(edge2)
          edge.nodeTo.outEdges.remove(edge2)
          edge.nodeTo.inEdges.remove(edge)

      for edge in edgesToRemove:
        node.outEdges.remove(edge)
        incompatibleEdges += 1
    print str(incompatibleEdges) + " incompatible edges removed"

  def getLargestConnectedComponent(self):
    maxNumberOfNodes = 0
    for component in self.getConnectedComponents():
      if len(component.nodes) > maxNumberOfNodes:
        maxNumberOfNodes = len(component.nodes)
        mainComponent = component
    return mainComponent

  def getCleanedLargestConnectedComponent(self):
    mainComponent = self.getLargestConnectedComponent()
    mainComponent.removeIncompatibleEdges()
    mainComponent.removeLoops()
    return mainComponent



class Network(Community):
  def __init__(self, networkName):
    super(Network,self).__init__()
    self.networkName = networkName
    self.parentCommunity = None
    self.sequence = 0
    
  def parseAliasFile(self,aliasFileName):
    aliasById= dict()
    aliasFile = open(aliasFileName,'r+')
    aliasId = 1
    for line in aliasFile:
      line = line.strip()
      if not line.startswith('#') and line!='':
	aliasById[aliasId] = line
	aliasId+=1
    return aliasById
	
    
    
  def importFromMatlabFile(self,fileName,aliasFileName):
    matlabNetwork = open(fileName, 'r+')
    aliasById = self.parseAliasFile(aliasFileName)
    for line in matlabNetwork:
      if not line.startswith('#'):
	line = line.split(' ')
	if len(line)==3:
	  aliasNode1 = aliasById[int(line[0])]
	  aliasNode2 = aliasById[int(line[1])]
	  node1 = self.findNodeByAlias(aliasNode1)
	  node2 = self.findNodeByAlias(aliasNode2)
	  if node1 == None:
	    node1 = self.addNodeFromSequence()
	    node1.alias = aliasNode1
	  if node2 == None:
	    node2 = self.addNodeFromSequence()
	    node2.alias = aliasNode2
	  #we check if there exists an edge between e1 and e2 (only 1 is possible->undirected)
	  selectedEdge = None
	  for edge in node1.inEdges:
	    if edge.nodeFrom == node2:
	      selectedEdge = edge
	  for edge in node1.outEdges:
	    if edge.nodeTo == node2:
	      selectedEdge = edge
	  if selectedEdge == None:
	    edge = Edge(node1,node2)
	    edge.setCoupling(-int(line[2]))
	  else:
	    newCoupling = selectedEdge.getCoupling() - int(line[2])
	    selectedEdge.setCoupling(newCoupling)
	    
  def importFromTSVFile(self,fileName):
    TSVNetwork = open(fileName, 'r+')
    nodeList = [None]*140000
    for line in TSVNetwork:
      line = line.split('\t')
      edge = line[0]
      coupling = line[1]

      nodeFromId = int(edge.split(' ')[0])
      nodeFrom = nodeList[nodeFromId]
      if nodeFrom == None:
	nodeFrom = Node(nodeFromId)
	nodeList[nodeFromId] = nodeFrom
	
      nodeToId = int(edge.split(' ')[1])
      nodeTo = nodeList[nodeToId]
      if nodeTo == None:
	nodeTo = Node(nodeToId)
	nodeList[nodeToId] = nodeTo
  
      edge = Edge(nodeFrom,nodeTo)
      edge.setCoupling(int(coupling))
      
    for node in nodeList:
      if node != None:
	self.addNode(node)
	
  def importPslIsingNetwork(self,fileName):
    pslIsingNetwork = open(fileName, 'r+')
    pslIsingAttribute = NodeAttribute("psl-ising")
    for line in pslIsingNetwork:
      line.strip()
      line = line.split(':')
      if len(line)==2:
	nodeId = int(line[0].split('x')[1])
        tentativeCommunity = int(line[1].strip())
	if not (tentativeCommunity==0 or tentativeCommunity==1):
	  print("Wrong parse exception")
	else:
          if tentativeCommunity == 1:
	    community = 1
          if tentativeCommunity == 0:
            community = -1
	  node = self.getNodeById(nodeId)
	  node.addAttribute(pslIsingAttribute,community)
	  
  def checkBalanceByAttribute(self,attrId):
    balancedEdges = 0
    for node in self.nodes:
      for edge in node.outEdges:
	if (int(edge.nodeFrom.getAttributeValueById(attrId))==int(edge.nodeTo.getAttributeValueById(attrId))):
	  if (edge.coupling == 1):
	    balancedEdges += 1
	if (int(edge.nodeFrom.getAttributeValueById(attrId))!=int(edge.nodeTo.getAttributeValueById(attrId))):
	  if (edge.coupling == -1):
	    balancedEdges += 1
    #print balancedEdges
    #print float(balancedEdges)/float(self.getNumberOfEdges())
    return float(balancedEdges)/float(self.getNumberOfEdges())

  def checkBalance(self,communityFileName):
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
            raise Exception("Wrong parse exception")
          else:
            node = self.getNodeById(nodeId)
            node.addAttribute(attribute,community)
      return self.checkBalanceByAttribute(attrId)

  def checkPerfectlyBalancedNodesByAttribute(self,attrId):
    balancedNodes = 0
    for node in self.nodes:
      isBalanced = True
      for edge in node.outEdges:
	if (int(edge.nodeFrom.getAttributeValueById(attrId))*int(edge.nodeTo.getAttributeValueById(attrId))*edge.coupling)==-1:
	  isBalanced = False
      for edge in node.inEdges:
	if (int(edge.nodeFrom.getAttributeValueById(attrId))*int(edge.nodeTo.getAttributeValueById(attrId))*edge.coupling)==-1:
	  isBalanced = False	
      if isBalanced:
	balancedNodes += 1
    print balancedNodes
    print float(balancedNodes)/float(len(self.nodes))
    return balancedNodes
	
    
  def exportToGraphMlFile(self, fileName):
    graphMlFile = open(fileName, 'w+')
    graphMlFile.truncate()
    fileContent = ""
    fileContent += "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    fileContent += "<graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\" "
    fileContent += "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "
    fileContent += "xsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns "
    fileContent += "http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd\">\n"
    #Attributes section: the attributes Ising community and coupling are (now) always endabled
    #We declare them here
    fileContent += "<key id=\"iScomm\" for=\"node\" attr.name=\"Ising community\" attr.type=\"int\">\n"
    fileContent += "\t<default>0</default>\n"
    fileContent += "</key>\n"
    fileContent += "<key id=\"coup\" for=\"edge\" attr.name=\"Coupling\" attr.type=\"int\">\n"
    fileContent += "\t<default>0</default>\n"
    fileContent += "</key>\n"
    #we go through each node to get the different attributes
    attributes = set()
    for node in self.nodes:
      for attribute in node.attributes:
	attributes.add(attribute)
    #we declare the attributes
    for attribute in attributes:
      fileContent += "<key id=\""+str(attribute.attrId)+"\" for=\"node\" attr.name=\""+str(attribute.name)+"\" attr.type=\""+str(attribute.attrType)+"\">\n"
      fileContent += "\t<default>0</default>\n"
      fileContent += "</key>\n"      
    
    fileContent += "<graph id=\""+str(self.networkName)+"\" edgedefault=\"directed\">\n"
    for node in self.nodes:
      fileContent+="<node id=\""+str(node.nodeId)+"\">\n"
      if node.isingCommunityId==0:
	fileContent+="\t<data key=\"iScomm\">0</data>\n"
      else:
	fileContent+="\t<data key=\"iScomm\">1</data>\n"
      #and here the custom values
      for attribute in node.attributes:
	fileContent+="\t<data key=\""+str(attribute.attrId)+"\">"+str(node.attributes[attribute])+"</data>\n"
      fileContent += "</node>\n"
    for node in self.nodes:
      for edge in node.outEdges:
	fileContent+="<edge id=\""+str(edge.edgeId)+"\" source=\""+str(edge.nodeFrom.nodeId)+"\" target=\""+str(edge.nodeTo.nodeId)+"\">\n"
	fileContent+="\t<data key=\"coup\">"+str(edge.coupling)+"</data>\n"
	fileContent+="</edge>\n"
    fileContent += "</graph>\n"
    fileContent += "</graphml>\n"
    graphMlFile.write(fileContent)
    
    
  def exportToFactorGraphFileWithoutLocalField(self, fileName, betha, numberOfCommunities):
    factorGraphFile = open(fileName, 'w+')
    factorGraphFile.truncate()
    fileContent = ""
    #the number of factor corresponds to the number of edges (one factor for each pair of connected nodes)
    fileContent += str(self.getNumberOfEdges()) + "\n"
    fileContent += "\n"
    first = True
    for node in self.nodes:
      for edge in node.outEdges:
	if first:
	  first = False
	else:
	  fileContent += "\n"
	#number of variables in the factor
	fileContent += "2\n"
	#the ids of the variables in the factor
	fileContent += str(edge.nodeFrom.nodeId) +" " + str(edge.nodeTo.nodeId) +"\n"
	#the possible values of the variables above (we have as many as possible communities)
	fileContent += str(numberOfCommunities) + " " +str(numberOfCommunities) + "\n"
	pairAtractingProbability = math.exp(edge.coupling*betha)
	pairRepulsingProbability = math.exp((-1)*edge.coupling*betha)
	#the number of non zero entries
	fileContent += str(numberOfCommunities*numberOfCommunities) +"\n"
	for i in range(numberOfCommunities):
	  for j in range(numberOfCommunities):
	    valuePosition = str(i*numberOfCommunities +j)
	    if i==j:
	      fileContent += valuePosition+ " "+ str(pairAtractingProbability) + "\n"
	    else:
	      fileContent += valuePosition+ " "+ str(pairRepulsingProbability) + "\n"
    factorGraphFile.write(fileContent)
    
  def exportToFactorGraphFileWithLocalField(self, fileName, betha):
    factorGraphFile = open(fileName, 'r+')
    factorGraphFile.truncate()
    fileContent = ""
    #the number of factor corresponds to the number of edges (one factor for each pair of connected nodes) plus the number of nodes (one factor for each local field)
    fileContent += str(self.getNumberOfEdges()+len(self.nodes)) + "\n"
    fileContent += "\n"
    #first we do the factors for the coupling between nodes (one for each edge)
    for node in self.nodes:
      for edge in node.outEdges:
	#number of variables in the factor
	fileContent += "2\n"
	#the ids of the variables in the factor
	fileContent += str(edge.nodeFrom.nodeId) +" " + str(edge.nodeTo.nodeId) +"\n"
	#the possible values of the variables above (in principle we only have two that represent the two communities)
	fileContent += "2 2\n"
	pairAtractingProbability = math.exp(edge.coupling*betha)
	pairRepulsingProbability = math.exp((-1)*edge.coupling*betha)
	#the number of non zero entries
	fileContent += "4\n"
	#-1 -1 (0 0)
	fileContent += "0 "+ str(pairAtractingProbability) + "\n"
	#1 -1 (1 0)
	fileContent += "1 "+ str(pairRepulsingProbability) + "\n"
	#-1 1 (0 1)
	fileContent += "2 "+ str(pairRepulsingProbability) + "\n"
	#1 1 (1 1)
	fileContent += "3 "+ str(pairAtractingProbability) + "\n"
    first = True
    #now we do the factors for the local fields
    for node in self.nodes:
      if first:
	first = False
      else:
	fileContent += "\n"
      #number of variables in the factor
      fileContent += "1\n"
      #the ids of the variable in the factor
      fileContent += str(node.nodeId) +"\n"
      #the possible values of the variables above (in principle we only have two that represent the two communities)
      fileContent += "2\n"
      localFieldAtractingProbability = math.exp(node.localField*betha)
      localFieldRepulsingProbability = math.exp((-1)*node.localField*betha)
      #the number of non zero entries
      fileContent += "2\n"
      #-1 (0)
      fileContent += "0 "+ str(localFieldAtractingProbability) + "\n"
      #1 (1)
      fileContent += "1 "+ str(localFieldRepulsingProbability) + "\n"
    factorGraphFile.write(fileContent)

  
  def exportToPslProgram(self,pslDataDirectory,numberOfCommunities,firstVertexHeuristic):
    verticesFile = open(pslDataDirectory+"sn_vertices.txt", 'w+')
    verticesFile.truncate()
    fileContent = ""
    first = True
    for node in self.nodes:
      if first:
	first = False
      else:
	fileContent += "\n"
      fileContent += str(node.nodeId)
    verticesFile.write(fileContent)
    antiEdgesFile = open(pslDataDirectory+"sn_anti_edges.txt", 'w+')
    antiEdgesFile.truncate()
    antiEdgesFileContent = ""
    firstAntiEdges = True
    ferroEdgesFile = open(pslDataDirectory+"sn_ferro_edges.txt", 'w+')
    ferroEdgesFile.truncate()
    ferroEdgesFileContent = ""
    firstFerroEdges = True
    for node in self.nodes:
      for edge in node.outEdges:
	if (edge.coupling < 0):
	  if firstAntiEdges:
	    firstAntiEdges = False
	  else:
	    antiEdgesFileContent += "\n"
	  antiEdgesFileContent += str(edge.nodeFrom.nodeId) +"\t" + str(edge.nodeTo.nodeId)
	  antiEdgesFileContent += "\n"
	  antiEdgesFileContent += str(edge.nodeTo.nodeId) +"\t"+ str(edge.nodeFrom.nodeId)
	if (edge.coupling > 0):
	  if firstFerroEdges:
	    firstFerroEdges = False
	  else:
	    ferroEdgesFileContent += "\n"
	  ferroEdgesFileContent += str(edge.nodeFrom.nodeId) +"\t" + str(edge.nodeTo.nodeId)
	  ferroEdgesFileContent += "\n"
	  ferroEdgesFileContent +=  str(edge.nodeTo.nodeId) +"\t"+ str(edge.nodeFrom.nodeId)	  
    
    antiEdgesFile.write(antiEdgesFileContent)
    ferroEdgesFile.write(ferroEdgesFileContent)
    
    
    communities_file = file("psl/psl-example/data/sn/sn_communities.txt","w+")
    communities_file.truncate()
    
    for i in range(numberOfCommunities):
        communities_file.write(str(i)+"\n")
    communities_file.close()
    
    firstVertexFile = open("psl/psl-example/data/sn/sn_first_vertex.txt", 'w+')
    firstVertexFile.truncate()

    nodeWithHighestPoDegree = self.getNodeWithHighestPositiveDegree()
    negativeNodes = self.getListOfNodesByNegativeDegree()
    positiveNodes = self.getListOfNodesByPositiveDegree()

    if numberOfCommunities==2:
        firstVertexFile.write(str(nodeWithHighestPoDegree.nodeId)+"\t0\n")
    else:
        if firstVertexHeuristic:
                setOfNodes = set()
                parity = 1
                for idx,community in enumerate(self.containedComunities):
                        if parity == 1:
                                highestDegreeNodes = copy.copy(negativeNodes)
                        if parity == -1:
                                highestDegreeNodes = copy.copy(positiveNodes)
                        i =0
                        while highestDegreeNodes[i] in setOfNodes:
                                i+=1
                        firstVertexFile.write(str(highestDegreeNodes[i])+"\t"+str(idx)+"\n")
                        setOfNodes.add(highestDegreeNodes[i])
                        parity=parity*(-1)
        else:
                for idx,community in enumerate(self.containedComunities):
                        firstVertexFile.write(str(list(community.nodes)[0].nodeId)+"\t"+str(idx)+"\n")

                        
    firstVertexFile.close()
    
    
  
  def showNodeByCommunity(self, fileName):
    nodeByCommunity = open(fileName, 'r+')
    nodeByCommunity.truncate()
    fileContent = ""
    i = 0
    for community in self.containedComunities:
      for node in community.nodes:
	fileContent += str(node.nodeId) + " comm:"+str(i)+"\n"
      i+=1
    nodeByCommunity.write(fileContent)
    
  def serializeNetwork(self):
    with open(self.networkName + ".network",'wb') as f:
      pickle.dump(self,f)
  
	
      
class NetworkGeneration:
  def __init__(self,numberOfNodes, numberOfEdges, numberOfCommunities, crossingEdgesProportion, unbalancedEdgesProportion):
    self.numberOfNodes = numberOfNodes
    self.numberOfEdges = numberOfEdges
    self.numberOfCommunities = numberOfCommunities
    self.crossingEdgesProportion = crossingEdgesProportion
    self.unbalancedEdgesProportion = unbalancedEdgesProportion
    self.landhaIn = 0.75
    self.landaOut = 3.55
    self.network = Network("test")
    self.network.addContainedCommunities(numberOfCommunities)
    
  def addEdgePrefAttachmentt(self,communityOut,communityIn):
    inNode = None
    outNode = None
    while inNode==outNode or outNode.pointsToNode(inNode) == True or inNode.pointsToNode(outNode) == True:
      outNode = communityOut.getNodeByPrefAttachOut(self.landaOut)
      inNode = communityIn.getNodeByPrefAttachIn(self.landhaIn)
    edge = Edge(outNode,inNode)
    communityIn.inDegreeSequence.append(inNode)
    communityOut.outDegreeSequence.append(outNode)
    return edge

  def posibleToAddEdgePrefAttachmentt(self,communityOut,communityIn):
    inNode = None
    outNode = None
    i = 0
    while (inNode==outNode or outNode.pointsToNode(inNode) == True or inNode.pointsToNode(outNode) == True) and i<500:
      outNode = communityOut.getNodeByPrefAttachOut(self.landaOut)
      inNode = communityIn.getNodeByPrefAttachIn(self.landhaIn)
      i+=1
    if i<500:
      return True
    else:
      return False
    
  def addEdgePrefAttachmentFromNode(self,outNode,communityOut,communityIn):
    inNode = outNode
    while inNode==outNode or outNode.pointsToNode(inNode)== True or inNode.pointsToNode(outNode)  == True:
      inNode = communityIn.getNodeByPrefAttachIn(self.landhaIn)
    edge = Edge(outNode,inNode)
    communityIn.inDegreeSequence.append(inNode)
    communityOut.outDegreeSequence.append(outNode)
    return edge
  
  def generateNetworkUniqueComp(self):
    commAttribute = NodeAttribute("comm")
    commAttribute.setName("Structural community")
    commAttribute.setType("int")
    
    #we add some initial nodes to each community to guarantee it's possible to attach edges 
    for community in self.network.containedComunities:
      nodes = community.addNodesFromSequence(3)
    for i in range(self.numberOfCommunities):
      for node in self.network.containedComunities[i].nodes:
	node.addAttribute(commAttribute,i)
    self.numberOfNodes -= 3*self.numberOfCommunities
    self.probNewNode=self.numberOfNodes/self.numberOfEdges

    for i in range(self.numberOfEdges):
      #print i
      selectedCommunityNumber = randint(0,self.numberOfCommunities-1)
      otherCommunityNumber = selectedCommunityNumber
      while otherCommunityNumber == selectedCommunityNumber:
	otherCommunityNumber = randint(0,self.numberOfCommunities-1)
      
      selectedCommunity = self.network.containedComunities[selectedCommunityNumber]
      otherCommunity = self.network.containedComunities[otherCommunityNumber]

      newNode = np.random.binomial(1, self.probNewNode, 1)
      crossingEdge = np.random.binomial(1, self.crossingEdgesProportion, 1)
      unbalancedEdge = np.random.binomial(1, self.unbalancedEdgesProportion, 1)
      edge = None
      if crossingEdge == 0:
	edgePossible = self.posibleToAddEdgePrefAttachmentt(selectedCommunity,selectedCommunity)
      else:
	edgePossible = self.posibleToAddEdgePrefAttachmentt(selectedCommunity,otherCommunity)
      if newNode==1 or not edgePossible:
	node = selectedCommunity.addNodeFromSequence()
	node.addAttribute(commAttribute,selectedCommunityNumber)
	if crossingEdge == 0:
	  edge = self.addEdgePrefAttachmentFromNode(node,selectedCommunity,selectedCommunity)
	  edge.coupling = 1
	else:
	  edge = self.addEdgePrefAttachmentFromNode(node,selectedCommunity,otherCommunity)
	  edge.coupling = -1
      else:
	if crossingEdge == 0:
	  edge = self.addEdgePrefAttachmentt(selectedCommunity,selectedCommunity)
	  edge.coupling = 1
	else:
	  edge = self.addEdgePrefAttachmentt(selectedCommunity,otherCommunity)
	  edge.coupling = -1
      if unbalancedEdge==1:
	edge.coupling *= -1
    #join isolated nodes to the community  
    for community in self.network.containedComunities:
      for node in community.nodes:
	if len(node.outEdges) == 0 and len(node.inEdges) == 0:
	  edge = self.addEdgePrefAttachmentFromNode(node,community,community)
	  edge.coupling = 1
	unbalancedEdge = np.random.binomial(1, self.unbalancedEdgesProportion, 1)
	if unbalancedEdge==1:
	  edge.coupling*=-1
	  
    
def generate_synthetic_network(numberOfNodes,numberOfCommunities,unbalance,firstVertexHeuristic):
  #the number of nodes is aproximate and may vary depending on the unbalance of the graph and the number of communities
  numberOfEdges = int(numberOfNodes*2.5)
  crossingEdges=0.3
  networkGeneration = NetworkGeneration(numberOfNodes,numberOfEdges,numberOfCommunities,crossingEdges,unbalance)
  networkGeneration.generateNetworkUniqueComp()
  root_dir = path.dirname(path.abspath(__file__))
  graphName = "synthetic_"+str(numberOfCommunities)+"_comm_"+str(unbalance)
  networkGeneration.network.exportToFactorGraphFileWithoutLocalField(root_dir+"/libdai/examples/tesis/test.fg",4,numberOfCommunities)
  networkGeneration.network.exportToPslProgram(root_dir+"/psl/psl-example/data/sn/",numberOfCommunities,firstVertexHeuristic)
  sys.setrecursionlimit(1000000)
  #networkGeneration.network.serializeNetwork()
  return networkGeneration.network



if __name__ == "__main__":
  firstVertexHeuristic=None
  if sys.argv[4]=="True":
        firstVertexHeuristic=True
  if sys.argv[4]=="False":
        firstVertexHeuristic=False
  if firstVertexHeuristic==None:
        raise Exception("The heuristic argument should be 'True' or 'False'")
        exit()
  generate_synthetic_network(int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3]),firstVertexHeuristic)

    
   
  
