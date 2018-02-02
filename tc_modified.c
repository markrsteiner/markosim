using System;
using System.Collections.Generic;
using System.Linq;

namespace bragarbarag.bragarbaragElectric.bragarbarag.Calc
{
  public static class CalculationCommonMethods
  {
    private static int moduleNum;

    public static void CheckSimulationCondition(SimulationCondition simCon, bool isThreeLevel = false)
    {

//    Checks that level is above zero for following variables:
//    voltage
//    current
//    mod depth
//    carrier freq
//    output freq
//    rg on
//    rg off

      simCon.dtInputV = CalculationCommonMethods.CheckLowerData(simCon.dtInputV);
      simCon.dtInputArms = CalculationCommonMethods.CheckLowerData(simCon.dtInputArms);
      simCon.dtInputM = CalculationCommonMethods.CheckLowerData(simCon.dtInputM);
      simCon.dtInputFc = CalculationCommonMethods.CheckLowerData(simCon.dtInputFc);
      simCon.dtInputFo = CalculationCommonMethods.CheckLowerData(simCon.dtInputFo);
      simCon.dtInputGateRegisterTr1On = CalculationCommonMethods.CheckLowerData(simCon.dtInputGateRegisterTr1On);
      simCon.dtInputGateRegisterTr1Off = CalculationCommonMethods.CheckLowerData(simCon.dtInputGateRegisterTr1Off);
      simCon.dtInputGateRegisterTr2On = CalculationCommonMethods.CheckLowerData(simCon.dtInputGateRegisterTr2On);
      simCon.dtInputGateRegisterTr2Off = CalculationCommonMethods.CheckLowerData(simCon.dtInputGateRegisterTr2Off);
      if (!isThreeLevel)
        return;
      simCon.dtInputGateRegisterTr3On = CalculationCommonMethods.CheckLowerData(simCon.dtInputGateRegisterTr3On);
      simCon.dtInputGateRegisterTr3Off = CalculationCommonMethods.CheckLowerData(simCon.dtInputGateRegisterTr3Off);
      simCon.dtInputGateRegisterTr4On = CalculationCommonMethods.CheckLowerData(simCon.dtInputGateRegisterTr4On);
      simCon.dtInputGateRegisterTr4Off = CalculationCommonMethods.CheckLowerData(simCon.dtInputGateRegisterTr4Off);
    }

    public static double CheckLowerData(double dtInput)
    {
      if (dtInput >= 0.0001)
        return dtInput;
      return 0.0001;
    }

    public static double CompareMax(double dtIn, double dtComp)
    {
      if (dtIn >= dtComp)
        return dtIn;
      return dtComp;
    }

    public static double CompareMin(double dtIn, double dtComp)
    {
      if (dtIn <= dtComp)
        return dtIn;
      return dtComp;
    }

    public static void InitialSimulationResult(ModuleSimulationResult[] modSimResult)
    {
//    Initializes variables used for calculations
      for (int index = 0; index < modSimResult.Length; ++index)
      {
        modSimResult[index].ltDivRad.Clear();
        modSimResult[index].ltTime.Clear();
        modSimResult[index].ltConVole.Clear();
        modSimResult[index].ltConIout.Clear();
        modSimResult[index].ltConVoleU.Clear();
        modSimResult[index].ltConVoleV.Clear();
        modSimResult[index].ltConVoleUV.Clear();
        modSimResult[index].ltDuty_P.Clear();
        modSimResult[index].ltDuty_N.Clear();
        modSimResult[index].lt_Di_Io.Clear();
        modSimResult[index].lt_Di_Powerloss.Clear();
        modSimResult[index].lt_Tr_Io.Clear();
        modSimResult[index].lt_Tr_Powerloss.Clear();
        modSimResult[index].dtPVCE = 0.0;
        modSimResult[index].dtEon = 0.0;
        modSimResult[index].dtEoff = 0.0;
        modSimResult[index].dtEon_Eoff = 0.0;
        modSimResult[index].dtPVF = 0.0;
        modSimResult[index].dtPVF_sbd = 0.0;
        modSimResult[index].dtEdsw = 0.0;
        modSimResult[index].dtPIGBT = 0.0;
        modSimResult[index].dtPFRD = 0.0;
        modSimResult[index].dtParm = 0.0;
        modSimResult[index].dtdTjIGBT = 0.0;
        modSimResult[index].dtdTjFRD = 0.0;
        modSimResult[index].dtdTc_f = 0.0;
        modSimResult[index].dtTjIGBT = 0.0;
        modSimResult[index].dtTjFRD = 0.0;
        modSimResult[index].dtTjmax = 0.0;
      }
    }

