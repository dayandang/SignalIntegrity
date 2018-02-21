"""differential RLGC transmission line"""
# Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
# Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
# All Rights Reserved.
# 
# Explicit license in accompanying README.txt file.  If you don't have that file
# or do not agree to the terms in that file, then you are not licensed to use
# this material whatsoever.

from SignalIntegrity.SParameters.SParameters import SParameters

import math

class TLineDifferentialRLGC(SParameters):
    """s-parameters of differential RLGC (telegrapher's) transmission line"""
    rtFraction=.01
    def __init__(self,f, Rp, Rsep, Lp, Gp, Cp, dfp,
                         Rn, Rsen, Ln, Gn, Cn, dfn,
                         Cm, dfm, Gm, Lm, Z0, K=0):
        """Constructor

        ports are 1,2,3,4 is +1,-1, +2, -2

        @param f list of float frequencies
        @param Rp float DC resistance of positive leg (Ohms)
        @param Rsep float skin-effect resistance of positive leg (Ohms/sqrt(Hz))
        @param Lp float inductance of positive leg (H)
        @param Gp float DC conductance of positive leg to ground (S)
        @param Cp float capacitance of positive leg to ground (F)
        @param dfp float dissipation factor (loss-tangent) of capacitance of positive leg to ground
        @param Rn float DC resistance of negative leg (Ohms)
        @param Rsen float skin-effect resistance of negative leg (Ohms/sqrt(Hz))
        @param Ln float inductance of negative leg (H)
        @param Gn float DC conductance of negative leg to ground (S)
        @param Cn float capacitance of negative leg to ground (F)
        @param dfn float dissipation factor (loss-tangent) of capacitance of negative leg to ground
        @param Cm float mutual capacitance (F)
        @param dfm float dissipation factor (loss-tangent) of mutual capacitance (F)
        @param Gm float mutual conductance (S)
        @param Lm float mutual inductance (H)
        @param Z0 float reference impedance
        @param K (optional) integer number of sections (defaults to zero)
        @note Regarding number of sections, an approximate solution will be computed
        as a distributed line with the number of sections specified using the class
        TLineDifferentialRLGCApproximate, unless the number provided is zero (the default).\n
        
        If zero is specified, then tests will be made
        for the appropriate analytic model to use according to the following table:

        | uncoupled | balanced |  Model                                             |
        |:--------: |:--------:|:---------------------------------------------------|
        |  True     | X        | TLineDifferentialRLGCUncoupled                     |
        |  False    | True     | TLineDifferentialRLGCBalanced                      |
        |  False    | False    | TLineDifferentialRLGCApproximate                   |

        If, because of imbalance and coupling, the approximate model must be used, the number of
        sections changed from K=0 specified to a value that will provided a very good numerical
        approximation.
        
        The calculation is such that round-trip propagation time (twice the electrical length)
        of any one small section is no more than one percent of the fastest possible risetime. 
        """
        balanced = Rp==Rn and Rsep==Rsen and Lp==Ln and Gp==Gn and Cp==Cn
        uncoupled = Cm==0 and (Cm != 0 and dfm==0) and Gm==0 and Lm==0
        if K != 0 or (not balanced and not uncoupled):
            # pragma: silent exclude
            from SignalIntegrity.SParameters.Devices.TLineDifferentialRLGCApproximate import TLineDifferentialRLGCApproximate
            # pragma: include
            if K==0:
                # max possible electrical length
                Td=math.sqrt((max(Lp,Ln)+Lm)*(max(Cp,Cn)+2*Cm))
                Rt=0.45/f[-1] # fastest risetime
                # sections such that fraction of risetime less than round trip
                # electrical length of one section
                K=int(math.ceil(Td*2/(Rt*self.rtFraction)))
            self.sp=TLineDifferentialRLGCApproximate(f,
                        Rp, Rsep, Lp, Gp, Cp, dfp,
                        Rn, Rsen, Ln, Gn, Cn, dfn,
                        Cm, dfm, Gm, Lm, Z0, K)
        elif uncoupled:
            # pragma: silent exclude
            from SignalIntegrity.SParameters.Devices.TLineDifferentialRLGCUncoupled import TLineDifferentialRLGCUncoupled
            # pragma: include
            self.sp=TLineDifferentialRLGCUncoupled(f,
                        Rp, Rsep, Lp, Gp, Cp, dfp,
                        Rn, Rsen, Ln, Gn, Cn, dfn,
                        Z0, K)
        elif balanced:
            # pragma: silent exclude
            from SignalIntegrity.SParameters.Devices.TLineDifferentialRLGCBalanced import TLineDifferentialRLGCBalanced
            # pragma: include
            self.sp=TLineDifferentialRLGCBalanced(f,
                        Rp, Rsep, Lp, Gp, Cp, dfp,
                        Cm, dfm, Gm, Lm, Z0, K)
        SParameters.__init__(self,f,None,Z0)
    def __getitem__(self,n):
        """overloads [n]
        @return list of list s-parameter matrix for the nth frequency element
        """
        return self.sp[n]