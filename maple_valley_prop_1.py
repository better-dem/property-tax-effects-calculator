# maple_valley_prop_1.py
### Data sources:
# https://factfinder.census.gov/bkmk/table/1.0/en/ACS/15_5YR/DP03/1600000US5343150
# https://factfinder.census.gov/bkmk/table/1.0/en/ACS/15_5YR/DP04/1600000US5343150
# http://www.maplevalleywa.gov/home/showdocument?id=7826

import sampling
import bayes
import histogram as h
from collections import Counter as C
import random as r

def indicator(b):
    if b:
        return 1.0
    return 0.0

# income distribution
bin_boundaries_HI = [ 0.0, 10000.0, 15000.0, 25000.0, 35000.0, 50000.0, 75000.0, 100000.0, 150000.0, 200000.0, 2000000.0]
bin_weights_HI = [0.014, 0.011, 0.043, 0.041, 0.055, 0.171, 0.162, 0.306, 0.108, 0.0910]
h_income = h.Histogram(bin_boundaries_HI, bin_weights_HI)
household_income = bayes.Variable("household_income", [], lambda par, prev: h_income.gen_random_walk_sample(prev), lambda par, gen: h_income.get_interpolated_unnormalized_prob(gen))


# BN = bayes.BayesianNetwork([household_income])
# S = sampling.MetropolisSampler(BN)
# population, acceptance_rate = S.generate_population(1000)
# print "acceptance rate:", acceptance_rate
# from matplotlib import pyplot as plt
# plt.hist([x["household_income"] for x in population], bins=50)
# plt.show()
# exit()


# household type distribution
bin_boundaries = [0, 1, 2, 3]   # 0-1 -> rent, 1-2 -> mortgage, 2-3 -> no mortgage
bin_weights = [.16418, .72585, .10997]
h_household_type = h.Histogram(bin_boundaries, bin_weights)
household_type = bayes.Variable("household_type", [], lambda par, prev: h_household_type.gen_random_walk_sample(prev), lambda par, gen: h_household_type.get_prob(gen)) # household type is secretly categorical, so we don't want to interpolate the acceptance probability



def get_home_type_string(individual):
    if individual["household_type"] < 1:
        return "rent"
    if individual["household_type"] < 2:
        return "mortgage"
    else:
        return "own"

# property value
bin_boundaries = [0.0, 50000.0, 100000.0, 150000.0, 200000.0, 300000.0, 500000.0, 1000000.0, 10000000.0]
bin_weights = [.019, .004, .025, .082, .413, .409, .045, .003]
h_house_value = h.Histogram(bin_boundaries, bin_weights)
house_value = bayes.Variable("home_value_if_owner", [], lambda par, prev: h_house_value.gen_random_walk_sample(prev), lambda par, gen: h_house_value.get_interpolated_unnormalized_prob(gen))

# property tax amount
def calculate_property_tax(par, prev):
    house_value = par[0]
    household_type = par[1]
    if household_type > 1 and household_type < 3:
        return 1.25/1000 * house_value # maple valley property tax as of 2015
    else:
        return 0.0              # not a homeowner

property_tax_2015_amount = bayes.Variable("property_tax_amount", [house_value, household_type], calculate_property_tax, lambda par, gen: 1.0) # this acceptance probability is 1 because the only values generated are guaranteed to be correct

# housing costs given household type distribution
# mortgage
bin_boundaries = [x*12 for x in [0.0, 500.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 30000.0]]
bin_weights = [0.009, 0.027, 0.12, 0.276, 0.336, 0.145, 0.087]
h1 = h.Histogram(bin_boundaries, bin_weights)

# no mortgage
bin_boundaries = [x*12 for x in [0.0, 250.0, 400.0, 600.0, 800.0, 1000.0, 10000.0]]
bin_weights = [0.037, 0.064, 0.428, 0.307, 0.077, 0.087]
h2 = h.Histogram(bin_boundaries, bin_weights)

# rent
bin_boundaries = [x*12 for x in [0.0, 500.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 30000.0]]
bin_weights = [0.055, 0.105, 0.271, 0.244, 0.29, 0.029, 0.07] 
h3 = h.Histogram(bin_boundaries, bin_weights)

