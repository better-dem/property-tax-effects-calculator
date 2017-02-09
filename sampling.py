# sampling.py
import bayes as b
import random as r
import sys
import numpy as np

stdev_fraction = 1.0/30

class MetropolisSampler:
    def __init__(self, bayes_net):
        self.bayes_net = bayes_net

    def generate_population(self, size):
        burning_in = 1000
        accepted = []
        n_attempts = 0
        current_sample = None
        current_acceptance_val = -1*np.inf
        while len(accepted) < size:                
            instance = dict()    # map variable names to values
            instance_acceptance_val = 0.0 # use log values

            # generate a candidate sample
            for var in self.bayes_net.get_ordered_variables():
                parent_values = [instance[p.name] for p in var.parents]
                current_value = 0.0
                if not current_sample is None: 
                    current_value = current_sample[var.name]
                gen_val = var.gen_function(parent_values, current_value)
                instance[var.name] = gen_val
                instance_acceptance_val += np.log(var.acceptance_probability_function(parent_values, gen_val)) # numpy correctly deals with log(0)

            if not current_sample is None and not burning_in > 0:
                n_attempts += 1
                if instance_acceptance_val == -1*np.inf:
                    continue

                # accept or reject the sample
                acceptance_ratio = np.exp(instance_acceptance_val - current_acceptance_val)
                if acceptance_ratio > 1 or r.random() < acceptance_ratio:
                    accepted.append(current_sample)
                    current_sample = instance
                    current_acceptance_val = instance_acceptance_val
                    if len(accepted) % 100 == 0 and not len(accepted)==0:
                        sys.stderr.write(str(len(accepted)) + " instances accepted, acceptance rate so far: " + str(1.0*len(accepted) / n_attempts)+"\n")
                        sys.stderr.flush()
                        
            else:
                if instance_acceptance_val == -1 * np.inf:
                    continue
                # accept or reject the sample
                acceptance_ratio = np.exp(instance_acceptance_val - current_acceptance_val)
                if acceptance_ratio > 1 or r.random() < acceptance_ratio:
                    burning_in -= 1
                    current_sample = instance
                    current_acceptance_val = instance_acceptance_val
                    if burning_in == 0:
                        sys.stderr.write("finished burn-in\n")
                        sys.stderr.flush()

        return accepted, 1.0 * len(accepted) / n_attempts
