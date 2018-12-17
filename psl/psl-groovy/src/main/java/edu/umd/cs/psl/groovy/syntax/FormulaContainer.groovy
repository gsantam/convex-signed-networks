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
package edu.umd.cs.psl.groovy.syntax;

import edu.umd.cs.psl.model.formula.*;
import edu.umd.cs.psl.model.atom.Atom;

class FormulaContainer {
	
	private final Formula formula;
	
	FormulaContainer(Formula f) {
		formula = f;
	}
	
	public Formula getFormula() {
		return formula;
	}
	
	private void checkFormula(Object f) {
		if (!(f instanceof FormulaContainer)) throw new IllegalArgumentException("Expected formula but got : ${f}");
	}
	
	private void checkAtom(Object f) {
		if (!(f instanceof FormulaContainer)) throw new IllegalArgumentException("Expected formula but got : ${f}");
		if (!(f.formula instanceof Atom)) throw new IllegalArgumentException("Expected atom but got : ${f.formula}");
	}
	
	private void checkAvgConjunction(Object f) {
		if (!(f instanceof FormulaContainer)) throw new IllegalArgumentException("Expected formula but got : ${f}");
		boolean isOtherAC = f.formula instanceof AvgConjunction;
		boolean isOtherAtom = f.formula instanceof Atom;
		boolean isOtherNegatedAtom = false;
		if (f.formula instanceof Negation && f.formula.getFormula() instanceof Atom) { 
			isOtherNegatedAtom = true;
		}
		boolean isAC = formula instanceof AvgConjunction;
		boolean isAtom = formula instanceof Atom;
		boolean isNegatedAtom = false;
		if (formula instanceof Negation && formula.getFormula() instanceof Atom) {
			isNegatedAtom = true;
		}
		if (!(isAC || isAtom || isNegatedAtom)) throw new IllegalArgumentException("For an average conjunction, the formula must be an average conjunction or a literal, but instead got : ${f.formula}");
		if (!(isOtherAC || isOtherAtom || isOtherNegatedAtom)) throw new IllegalArgumentException("For an average conjunction, expected another average conjunction or a literal, but instead got : ${f.formula}");
	}
	
	def and(f2) {
		checkFormula(f2);
		return new FormulaContainer(new Conjunction(formula,f2.formula));
	}
	
	def or(f2) {
		checkFormula(f2);
		return new FormulaContainer(new Disjunction(formula,f2.formula));
	}
	
	def rightShift(FormulaContainer f2) {
		then(f2);
	}
	
	def leftShift(f2) {
		checkFormula(f2);
		return new FormulaContainer(new Rule(f2.formula,formula));
	}
	
	def then(f2) {
		checkFormula(f2);
		return new FormulaContainer(new Rule(formula,f2.formula));
	}
	
	def bitwiseNegate() {
		return new FormulaContainer(new Negation(formula));
	}
	
	def xor(f2) {
		//Average conjunction operator
		checkAvgConjunction(f2);
		return new FormulaContainer(new AvgConjunction(formula,f2.formula));
	}
	
}
