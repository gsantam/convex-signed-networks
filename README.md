# Convex inference for community discovery in signed networks. 

This repository contains the necessary tools to reproduce the experiments of
the paper

* G. Santatmaría, V. Gómez (2015)
  Convex inference for community discovery in signed networks
  NIPS 2015 Workshop: Networks in the Social and Information Sciences

The method first maps the MAP problem on the Potts model as a hinge-loss
minimization problem (see the paper for details).  To run the code you need to
install psl (included here) and if you want to additionally compare with other
inference methods, such as max prod belief propagation or junction tree, you
need to install the libDAI library (also included here)

The directory europeanCongressData/ (~500 Mb) contains the votings of the EU
parlament, including 300 votings events from the actual term, from May 2014 to
June 2015, obtained from http://www.votewatch.eu/

- data/ 		: json files with the european votes
- network.net		: signed network built from the votes
- political_parties.txt	: "ground truth" party
- community_results/	: results for different number of communities and
			  initial vertices
- dataComputations.py	: used to build the signed network
- dataProcessing.py	: used to build the signed network

We would appreciate if you cite the paper after using the data or the code

## Dependencies

The code has been tested in Linux Mint 18.1 Serena and Ubuntu 14.04

- For PSL library, you need to have
	java 1.8
	you may need to export JAVA_HOME='/usr/lib/jvm/YOUR_JAVA_1.8_FOLDER'
	maven 3.x

- For libDAI you will need:
	make doxygen graphviz libboost-dev libboost-graph-dev
	libboost-program-options-dev libboost-test-dev libgmp-dev cimg-dev
	libgmp-dev

## Code to run the following experiments:

Compare the performance in terms of structural balance of max prod bp and our
method against an exact inference method (junction tree), with different number
of communities 

## Install 

To install the experiments you have to follow the next steps:

1 Build the libdai library by doing:
	make -B

on the folder (libdai)

2 Generate the class path of the groovy project:
	mvn clean install
	mvn dependency:build-classpath -Dmdep.outputFile=classpath.out

on the psl root folder (You need to have java 1.8 and maven 3.x installed)

3 Grant exec permissions to the run.sh script

## Options

The main python file to run the experiments is

evaluate_balance_on_sn.py.

It accepts the following parameters:

1 (Int) Nodes of the graph. In order to run the junction tree we recommend to
	set this paremeter to 150 or less
2 (Int) The number of underlying communities
3 (Float) The maximum amount of unbalance for the experiments. We recommend 0.45
4 (Bool) Whether to use an heuristic to find the initial node for each
	community or to use directly random nodes from the ground truth communities.
	This heuristic looks alternatively for the nodes with highest negative degree
	and highest positive degree.  For the case when the number of communities is
	equal to 2 (Ising Model), the heuristic is used by default.
	
4 (Bool) Whether to execute all solvers or only the Hinge-Loss one


An example of execution would be:

	python evaluate_balance_on_sn.py 120 3 0.45 True True
        
The results of the experiments are save in the folder results/

## Scripts

The main script of the hinge-loss method can be found in the folder
psl/psl-example/src/main/java/edu/umd/cs/example/PottsCommunities.groovy


Authors:

Guillermo Santamaria & Vicenc Gomez
Mar 5, 2017
-----------------------------------

For further questions, please contact vicen.gomez@upf.edu or santamaria.guille@gmail.com

