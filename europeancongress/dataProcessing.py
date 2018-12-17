# coding=utf-8
from __future__ import division
import sys
import json
from HTMLParser import HTMLParser
import os
import pickle
import math

class Voting:
    def __init__(self,votingFileName,voters):
      votings = file("data/" + votingFileName,"r")
      self.votingText = votings.read()
      votings.close()
      self.votingId = self.getVotingId(votingFileName)
      self.voters = voters
      self.getVotingResult()
      
    def getVotingId(self,votingFileName):
      votingFileName = votingFileName.split('.')
      fileNameWithouExt = votingFileName[0]
      return int(fileNameWithouExt.split('-')[1])
    
    def getVotingResult(self):
      self.favour = 0
      self.against = 0
      self.abstain = 0
      votingClass = json.loads(self.votingText)
      votings = votingClass["all_votes"]
      for vote in votings:
	safeVoterName = vote["mep_name_name"].encode('utf', 'ignore')
	if safeVoterName in self.voters:
	  voter = self.voters[safeVoterName]
	  voteValue = vote["euro_vot_valoare_sign"]
	  if voteValue == '+':
	    self.favour += 1
	    #if the voting is positive:1 
	    voter.voteForVoting[self] = True
	  if voteValue == '-':
	    self.against += 1
	    #if the voting is negative:-1 
	    voter.voteForVoting[self] = False
	  if voteValue == '0': 
	    self.abstain += 1
      self.totalRealVotes = self.favour + self.against

	    
    def printVotingResult(self):
      self.getVotingResult()
      print "For: " + str(self.favour) + "\n"
      print  "Against: " + str(self.against) + "\n"
      print  "Abstains: " + str(self.abstain)+ "\n"
      
    def getBalanceBetweenFavAgainst(self):
      self.getVotingResult()
      if self.favour >= self.against:
	return float(self.favour)/float(self.against)
      else:
	return float(self.against)/float(self.favour)
      


#this is the class that defines a voter
class Voter:
    def __init__(self,voterId,voterName):
      self.voterId = voterId
      self.voterName = voterName
      self.initializeDictOfOpinions()
      self.grup = ""
      self.voteForVoting = dict()
      
    def initializeDictOfOpinions(self):
      self.voterOpinions = dict()
      listOfVoters = file("voters.txt",'r+')
      for line in listOfVoters:
	line = line.strip()
	line = line.split('\t')
	voterId = line[0]
	voterName = line[1]
	if voterId != self.voterId:
	  self.voterOpinions[voterName] = 0
	  
#this class defines a concrete processing for a set of votings
class VotingProcessing:
  #initialize the processing of the voting by specifying a file with
  #the voters we want to consider and a folder containing all the votings
  def __init__(self,votersFile,votingsFolder):
    #we first create the list of voters    
    listOfVoters = file(votersFile,'r+')
    self.voters = dict()
    for line in listOfVoters:
      line = line.strip()
      line = line.split('\t')
      voterId = line[0]
      voterName = line[1]
      self.voters[voterName] = Voter(voterId,voterName)
      print str(len(self.voters)) + " voters considered"
      #now we go through each voting file and analyze the result
      votingNumber = 0
      self.votings = list()
      for fileName in os.listdir(votingsFolder):
	votingNumber += 1
	voting = Voting(fileName,self.voters)
	self.votings.append(voting)
	print voting.votingId
      #finally we serialize the voting object
      with open("votings2.txt",'wb') as f:
	pickle.dump(self.votings,f)
	
  def entropyAffinityBetweenPairsWithThreshold(threshold):
    for voting in self.votings:
      print voting.votingId
      totalVotes = voting.favour + voting.against
      ratioAgainst = voting.favour/totalVotes
      ratioFavour = voting.against/totalVotes
      entropy = -ratioAgainst*math.log(ratioAgainst,10) - ratioFavour*math.log(ratioFavour,10)
      proportionOfVotes = totalVotes/733
      factor = entropy * proportionOfVotes
      for voterName1 in voters:
	voter1 = voters[voterName1]
	if voting in voter1.voteForVoting:
	  for voterName2 in voters:
	    voter2 = voters[voterName2]
	    if voter1 != voter2:
	      if voting in voter2.voteForVoting:
		v1 = voter1.voteForVoting[voting]
		v2 = voter2.voteForVoting[voting]
		if v1 and v2:
		  voter1.voterOpinions[voter2.voterName] += factor*ratioFavour
		elif not v1 and not v2:
		  voter1.voterOpinions[voter2.voterName] += factor*ratioAgainst
		else:
		  voter1.voterOpinions[voter2.voterName] -= factor*max(ratioAgainst, ratioFavour)

    sys.setrecursionlimit(10000)
    with open("finalResults2.txt",'wb') as f:
      pickle.dump(voters,f)
	  

if __name__ == "__main__":
    votingProcessing = VotingProcessing("voters.txt","data")
	
    
    
    
    
'''
members = dict()
numberVotings = 0
for fileName in os.listdir("data"):
  numberVotings+=1
  votings = file("data/" + fileName,"r")
  votingText = votings.read()
  votings.close()
  votingClass = json.loads(votingText)
  votings = votingClass["all_votes"]
  for vote in votings:
    safe_str = vote["mep_name_name"].encode('utf-8', 'ignore')
    
    if (safe_str not in members):
      members[safe_str]=1
    else:
      members[safe_str]+=1

print numberVotings
permanentMembers = dict()


for fileName in os.listdir("data"):
  numberVotings+=1
  votings = file("data/" + fileName,"r")
  votingText = votings.read()
  votings.close()
  votingClass = json.loads(votingText)
  votings = votingClass["all_votes"]
  for vote in votings:
    safe_str = vote["mep_name_name"].encode('utf-8', 'ignore')
    
    if (safe_str not in members):
      members[safe_str]=1
    else:
      members[safe_str]+=1
'''

	