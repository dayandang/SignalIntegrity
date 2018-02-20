# Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
# Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
# All Rights Reserved.
# 
# Explicit license in accompanying README.txt file.  If you don't have that file
# or do not agree to the terms in that file, then you are not licensed to use
# this material whatsoever.

from numpy import empty

def Tee(P=None):
    """AtPackage si.dev.Tee
    Tee device
    @param P (optional) integer number of ports for the tee (default is three).
    @return the list of list s-parameter matrix for a tee connection.
    @remark A tee connection is a dot in a schematic.
    """
    if P is None:
        P=3
    mat=empty((P,P))
    mat.fill(2.0/P)
    for r in range(P):
        mat.itemset((r,r),(2.0-P)/P)
    return mat.tolist()
# pragma: silent exclude

def TeeThreePortSafe(Z,Z0=50.):
    D=3*(Z+Z0)
    DiagEle=(3*Z-Z0)/D
    OffDiagEle=2*Z0/D
    return [[DiagEle,OffDiagEle,OffDiagEle],
            [OffDiagEle,DiagEle,OffDiagEle],
            [OffDiagEle,OffDiagEle,DiagEle]]
