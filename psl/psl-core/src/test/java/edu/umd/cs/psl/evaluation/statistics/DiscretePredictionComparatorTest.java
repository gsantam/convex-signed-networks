/*
 * This file is part of the PSL software.
 * Copyright 2011-2015 University of Maryland
 * Copyright 2013-2015 The Regents of the University of California
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package edu.umd.cs.psl.evaluation.statistics;

import static org.junit.Assert.assertEquals;

import java.util.HashSet;
import java.util.Set;

import org.junit.Before;
import org.junit.Test;

import edu.umd.cs.psl.config.EmptyBundle;
import edu.umd.cs.psl.database.DataStore;
import edu.umd.cs.psl.database.Database;
import edu.umd.cs.psl.database.Partition;
import edu.umd.cs.psl.database.rdbms.RDBMSDataStore;
import edu.umd.cs.psl.database.rdbms.driver.H2DatabaseDriver;
import edu.umd.cs.psl.evaluation.statistics.DiscretePredictionStatistics.BinaryClass;
import edu.umd.cs.psl.model.argument.ArgumentType;
import edu.umd.cs.psl.model.argument.GroundTerm;
import edu.umd.cs.psl.model.atom.RandomVariableAtom;
import edu.umd.cs.psl.model.predicate.PredicateFactory;
import edu.umd.cs.psl.model.predicate.StandardPredicate;

public class DiscretePredictionComparatorTest {

	private StandardPredicate predicate;
	private DiscretePredictionComparator comparator;
	
	@Before
	public void setUp() throws Exception {
		// create a predicate
		PredicateFactory factory = PredicateFactory.getFactory();
		predicate = factory.createStandardPredicate(
				"DiscretePredictionComparatorTest_same"
				, new ArgumentType[]{ArgumentType.UniqueID, ArgumentType.UniqueID}
			);
		
		// Instantiate an in-memory database
		DataStore ds = new RDBMSDataStore(new H2DatabaseDriver(H2DatabaseDriver.Type.Memory, "./comparator", false), new EmptyBundle());
		ds.registerPredicate(predicate);
		Database results = ds.getDatabase(new Partition(1), new Partition(1));
		Database baseline = ds.getDatabase(new Partition(2), new Partition(2));
		
		// create some canned ground inference atoms
		GroundTerm[][] cannedTerms = new GroundTerm[5][];
		cannedTerms[0] = new GroundTerm[]{ ds.getUniqueID(1), ds.getUniqueID(2) };
		cannedTerms[1] = new GroundTerm[]{ ds.getUniqueID(2), ds.getUniqueID(1) };
		cannedTerms[2] = new GroundTerm[]{ ds.getUniqueID(3), ds.getUniqueID(4) };
		cannedTerms[3] = new GroundTerm[]{ ds.getUniqueID(5), ds.getUniqueID(6) };
		cannedTerms[4] = new GroundTerm[]{ ds.getUniqueID(6), ds.getUniqueID(5) };
		
		// Store this in the "results" database
		for (GroundTerm[] terms : cannedTerms) {
			RandomVariableAtom atom = (RandomVariableAtom) results.getAtom(predicate, terms);
			atom.setValue(0.8);
			results.commit(atom);
		}
		
		// create some ground truth atoms
		GroundTerm[][] baselineTerms = new GroundTerm[4][];
		baselineTerms[0] = new GroundTerm[]{ ds.getUniqueID(1), ds.getUniqueID(2) };
		baselineTerms[1] = new GroundTerm[]{ ds.getUniqueID(2), ds.getUniqueID(1) };
		baselineTerms[2] = new GroundTerm[]{ ds.getUniqueID(3), ds.getUniqueID(4) };
		baselineTerms[3] = new GroundTerm[]{ ds.getUniqueID(4), ds.getUniqueID(3) };
		
		// Store this in the "baseline" database
		for (GroundTerm[] terms : baselineTerms) {
			RandomVariableAtom atom = (RandomVariableAtom) baseline.getAtom(predicate, terms);
			atom.setValue(1.0);
			baseline.commit(atom);
		}
		baseline.close();
		Set<StandardPredicate> closed = new HashSet<StandardPredicate>();
		closed.add(predicate);
		baseline = ds.getDatabase(new Partition(0), closed, new Partition(2));
		
		comparator = new DiscretePredictionComparator(results);
		comparator.setBaseline(baseline);
	}

	@Test
	public void testPrecision() {
		for (double thresh = 0.1; thresh <= 1.0; thresh += 0.1) {
			comparator.setThreshold(thresh);
			DiscretePredictionStatistics comparison = comparator.compare(predicate, 6*5);
			double prec = comparison.getPrecision(BinaryClass.POSITIVE);
			if (thresh <= 0.8)
				assertEquals(0.6, prec, 1e-10);
			else
				assertEquals(1.0, prec, 1e-10);
		}
	}
	
	@Test
	public void testRecall() {
		for (double thresh = 0.1; thresh <= 1.0; thresh += 0.1) {
			comparator.setThreshold(thresh);
			DiscretePredictionStatistics comparison = comparator.compare(predicate, 6*5);
			double recall = comparison.getRecall(BinaryClass.POSITIVE);
			if (thresh <= 0.8)
				assertEquals(0.75, recall, 1e-10);
			else
				assertEquals(0.0, recall, 1e-10);
		}		
	}
	
	@Test
	public void testF1() {
		for (double thresh = 0.1; thresh <= 1.0; thresh += 0.1) {
			comparator.setThreshold(thresh);
			DiscretePredictionStatistics comparison = comparator.compare(predicate, 6*5);
			double f1 = comparison.getF1(BinaryClass.POSITIVE);
			if (thresh <= 0.8)
				assertEquals(2.0/3.0, f1, 1e-10);
			else
				assertEquals(0.0, f1, 1e-10);
		}		
	}
	
	@Test
	public void testAccuracy() {
		for (double thresh = 0.1; thresh <= 1.0; thresh += 0.1) {
			comparator.setThreshold(thresh);
			DiscretePredictionStatistics comparison = comparator.compare(predicate, 6*5);
			double acc = comparison.getAccuracy();
			if (thresh <= 0.8)
				assertEquals(0.9, acc, 1e-10);
			else
				assertEquals(26.0/30.0, acc, 1e-10);
		}		
	}
}
