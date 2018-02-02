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
      CalculationCommonMethods.CheckSimulationCondition(simCon, isThreeLevel);
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
      for (int index1 = 0; index1 < moduleNum; ++index1)
      {
        RthTrValue[index1] = (double) modTmp[index1].BaseInfo.RthTrValue;
        RthDiValue[index1] = (double) modTmp[index1].BaseInfo.RthDiValue;
        ThermalContactResistanceValue[index1] = (double) modTmp[index1].BaseInfo.ThermalContactResistanceValue;
        dtPIGBT[index1] = modSimResult[index1].dtPIGBT;
        dtFRD[index1] = modSimResult[index1].dtPFRD;
        modSimResult[index1].lt_Tr_Temp.Clear();
        modSimResult[index1].lt_Di_Temp.Clear();
        modSimResult[index1].lt_Temp_Rad.Clear();
        modSimResult[index1].lt_Temp_Time.Clear();
        modSimResult[index1].lt_Tr_Temp_Powerloss.Clear();
        modSimResult[index1].lt_Di_Temp_Powerloss.Clear();
        modSimResult[index1].dtTrTcmax = modSimResult[index1].dtTjIGBT - modSimResult[index1].dtdTjIGBT;
        modSimResult[index1].dtDiTcmax = modSimResult[index1].dtTjFRD - modSimResult[index1].dtdTjFRD;
        for (int index2 = 0; index2 < 360; ++index2)
        {
          numArray8[index2] = modSimResult[0].ltTime[index2];
          if (circuitType == CircuitType.Chopper)
            numArray8[index2] /= 1000.0;
          TrInstPowerLoss[index1, index2] = modSimResult[index1].lt_Tr_Powerloss[index2];
          DiInstPowerLoss[index1, index2] = modSimResult[index1].lt_Di_Powerloss[index2];
        }
      }
      List<int> intList = new List<int>();
      double resistanceByTime1 = modTmp[0].BaseInfo.GetTransisterTransientThermalResistanceByTime(10.0);
      double resistanceByTime2 = modTmp[0].BaseInfo.GetDiodeTransientThermalResistanceByTime(10.0);
      double secondsPerCycleDegree = circuitType == CircuitType.Chopper ? numArray8[1] - numArray8[0] : 1.0 / simCon.dtInputFo / 360.0;
      double time1 = circuitType == CircuitType.Chopper ? numArray8[0] : secondsPerCycleDegree / 2.0;
      double timeStep = 0.0;
      for (int index1 = 0; index1 < moduleNum; ++index1)
      {
        if (modTmp[index1].BaseInfo.TrFreqAndThermoDict.ContainsKey(secondsPerCycleDegree))
        {
          for (int index2 = 0; index2 < modTmp[index1].BaseInfo.TrFreqAndThermoDict[secondsPerCycleDegree].Count; ++index2)
          {
            TrFreqAndThermoDict[index1, index2] = modTmp[index1].BaseInfo.TrFreqAndThermoDict[secondsPerCycleDegree][index2];
            DiFreqAndThermoDict[index1, index2] = modTmp[index1].BaseInfo.DiFreqAndThermoDict[secondsPerCycleDegree][index2];
          }
        }
        else
        {
          intList.Add(index1);
          for (int index2 = 0; index2 < index1; ++index2)
          {
            if (modTmp[index2] == modTmp[index1])
              intList.Remove(index1);
          }
        }
      }
      while (time1 <= 10.0)
      {
        timeStep += secondsPerCycleDegree * 360.0;
        double resistanceByTime3 = modTmp[0].BaseInfo.GetTransisterTransientThermalResistanceByTime(timeStep);
        double resistanceByTime4 = modTmp[0].BaseInfo.GetDiodeTransientThermalResistanceByTime(timeStep);
        for (int index1 = 0; index1 < 360; ++index1)
        {
          foreach (int index2 in intList)
          {
            TrFreqAndThermoDict[index2, index1] += modTmp[index2].BaseInfo.GetTransisterTransientThermalResistanceByTime(time1);
            DiFreqAndThermoDict[index2, index1] += modTmp[index2].BaseInfo.GetDiodeTransientThermalResistanceByTime(time1);
          }
          time1 += secondsPerCycleDegree;
        }
        if (resistanceByTime3 / resistanceByTime1 >= 0.99 && resistanceByTime4 / resistanceByTime2 >= 0.99)
          break;
      }
      foreach (int index1 in intList)
      {
        modTmp[index1].BaseInfo.TrFreqAndThermoDict[secondsPerCycleDegree] = new List<double>();
        modTmp[index1].BaseInfo.DiFreqAndThermoDict[secondsPerCycleDegree] = new List<double>();
        for (int index2 = 0; index2 < 360; ++index2)
        {
          modTmp[index1].BaseInfo.TrFreqAndThermoDict[secondsPerCycleDegree].Add(TrFreqAndThermoDict[index1, index2]);
          modTmp[index1].BaseInfo.DiFreqAndThermoDict[secondsPerCycleDegree].Add(DiFreqAndThermoDict[index1, index2]);
        }
      }
      for (int index1 = 0; index1 < moduleNum; ++index1)
      {
        if (TrFreqAndThermoDict[index1, 0] == 0.0)
        {
          for (int index2 = 0; index2 < modTmp[index1].BaseInfo.TrFreqAndThermoDict[secondsPerCycleDegree].Count; ++index2)
          {
            TrFreqAndThermoDict[index1, index2] = modTmp[index1].BaseInfo.TrFreqAndThermoDict[secondsPerCycleDegree][index2];
            DiFreqAndThermoDict[index1, index2] = modTmp[index1].BaseInfo.DiFreqAndThermoDict[secondsPerCycleDegree][index2];
          }
        }
      }
      for (int index1 = 0; index1 < 360; ++index1)
      {
        for (int index2 = 0; index2 < moduleNum; ++index2)
        {
          TjIGBT[index2] = dtInputCaseTemp + dtPIGBT[index2] * RthTrValue[index2] + ThermalContactResistanceValue[index2] * (dtPIGBT[index2] + dtFRD[index2]);
          TjFWD[index2] = dtInputCaseTemp + dtFRD[index2] * RthDiValue[index2] + ThermalContactResistanceValue[index2] * (dtPIGBT[index2] + dtFRD[index2]);
          if (modTmp[index2].Segment != ModuleSegment.OneInOne && modTmp[index2].Segment != ModuleSegment.OneInOneDiode)
          {
            if (simCon.modType == ModulationType.MotorLock && (modTmp[index2].Segment == ModuleSegment.SixInOne || modTmp[index2].Segment == ModuleSegment.SevenInOne || modTmp[index2].Segment == ModuleSegment.CIB))
            {
              double num = (dtPIGBT[0] + dtFRD[1] + dtPIGBT[2] + dtFRD[3] + dtPIGBT[4] + dtFRD[5]) / 6.0;
              TjIGBT[index2] = dtInputCaseTemp + dtPIGBT[index2] * RthTrValue[index2] + ThermalContactResistanceValue[index2] * num;
              TjFWD[index2] = dtInputCaseTemp + dtFRD[index2] * RthDiValue[index2] + ThermalContactResistanceValue[index2] * num;
            }
            else if (circuitType != CircuitType.Sinusoidal || circuitType == CircuitType.Sinusoidal && (simCon.modType == ModulationType.TwoPhase2 || simCon.modType == ModulationType.HighSideChopping))
            {
              int index3 = index2 % 2 == 0 ? index2 + 1 : index2 - 1;
              double num = (dtPIGBT[index2] + dtFRD[index2] + dtPIGBT[index3] + dtFRD[index3]) / 2.0;
              TjIGBT[index2] = dtInputCaseTemp + dtPIGBT[index2] * RthTrValue[index2] + ThermalContactResistanceValue[index2] * num;
              TjFWD[index2] = dtInputCaseTemp + dtFRD[index2] * RthDiValue[index2] + ThermalContactResistanceValue[index2] * num;
            }
          }
          TjIGBT[index2] -= (TrInstPowerLoss[index2, 359] - dtPIGBT[index2]) * TrFreqAndThermoDict[index2, index1];
          TjFWD[index2] -= (DiInstPowerLoss[index2, 359] - dtFRD[index2]) * DiFreqAndThermoDict[index2, index1];
          TrFreqAndThermoDict[index2, index1] += modTmp[index2].BaseInfo.GetTransisterTransientThermalResistanceByTime(time1);
          DiFreqAndThermoDict[index2, index1] += modTmp[index2].BaseInfo.GetDiodeTransientThermalResistanceByTime(time1);
          TjIGBT[index2] += (TrInstPowerLoss[index2, 0] - dtPIGBT[index2]) * TrFreqAndThermoDict[index2, index1];
          TjFWD[index2] += (DiInstPowerLoss[index2, 0] - dtFRD[index2]) * DiFreqAndThermoDict[index2, index1];
        }
        time1 += secondsPerCycleDegree;
        for (int index2 = 1; index2 < 360; ++index2)
        {
          for (int index3 = 0; index3 < moduleNum; ++index3)
          {
            double TrPowerLossDelta = TrInstPowerLoss[index3, index2] - TrInstPowerLoss[index3, index2 - 1];
            double DiPowerLossDelta = DiInstPowerLoss[index3, index2] - DiInstPowerLoss[index3, index2 - 1];
            TjIGBT[index3] += TrPowerLossDelta * TrFreqAndThermoDict[index3, (360 + index1 - index2) % 360];
            TjFWD[index3] += DiPowerLossDelta * DiFreqAndThermoDict[index3, (360 + index1 - index2) % 360];
          }
        }
        for (int index2 = 0; index2 < moduleNum; ++index2)
        {
          modSimResult[index2].lt_Temp_Time.Add(modSimResult[index2].ltTime[index1] / 1000.0);
          modSimResult[index2].lt_Temp_Rad.Add((double) (index1 + 1));
          modSimResult[index2].lt_Tr_Temp.Add(TjIGBT[index2]);
          modSimResult[index2].lt_Tr_Temp_Powerloss.Add(TrInstPowerLoss[index2, index1]);
          modSimResult[index2].lt_Di_Temp.Add(TjFWD[index2]);
          modSimResult[index2].lt_Di_Temp_Powerloss.Add(DiInstPowerLoss[index2, index1]);
        }
      }
      CalculationCommonMethods.CalcTemperatureStatistics(modSimResult, moduleNum);
    }

    private static void CalcTemperatureStatistics(ModuleSimulationResult[] modSimResult, int moduleNum)
    {
      for (int index1 = 0; index1 < moduleNum; ++index1)
      {
        modSimResult[index1].dtTrAveTemp = modSimResult[index1].lt_Tr_Temp.Average();
        modSimResult[index1].dtDiAveTemp = modSimResult[index1].lt_Di_Temp.Average();
        double num1 = modSimResult[index1].dtTjIGBT - modSimResult[index1].dtTrAveTemp;
        double num2 = modSimResult[index1].dtTjFRD - modSimResult[index1].dtDiAveTemp;
        for (int index2 = 0; index2 < 360; ++index2)
        {
          List<double> ltTrTemp;
          int index3;
          (ltTrTemp = modSimResult[index1].lt_Tr_Temp)[index3 = index2] = ltTrTemp[index3] + num1;
          List<double> ltDiTemp;
          int index4;
          (ltDiTemp = modSimResult[index1].lt_Di_Temp)[index4 = index2] = ltDiTemp[index4] + num2;
          modSimResult[index1].lt_Temp_Time.Add(modSimResult[index1].lt_Temp_Time[359] + modSimResult[index1].lt_Temp_Time[index2]);
          modSimResult[index1].lt_Temp_Rad.Add((double) (360 + index2 + 1));
          modSimResult[index1].lt_Tr_Temp.Add(modSimResult[index1].lt_Tr_Temp[index2]);
          modSimResult[index1].lt_Tr_Temp_Powerloss.Add(modSimResult[index1].lt_Tr_Temp_Powerloss[index2]);
          modSimResult[index1].lt_Di_Temp.Add(modSimResult[index1].lt_Di_Temp[index2]);
          modSimResult[index1].lt_Di_Temp_Powerloss.Add(modSimResult[index1].lt_Di_Temp_Powerloss[index2]);
        }
        modSimResult[index1].dtTrMaxTemp = modSimResult[index1].lt_Tr_Temp.Max();
        modSimResult[index1].dtTrMinTemp = modSimResult[index1].lt_Tr_Temp.Min();
        modSimResult[index1].dtDiMaxTemp = modSimResult[index1].lt_Di_Temp.Max();
        modSimResult[index1].dtDiMinTemp = modSimResult[index1].lt_Di_Temp.Min();
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
