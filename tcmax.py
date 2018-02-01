import math

R1TrPerR0Value = 0.012413952
R2TrPerJ0Value = 0.073850782
R3TrPerT0Value = 0.350547328
R4TrPerR1Value = 0.563187938
T1TrPerJ1Value = 0.0000196
T2TrPerT1Value = 0.001398007
T3TrValue = 0.017902919
T4TrValue = 0.094420415

R1aDiPerRd0Value = 0.012413952
R2aDiPerJd0Value = 0.073850782
R3aDiPerTd0Value = 0.350547328
R4aDiPerRd1Value = 0.563187938
T1aDiPerJd1Value = .0000196
T2aDiPerTd1Value = 0.001398007
T3aDiValue = 0.017902919
T4aDiValue = 0.094420415

def GetTransistorTransientThermalResistanceByTime(time):
    num1 = R1TrPerR0Value * (1.0 - math.exp(-1.0 * time / T1TrPerJ1Value))
    num2 = R2TrPerJ0Value * (1.0 - math.exp(-1.0 * time / T2TrPerT1Value))
    num3 = R3TrPerT0Value * (1.0 - math.exp(-1.0 * time /  T3TrValue))
    num4 = R4TrPerR1Value * (1.0 - math.exp(-1.0 * time /  T4TrValue))
    total_resistance = (num1+num2+num3+num4)*rth_tr_value
    return total_resistance

def GetDiodeTransientThermalResistanceByTime(time):
    num1 = R1aDiPerRd0Value * (1.0 - math.exp(-1.0 * time / T1aDiPerJd1Value))
    num2 = R2aDiPerJd0Value * (1.0 - math.exp(-1.0 * time / T2aDiPerTd1Value))
    num3 = R3aDiPerTd0Value * (1.0 - math.exp(-1.0 * time /  T3aDiValue))
    num4 = R4aDiPerRd1Value * (1.0 - math.exp(-1.0 * time /  T4aDiValue))
    total_resistance = (num1+num2+num3+num4)*rth_di_value
    return total_resistance


rth_tr_value = 0.048
rth_di_value = 0.076
thermal_contact_resistance_value = 0.0115

tr_tc_max = tj_tr - delta_tj_tr
fwd_tc_max = tj_fwd - delta_tj_fwd

tr_long_thermal_resistance = GetTransistorTransientThermalResistanceByTime(10.0)
fwd_long_thermal_resistance = GetDiodeTransientThermalResistanceByTime(10.0)
secondsPerCycleDegree = 1.0 / dtInputFo / 360.0
time1 = secondsPerCycleDegree / 2.0
timeStep = 0.0

TrFreqAndThermoDict = []
DiFreqAndThermoDict = []

while time1 <= 10.0:
    timeStep += secondsPerCycleDegree * 360.0
    resistanceByTime3 = GetTransistorTransientThermalResistanceByTime(timeStep)
    resistanceByTime4 = GetDiodeTransientThermalResistanceByTime(timeStep)
    for index1 in range (0,360):
        TrFreqAndThermoDict[index1] += GetTransistorTransientThermalResistanceByTime(time1)
        DiFreqAndThermoDict[index1] += GetDiodeTransientThermalResistanceByTime(time1)
        time1 += secondsPerCycleDegree
        if resistanceByTime3 / tr_long_thermal_resistance >= 0.99 and resistanceByTime4 / fwd_long_thermal_resistance >= 0.99:
            break

for index1 in range(0,360):
    for degree_count in range(0,360):
        TjIGBT[degree_count] = dtInputCaseTemp + dtPIGBT[degree_count] * RthTrValue[degree_count] + ThermalContactResistanceValue[degree_count] * (dtPIGBT[degree_count] + dtFRD[degree_count])
        TjFWD[degree_count] = dtInputCaseTemp + dtFRD[degree_count] * RthDiValue[degree_count] + ThermalContactResistanceValue[degree_count] * (dtPIGBT[degree_count] + dtFRD[degree_count])
        TjIGBT[degree_count] -= (TrInstPowerLoss[degree_count, 359] - dtPIGBT[degree_count]) * TrFreqAndThermoDict[degree_count, index1]
        TjFWD[degree_count] -= (DiInstPowerLoss[degree_count, 359] - dtFRD[degree_count]) * DiFreqAndThermoDict[degree_count, index1]
        TrFreqAndThermoDict[degree_count, index1] += modTmp[degree_count].BaseInfo.GetTransisterTransientThermalResistanceByTime(time1)
        DiFreqAndThermoDict[degree_count, index1] += modTmp[degree_count].BaseInfo.GetDiodeTransientThermalResistanceByTime(time1)
        TjIGBT[degree_count] += (TrInstPowerLoss[degree_count, 0] - dtPIGBT[degree_count]) * TrFreqAndThermoDict[degree_count, index1]
        TjFWD[degree_count] += (DiInstPowerLoss[degree_count, 0] - dtFRD[degree_count]) * DiFreqAndThermoDict[degree_count, index1]
    time1 += secondsPerCycleDegree
    for (int degree_count = 1 degree_count < 360 ++degree_count):
        for (int index3 = 0 index3 < moduleNum ++index3):
            double TrPowerLossDelta = TrInstPowerLoss[index3, degree_count] - TrInstPowerLoss[index3, degree_count - 1]
            double DiPowerLossDelta = DiInstPowerLoss[index3, degree_count] - DiInstPowerLoss[index3, degree_count - 1]
            TjIGBT[index3] += TrPowerLossDelta * TrFreqAndThermoDict[index3, (360 + index1 - degree_count) % 360]
            TjFWD[index3] += DiPowerLossDelta * DiFreqAndThermoDict[index3, (360 + index1 - degree_count) % 360]

    
    modSimResult.lt_Temp_Time.Add(modSimResult.ltTime / 1000.0)
    modSimResult.lt_Temp_Rad.Add((double) (index1 + 1))
    modSimResult.lt_Tr_Temp.Add(TjIGBT)
    modSimResult.lt_Tr_Temp_Powerloss.Add(TrInstPowerLoss[index2, ])
    modSimResult.lt_Di_Temp.Add(TjFWD)
    modSimResult.lt_Di_Temp_Powerloss.Add(DiInstPowerLoss[index2, ])
    
CalculationCommonMethods.CalcTemperatureStatistics(modSimResult, moduleNum)