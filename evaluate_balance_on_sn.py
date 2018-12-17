from __future__ import division
import subprocess
import pickle
from network_generator import *
import sys
import numpy as np
import pandas as pd
from os import path


def main():
        
        number_of_nodes = int(sys.argv[1])
        #the number of underlying communities of the synthetic networks 
        number_of_communities = int(sys.argv[2])

        #the maximum p_unbalance (about 0.45 is recommended)
        max_unbalance = float(sys.argv[3])
       
        
        firstVertexHeuristic=None
        if sys.argv[4]=="True":
                firstVertexHeuristic=True
        if sys.argv[4]=="False":
                firstVertexHeuristic=False
        if firstVertexHeuristic==None:
                raise Exception("The heuristic argument should be 'True' or 'False'")
                exit() 
                
        #whether to execute all solvers or just the hinge loss one
        allSolvers=None
        if sys.argv[5]=="True":
                allSolvers=True
        if sys.argv[5]=="False":
                allSolvers=False
        if allSolvers==None:
                raise Exception("The all solvers argument should be 'True' or 'False'")
                exit() 
                
        step = 0.025
        rep = int(max_unbalance/0.025)

        #data frames containing the results (columns=p_unbalance, rows=different experiments for the same unbalance)
        exactResults = pd.DataFrame()
        maxProdResults = pd.DataFrame()
        hingeResults = pd.DataFrame()

        for i in range(rep):
                unbalance = i*0.025+0
                print "unbalance: " + str(unbalance)

                #number of iterations of each experiment
                n_rep = 10

                exactResultsIt = np.ndarray(n_rep)
                maxProdResultsIt = np.ndarray(n_rep)
                hingeResultsIt = np.ndarray(n_rep)

                for j in range(n_rep):


                        print "it: " + str(j)
                        
                        #generates the synthetic network with the given p_unbalance and number of communities
                        network=generate_synthetic_network(number_of_nodes,number_of_communities,unbalance,firstVertexHeuristic)
                        #executes the solvers: exact, maxprod and hinge-loss
                        
                        if allSolvers:
                                p = subprocess.Popen(['sh', 'run.sh','true'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                out, err = p.communicate()

                                #check the performance of each method in terms of structural balance
                                #print err
                                #it may happend that the synthetic network is too big for the exact solver
                                try:
                                        exactResultsIt[j]=network.checkBalance("Exact.comm")
                                except IOError:
                                        exactResultsIt[j]=np.nan
                                        print "Skipping junction tree"
                                
                                maxProdResultsIt[j]=network.checkBalance("Aprox.comm")
                        else:
                                p = subprocess.Popen(['sh', 'run.sh','false'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                out, err = p.communicate()
                

                        hingeResultsIt[j]=network.checkBalance("psl/psl-example/data/testPslPotts.comm")
                
                if allSolvers:
                        exactResults = pd.concat([exactResults,pd.DataFrame(exactResultsIt,columns=[str(unbalance)])],axis=1)
                        maxProdResults = pd.concat([maxProdResults,pd.DataFrame(maxProdResultsIt,columns=[str(unbalance)])],axis=1)
                hingeResults = pd.concat([hingeResults,pd.DataFrame(hingeResultsIt,columns=[str(unbalance)])],axis=1)
        
        if allSolvers:
                exactResults.to_csv("results/exactResults_"+str(number_of_communities)+"_comm.csv",index=False)
                maxProdResults.to_csv("results/maxProdResults_"+str(number_of_communities)+"_comm.csv",index=False)
        hingeResults.to_csv("results/hingeResults_"+str(number_of_communities)+"_comm.csv",index=False)


if __name__=="__main__":
    main()