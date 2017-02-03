# bayes.py

class Variable:
    def __init__(self, name, parents, gen_function, is_generatable=True, acceptance_probability_function=None):
        """
        If not is_generatable, 
        the gen. function is a proposal distribution
        and the acceptance function is proportional to the actual probability function, making it suitable for metropolis sampling
        """
        self.name = name
        self.parents = parents
        self.gen_function = gen_function
        self.is_generatable = is_generatable
        self.acceptance_probability_function = acceptance_probability_function

class BayesianNetwork:
    def __init__(self, variables):
        self.variables = variables
        # TODO: check for cycles...

    def get_ordered_variables(self):
        remaining = set(self.variables)
        ans = []
        while not len(remaining) == 0:
            for i in remaining:
                if all(i.parents in ans):
                    next_var = i
                    break
            ans.add(next_var)
            remaining.remove(next_var)
        return ans

        
