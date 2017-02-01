package org.betterdem;

import com.google.common.primitives.Doubles;
import org.apache.commons.lang3.ArrayUtils;
import org.apache.commons.lang3.tuple.ImmutablePair;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

import static org.betterdem.CurrentStateModel.Household.NUM_HOUSEHOLD_FIELDS;

/**
 * Created by David Cohen on 2/1/17.
 */
public class CurrentStateModel {

    public static class Household {
        public static final int NUM_HOUSEHOLD_FIELDS=4;

        public Household(List<Double> householdFields){
            if (householdFields.size() != NUM_HOUSEHOLD_FIELDS){
                throw new Error("Incorrect number of fields used to create a household object model ("+householdFields.size()+")");
            }
            annualIncome = householdFields.get(0);
            housingCostsBeforePropertyTax = householdFields.get(1);
            householdType = householdFields.get(2); // Note, this is reinterpreted as one of {rent, own, mortgage}
            homeValue = householdFields.get(3);
        }

        List<Double> getListRepr(){
            List<Double> ans = new LinkedList<Double>();
            ans.add(annualIncome);
            ans.add(housingCostsBeforePropertyTax);
            ans.add(householdType);
            ans.add(homeValue);
            return ans;
        }

        double annualIncome;
        double housingCostsBeforePropertyTax;
        double householdType;
        double homeValue;
    }

    Household[] households;
    int numHouseholds;

    double[] evaluateConstraints(){
        /*
        * This function scores how well a current state model meets the required constraints
        * For each dimension, lower is better.
        * So, for some dimensions, we can just count up the number of violations
        * However, more information helps guide the optimization, so we want to give some credit for being close in some dimensions
        * */
        List<Double> scores = new ArrayList<Double>();

        //// Constraint 0: distance between distribution of household incomes in the model, and the distribution in the census
        // data from here: https://factfinder.census.gov/bkmk/table/1.0/en/ACS/15_5YR/DP03/1600000US5343150
        List<ImmutablePair<Double, Double>> householdIncomes = new ArrayList<>();
        householdIncomes.add(new ImmutablePair<>(10000.0, .014));
        householdIncomes.add(new ImmutablePair<>(15000.0, .011));
        householdIncomes.add(new ImmutablePair<>(25000.0, .043));
        householdIncomes.add(new ImmutablePair<>(35000.0, .041));
        householdIncomes.add(new ImmutablePair<>(50000.0, .055));
        householdIncomes.add(new ImmutablePair<>(75000.0, .171));
        householdIncomes.add(new ImmutablePair<>(100000.0, .162));
        householdIncomes.add(new ImmutablePair<>(150000.0, .306));
        householdIncomes.add(new ImmutablePair<>(200000.0, .108));
        householdIncomes.add(new ImmutablePair<>((Double)(null), .09));

        // TODO: calculate historgram for this and compare

        return Doubles.toArray(scores);
    }



    public CurrentStateModel(int numHouseholds) {
        this.numHouseholds = numHouseholds;
        this.households = new Household[numHouseholds];
    }

    double[] encodeAsIndividual(){
        List<Double> ansAsList = new LinkedList<Double>();
        for (int i = 0; i < numHouseholds; i++) {
            ansAsList.addAll(households[i].getListRepr());
        }
        return Doubles.toArray(ansAsList);
    }

    static CurrentStateModel decodeFromIndividual(double[] individual){
        CurrentStateModel ans = new CurrentStateModel(individual.length/NUM_HOUSEHOLD_FIELDS);
        for (int i = 0; i < ans.numHouseholds/NUM_HOUSEHOLD_FIELDS; i++) {
            List<Double> householdFields = Arrays.asList(ArrayUtils.toObject(individual)).
                    subList(i*NUM_HOUSEHOLD_FIELDS, i*NUM_HOUSEHOLD_FIELDS+NUM_HOUSEHOLD_FIELDS);
            Household tmp = new Household(householdFields);
            ans.households[i] = tmp;
        }
        return ans;
    }
}
