'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
import copy
import math

from SignalIntegrity.TimeDomain.Filters import WaveformTrimmer
from SignalIntegrity.SParameters.SParameters import SParameters
from SignalIntegrity.Wavelets.WaveletDenoiser import WaveletDenoiser

class TDRWaveformToSParameterConverter(object):
    sigmaMultiple=5
    def __init__(self,
                 WindowHalfWidthTime=0,
                 WindowRaisedCosineDuration=0,
                 Step=True,
                 Length=0,
                 Sigma=0,
                 Inverted=False
                 ):
        self.whwt=WindowHalfWidthTime
        self.wrcdr=WindowRaisedCosineDuration
        self.step=Step
        self.length=Length
        self.sigma=Sigma
        self.inverted=Inverted
    def Convert(self,wfListProvided,incidentIndex=0):
        # pragma: silent exclude
        wfList=copy.deepcopy(wfListProvided)
        if not isinstance(wfList, list):
            wfList=[wfList]
        # pragma: silent include
        if self.length!=0:
            lengthSamples=int(self.length*
                wfList[incidentIndex].TimeDescriptor().Fs+0.5)
            wfList=[wf*WaveformTrimmer(0,wf.TimeDescriptor().N-lengthSamples)
                for wf in wfList]
        if self.step:
            wfList=[wf.Derivative(removePoint=False)*(1./wf.TimeDescriptor().Fs) for wf in wfList]
        if self.inverted:
            wfList=[wf*-1. for wf in wfList]
        incwf=copy.deepcopy(wfList[incidentIndex])
        maxValueIndex=0
        maxValue=incwf[0]
        for k in range(1,len(incwf)):
            if incwf[k]>maxValue:
                maxValue=incwf[k]
                maxValueIndex=k
        sideSamples=int(self.whwt*incwf.TimeDescriptor().Fs)
        raisedCosineSamples=int(self.wrcdr*incwf.TimeDescriptor().Fs)
        for k in range(len(incwf)):
            if k<=maxValueIndex+sideSamples:
                pass
            elif k<=maxValueIndex+sideSamples+raisedCosineSamples:
                si=k-(maxValueIndex+sideSamples)
                f=float(si)/raisedCosineSamples
                incwf[k]=incwf[k]*(math.cos(f*math.pi)+1.)/2.
            else:
                incwf[k]=0.
        wfList[incidentIndex]=wfList[incidentIndex]-incwf
        if not self.sigma == 0:
            wfList=[WaveletDenoiser.DenoisedWaveform(wf,isDerivative=self.step,mult=5) for wf in wfList]
            incwf=WaveletDenoiser.DenoisedWaveform(incwf,isDerivative=self.step,mult=5)
        incwffc=incwf.FrequencyContent()
        res=[wf.FrequencyContent() for wf in wfList]
        for fc in res:
            for n in range(len(fc)):
                fc[n]=fc[n]/incwffc[n]
        # pragma: silent exclude
        if (len(res)==1) and (not isinstance(wfListProvided,list)):
            res=res[0]
        # pragma: include
        return res
    def RawMeasuredSParameters(self,wfList):
        # pragma: silent exclude
        wfList=copy.deepcopy(wfList)
        if not isinstance(wfList, list):
            wfList=[wfList]
        # pragma: silent include
        ports=len(wfList)
        S=[[None for _ in range(ports)] for _ in range(ports)]
        for d in range(ports):
            # pragma: silent exclude
            if not isinstance(wfList[d],list):
                wfList[d]=[wfList[d]]
            # pragma: include
            fc=self.Convert(wfList[d],d)
            for o in range(ports):
                S[o][d]=fc[o]
        f=S[0][0].Frequencies()
        return SParameters(f,
            [[[S[r][c][n] for c in range(ports)] for r in range(ports)]
            for n in range(len(f))])