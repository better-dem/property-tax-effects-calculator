package org.betterdem;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Stores a histogram of doubles, compares incoming data to the histogram and returns a difference
 *
 * Created by David Cohen on 2/1/17.
 */
public class HistogramComparator {
    private List<Double> sortedBinBoundaries; // from lowest to highest
    private List<Double> binWeights; // corresponding to the bin boundaries given, with an extra zero at the front and back

    public HistogramComparator(List<Double> sortedBinBoundaries, List<Double> binWeights) {
        if (sortedBinBoundaries.size() < 2){
            throw new Error("Require at least two bin boundaries");
        }

        if (sortedBinBoundaries.size() != binWeights.size()+1){
            System.out.println(sortedBinBoundaries.size());
            System.out.println(binWeights.size());
            throw new Error("Incorrect number of bin weights for the given set of boundaries");
        }

        if (Math.abs(binWeights.stream().mapToDouble(Double::doubleValue).sum() - 1) > 1.0E-2){
            throw new Error("bin weights don't sum to 1");
        }

        //// todo: more validity checks

        this.sortedBinBoundaries = new ArrayList<>(sortedBinBoundaries);
        this.binWeights = new ArrayList<>(binWeights);
        this.binWeights.add(0, 0.0);
        this.binWeights.add(0.0);
    }

    private int getBin(double d){
        for (int i = 0; i < sortedBinBoundaries.size(); i++) {
            if (sortedBinBoundaries.get(i) > d){
                return i;
            }
        }
        return sortedBinBoundaries.size();
    }

    public double distance(List<Double> dataset){
        final Map<Integer, Integer> binCounter = new HashMap<>();
        dataset.forEach(x -> binCounter.put(getBin(x), binCounter.getOrDefault(getBin(x), 0) + 1));
        return binCounter.keySet().stream().
                map(i -> Math.pow((1.0*binCounter.get(i)/dataset.size()) - binWeights.get(i), 2)).
                mapToDouble(Double::doubleValue).sum();
    }

}
