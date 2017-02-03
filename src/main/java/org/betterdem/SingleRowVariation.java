package org.betterdem;

import org.moeaframework.core.PRNG;
import org.moeaframework.core.Solution;
import org.moeaframework.core.Variation;
import org.moeaframework.core.variable.RealVariable;

/**
 * Created by David Cohen on 2/2/17.
 */
public class SingleRowVariation implements Variation {
    private int population;

    public SingleRowVariation(int population) {
        this.population = population;
    }

    private int currentRow = 0;
    private int remainingAttemptsAtCurrentRow = 100;

    @Override
    public int getArity() {
        return 1;
    }

    @Override
    public Solution[] evolve(Solution[] solutions) {
        Solution result = solutions[0].copy();
        int rowSize = CurrentStateModel.Household.NUM_HOUSEHOLD_FIELDS;

        int rowToVary = currentRow;
        if (remainingAttemptsAtCurrentRow <= 0) {
            currentRow = (currentRow + 1) % population;
            rowToVary = currentRow;
            remainingAttemptsAtCurrentRow = 100;
        } else {
            remainingAttemptsAtCurrentRow -= 1;
        }

        for (int i = 0; i < rowSize; i++) {
            RealVariable v = (RealVariable) result.getVariable(i + rowToVary * rowSize);
            double variableScale = v.getUpperBound() - v.getLowerBound();
            double newV = PRNG.nextGaussian(v.getValue(), variableScale / 10);
            if (newV < v.getLowerBound()) {
                newV = v.getLowerBound();
            }
            if (newV > v.getUpperBound()) {
                newV = v.getUpperBound();
            }
            v.setValue(newV);
        }


        return new Solution[]{result};
    }
}
