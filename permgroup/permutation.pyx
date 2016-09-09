#!/usr/bin/python


import cython

from libc.stdlib cimport calloc, malloc, free
from libc.stdint cimport uint32_t

import core_py


cdef class Permutation(object):

    cdef uint32_t *permutation
    cdef uint32_t *support
    cdef uint32_t **cycles
    cdef uint32_t *cycle_lengths
    cdef uint32_t num_cycles
    cdef public uint32_t max_support
    cdef public uint32_t degree
    cdef public bint is_identity

    def __cinit__(self, list action):

        # Verify that the action is well-formed
        if not core_py._verify_tuples_(action):
            raise TypeError("`action` is not a non-empty list of tuples")
        if not core_py._has_unique_points_(action):
            raise ValueError("`action` has repeated points")

        # Set the max_support
        self.max_support = <uint32_t>core_py._get_max_support_(action)

        # Set the degree
        self.degree = <uint32_t>core_py._get_degree_(action)

        # Determine if this is the identity permutation
        if core_py._is_identity_action_(action):
            self.is_identity = True
        else:
            self.is_identity = False

        # Get the action as an array map
        action = core_py._make_map_(action)

        # Save the permutation map and support as C arrays
        self.permutation = <uint32_t *>malloc((self.max_support+1)*sizeof(uint32_t))
        self.support = <uint32_t *>malloc(self.degree*sizeof(uint32_t))
        self.permutation[0] = self.max_support
        cdef uint32_t i = 1
        cdef uint32_t j = 0
        while i <= self.max_support:
            self.permutation[i] = <uint32_t>action[i]
            if i != self.permutation[i]:
                self.support[j] = i
                j += 1
            i += 1

        # Compute cycle information
        cdef bint *support_flags = <bint *>calloc((self.max_support+1), sizeof(bint))
        


    def __dealloc__(self):
        """
        Ddeconstruct the class and free C memory objects.
        """
        free(self.permutation)
        free(self.support)


    def __repr__(self):
        """
        Machine readable representation of Permutation object.
        """
        return "repr string"


    def __str__(self):
        """
        Human readable representation of Permutation object.
        """
        return "str string"


    cdef uint32_t get_cycle_length(self, uint32_t pnt):
        """
        Returns the cycle length of the cycle starting at point pnt.
        """
        cdef uint32_t image = self.get_image(pnt)
        cdef uint32_t length = 1

        while image != pnt:
            length += 1
            image = self.get_image(image)
        return length


    cdef uint32_t get_image(self, uint32_t pnt):
        """
        Returns the image of a point under the permutation.
        """
        return self.permutation[pnt]


    cdef uint32_t * get_cycle(self, uint32_t pnt):
        """
        Returns an array representing the cycle starting at point pnt.
        """
        cdef uint32_t *cycle
        cdef uint32_t length = self.get_cycle_length(pnt)
        cdef uint32_t image = pnt
        cdef uint32_t i = 0

        cycle = <uint32_t *>malloc(length*sizeof(uint32_t))
        while i < length:
            cycle[i] = image
            i += 1
            image = self.get_image(image)
        return cycle       


"""
    cpdef support(self):
        cdef uint32_t i = 0
        L = []
        while i < self.degree:
            L.append(self.support[i])
            i += 1
        return L
"""

