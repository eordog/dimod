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

"""
Samplers can be composed. The `composite pattern <https://en.wikipedia.org/wiki/Composite_pattern>`_
allows layers of pre- and post-processing to be applied to binary quadratic programs without needing
to change the underlying sampler implementation.

We refer to these layers as `composites`. Each composed sampler must
include at least one sampler, and possibly many composites.

Each composed sampler is itself a dimod sampler with all of the
included methods and parameters. In this way complex samplers
can be constructed.

The dimod :class:`.ComposedSampler` abstract base class inherits from :class:`.Sampler` class
its abstract methods, properties, and mixins (for example, a `sample_Ising` method) and from
:class:`.Composite` class the `children` property and `child` mixin (`children` being a list of
supported samplers with `child` providing the first).

Examples:
    The :class:`~dwave.preprocessing.composites.SpinReversalTransformComposite`
    performs spin-reversal transforms ("gauge transformations") as a preprocessing
    step for a given sampler. It implements the pseudocode below:

    .. code-block:: python

        class SpinReversalTransformComposite(Sampler, Composite):

            # Updates to inherited sampler properties and parameters
            # Definition of the composite's children (i.e., supported samplers):
            children = None
            def __init__(self, child):
                self.children = [child]

            # The composite's implementation of spin-transformation functionality:
            def sample(self, bqm, num_spin_reversal_transforms=2, spin_reversal_variables=None, **kwargs):
                response = None
                # Preprocessing code that includes instantiation of a sampler:
                # flipped_response = self.child.sample(bqm, **kwargs)
                return response

    Given dimod sampler :class:`.ExactSolver` for example, the composed sampler is
    used as any dimod sampler, inheriting an Ising sampling method:

    >>> from dwave.preprocessing import SpinReversalTransformComposite
    >>> composed_sampler = SpinReversalTransformComposite(dimod.ExactSolver())
    >>> h = {0: -1, 1: 1}
    >>> num_srt = 2
    >>> solutions = composed_sampler.sample_ising(h, {},
    ...                                    num_spin_reversal_transforms=num_srt)
    >>> len(solutions) == num_srt*len(dimod.ExactSolver().sample_ising(h, {}))
    True

    For more examples, see the source code for the composed
    documented in :ref:`quadratic_composites`.
"""
import abc

from dimod.core.sampler import Sampler

__all__ = ['Composite', 'ComposedSampler']


class Composite(abc.ABC):
    """Abstract base class for dimod composites.

    Provides the :attr:`Composite.child` mixin property and defines the :attr:`Composite.children`
    abstract property to be implemented. These define the supported samplers for the composed sampler.

    """
    @abc.abstractproperty
    def children(self):
        """list[ :obj:`.Sampler`]: List of child samplers that that are used by
        this composite.
        """
        pass

    @property
    def child(self):
        """:obj:`.Sampler`: The child sampler. First sampler in :attr:`Composite.children`."""
        try:
            return self.children[0]
        except IndexError:
            raise RuntimeError("A Composite must have at least one child Sampler")


class ComposedSampler(Sampler, Composite):
    """Abstract base class for dimod composed samplers.

    Inherits from :class:`.Sampler` and :class:`.Composite`.

    """
    pass
