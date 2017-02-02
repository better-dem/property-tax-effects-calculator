package org.betterdem;

import org.moeaframework.algorithm.NSGAII;
import org.moeaframework.core.*;
import org.moeaframework.core.comparator.ParetoDominanceComparator;
import org.moeaframework.core.operator.CompoundVariation;
import org.moeaframework.core.operator.RandomInitialization;
import org.moeaframework.core.operator.TournamentSelection;
import org.moeaframework.core.operator.TwoPointCrossover;
import org.moeaframework.core.spi.AlgorithmProvider;
import org.moeaframework.util.TypedProperties;

import java.util.Properties;

/**
 * Created by David Cohen on 2/2/17.
 */
public class CustomAlgorithmProvider extends AlgorithmProvider {
    @Override
    public Algorithm getAlgorithm(String s, Properties properties, Problem problem) {
        if (s.equalsIgnoreCase("BDNCustom")) {
            // if the user requested the RandomWalker algorithm
            TypedProperties typedProperties = new TypedProperties(properties);

            // allow the user to customize the POPULATION size (default to 100)
            int populationSize = typedProperties.getInt("populationSize", 100);

            // initialize the algorithm with randomly-generated solutions
            Initialization initialization = new RandomInitialization(problem, populationSize);

            return new NSGAII(problem,
                    new NondominatedSortingPopulation(),
                    new EpsilonBoxDominanceArchive(0.01),
                    new TournamentSelection(2, new ParetoDominanceComparator()),
                    new CompoundVariation(new TwoPointCrossover(1.0), new SingleRowVariation()),
                    initialization);
        } else {
            // return null if the user requested a different algorithm
            return null;
        }
    }
}
