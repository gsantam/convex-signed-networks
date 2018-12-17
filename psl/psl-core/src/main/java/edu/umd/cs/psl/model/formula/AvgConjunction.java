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
package edu.umd.cs.psl.model.formula;

import java.util.ArrayList;

/**
 * An averaging conjunction formula.
 * 
 * @author Jimmy Foulds <jfoulds@ucsc.edu>
 */
public class AvgConjunction extends AbstractBranchFormula {

	public AvgConjunction(Formula... f) {
		super(f);
	}
	
	@Override
	public Formula getDNF() {
		//DNF doesn't make sense for AvgConjunctions, which are not logical operations.
		//We don't want to decompose it any further.
		return this; 
	}
	
	/**
	 * Collapses nested AvgConjunctions.
	 * <p>
	 * Stops descending where ever a Formula other than an AvgConjunction is.
	 * 
	 * @return the flattened AvgConjunction
	 */
	public AvgConjunction flatten() {
		ArrayList<Formula> avgconj = new ArrayList<Formula>(getNoFormulas());
		for (Formula f : formulas) {
			if (f instanceof AvgConjunction) {
				Formula[] newFormulas = ((AvgConjunction) f).flatten().formulas;
				for (Formula newF : newFormulas)
					avgconj.add(newF);
			}
			else
				avgconj.add(f);
		}
		return new AvgConjunction((Formula[]) avgconj.toArray(new Formula[avgconj.size()]));
	}

	@Override
	protected String separatorString() {
		return "^";
	}

}
