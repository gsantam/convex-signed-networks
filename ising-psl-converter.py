from collections import OrderedDict


def oneCommunityParser(pslTempFileName):
  pslCommunities = open(pslTempFileName, 'r+')
  confidenceCommA = dict()
  confidenceCommB = dict()
  for line in pslCommunities:
    line = line.strip("\n")
    line = line.strip(")")
    if line!="":
      property_id = line.split("\t")[0]
      prob = line.split("\t")[1]
      if (property_id.split("(")[0]=="CONFIDENCECOMMA"):
        confidenceCommA[int(property_id.split("(")[1].split(")")[0])] = prob
      else:
        confidenceCommB[int(property_id.split("(")[1].split(")")[0])] = prob
  return confidenceCommA,confidenceCommB

def twoCommunitiesParser(pslTempFileName):
  pslCommunities = open(pslTempFileName, 'r+')
  confidenceCommA = dict()
  confidenceCommB = dict()
  for line in pslCommunities:
    line = line.strip("\n")
    line = line.strip(")")
    if line!="":
      property_id = line.split("\t")[0]
      prob = line.split("\t")[1]
      if property_id.split(',')[1]==" '0')":
        confidenceCommA[int(property_id.split("(")[1].split(",")[0])] = prob
        confidenceCommB[int(property_id.split("(")[1].split(",")[0])] = str(1-float(prob))
      else:
        confidenceCommB[int(property_id.split("(")[1].split(",")[0])] = prob
        confidenceCommA[int(property_id.split("(")[1].split(",")[0])] = str(1-float(prob))
  return confidenceCommA,confidenceCommB
  

def convertFile(pslTempFileName,pslObjFileName,parseFunction):
  
  confidenceCommA,confidenceCommB = parseFunction(pslTempFileName)

  pslCommFile = open(pslObjFileName, 'w+')
  pslCommFile.truncate()
  fileContent = ""

  for key in sorted(confidenceCommA):
    if key in sorted(confidenceCommB):
      if float(confidenceCommA[key])>float(confidenceCommB[key]):
        fileContent += "x"+str(key)+": 0"
      else:
        fileContent += "x"+str(key)+": 1"
    else:
      if float(confidenceCommA[key])>=float(0.5):
        fileContent += "x"+str(key)+": 0"
      else:
        fileContent += "x"+str(key)+": 1"
    fileContent += "\n"
  pslCommFile.write(fileContent)

#convertFile("testPslTemp.comm","testPsl.comm",oneCommunityParser)
#convertFile("testTestPslTemp.comm","testTestPsl.comm",oneCommunityParser)
convertFile("psl/psl-example/data/testPslIsingTemp.comm","psl/psl-example/data/testPslIsing.comm",oneCommunityParser)