    public static void CalculationThermalResistance(SimulationCondition simCon, ModuleEntity[] modTmp, ModuleSimulationResult[] modSimResult, CircuitType circuitType, int moduleNum, bool isThreeLevel = false)
    {
//    Tj max calculation
      CalculationCommonMethods.CheckSimulationCondition(simCon, isThreeLevel);

      // initialize values
      double[] RthTrValue = new double[moduleNum];
      double[] RthDiValue = new double[moduleNum];
      double[] ThermalContactResistanceValue = new double[moduleNum];
      double[] dtPIGBT = new double[moduleNum];
      double[] dtFRD = new double[moduleNum];
      double[] TjIGBT = new double[moduleNum];
      double[] TjFWD = new double[moduleNum];
      double[] numArray8 = new double[720];
      double[,] TrInstPowerLoss = new double[moduleNum, 720];
      double[,] DiInstPowerLoss = new double[moduleNum, 720];
      double[,] TrFreqAndThermoDict = new double[moduleNum, 360];
      double[,] DiFreqAndThermoDict = new double[moduleNum, 360];
      double dtInputCaseTemp = simCon.dtInputCaseTemp;
      ///////

      for (int moduleCount = 0; moduleCount < moduleNum; ++moduleCount) //for each module
      {
        RthTrValue[moduleCount] = (double) modTmp[moduleCount].BaseInfo.RthTrValue; // get rth tr
        RthDiValue[moduleCount] = (double) modTmp[moduleCount].BaseInfo.RthDiValue; // get rth fwd
        ThermalContactResistanceValue[moduleCount] = (double) modTmp[moduleCount].BaseInfo.ThermalContactResistanceValue; // get tcr
        dtPIGBT[moduleCount] = modSimResult[moduleCount].dtPIGBT; // get pigbt
        dtFRD[moduleCount] = modSimResult[moduleCount].dtPFRD; //get pfwd
        modSimResult[moduleCount].lt_Tr_Temp.Clear(); //initialize this value
        modSimResult[moduleCount].lt_Di_Temp.Clear(); //initialize this value
        modSimResult[moduleCount].lt_Temp_Rad.Clear(); //initialize this value
        modSimResult[moduleCount].lt_Temp_Time.Clear(); //initialize this value
        modSimResult[moduleCount].lt_Tr_Temp_Powerloss.Clear(); //initialize this value
        modSimResult[moduleCount].lt_Di_Temp_Powerloss.Clear(); //initialize this value
        modSimResult[moduleCount].dtTrTcmax = modSimResult[moduleCount].dtTjIGBT - modSimResult[moduleCount].dtdTjIGBT; //find the max tc value
        modSimResult[moduleCount].dtDiTcmax = modSimResult[moduleCount].dtTjFRD - modSimResult[moduleCount].dtdTjFRD; //find the max tc value
        for (int degreeCount = 0; degreeCount < 360; ++degreeCount) //for each degree in a circle
        {
          numArray8[degreeCount] = modSimResult[0].ltTime[degreeCount]; //used for chopper calculations
//          if (circuitType == CircuitType.Chopper)
//            numArray8[degreeCount] /= 1000.0;
          TrInstPowerLoss[moduleCount, degreeCount] = modSimResult[moduleCount].lt_Tr_Powerloss[degreeCount]; //extract igbt loss into this array
          DiInstPowerLoss[moduleCount, degreeCount] = modSimResult[moduleCount].lt_Di_Powerloss[degreeCount]; //extract fwd loss into this array
        }
      }
      List<int> intList = new List<int>();
      double resistanceByTime1 = modTmp[0].BaseInfo.GetTransisterTransientThermalResistanceByTime(10.0); //get 10sec's transient thermal impedance igbt
      double resistanceByTime2 = modTmp[0].BaseInfo.GetDiodeTransientThermalResistanceByTime(10.0); // same as above, fwd
      double secondsPerCycleDegree = circuitType == CircuitType.Chopper ? numArray8[1] - numArray8[0] : 1.0 / simCon.dtInputFo / 360.0; //set sec/cycle*deg
      double time1 = circuitType == CircuitType.Chopper ? numArray8[0] : secondsPerCycleDegree / 2.0; //set time1
      double timeStep = 0.0; //init timestep
      for (int moduleCount = 0; moduleCount < moduleNum; ++moduleCount) //for each module
      {
        if (modTmp[moduleCount].BaseInfo.TrFreqAndThermoDict.ContainsKey(secondsPerCycleDegree)) //if thermo dict available
        {
          for (int dictCount = 0; dictCount < modTmp[moduleCount].BaseInfo.TrFreqAndThermoDict[secondsPerCycleDegree].Count; ++dictCount)
          {
            TrFreqAndThermoDict[moduleCount, dictCount] = modTmp[moduleCount].BaseInfo.TrFreqAndThermoDict[secondsPerCycleDegree][dictCount]; //extract freq and thermo dict for each module
            DiFreqAndThermoDict[moduleCount, dictCount] = modTmp[moduleCount].BaseInfo.DiFreqAndThermoDict[secondsPerCycleDegree][dictCount]; //extract freq and thermo dict for each module
          }
        }
        else
        {
          intList.Add(moduleCount);
          for (int moduleCountAux = 0; moduleCountAux < moduleCount; ++moduleCountAux)
          {
            if (modTmp[moduleCountAux] == modTmp[moduleCount])
              intList.Remove(moduleCount);
          }
        }
      }
      while (time1 <= 10.0) //until 10sec
      {
        timeStep += secondsPerCycleDegree * 360.0; //add 1 full cycle to timestep
        double resistanceByTime3 = modTmp[0].BaseInfo.GetTransisterTransientThermalResistanceByTime(timeStep); //get igbt transient rth for 1 cycle later
        double resistanceByTime4 = modTmp[0].BaseInfo.GetDiodeTransientThermalResistanceByTime(timeStep); // same as above, fwd
        for (int degreeCount = 0; degreeCount < 360; ++degreeCount)
        {
          foreach (int moduleCount in intList)
          {
            TrFreqAndThermoDict[moduleCount, degreeCount] += modTmp[moduleCount].BaseInfo.GetTransisterTransientThermalResistanceByTime(time1);  //get trans rth at time1 igbt
            DiFreqAndThermoDict[moduleCount, degreeCount] += modTmp[moduleCount].BaseInfo.GetDiodeTransientThermalResistanceByTime(time1); //same as above, fwd
          }
          time1 += secondsPerCycleDegree; //increment
        }
        if (resistanceByTime3 / resistanceByTime1 >= 0.99 && resistanceByTime4 / resistanceByTime2 >= 0.99) //stop when we get to within 99% of 10sec rth
          break;
      }
      foreach (int moduleCount in intList)
      {
        modTmp[moduleCount].BaseInfo.TrFreqAndThermoDict[secondsPerCycleDegree] = new List<double>();
        modTmp[moduleCount].BaseInfo.DiFreqAndThermoDict[secondsPerCycleDegree] = new List<double>();
        for (int degreeCount = 0; degreeCount < 360; ++degreeCount) //not sure what this does exactly
        {
          modTmp[moduleCount].BaseInfo.TrFreqAndThermoDict[secondsPerCycleDegree].Add(TrFreqAndThermoDict[moduleCount, degreeCount]);
          modTmp[moduleCount].BaseInfo.DiFreqAndThermoDict[secondsPerCycleDegree].Add(DiFreqAndThermoDict[moduleCount, degreeCount]);
        }
      }
      for (int moduleCount = 0; moduleCount < moduleNum; ++moduleCount) //not sure what this does
      {
        if (TrFreqAndThermoDict[moduleCount, 0] == 0.0)
        {
          for (int moduleCountAux = 0; moduleCountAux < modTmp[moduleCount].BaseInfo.TrFreqAndThermoDict[secondsPerCycleDegree].Count; ++moduleCountAux)
          {
            TrFreqAndThermoDict[moduleCount, moduleCountAux] = modTmp[moduleCount].BaseInfo.TrFreqAndThermoDict[secondsPerCycleDegree][moduleCountAux];
            DiFreqAndThermoDict[moduleCount, moduleCountAux] = modTmp[moduleCount].BaseInfo.DiFreqAndThermoDict[secondsPerCycleDegree][moduleCountAux];
          }
        }
      }
      for (int degreeCount = 0; degreeCount < 360; ++degreeCount)
      {
        for (int moduleCount = 0; moduleCount < moduleNum; ++moduleCount)
        {
          TjIGBT[moduleCount] = dtInputCaseTemp + dtPIGBT[moduleCount] * RthTrValue[moduleCount] + ThermalContactResistanceValue[moduleCount] * (dtPIGBT[moduleCount] + dtFRD[moduleCount]);
          TjFWD[moduleCount] = dtInputCaseTemp + dtFRD[moduleCount] * RthDiValue[moduleCount] + ThermalContactResistanceValue[moduleCount] * (dtPIGBT[moduleCount] + dtFRD[moduleCount]);
//          if (modTmp[moduleCount].Segment != ModuleSegment.OneInOne && modTmp[moduleCount].Segment != ModuleSegment.OneInOneDiode)
//          {
//            if (simCon.modType == ModulationType.MotorLock && (modTmp[moduleCount].Segment == ModuleSegment.SixInOne || modTmp[moduleCount].Segment == ModuleSegment.SevenInOne || modTmp[moduleCount].Segment == ModuleSegment.CIB))
//            {
//              double num = (dtPIGBT[0] + dtFRD[1] + dtPIGBT[2] + dtFRD[3] + dtPIGBT[4] + dtFRD[5]) / 6.0;
//              TjIGBT[moduleCount] = dtInputCaseTemp + dtPIGBT[moduleCount] * RthTrValue[moduleCount] + ThermalContactResistanceValue[moduleCount] * num;
//              TjFWD[moduleCount] = dtInputCaseTemp + dtFRD[moduleCount] * RthDiValue[moduleCount] + ThermalContactResistanceValue[moduleCount] * num;
//            }
//            else if (circuitType != CircuitType.Sinusoidal || circuitType == CircuitType.Sinusoidal && (simCon.modType == ModulationType.TwoPhase2 || simCon.modType == ModulationType.HighSideChopping))
//            {
//              int moduleCountAux2 = moduleCount % 2 == 0 ? moduleCount + 1 : moduleCount - 1;
//              double num = (dtPIGBT[moduleCount] + dtFRD[moduleCount] + dtPIGBT[moduleCountAux2] + dtFRD[moduleCountAux2]) / 2.0;
//              TjIGBT[moduleCount] = dtInputCaseTemp + dtPIGBT[moduleCount] * RthTrValue[moduleCount] + ThermalContactResistanceValue[moduleCount] * num;
//              TjFWD[moduleCount] = dtInputCaseTemp + dtFRD[moduleCount] * RthDiValue[moduleCount] + ThermalContactResistanceValue[moduleCount] * num;
//            }
//          }

          TjIGBT[moduleCount] -= (TrInstPowerLoss[moduleCount, 359] - dtPIGBT[moduleCount]) * TrFreqAndThermoDict[moduleCount, degreeCount];
          TjFWD[moduleCount] -= (DiInstPowerLoss[moduleCount, 359] - dtFRD[moduleCount]) * DiFreqAndThermoDict[moduleCount, degreeCount];
          TrFreqAndThermoDict[moduleCount, degreeCount] += modTmp[moduleCount].BaseInfo.GetTransisterTransientThermalResistanceByTime(time1);
          DiFreqAndThermoDict[moduleCount, degreeCount] += modTmp[moduleCount].BaseInfo.GetDiodeTransientThermalResistanceByTime(time1);
          TjIGBT[moduleCount] += (TrInstPowerLoss[moduleCount, 0] - dtPIGBT[moduleCount]) * TrFreqAndThermoDict[moduleCount, degreeCount];
          TjFWD[moduleCount] += (DiInstPowerLoss[moduleCount, 0] - dtFRD[moduleCount]) * DiFreqAndThermoDict[moduleCount, degreeCount];
        }
        time1 += secondsPerCycleDegree;
        for (int degreeCountAux = 1; degreeCountAux < 360; ++degreeCountAux)
        {
          for (int moduleCount = 0; moduleCount < moduleNum; ++moduleCount)
          {
            double TrPowerLossDelta = TrInstPowerLoss[moduleCount, degreeCountAux] - TrInstPowerLoss[moduleCount, degreeCountAux - 1];
            double DiPowerLossDelta = DiInstPowerLoss[moduleCount, degreeCountAux] - DiInstPowerLoss[moduleCount, degreeCountAux - 1];
            TjIGBT[moduleCount] += TrPowerLossDelta * TrFreqAndThermoDict[moduleCount, (360 + degreeCount - degreeCountAux) % 360];
            TjFWD[moduleCount] += DiPowerLossDelta * DiFreqAndThermoDict[moduleCount, (360 + degreeCount - degreeCountAux) % 360];
          }
        }
        for (int moduleCount = 0; moduleCount < moduleNum; ++moduleCount)
        {
          modSimResult[moduleCount].lt_Temp_Time.Add(modSimResult[moduleCount].ltTime[degreeCount] / 1000.0);
          modSimResult[moduleCount].lt_Temp_Rad.Add((double) (degreeCount + 1));
          modSimResult[moduleCount].lt_Tr_Temp.Add(TjIGBT[moduleCount]);
          modSimResult[moduleCount].lt_Tr_Temp_Powerloss.Add(TrInstPowerLoss[moduleCount, degreeCount]);
          modSimResult[moduleCount].lt_Di_Temp.Add(TjFWD[moduleCount]);
          modSimResult[moduleCount].lt_Di_Temp_Powerloss.Add(DiInstPowerLoss[moduleCount, degreeCount]);
        }
      }
      CalculationCommonMethods.CalcTemperatureStatistics(modSimResult, moduleNum);
    }

