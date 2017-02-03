# maple_valley_prop_1.py
### Data sources:
# https://factfinder.census.gov/bkmk/table/1.0/en/ACS/15_5YR/DP03/1600000US5343151
# https://factfinder.census.gov/bkmk/table/1.0/en/ACS/15_5YR/DP04/1600000US5343150
# http://www.maplevalleywa.gov/home/showdocument?id=7826

import sampling
import bayes
import histogram as h

def indicator(b):
    if b:
        return 1.0
    return 0.0

# income distribution
bin_boundaries = [ 0.0, 10000.0, 15000.0, 25000.0, 35000.0, 50000.0, 75000.0, 100000.0, 150000.0, 200000.0, 100000000.0]
bin_weights = [0.014, 0.011, 0.043, 0.041, 0.055, 0.171, 0.162, 0.306, 0.108, 0.0910]
h_income = h.Histogram(bin_boundaries, bin_weights)
household_income = bayes.Variable("household_income", [], lambda x: h_income.gen_sample())

# household type distribution
bin_boundaries = [0, 1, 2, 3]   # 0-1 -> rent, 1-2 -> mortgage, 2-3 -> no mortgage
bin_weights = [.16418, .72585, .10997]
h_household_type = h.Histogram(bin_boundaries, bin_weights)
household_type = bayes.Variable("household_type", [], lambda x: h_household_type.gen_sample())

# property value
bin_boundaries = [0.0, 50.000, 100000.0, 150000.0, 200000.0, 300000.0, 500000.0, 1000000.0, 10000000.0]
bin_weights = [.019, .004, .025, .082, .413, .409, .045, .003]
h_house_value = h.Histogram(bin_boundaries, bin_weights)
house_value = bayes.Variable("home_value_if_owner", [], lambda x: h_house_value.gen_sample())

# property tax amount
def calculate_property_tax(par):
    house_value = par[0]
    household_type = par[1]
    if household_type > 1 and household_type < 3:
        return 1.25/1000 * house_value # maple valley property tax as of 2015
    else:
        return 0.0              # not a homeowner

property_tax_2015_amount = bayes.Variable("property_tax_amount", [house_value, household_type], calculate_property_tax)

# housing costs given household type distribution
# mortgage
bin_boundaries = [0.0, 500.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 30000.0]
bin_weights = [0.009, 0.027, 0.12, 0.276, 0.336, 0.145, 0.087]
h1 = h.Histogram(bin_boundaries, bin_weights)

# no mortgage
bin_boundaries = [0.0, 250.0, 400.0, 600.0, 800.0, 1000.0, 10000.0]
bin_weights = [0.037, 0.064, 0.428, 0.307, 0.077, 0.087]
h2 = h.Histogram(bin_boundaries, bin_weights)

# rent
bin_boundaries = [0.0, 500.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 30000.0]
bin_weights = [0.055, 0.105, 0.271, 0.244, 0.29, 0.029, 0.07] 
h3 = h.Histogram(bin_boundaries, bin_weights)

def get_housing_cost_hist(h):
    h = h[0]
    if h < 1:
        return h3.gen_sample()
    elif h < 2:
        return h1.gen_sample()
    else:
        return h3.gen_sample()

housing_costs = bayes.Variable("selected_housing_costs", [household_type, property_tax_2015_amount], get_housing_cost_hist, False, lambda par, val: indicator(val > par[1]))

# housing costs as a fraction of income
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
        return h6.get_prob(val)
    elif ht < 2:
        return h4.get_prob(val)
    else:
        return h5.get_prob(val)

def get_CPI(par):
    income = par[0]
    hc = par[1]
    ht = par[2]
    if income == 0:
        return 100.0
    return 100.0 * hc / income

housing_cost_percentage_of_income = bayes.Variable("selected_housing_costs_as_a_percentage_of_income", [household_income, housing_costs, household_type], get_CPI, False, get_CPI_acceptance)








BN = bayes.BayesianNetwork([household_income, household_type, house_value, property_tax_2015_amount, housing_costs, housing_cost_percentage_of_income])

S = sampling.MetropolisSampler(BN)

population, acceptance_rate = S.generate_population(8848)

print "done sampling. Acceptance rate: ", acceptance_rate

for i in range(10):
    print population[i]

print "total property tax collected:", sum([x["property_tax_amount"] for x in population])
print "(should be about $3.5M)"

