import pickle
from dataProcessing import Voting
from dataProcessing import Voter


with open('finalResults.txt','rb') as f:
  voters =  pickle.load(f)
 
voterPablo = voters["Marine LE PEN"]
for opinionName in voterPablo.voterOpinions:
  print str(opinionName) + ", " +  str(voterPablo.voterOpinions[opinionName])
