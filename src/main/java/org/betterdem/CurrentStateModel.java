package org.betterdem;

import com.google.common.primitives.Doubles;
import org.apache.commons.lang3.ArrayUtils;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.stream.Collectors;

import static org.betterdem.CurrentStateModel.Household.NUM_HOUSEHOLD_FIELDS;

/**
 * Created by David Cohen on 2/1/17.
 */
public class CurrentStateModel {
    public static final int POPULATION = 100;

    public static class Household {
        public static final int NUM_HOUSEHOLD_FIELDS=3;

        public Household(List<Double> householdFields){
            if (householdFields.size() != NUM_HOUSEHOLD_FIELDS){
                throw new Error("Incorrect number of fields used to create a household object model ("+householdFields.size()+")");
            }
            annualIncome = householdFields.get(0);
            housingCosts = householdFields.get(1);
            householdType = householdFields.get(2); // Note, this is reinterpreted as one of {rent, own, mortgage}
//            homeValue = householdFields.get(3);
        }

        List<Double> getListRepr(){
            List<Double> ans = new LinkedList<Double>();
            ans.add(annualIncome);
            ans.add(housingCosts);
            ans.add(householdType);
//            ans.add(homeValue);
            return ans;
        }

        double annualIncome;
        double housingCosts;
        double householdType;
//        double homeValue;
    }

    public static double[] variableRange(int i){
        if (i % NUM_HOUSEHOLD_FIELDS == 0){
            return new double[] {0.0, 10000000};
        } else if (i % NUM_HOUSEHOLD_FIELDS == 1){
            return new double[] {0.0, 10000000};
        } else if (i % NUM_HOUSEHOLD_FIELDS == 2){
            return new double[] {0.0, 3.0};
        } else if (i % NUM_HOUSEHOLD_FIELDS == 3){
            return new double[] {0.0, 10000000};
        }
        else throw new Error("variable range method is broken, mod didn't work");
    }

    List<Household> households;

    static HistogramComparator householdIncomesCensus;
    static HistogramComparator householdTypes;
    static HistogramComparator mortgagedHomeMonthlyCosts;
    static HistogramComparator noMortgageHomeMonthlyCosts;
    static HistogramComparator renterMonthlyCosts;
    static {
        //// Constraint 0: distance between distribution of household incomes in the model, and the distribution in the census
        // data from here: https://factfinder.census.gov/bkmk/table/1.0/en/ACS/15_5YR/DP03/1600000US5343150
        List<Double> sortedBinBoundaries = Arrays.asList(
                0.0,
                10000.0,
                15000.0,
                25000.0,
                35000.0,
                50000.0,
                75000.0,
                100000.0,
                150000.0,
                200000.0,
                100000000.0); // assuming nobody in Maple Valley has greater than $100B annual income
        List<Double> binWeights = Arrays.asList(
                0.014,
                0.011,
                0.043,
                0.041,
                0.055,
                0.171,
                0.162,
                0.306,
                0.108,
                0.09);
        householdIncomesCensus = new HistogramComparator(sortedBinBoundaries, binWeights);

        //// Constraint 1: similarity of household types distribution to census
        // data from here: https://factfinder.census.gov/bkmk/table/1.0/en/ACS/15_5YR/DP04/1600000US5343150
        sortedBinBoundaries = Arrays.asList(
                0.0, // rent
                1.0,  // mortgage
                2.0,   // own
                3.0);
        binWeights = Arrays.asList(
                0.16418,
                0.72585,
                0.10997);
        householdTypes = new HistogramComparator(sortedBinBoundaries, binWeights);


        //// Constraint 2: distance between distribution of monthly costs given homeowner status
        // data from here: https://factfinder.census.gov/bkmk/table/1.0/en/ACS/15_5YR/DP04/1600000US5343150
        sortedBinBoundaries = Arrays.asList(
                0.0,
                500.0,
                1000.0,
                1500.0,
                2000.0,
                2500.0,
                3000.0,
                10000000.0); // assuming nobody in Maple Valley has greater than $10M monthly owner costs
        binWeights = Arrays.asList(
                0.009,
                0.027,
                0.12,
                0.276,
                0.336,
                0.145,
                0.087);
        mortgagedHomeMonthlyCosts = new HistogramComparator(sortedBinBoundaries, binWeights);

        sortedBinBoundaries = Arrays.asList(
                0.0,
                250.0,
                400.0,
                600.0,
                800.0,
                1000.0,
                100000.0);
        binWeights = Arrays.asList(
                0.037,
                0.064,
                0.428,
                0.307,
                0.077,
                0.087);
        noMortgageHomeMonthlyCosts = new HistogramComparator(sortedBinBoundaries, binWeights);

        sortedBinBoundaries = Arrays.asList(
                0.0,
                500.0,
                1000.0,
                1500.0,
                2000.0,
                2500.0,
                3000.0,
                100000.0);
        binWeights = Arrays.asList(
                0.055,
                0.105,
                0.271,
                0.244,
                0.29,
                0.029,
                0.07);
        renterMonthlyCosts = new HistogramComparator(sortedBinBoundaries, binWeights);
    }