    private static void CalcTemperatureStatistics(ModuleSimulationResult[] modSimResult, int moduleNum)
    {
      for (int moduleCount = 0; moduleCount < moduleNum; ++moduleCount)
      {
        modSimResult[moduleCount].dtTrAveTemp = modSimResult[moduleCount].lt_Tr_Temp.Average();
        modSimResult[moduleCount].dtDiAveTemp = modSimResult[moduleCount].lt_Di_Temp.Average();
        double num1 = modSimResult[moduleCount].dtTjIGBT - modSimResult[moduleCount].dtTrAveTemp;
        double num2 = modSimResult[moduleCount].dtTjFRD - modSimResult[moduleCount].dtDiAveTemp;
        for (int index2 = 0; index2 < 360; ++index2)
        {
          List<double> ltTrTemp;
          int index3;
          (ltTrTemp = modSimResult[moduleCount].lt_Tr_Temp)[index3 = index2] = ltTrTemp[index3] + num1;
          List<double> ltDiTemp;
          int index4;
          (ltDiTemp = modSimResult[moduleCount].lt_Di_Temp)[index4 = index2] = ltDiTemp[index4] + num2;
          modSimResult[moduleCount].lt_Temp_Time.Add(modSimResult[moduleCount].lt_Temp_Time[359] + modSimResult[moduleCount].lt_Temp_Time[index2]);
          modSimResult[moduleCount].lt_Temp_Rad.Add((double) (360 + index2 + 1));
          modSimResult[moduleCount].lt_Tr_Temp.Add(modSimResult[moduleCount].lt_Tr_Temp[index2]);
          modSimResult[moduleCount].lt_Tr_Temp_Powerloss.Add(modSimResult[moduleCount].lt_Tr_Temp_Powerloss[index2]);
          modSimResult[moduleCount].lt_Di_Temp.Add(modSimResult[moduleCount].lt_Di_Temp[index2]);
          modSimResult[moduleCount].lt_Di_Temp_Powerloss.Add(modSimResult[moduleCount].lt_Di_Temp_Powerloss[index2]);
        }
        modSimResult[moduleCount].dtTrMaxTemp = modSimResult[moduleCount].lt_Tr_Temp.Max();
        modSimResult[moduleCount].dtTrMinTemp = modSimResult[moduleCount].lt_Tr_Temp.Min();
        modSimResult[moduleCount].dtDiMaxTemp = modSimResult[moduleCount].lt_Di_Temp.Max();
        modSimResult[moduleCount].dtDiMinTemp = modSimResult[moduleCount].lt_Di_Temp.Min();
      }
    }

