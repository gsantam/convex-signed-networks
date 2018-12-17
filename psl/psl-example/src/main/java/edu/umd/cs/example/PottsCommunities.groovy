package edu.umd.cs.example;

import edu.umd.cs.psl.application.inference.LazyMPEInference;
import edu.umd.cs.psl.application.learning.weight.maxlikelihood.LazyMaxLikelihoodMPE;
import edu.umd.cs.psl.config.*
import edu.umd.cs.psl.database.DataStore
import edu.umd.cs.psl.database.Database;
import edu.umd.cs.psl.database.Partition;
import edu.umd.cs.psl.database.ReadOnlyDatabase;
import edu.umd.cs.psl.database.rdbms.RDBMSDataStore
import edu.umd.cs.psl.database.rdbms.driver.H2DatabaseDriver
import edu.umd.cs.psl.database.rdbms.driver.H2DatabaseDriver.Type
import edu.umd.cs.psl.groovy.PSLModel;
import edu.umd.cs.psl.groovy.PredicateConstraint;
import edu.umd.cs.psl.groovy.SetComparison;
import edu.umd.cs.psl.model.argument.ArgumentType;
import edu.umd.cs.psl.model.argument.GroundTerm;
import edu.umd.cs.psl.model.atom.GroundAtom;
import edu.umd.cs.psl.model.function.ExternalFunction;
import edu.umd.cs.psl.ui.functions.textsimilarity.*
import edu.umd.cs.psl.ui.loading.InserterUtils;
import edu.umd.cs.psl.util.database.Queries;

/*
 * The first thing we need to do is initialize a ConfigBundle and a DataStore
 */

/*
 * A ConfigBundle is a set of key-value pairs containing configuration options. One place these
 * can be defined is in psl-example/src/main/resources/psl.properties
 */
ConfigManager cm = ConfigManager.getManager()
ConfigBundle config = cm.getBundle("test-example")

/* Uses H2 as a DataStore and stores it in a temp. directory by default */
def defaultPath = System.getProperty("java.io.tmpdir")

String dbpath = config.getString("dbpath", defaultPath + File.separator + "basic-example")
DataStore data = new RDBMSDataStore(new H2DatabaseDriver(Type.Disk, dbpath, true), config)

/*
 * Now we can initialize a PSLModel, which is the core component of PSL.
 * The first constructor argument is the context in which the PSLModel is defined.
 * The second argument is the DataStore we will be using.
 */
PSLModel m = new PSLModel(this, data)

/*
 * We create three predicates in the model, giving their names and list of argument types
 */

//Each community has an initial vertex
m.add predicate: "firstVertex" , types: [ArgumentType.UniqueID,ArgumentType.UniqueID]
//List of all networks vertices
m.add predicate: "vertex" , types: [ArgumentType.UniqueID]
//Ferromagnetic edges
m.add predicate: "edgeFerro" , types: [ArgumentType.UniqueID, ArgumentType.UniqueID]
//Antiferromagnetic edges
m.add predicate: "edgeAnti" , types: [ArgumentType.UniqueID, ArgumentType.UniqueID]
//The confidence of each vertex in each community
m.add predicate: "confidenceComm", types: [ArgumentType.UniqueID, ArgumentType.UniqueID]
//List of communities
m.add predicate: "community", types: [ArgumentType.UniqueID]


//Prior: the initial vertices belong to their respective communities
m.add rule : (   firstVertex(A,C) ) >>  confidenceComm(A,C) ,  weight :10000, squared : true

//Two vertices connected with an antiferromagnetic edge must belong to different communities
m.add rule : (   edgeAnti(A,B)  & confidenceComm(A,C)) >> ~confidenceComm(B,C),  weight : 1, squared : true
m.add rule : (   edgeAnti(A,B)  & community(C)  & ~confidenceComm(A,C) ) >> confidenceComm(B,C),  weight : 1, squared : true


//Two vertices connected with a ferromagnetic edge must belong to the same community
m.add rule : (   edgeFerro(A,B)  & confidenceComm(A,C)) >> confidenceComm(B,C),  weight : 1, squared : true
m.add rule : (   edgeFerro(A,B)  & community(C) & ~confidenceComm(A,C)) >> ~confidenceComm(B,C),  weight : 1, squared : true

//For each vertex, confidenceComm should be a probability distribution on the different communities
m.add PredicateConstraint.Functional , on : confidenceComm



println m;

/*
 * We now insert data into our DataStore. All data is stored in a partition.
 *
 * We can use insertion helpers for a specified predicate. Here we show how one can manually insert data
 * or use the insertion helpers to easily implement custom data loaders.
 */
def partition = new Partition(0);
def dir = 'data'+java.io.File.separator+'sn'+java.io.File.separator;
def insert = data.getInserter(vertex, partition);
InserterUtils.loadDelimitedData(insert, dir+"sn_vertices.txt");


insert = data.getInserter(firstVertex, partition)
InserterUtils.loadDelimitedData(insert, dir+"sn_first_vertex.txt");

insert = data.getInserter(edgeFerro, partition)
InserterUtils.loadDelimitedData(insert, dir+"sn_ferro_edges.txt");

insert = data.getInserter(edgeAnti, partition)
InserterUtils.loadDelimitedData(insert, dir+"sn_anti_edges.txt");

insert = data.getInserter(community, partition)
InserterUtils.loadDelimitedData(insert, dir+"sn_communities.txt");


Database db = data.getDatabase(partition, [FirstVertex,Vertex, EdgeFerro, EdgeAnti] as Set);
LazyMPEInference inferenceApp = new LazyMPEInference(m, db, config);
inferenceApp.mpeInference();

/*
 * Let's see the results
 */
String filename = "data/testPslPottsTemp.comm"
def inputFile = new File(filename)
def fileContent = ""

for (GroundAtom atom : Queries.getAllAtoms(db, ConfidenceComm)) {
	fileContent += atom.toString() + "\t" + atom.getValue() + "\n"
	//println atom.toString() + "\t" + atom.getValue();
}

inputFile.write(fileContent)



