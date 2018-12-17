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

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import edu.umd.cs.psl.database.Database;
import edu.umd.cs.psl.evaluation.statistics.filter.AtomFilter;
import edu.umd.cs.psl.model.atom.GroundAtom;
import edu.umd.cs.psl.model.predicate.Predicate;
import edu.umd.cs.psl.util.collection.HashList;
import edu.umd.cs.psl.util.database.Queries;

public class SimpleRankingComparator implements RankingComparator {

	private static final Logger log = LoggerFactory.getLogger(SimpleRankingComparator.class);
	
	private final Database result;
	private Database baseline;
	private AtomFilter resultFilter = AtomFilter.NoFilter;
	private RankingScore rankScore; 
	
	public SimpleRankingComparator(Database result) {
		this.result=result;
		baseline = null;
		resultFilter = AtomFilter.NoFilter;
		rankScore = null;
	}

	@Override
	public void setRankingScore(RankingScore score) {
		rankScore = score;
	}

	@Override
	public void setBaseline(Database db) {
		this.baseline = db;
	}

	@Override
	public void setResultFilter(AtomFilter af) {
		resultFilter = af;
	}
	
	@Override
	public double compare(Predicate p) {
		/* Result atoms */
		List<GroundAtom> resultAtoms = new ArrayList<GroundAtom>();
		Iterator<GroundAtom> itr = resultFilter.filter(Queries.getAllAtoms(result, p).iterator());
		while (itr.hasNext())
			resultAtoms.add(itr.next());
		Collections.sort(resultAtoms, new AtomComparator());

		log.debug("Collected and sorted result atoms. Size: {}", resultAtoms.size());
		
		/* Baseline atoms */
		List<GroundAtom> baselineAtoms = new ArrayList<GroundAtom>();
		itr = resultFilter.filter(Queries.getAllAtoms(baseline, p).iterator());
		while (itr.hasNext())
			baselineAtoms.add(itr.next());
		Collections.sort(baselineAtoms, new AtomComparator());
		
		log.debug("Collected and sorted base atoms. Size: {}", baselineAtoms.size());
		
		
		HashList<GroundAtom> baselineHashList = new HashList<GroundAtom>(baselineAtoms.size());
		for (GroundAtom atom : baselineAtoms)
			baselineHashList.add(atom);	
		HashList<GroundAtom> resultHashList = new HashList<GroundAtom>(resultAtoms.size());
		for (GroundAtom atom : resultAtoms)
			resultHashList.add(atom);	
		
		return rankScore.getScore(baselineHashList, resultHashList);
	}
	
	private class AtomComparator implements Comparator<GroundAtom> {
		@Override
		public int compare(GroundAtom a1, GroundAtom a2) {
			if (a1.getValue() > a2.getValue())
				return 1;
			else if (a1.getValue() == a2.getValue())
				return a1.toString().compareTo(a2.toString());
			else
				return -1;
		}
	}
	
}