    public static void UpdateMaxAndMinTempByAverage(ModuleSimulationResult[] modSimResults, int targetModuleIndex, int module1Index, int module2Index)
    {
      modSimResults[targetModuleIndex].dtTrMaxTemp = (modSimResults[module1Index].dtTrMaxTemp + modSimResults[module2Index].dtTrMaxTemp) / 2.0;
      modSimResults[targetModuleIndex].dtTrMinTemp = (modSimResults[module1Index].dtTrMinTemp + modSimResults[module2Index].dtTrMinTemp) / 2.0;
      modSimResults[targetModuleIndex].dtDiMaxTemp = (modSimResults[module1Index].dtDiMaxTemp + modSimResults[module2Index].dtDiMaxTemp) / 2.0;
      modSimResults[targetModuleIndex].dtDiMinTemp = (modSimResults[module1Index].dtDiMinTemp + modSimResults[module2Index].dtDiMinTemp) / 2.0;
    }

    public static void CalcPowerLossSharePakage(ModuleSimulationResult modSimResultA, ModuleEntity modEntA, ModuleSimulationResult modSimResultB, ModuleEntity modEntB, double dtInputCaseTemp)
    {
      modSimResultA.dtParm = (modSimResultA.dtPIGBT + modSimResultA.dtPFRD + modSimResultB.dtPIGBT + modSimResultB.dtPFRD) / 2.0;
      modSimResultB.dtParm = (modSimResultA.dtPIGBT + modSimResultA.dtPFRD + modSimResultB.dtPIGBT + modSimResultB.dtPFRD) / 2.0;
      modSimResultA.dtdTjIGBT = modSimResultA.dtPIGBT * ConvertUtility.DoubleParseImprement(modEntA.BaseInfo.RthTrValue.ToString());
      modSimResultA.dtdTjFRD = modSimResultA.dtPFRD * ConvertUtility.DoubleParseImprement(modEntA.BaseInfo.RthDiValue.ToString());
      modSimResultA.dtdTc_f = modSimResultA.dtParm * ConvertUtility.DoubleParseImprement(modEntA.BaseInfo.ThermalContactResistanceValue.ToString());
      modSimResultA.dtTjIGBT = modSimResultA.dtdTjIGBT + modSimResultA.dtdTc_f + dtInputCaseTemp;
      modSimResultA.dtTjFRD = modSimResultA.dtdTjFRD + modSimResultA.dtdTc_f + dtInputCaseTemp;
      modSimResultA.dtTjmax = CalculationCommonMethods.CompareMax(modSimResultA.dtTjIGBT, modSimResultA.dtTjFRD);
      modSimResultB.dtdTjIGBT = modSimResultB.dtPIGBT * ConvertUtility.DoubleParseImprement(modEntB.BaseInfo.RthTrValue.ToString());
      modSimResultB.dtdTjFRD = modSimResultB.dtPFRD * ConvertUtility.DoubleParseImprement(modEntB.BaseInfo.RthDiValue.ToString());
      modSimResultB.dtdTc_f = modSimResultB.dtParm * ConvertUtility.DoubleParseImprement(modEntB.BaseInfo.ThermalContactResistanceValue.ToString());
      modSimResultB.dtTjIGBT = modSimResultB.dtdTjIGBT + modSimResultB.dtdTc_f + dtInputCaseTemp;
      modSimResultB.dtTjFRD = modSimResultB.dtdTjFRD + modSimResultB.dtdTc_f + dtInputCaseTemp;
      modSimResultB.dtTjmax = CalculationCommonMethods.CompareMax(modSimResultB.dtTjIGBT, modSimResultB.dtTjFRD);
    }

