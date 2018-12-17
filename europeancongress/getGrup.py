# coding=utf-8
from __future__ import division
import sys
import json
from HTMLParser import HTMLParser
import os
import pickle
import math
import pickle
from dataProcessing import Voting
from dataProcessing import Voter
import operator
def main():
  #we first create the list of voters    
  listOfVoters = file("voters.txt",'r+')
  voters = dict()
  grupies = set()
  for line in listOfVoters:
    line = line.strip()
    line = line.split('\t')
    voterId = line[0]
    voterName = line[1]
    voters[voterName] = Voter(voterId,voterName)
  fileVot = file("data/voting-41.json")
  votingClass = json.loads(fileVot.read())
  votings = votingClass["all_votes"]
  for vote in votings:
    safeVoterName = vote["mep_name_name"].encode('utf', 'ignore')
    if safeVoterName in voters:
      voter = voters[safeVoterName]
      if voter.grup == "":
	grupName = vote["grup"]
	voter.grup = grupName
	grupies.add(grupName)
  
  comm = file("testPslPotts.comm","r")
  communities = dict()
  for line in comm:
    line = line.strip()
    line = line.strip("x")
    line = line.split(": ")
    communities[line[0]] = line[1]
  
#  reportFile = file("community_results/results_"+str(sys.argv[1]),"a")
  partyFile = file("political_parties.txt","w")
  for voter in voters:
#      if voters[voter].grup == grupieName and voters[voter].voterId in communities:
      partyFile.write("x"+voters[voter].voterId+": " + voters[voter].grup + "\n")

  #for grupieName in grupies:
  #  numberOfMembers = 0
  #  communitiesOfGrupie = dict()
  #  for voter in voters:
#      if voters[voter].grup == grupieName and voters[voter].voterId in communities:
#	partyFile.write("x"+voters[voter].voterId+": " + grupieName + "\n")
#	numberOfMembers += 1
	#print communities[voters[voter].voterId]
#	community = str(communities[voters[voter].voterId])
#	if community not in communitiesOfGrupie:
#	  communitiesOfGrupie[community]=0
#	communitiesOfGrupie[community]+=1
#    print grupieName
#    print numberOfMembers
#    reportFile.write(grupieName)
#    reportFile.write("\n")
    
#    for community in sorted(communitiesOfGrupie, key=communitiesOfGrupie.get, reverse=True):
#      reportFile.write(community + ": " + str(communitiesOfGrupie[community]/numberOfMembers)+"\n")
#    reportFile.write( "----------------\n")
      
if __name__ == "__main__":
    main()
