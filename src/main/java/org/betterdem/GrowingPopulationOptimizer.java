package org.betterdem;

import org.moeaframework.Executor;
import org.moeaframework.core.NondominatedPopulation;

/**
 *
 * Perform the optimization with large populations by solving first with small populations and using
 * those solutions to seed the larger population problems.
 *
 * Created by David Cohen on 2/2/17.
 */
public class GrowingPopulationOptimizer {
    public static int newPopulationSize = 1;

    public static void main(String[] args) {
        NondominatedPopulation result = null;

        for (int i = 1; i <= 3; i++) {
            newPopulationSize = i;
            System.out.println("\n==== New Population Size ====");
            result = new Executor()
                    .withProblemClass(CurrentStateInferenceProblem.class)
                    .withAlgorithm("GDE3")
                    .withMaxEvaluations(10000)
                    .distributeOnAllCores()
                    .run();

            CalculateEffects.displayResults(result);
        }
    }

}
