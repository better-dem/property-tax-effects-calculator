package org.betterdem;

import org.moeaframework.core.PRNG;
import org.moeaframework.core.Solution;
import org.moeaframework.core.Variation;
import org.moeaframework.core.variable.RealVariable;

/**
 * Created by David Cohen on 2/2/17.
 */
public class SingleRowVariation implements Variation {
    @Override
    public int getArity() {
        return 1;
    }

    @Override
    public Solution[] evolve(Solution[] solutions) {
        Solution result = solutions[0].copy();
        int rowToVary = PRNG.nextInt(0, CurrentStateModel.POPULATION-1); // bizarrely, nextInt is INCLUSIVE of the 'max' index
        int rowSize = CurrentStateModel.Household.NUM_HOUSEHOLD_FIELDS;

        for (int i = 0; i < rowSize; i++) {
            RealVariable v = (RealVariable)result.getVariable(i + rowToVary*rowSize);
            double variableScale = v.getUpperBound() - v.getLowerBound();
            double newV = PRNG.nextGaussian(v.getValue(), variableScale / 4);
            if (newV < v.getLowerBound()) {
                newV = v.getLowerBound();
            }
            if (newV > v.getUpperBound()) {
                newV = v.getUpperBound();
            }
            v.setValue(newV);
        }

        return new Solution[] {result};
    }
}
