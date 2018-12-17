import pickle
from dataProcessing import Voting
from dataProcessing import Voter


with open('finalResults.txt','rb') as f:
  voters =  pickle.load(f)

repeat = dict()
networkFile = file("network.net","w")
networkFileText = ""

for voter in voters:
 voterId = voters[voter].voterId
 for opinionName in voters[voter].voterOpinions:
    if voters[voter].voterOpinions[opinionName]>19:
      otherVoterId = voters[opinionName].voterId
      if not (otherVoterId,voterId) in repeat:
        networkFileText += str(voterId) + " " + str(otherVoterId) + "\t1\n"
        repeat[(voterId,otherVoterId)] = True
    if voters[voter].voterOpinions[opinionName]<-19:
      otherVoterId = voters[opinionName].voterId
      if not (otherVoterId,voterId) in repeat:
        networkFileText += str(voterId) + " " + str(otherVoterId) + "\t-1\n"
        repeat[(voterId,otherVoterId)] = True

networkFile.write(networkFileText)
networkFile.close()
