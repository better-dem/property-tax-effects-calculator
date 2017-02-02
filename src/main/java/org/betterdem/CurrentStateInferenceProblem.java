package org.betterdem;

import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.EncodingUtils;
import org.moeaframework.core.variable.RealVariable;
import org.moeaframework.problem.AbstractProblem;

/**
 * The first part of the property tax effects calculation is to determine the current state from incomplete information.
 */
public class CurrentStateInferenceProblem extends AbstractProblem {
    public CurrentStateInferenceProblem() {
        super(CurrentStateModel.population*CurrentStateModel.Household.NUM_HOUSEHOLD_FIELDS, CurrentStateModel.number_of_objectives);
    }

    @Override
    public void evaluate(Solution solution){
        double[] codedIndividual = EncodingUtils.getReal(solution);
        CurrentStateModel stateModel = CurrentStateModel.decodeFromIndividual(codedIndividual);
        solution.setObjectives(stateModel.evaluateConstraints());
    }

    @Override
    public Solution newSolution() {
        Solution solution = new Solution(getNumberOfVariables(),
                getNumberOfObjectives());

        for (int i = 0; i < getNumberOfVariables(); i++) {
            double[] range = CurrentStateModel.variableRange(i);
            solution.setVariable(i, new RealVariable(range[0], range[1]));
        }

        return solution;

    }
}
