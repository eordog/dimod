# Copyright 2018 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# ================================================================================================
"""
A solver that calculates the energy of all possible samples.

Note:
    This sampler is designed for use in testing. Because it calculates the
    energy for every possible sample, it is very slow.

"""
import itertools


from dimod.core.sampler import Sampler
from dimod.sampleset import SampleSet

__all__ = ['ExactSolver']


class ExactSolver(Sampler):
    """A simple exact solver for testing and debugging code using your local CPU.

    Notes:
        This solver becomes slow for problems with 18 or more
        variables.

    Examples:
        This example solves a two-variable Ising model.

        >>> h = {'a': -0.5, 'b': 1.0}
        >>> J = {('a', 'b'): -1.5}
        >>> sampleset = dimod.ExactSolver().sample_ising(h, J)
        >>> print(sampleset)
           a  b energy num_oc.
        3 -1 -1   -2.0       1
        0 +1 +1   -1.0       1
        1 +1 -1    0.0       1
        2 -1 +1    3.0       1
        ['SPIN', 4 rows, 4 samples, 2 variables]

        This example solves a two-variable QUBO.

        >>> Q = {('a', 'b'): 2.0, ('a', 'a'): 1.0, ('b', 'b'): -0.5}
        >>> sampleset = dimod.ExactSolver().sample_qubo(Q)


        This example solves a two-variable binary quadratic model

        >>> bqm = dimod.BinaryQuadraticModel({'a': 1.5}, {('a', 'b'): -1}, 0.0, 'SPIN')
        >>> sampleset = dimod.ExactSolver().sample(bqm)

    """
    properties = None
    parameters = None

    def __init__(self):
        self.properties = {}
        self.parameters = {}

    def sample(self, bqm):
        """Sample from a binary quadratic model.

        Args:
            bqm (:obj:`~dimod.BinaryQuadraticModel`):
                Binary quadratic model to be sampled from.

        Returns:
            :obj:`~dimod.SampleSet`

        """
        n = len(bqm)
        if n == 0:
            return SampleSet.from_samples([], bqm.vartype, energy=[])
        samples = list(itertools.product(bqm.vartype.value, repeat=n))
        response = SampleSet.from_samples_bqm((samples, list(bqm)), bqm)
        return response
