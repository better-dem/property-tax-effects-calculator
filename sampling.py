# sampling.py
import bayes as b
import random as r

class MetropolisSampler:
    def __init__(self, bayes_net):
        self.bayes_net = bayes_net

    def generate_population(self, size, max_attempts = 1000000):
        burning_in = 100
        accepted = []
        n_attempts = 0
        current_sample = None
        current_acceptance_val = None
        while n_attempts < max_attempts and len(accepted) < size:
            instance = dict()    # map variable names to values
            instance_acceptance_val = 1.0

            # generate a candidate sample
            for var in self.bayes_net.get_ordered_variables():
                parent_values = [instance[p.name] for p in var.parents]
                gen_val = var.gen_function(parent_values)
                instance[var.name] = gen_val
                if not var.is_generatable:
                    instance_acceptance_val *= var.acceptance_probability_function(parent_values, gen_val)

            if not current_sample is None and not burning_in > 0:
                n_attempts += 1
                if instance_acceptance_val <= 0.0:
                    continue

                # accept or reject the sample
                acceptance_ratio = 1.0*instance_acceptance_val / current_acceptance_val
                if acceptance_ratio > 1 or r.random() < acceptance_ratio:
                    accepted.append(current_sample)
                    current_sample = instance
                    current_acceptance_val = instance_acceptance_val
                        
            else:
                if instance_acceptance_val <= 0.0:
                    continue
                burning_in -= 1
                current_sample = instance
                current_acceptance_val = instance_acceptance_val

        return accepted, 1.0 * len(accepted) / n_attempts
