import unittest

import SignalIntegrity as si

from numpy import linalg
from numpy import matrix
from numpy import identity
from TestHelpers import *

class TestCommonElements(unittest.TestCase,SourcesTesterHelper,RoutineWriterTesterHelper):
    def __init__(self, methodName='runTest'):
        RoutineWriterTesterHelper.__init__(self)
        unittest.TestCase.__init__(self,methodName)
    def testDeviceShuntFourPort(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 2',
            'port 1 D 1 2 D 2 3 D 1 4 D 2'])
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),True)
        ssps.LaTeXSolution(size='big').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Shunt Device Four Port Symbolic')
    def testDeviceShuntFourPortNumericDeriv(self):
        Z=45.
        D=si.dev.SeriesZ(Z)
        resdef=si.dev.ShuntDeviceFourPort(D)
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 2',
            'port 1 D 1 2 D 2 3 D 1 4 D 2'])
        sspn=si.sd.SystemSParametersNumeric(sdp.SystemDescription())
        sspn.AssignSParameters('D',D)
        resderiv=sspn.SParameters()
        difference = linalg.norm(matrix(resdef)-matrix(resderiv))
        self.assertTrue(difference<1e-10,'Z Shunt Four Port derivation different than device')
    def testDeviceShuntFourPortNumericSimplifiedSymbolic(self):
        Z=45.
        D=si.dev.SeriesZ(Z)
        resdef=si.dev.ShuntDeviceFourPort(D)
        Wba=matrix([[-1./3,0,2./3,0],
        [0,-1./3,0,2./3],
        [2./3,0,-1./3,0],
        [0,2./3,0,-1./3]])
        Wbx=matrix([[0,0,2./3,0],
        [2./3,0,0,0],
        [0,0,2./3,0],
        [2./3,0,0,0]])
        Wxa=matrix([[0,0,0,0],
            [0,2./3,0,2./3],
            [0,0,0,0],
            [2./3,0,2./3,0]])
        Wxx=matrix([[0,D[1][1],0,D[1][0]],
            [-1./3,0,0,0],
            [0,D[0][1],0,D[0][0]],
            [0,0,-1./3,0]])
        I=matrix(identity(4))
        resderiv=matrix(Wba)+matrix(Wbx)*(I-matrix(Wxx)).getI()*matrix(Wxa)
        difference = linalg.norm(matrix(resdef)-matrix(resderiv))
        self.assertTrue(difference<1e-10,'Z Shunt Four Port derivation different than device')
    def testZShuntFourPort(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 2 ',
            'port 1 D 1 2 D 2 3 D 1 4 D 2'])
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),True)
        ssps.AssignSParameters('D',si.sy.SeriesZ('Z'))
        ssps.LaTeXSolution(size='big').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Shunt Z Four Port')
    def testZShuntFourPortSafeTee(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 2 ',
            'port 1 D 1 2 D 2 3 D 1 4 D 2'])
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),True)
        ssps.AssignSParameters('D',si.sy.SeriesZ('Z'))
        ssps.InstallSafeTees()
        ssps.LaTeXSolution(size='biggest').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Shunt Z Four Port')
    def testZShuntFourPortSymbolic(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 4','port 1 D 1 2 D 2 3 D 3 4 D 4'])
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),True,False)
        ssps.m_eqPrefix='\\begin{equation} '
        ssps.m_eqSuffix=' \\end{equation}'
        ssps.AssignSParameters('D',si.sy.ShuntZFourPort('Z'))
        ssps.LaTeXSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Z Shunt Four Port Symbolic')
    def testZShuntFourPortNumeric(self):
        Z=-34.45+1j*24.98
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 2',
            'port 1 D 1 2 D 2 3 D 1 4 D 2'])
        sspn=si.sd.SystemSParametersNumeric(sdp.SystemDescription())
        sspn.AssignSParameters('D',si.dev.SeriesZ(Z))
        rescalc=sspn.SParameters()
        rescorrect=si.dev.ShuntZFourPort(Z)
        difference = linalg.norm(matrix(rescalc)-matrix(rescorrect))
        self.assertTrue(difference<1e-10,'Z Shunt Four Port Numeric incorrect')
    def testZShuntThreePortPossibility1(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 2',
            'port 1 D 1 2 D 1 3 D 2'])
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),True)
        ssps.AssignSParameters('D',si.sy.SeriesZ('Z'))
        ssps.LaTeXSolution(size='big').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Shunt Z Three Port')
    def testZShuntThreePortPossibility2(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 4','device O 1 open',
            'port 1 D 1 2 D 3 3 D 2',
            'connect D 4 O 1'])
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),True,True)
        ssps.AssignSParameters('D',si.sy.ShuntZFourPort('Z'))
        ssps.LaTeXSolution(size='big').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Shunt Z Three Port')
    def testZShuntThreePortPossibility3(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 4','device Z 2',
            'port 1 D 1 2 D 3 3 D 2',
            'connect D 2 Z 2','connect Z 1 D 4'])
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),True)
        ssps.AssignSParameters('D',si.sy.ShuntZFourPort('Z'))
        ssps.AssignSParameters('Z',si.sy.SeriesZ('\\varepsilon'))
        ssps.LaTeXSolution(size='biggest').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Shunt Z Three Port')
    def testZShuntThreePortSymbolic(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 3','port 1 D 1 2 D 2 3 D 3'])
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),True,False)
        ssps.m_eqPrefix='\\begin{equation} '
        ssps.m_eqSuffix=' \\end{equation}'
        ssps.AssignSParameters('D',si.sy.ShuntZThreePort('Z'))
        ssps.LaTeXSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Z Shunt Three Port Symbolic')
    def testZShuntThreePortPossibility1Numeric(self):
        Z=-34.45+1j*24.98
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 2',
            'port 1 D 1 2 D 1 3 D 2'])
        sspn=si.sd.SystemSParametersNumeric(sdp.SystemDescription())
        sspn.AssignSParameters('D',si.dev.SeriesZ(Z))
        rescalc=sspn.SParameters()
        rescorrect=si.dev.ShuntZThreePort(Z)
        difference = linalg.norm(matrix(rescalc)-matrix(rescorrect))
        self.assertTrue(difference<1e-10,'Z Shunt Three Port Possibility 1 Numeric incorrect')
    def testZShuntThreePortPossibility2Numeric(self):
        Z=-34.45+1j*24.98
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 4','device O 1 open',
            'port 1 D 1 2 D 3 3 D 2',
            'connect D 4 O 1'])
        sspn=si.sd.SystemSParametersNumeric(sdp.SystemDescription())
        sspn.AssignSParameters('D',si.dev.ShuntZFourPort(Z))
        rescalc=sspn.SParameters()
        rescorrect=si.dev.ShuntZThreePort(Z)
        difference = linalg.norm(matrix(rescalc)-matrix(rescorrect))
        self.assertTrue(difference<1e-10,'Z Shunt Three Port Possibility 2 Numeric incorrect')
    def testZShuntThreePortPossibility3NumericDirectSave(self):
        Z=-34.45+1j*24.98
        Z=50.
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 4','device T 2 thru','connect T 1 D 2','connect T 1 D 4',
            'port 1 D 1 2 D 3 3 T 2'])
        sspn=si.sd.SystemSParametersNumeric(sdp.SystemDescription())
        sspn.AssignSParameters('D',si.dev.ShuntZFourPort(Z))
        sspn.InstallSafeTees()
        rescalc=sspn.SParameters(type='direct')
        rescorrect=si.dev.ShuntZThreePort(Z)
        difference = linalg.norm(matrix(rescalc)-matrix(rescorrect))
        self.assertTrue(difference<1e-10,'Z Shunt Three Port Possibility 3 Numeric incorrect')
    def testZShuntThreePortPossibility3NumericBlock(self):
        Z=-34.45+1j*24.98
        Z=50.
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 4','connect D 2 D 4',
            'port 1 D 1 2 D 3 3 D 2'])
        sspn=si.sd.SystemSParametersNumeric(sdp.SystemDescription())
        sspn.AssignSParameters('D',si.dev.ShuntZFourPort(Z))
        sspn.InstallSafeTees()
        rescalc=sspn.SParameters()
        rescorrect=si.dev.ShuntZThreePort(Z)
        difference = linalg.norm(matrix(rescalc)-matrix(rescorrect))
        self.assertTrue(difference<1e-6,'Z Shunt Three Port Possibility 3 Numeric incorrect')
    def testZShuntThreePortPossibility3NumericDirect(self):
        Z=-34.45+1j*24.98
        Z=50.
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 4','connect D 2 D 4',
            'port 1 D 1 2 D 3 3 D 2'])
        sspn=si.sd.SystemSParametersNumeric(sdp.SystemDescription())
        sspn.AssignSParameters('D',si.dev.ShuntZFourPort(Z))
        rescalc=sspn.SParameters(type='direct')
        rescorrect=si.dev.ShuntZThreePort(Z)
        difference = linalg.norm(matrix(rescalc)-matrix(rescorrect))
        self.assertTrue(difference<1e-10,'Z Shunt Three Port Possibility 3 Numeric incorrect')
    def testTeeNumeric(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 2 thru','port 1 D 1 2 D 1 3 D 2','connect D 2 D 2'])
        sspn=si.sd.SystemSParametersNumeric(sdp.SystemDescription())
        sspn.InstallSafeTees()
        rescalc1=sspn.SParameters()
        rescalc2=sspn.SParametersDirect()
        rescorrect=si.dev.Tee()
        difference = linalg.norm(matrix(rescalc1)-matrix(rescorrect))
        self.assertTrue(difference<1e-6,'Tee Numeric incorrect')
    def testZShuntTwoPortPossibility1(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 2','device G 1 ground',
            'port 1 D 1 2 D 1','connect D 2 G 1'])
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),True)
        ssps.AssignSParameters('D',si.sy.SeriesZ('Z'))
        ssps.LaTeXSolution(size='big').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Shunt Z Two Port')
    def testZShuntTwoPortPossibility2(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 3','device G 1 ground',
            'port 1 D 1 2 D 2','connect D 3 G 1'])
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),True)
        ssps.AssignSParameters('D',si.sy.ShuntZThreePort('Z'))
        ssps.LaTeXSolution(size='big').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Shunt Z Three Port')
    def testZShuntTwoPortSymbolic(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device D 2','port 1 D 1 2 D 2'])
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),True,False)
        ssps.m_eqPrefix='\\begin{equation} '
        ssps.m_eqSuffix=' \\end{equation}'
        ssps.AssignSParameters('D',si.sy.ShuntZTwoPort('Z'))
        ssps.LaTeXSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Z Shunt Three Port Symbolic')
    def testDeviceFourPortShuntCode(self):
        self.WriteCode('TestCommonElements.py','testDeviceShuntFourPort(self)',self.standardHeader)
    def testZShuntFourPortCode(self):
        self.WriteCode('TestCommonElements.py','testZShuntFourPort(self)',self.standardHeader)
    def testZShuntFourPortSafeTeeCode(self):
        self.WriteCode('TestCommonElements.py','testZShuntFourPortSafeTee(self)',self.standardHeader)
    def testZShuntThreePortCode(self):
        self.WriteCode('TestCommonElements.py','testZShuntThreePortPossibility2(self)',self.standardHeader)
    def testZShuntTwoPortCode(self):
        self.WriteCode('TestCommonElements.py','testZShuntTwoPortPossibility2(self)',self.standardHeader)
    def testZShuntThreePortPossibility3Code(self):
        self.WriteCode('TestCommonElements.py','testZShuntThreePortPossibility3(self)',self.standardHeader)

if __name__ == '__main__':
    unittest.main()

