


def convertFile(pslTempFileName,pslObjFileName):
  communities = dict()
  pslCommunities = open(pslTempFileName, 'r+')
  for line in pslCommunities:
    line = line.strip("\n")
    line = line.strip(")")
    if line!="":
      property_id = line.split("\t")[0]
      prob = line.split("\t")[1]
      nodeId = int(property_id.split("(")[1].split(",")[0])
      community = int(property_id.split("(")[1].split(",")[1].strip(")"))      
      if nodeId in communities:
	if float(prob) > float(communities[nodeId][1]):
	   communities[nodeId] = (community,prob)
      else:
	communities[nodeId] = (community,prob)
  pslCommFile = open(pslObjFileName, 'w+')
  pslCommFile.truncate()
  fileContent = ""
  for key in sorted(communities):
    fileContent += "x"+str(key)+": " +  str(communities[key][0]) + "\n"
    
  pslCommFile.write(fileContent)


#convertFile("testPslTemp.comm","testPsl.comm")
convertFile("psl/psl-example/data/testPslPottsTemp.comm","psl/psl-example/data/testPslPotts.comm")
