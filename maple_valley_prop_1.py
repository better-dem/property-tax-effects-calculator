# maple_valley_prop_1.py
import sampling
import bayes

# income distribution

# household type distribution

# housing costs given household type distribution

# housing costs as a fraction of income

BN = bayes.BayesianNetwork([household_income, household_type, housing_cost, housing_cost_as_fraction_income])

S = sampling.MetropolisSampler(BN)

population, rejection_rate = S.generate_population(100)

print "done sampling, rejection rate: ", rejection_rate

for i in range(10):
    print population[i]