def random_walk_housing_cost(par, prev):
    l = min([h1.sorted_bin_boundaries[0], h2.sorted_bin_boundaries[0], h3.sorted_bin_boundaries[0]])
    u = max([h1.sorted_bin_boundaries[-1], h2.sorted_bin_boundaries[-1], h3.sorted_bin_boundaries[-1]])
    stdev = (l-u)/15
    return r.gauss(prev, stdev)

def get_housing_cost_acceptance(par, gen):
    housing_type = par[0]
    if housing_type < 1:
        return h3.get_interpolated_unnormalized_prob(gen)
    elif housing_type < 2:
        return h1.get_interpolated_unnormalized_prob(gen)
    else:
        return h3.get_interpolated_unnormalized_prob(gen)    

housing_costs = bayes.Variable("selected_housing_costs", [household_type, property_tax_2015_amount], random_walk_housing_cost, lambda par, val: indicator(val > par[1]) * get_housing_cost_acceptance(par, val))

# housing costs as a percentage of income
# mortgage
bin_boundaries = [0.0, 20.0, 25.0, 30.0, 35.0, 100.0]
bin_weights = [.359, .199, .14, .098, .205]
h4 = h.Histogram(bin_boundaries, bin_weights)

# no mortgage
bin_boundaries = [0.0, 10.0, 15.05, 20.0, 25.0, 30.0, 35.0, 100.0]
bin_weights = [.522, .088, .083, .056, .084, .028, .139]
h5 = h.Histogram(bin_boundaries, bin_weights)

# rent
bin_boundaries = [0.0, 15.0, 20.0, 25.0, 30.0, 35.0, 100.0]
bin_weights = [.16, .104, .199, .13, .085, .322]
h6 = h.Histogram(bin_boundaries, bin_weights)

def get_CPI_acceptance(par, val):
    income = par[0]
    hc = par[1]
    ht = par[2]
    if ht < 1:
        return h6.get_interpolated_unnormalized_prob(val)
    elif ht < 2:
        return h4.get_interpolated_unnormalized_prob(val)
    else:
        return h5.get_interpolated_unnormalized_prob(val)

def get_CPI(par, prev):
    income = par[0]
    hc = par[1]
    ht = par[2]
    if income == 0:
        return 100.0
    return 100.0 * hc / income

housing_cost_percentage_of_income = bayes.Variable("selected_housing_costs_as_a_percentage_of_income", [household_income, housing_costs, household_type], get_CPI, get_CPI_acceptance)

BN = bayes.BayesianNetwork([household_income, household_type, house_value, property_tax_2015_amount, housing_costs, housing_cost_percentage_of_income])

S = sampling.MetropolisSampler(BN)

population, acceptance_rate = S.generate_population(8848)
# population, acceptance_rate = S.generate_population(1000)
print "acceptance rate:", acceptance_rate
print "total property tax collected (should be about $3.5M):", sum([x["property_tax_amount"] for x in population])
print C([get_home_type_string(i) for i in population])

from matplotlib import pyplot as plt
plt.hist([x["household_income"] for x in population], bins=50)
plt.show()

plt.hist([x["home_value_if_owner"] for x in population if not get_home_type_string(x) == "rent"], bins=50)
plt.show()

# for i in range(10):
#     print population[i]

def update_for_prop_1_and_output(population):
    keys = sorted(population[0].keys())
    print ",".join(["vote", "home_type", "selected_housing_costs_in_thousands_of_dollars", "selected_housing_costs_as_a_percentage_of_income"])
    for individual in population:
        htype = get_home_type_string(individual)
        additional_tax = 0
        additional_tax_as_percentage_income = 0
        if not htype == "rent":
            additional_tax = .35/1000 * individual["home_value_if_owner"]
            additional_tax_as_percentage_income = 100 * additional_tax / individual["household_income"]
        n_row = ["no", htype, str(round( individual["selected_housing_costs"]/1000, 3)), str(round(individual["selected_housing_costs_as_a_percentage_of_income"], 2))]
        y_row = ["yes", htype, str(round( (individual["selected_housing_costs"]+additional_tax)/1000, 3)), str(round(individual["selected_housing_costs_as_a_percentage_of_income"] + additional_tax_as_percentage_income, 2))]
        print ",".join(n_row)
        print ",".join(y_row)

update_for_prop_1_and_output(population)
