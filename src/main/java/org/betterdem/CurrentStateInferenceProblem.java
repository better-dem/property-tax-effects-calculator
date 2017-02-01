package org.betterdem;

import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.EncodingUtils;
import org.moeaframework.problem.AbstractProblem;

/**
 * The first part of the property tax effects calculation is to determine the current state from incomplete information.
 */
public class CurrentStateInferenceProblem extends AbstractProblem {
    @Override
    public void evaluate(Solution solution){
        double[] codedIndividual = EncodingUtils.getReal(solution);
        CurrentStateModel stateModel = CurrentStateModel.decodeFromIndividual(codedIndividual);
        solution.setObjectives(stateModel.);
    }

    private double[] evaluateConstraints(double[] individual){
        /*
        * Each index refers to a
        * */

    }

}