    public static int NUM_OBJECTIVES = 5;
    double[] evaluateConstraints(){
        /*
        * This function scores how well a current state model meets the required constraints
        * For each dimension, lower is better.
        * So, for some dimensions, we can just count up the number of violations
        * However, more information helps guide the optimization, so we want to give some credit for being close in some dimensions
        * */
        List<Double> scores = new ArrayList<Double>();
        //// Constraint 0: distance between distribution of household incomes in the model, and the distribution in the census
        scores.add(householdIncomesCensus.distance(
                households.stream().map(x -> x.annualIncome).collect(Collectors.toList())
        ));

        //// Constraint 1: similarity of household types distribution to census
        scores.add(householdTypes.distance(
                households.stream().map(x -> x.householdType).collect(Collectors.toList())
        ));

        //// Constraints 2-4: distance between distribution of monthly costs given homeowner status
        scores.add(renterMonthlyCosts.distance(
                households.stream().
                        filter(x -> x.householdType >= 0.0  && x.householdType <= 1.0).
                        map(x -> x.housingCosts).collect(Collectors.toList())
        ));

        scores.add(mortgagedHomeMonthlyCosts.distance(
                households.stream().
                        filter(x -> x.householdType > 1.0  && x.householdType <= 2.0).
                        map(x -> x.housingCosts).collect(Collectors.toList())
        ));

        scores.add(noMortgageHomeMonthlyCosts.distance(
                households.stream().
                        filter(x -> x.householdType > 2.0  && x.householdType <= 3.0).
                        map(x -> x.housingCosts).collect(Collectors.toList())
        ));

         return Doubles.toArray(scores);
        // to simplify the optimization problem, sum all the objectives
//        double ans = scores.stream().mapToDouble(Double::doubleValue).sum();
//        return new double[] {ans};

    }

    public CurrentStateModel() {
        this.households = new ArrayList<>();
    }

    double[] encodeAsIndividual(){
        List<Double> ansAsList = new LinkedList<Double>();
        for (int i = 0; i < households.size(); i++) {
            ansAsList.addAll(households.get(i).getListRepr());
        }
        return Doubles.toArray(ansAsList);
    }

    static CurrentStateModel decodeFromIndividual(double[] individual){
        CurrentStateModel ans = new CurrentStateModel();
        for (int i = 0; i < individual.length/NUM_HOUSEHOLD_FIELDS; i++) {
            List<Double> householdFields = Arrays.asList(ArrayUtils.toObject(individual)).
                    subList(i*NUM_HOUSEHOLD_FIELDS, i*NUM_HOUSEHOLD_FIELDS+NUM_HOUSEHOLD_FIELDS);
            Household tmp = new Household(householdFields);
            ans.households.add(tmp);
        }
        return ans;
    }
}
