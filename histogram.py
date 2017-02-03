# histogram.py
# class for generating samples and getting pdf of a value given a histogram

import random as r

class Histogram:
    def __init__(self, sorted_bin_boundaries, bin_weights):
        assert(isinstance(sorted_bin_boundaries, list)) 
        assert(isinstance(bin_weights, list)) 
        assert(len(sorted_bin_boundaries) > 2)
        assert(len(sorted_bin_boundaries) == len(bin_weights) + 1)
        
        self.sorted_bin_boundaries = sorted_bin_boundaries
        # normalize and cast to float
        self.bin_weights = map(lambda x: float(x)/sum(bin_weights), bin_weights)

    def get_bin(self, x):
        for i in range(len(self.sorted_bin_boundaries)):
            if self.sorted_bin_boundaries[i] > x:
                return i
        return len(self.sorted_bin_boundaries)

    def get_prob(self, x):
        """
        return pdf(x)
        """
        b = self.get_bin(x)
        if b == 0 or b == len(self.sorted_bin_boundaries):
            return 0.0
        l = self.sorted_bin_boundaries[b-1]
        u = self.sorted_bin_boundaries[b]
        return self.bin_weights[b-1] / (u-l)

    def gen_sample(self):
        x = r.random()
        for i, w in enumerate(self.bin_weights):
            if x < w:
                l = self.sorted_bin_boundaries[i]
                u = self.sorted_bin_boundaries[i+1]
                return l + (1.0*x/w)*(u-l) # select value from within the bin at uniform
            x -= w
        # if we reach here due to float madness, return the highest possible value
        return self.sorted_bin_boundaries[-1]
                