    public static void CalcPowerLossSharePakage(ModuleSimulationResult[] modSimResults, ModuleEntity modEnt, double dtInputCaseTemp)
    {
      double averageParm = 0.0;
      ((IEnumerable<ModuleSimulationResult>) modSimResults).ToList<ModuleSimulationResult>().ForEach((Action<ModuleSimulationResult>) (m => averageParm += (m.dtPIGBT + m.dtPFRD) / 6.0));
      ((IEnumerable<ModuleSimulationResult>) modSimResults).ToList<ModuleSimulationResult>().ForEach((Action<ModuleSimulationResult>) (m =>
      {
        m.dtdTc_f = averageParm * ConvertUtility.DoubleParseImprement(modEnt.BaseInfo.ThermalContactResistanceValue.ToString());
        m.dtTjIGBT = m.dtdTjIGBT + m.dtdTc_f + dtInputCaseTemp;
        m.dtTjFRD = m.dtdTjFRD + m.dtdTc_f + dtInputCaseTemp;
        m.dtTjmax = CalculationCommonMethods.CompareMax(m.dtTjIGBT, m.dtTjFRD);
      }));
    }

    public static void PareringCalculation(ModuleSimulationResult modSimResultA, ModuleSimulationResult modSimResultB)
    {
      modSimResultB.dtDiAveTemp = modSimResultA.dtDiAveTemp;
      modSimResultB.dtDiFcProperty = modSimResultA.dtDiFcProperty;
      modSimResultB.dtDiMaxTemp = modSimResultA.dtDiMaxTemp;
      modSimResultB.dtDiMinTemp = modSimResultA.dtDiMinTemp;
      modSimResultB.dtDiTcmax = modSimResultA.dtDiTcmax;
      modSimResultB.dtdTc_f = modSimResultA.dtdTc_f;
      modSimResultB.dtdTjFRD = modSimResultA.dtdTjFRD;
      modSimResultB.dtdTjIGBT = modSimResultA.dtdTjIGBT;
      modSimResultB.dtEdsw = modSimResultA.dtEdsw;
      modSimResultB.dtEoff = modSimResultA.dtEoff;
      modSimResultB.dtEon_Eoff = modSimResultA.dtEon_Eoff;
      modSimResultB.dtEon = modSimResultA.dtEon;
      modSimResultB.dtParm = modSimResultA.dtParm;
      modSimResultB.dtPFRD = modSimResultA.dtPFRD;
      modSimResultB.dtPIGBT = modSimResultA.dtPIGBT;
      modSimResultB.dtPVCE = modSimResultA.dtPVCE;
      modSimResultB.dtPVF = modSimResultA.dtPVF;
      modSimResultB.dtPVF_sbd = modSimResultA.dtPVF_sbd;
      modSimResultB.dtTjFRD = modSimResultA.dtTjFRD;
      modSimResultB.dtTjIGBT = modSimResultA.dtTjIGBT;
      modSimResultB.dtTjmax = modSimResultA.dtTjmax;
      modSimResultB.dtTjmaxDi = modSimResultA.dtTjmaxDi;
      modSimResultB.dtTrAveTemp = modSimResultA.dtTrAveTemp;
      modSimResultB.dtTrFcProperty = modSimResultA.dtTrFcProperty;
      modSimResultB.dtTrMaxTemp = modSimResultA.dtTrMaxTemp;
      modSimResultB.dtTrMinTemp = modSimResultA.dtTrMinTemp;
      modSimResultB.dtTrTcmax = modSimResultA.dtTrTcmax;
    }
  }
}
