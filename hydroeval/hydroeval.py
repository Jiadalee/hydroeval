# -*- coding: utf-8 -*-

# This file is part of HydroEval: An Evaluator for Stream Flow Time Series
# Copyright (C) 2019  Thibault Hallouin (1)
#
# (1) Dooge Centre for Water Resources Research, University College Dublin, Ireland
#
# HydroEval is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HydroEval is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HydroEval. If not, see <http://www.gnu.org/licenses/>.

import numpy as np


def evaluator(obj_fn, simulations, evaluation, axis=0,
              transform=None, epsilon=None):
    """Evaluate the goodness of fit between one time series of simulated
    streamflow stored in a 1D array (or several time series of equal
    length stored in a 2D array) and one time series of the corresponding
    observed streamflow for the same period stored in a 1D array.

    :Parameters:

        obj_fn: `hydroeval` objective function
            The objective function to use to evaluate the goodness of
            fit between the *simulations* series and the *evaluation*
            series.

            *Parameter example:* ::

                obj_fn=nse

            *Parameter example:* ::

                obj_fn=kge

        simulations: `numpy.ndarray`
            The array of simulated streamflow values to be compared
            against the *observation* using the *obj_fn*. Note, the
            array can be one or two dimensional. If it is 2D, the time
            dimension must be the one specified through *axis*.

        evaluation: `numpy.ndarray`
            The array of observed streamflow values to be compared
            against the *simulations* using the *obj_fn*. Note, the
            array can be one or two dimensional. If it is 2D, the
            dimension specified through *axis* must be of size 1.
            Moreover, the length of the *evaluation* series must match
            the length of *simulations* series ― missing values must
            be set as `numpy.nan` so that pairwise deletion in both
            *simulations* and *evaluation* series can be performed prior
            the calculation of the *obj_fn*.

        axis: `int`, optional
            The axis along which the *simulations* and/or *evaluation*
            time dimension is, if any is a 2D array. If not provided,
            set to default value 0.

        transform: `str`, optional
            The transformation to apply to both the *simulations* and
            *evaluation* streamflow values **Q** prior the evaluation of
            the goodness of fit with the *obj_fn*. If not provided, set
            to default value `None` (i.e. no transformation). The
            supported transform arguments are listed in the table below.

            =========================  =================================
            transformations            details
            =========================  =================================
            ``'inv'``                  The reciprocal function
                                       **f(Q) = 1/Q** is applied.
            ``'sqrt'``                 The square root function
                                       **f(Q) = √Q** is applied.
            ``'log'``                  The natural logarithm function
                                       **f(Q) = ln(Q)** is applied.
            =========================  =================================

        epsilon: `float`, optional
            The value of the small constant ε to add to both the
            *simulations* and *evaluation* streamflow values **Q** prior
            the evaluation of the goodness of fit with the *obj_fn*
            when the *transform* is the reciprocal function or the
            natural logarithm since neither are defined for 0. If not
            provided, set to default value equal to one hundredth of
            the mean of the *evaluation* streamflow series, as
            recommended by `Pushpalatha et al. (2012)
            <https://doi.org/10.1016/j.jhydrol.2011.11.055>`_.

        """
    assert isinstance(simulations, np.ndarray)
    assert isinstance(evaluation, np.ndarray)
    assert (axis == 0) or (axis == 1)

    # check that the evaluation data provided is a single series of data
    if evaluation.ndim == 1:
        my_eval = np.reshape(evaluation, (evaluation.size, 1))
    elif evaluation.ndim == 2:
        if axis == 0:
            my_eval = evaluation
        else:
            my_eval = evaluation.T
    else:
        raise Exception('evaluation array contains more than 2 dimensions')
    if not my_eval.shape[1] == 1:
        raise Exception('evaluation array is not flat')

    # check the dimensions of the simulation data provided
    if simulations.ndim == 1:
        my_simu = np.reshape(simulations, (simulations.size, 1))
    elif simulations.ndim == 2:
        if axis == 0:
            my_simu = simulations
        else:
            my_simu = simulations.T
    else:
        raise Exception('simulation array contains more than 2 dimensions')

    # check that the two arrays have compatible lengths
    if not my_simu.shape[0] == my_eval.shape[0]:
        raise Exception('simulation and evaluation arrays feature '
                        'incompatible dimensions')

    # generate a subset of simulation and evaluation series
    # where evaluation data is available
    my_simu = my_simu[~np.isnan(my_eval[:, 0]), :]
    my_eval = my_eval[~np.isnan(my_eval[:, 0]), :]

    # transform the flow series if required
    if transform == 'log':  # log transformation
        if not epsilon:
            # determine an epsilon value to avoid log of zero
            # (following recommendation in Pushpalatha et al. (2012))
            epsilon = 0.01 * np.mean(my_eval)
        my_eval, my_simu = np.log(my_eval + epsilon), np.log(my_simu + epsilon)
    elif transform == 'inv':  # inverse transformation
        if not epsilon:
            # determine an epsilon value to avoid zero divide
            # (following recommendation in Pushpalatha et al. (2012))
            epsilon = 0.01 * np.mean(my_eval)
        my_eval, my_simu = 1.0 / (my_eval + epsilon), 1.0 / (my_simu + epsilon)
    elif transform == 'sqrt':  # square root transformation
        my_eval, my_simu = np.sqrt(my_eval), np.sqrt(my_simu)

    # calculate the requested function and return in the same array orientation
    if axis == 0:
        return obj_fn(my_simu, my_eval)
    else:
        return obj_fn(my_simu, my_eval).T
