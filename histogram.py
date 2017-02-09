# histogram.py
# class for generating samples and getting pdf of a value given a histogram

import random as r
import sampling

class Histogram:
    def __init__(self, sorted_bin_boundaries, bin_weights):
        assert(isinstance(sorted_bin_boundaries, list)) 
        assert(isinstance(bin_weights, list)) 
        assert(len(sorted_bin_boundaries) > 2)
        assert(len(sorted_bin_boundaries) == len(bin_weights) + 1)
        
        self.sorted_bin_boundaries = sorted_bin_boundaries
        # normalize and cast to float
        self.bin_weights = map(lambda x: float(x)/sum(bin_weights), bin_weights)

    def gen_random_walk_sample(self, prev):
        """
        not guarenteed to return non-zero-probability samples
        is symmetric, satisfying metropolis requirement
        """
        l = self.sorted_bin_boundaries[0]
        u = self.sorted_bin_boundaries[-1]
        stdev = (l-u) * sampling.stdev_fraction
        return r.gauss(prev, stdev)

    def gen_unif_sample(self):
        x = r.random()
        l = self.sorted_bin_boundaries[0]
        u = self.sorted_bin_boundaries[-1]
        return l + x*(u-l)

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

    def get_interpolated_unnormalized_prob(self, x):
        """
        return 1/z*pdf'(x), where:
        pdf' is interpolated from the histogram to blur toward the edges of each bin
        z is a normalizing constant which isn't computed
        """
        return self.get_prob(x)

        # b = self.get_bin(x)
        # if b == 0 or b == len(self.sorted_bin_boundaries):
        #     return 0.0
        # l = self.sorted_bin_boundaries[b-1]
        # u = self.sorted_bin_boundaries[b]

        # lower_bin_pdf = None
        # if b == 1:
        #     lower_bin_pdf = 0.0
        # else:
        #     l_minus = self.sorted_bin_boundaries[b-2]
        #     lower_bin_pdf = self.bin_weights[b-2] / (l - l_minus)

        # upper_bin_pdf = None
        # if b == len(self.sorted_bin_boundaries) - 1:
        #     upper_bin_pdf = 0.0
        # else:
        #     u_plus = self.sorted_bin_boundaries[b+1]
        #     upper_bin_pdf = self.bin_weights[b] / (u_plus - u)

        # this_bin_pdf = self.bin_weights[b-1] / (u-l)
        # this_bin_center = (l+u) / 2.0
        # interpolated_bin_area = (l-u) / 2 * (this_bin_pdf + (upper_bin_pdf + lower_bin_pdf) / 2)

        # if x > this_bin_center:
        #     edge_pdf = (upper_bin_pdf + this_bin_pdf)/2.0
        #     fraction_toward_edge = 1.0 * abs(x - this_bin_center) / abs(u - this_bin_center)
        #     return ((1.0 - fraction_toward_edge) * this_bin_pdf + fraction_toward_edge * edge_pdf) * this_bin_pdf / interpolated_bin_area
        # else:
        #     edge_pdf = (lower_bin_pdf + this_bin_pdf)/2.0
        #     fraction_toward_edge = 1.0 * abs(x - this_bin_center) / abs(l - this_bin_center)
        #     return ((1.0 - fraction_toward_edge) * this_bin_pdf + fraction_toward_edge * edge_pdf) * this_bin_pdf / interpolated_bin_area
        

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
                
