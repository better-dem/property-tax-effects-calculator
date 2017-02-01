package org.betterdem;

import org.moeaframework.Executor;
import org.moeaframework.core.NondominatedPopulation;
import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.EncodingUtils;

/**
 * Hello world!
 *
 */
public class CalculateEffects
{
    public static void main( String[] args )
    {
        System.out.println( "Starting optimization...");

        NondominatedPopulation result = new Executor()
                .withProblemClass(CurrentStateInferenceProblem.class)
                .withAlgorithm("GDE3")
                .withMaxEvaluations(1000000)
                .distributeOnAllCores()
                .run();

        System.out.println("number of non-dominated results:" + result.size());

        // display the results
        System.out.println("non-dominated results:");
        for (Solution solution : result) {
            double[] individual = EncodingUtils.getReal(solution);
            CurrentStateModel model = CurrentStateModel.decodeFromIndividual(individual);
            System.out.println("some households in this result ....");
            for (int i = 0; i < 10; i++) {
                System.out.println(model.households.get(i).getListRepr());
            }
        }


    }
}
