package org.betterdem;

import org.apache.commons.lang3.ArrayUtils;

import java.util.Arrays;
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

        double annualIncome;
        double housingCostsBeforePropertyTax;
        double householdType;
        double homeValue;
    }

    Household[] households;
    int numHouseholds;

    public CurrentStateModel(int numHouseholds) {
        this.numHouseholds = numHouseholds;
        this.households = new Household[numHouseholds];
    }

    double[] encodeAsIndividual(){

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

    double[] evaluateConstraints(){

    }

}
