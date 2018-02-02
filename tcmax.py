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

dtInputFo = 60
dtInputCaseTemp = 50

dtPIGBT = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0011525630328873089,
           0.010362188395864568, 0.020247593699251741, 0.030811461962555999, 0.042058319354984011, 0.053991433019874704,
           0.066630479873903678, 0.080120750969570664, 0.094351160204587045, 0.10932027247219207, 0.12502517891104978,
           0.14147166472885384, 0.15882831109016621, 0.1769364096946901, 0.1957871135844152, 0.21536999230890053,
           0.23567303459816874, 0.25668982875119356, 0.27839966889019724, 0.30078516860558385, 0.32382808393702656,
           0.347508656037891, 0.37173496158609459, 0.39650372452640553, 0.42183217971804732, 0.44769498594969481,
           0.4740654669379854, 0.50088045872269349, 0.52790657111369998, 0.55533548766699081, 0.58313618569398262,
           0.61127658305332044, 0.63972359301121684, 0.66836921679188044, 0.69711543935214715, 0.72605421266911108,
           0.75514950914670842, 0.78436462665283091, 0.813662255622986, 0.84272124118467495, 0.87053131683846841,
           0.89826306461719163, 0.92588121228506015, 0.95335032329895464, 0.98063486231027464, 1.0076992612184359,
           1.0346025277962556, 1.0613488476158999, 1.087772124719145, 1.1138367463725114, 1.1395073973036167,
           1.1647491273491311, 1.1895274186012452, 1.2138082518991153, 1.2377844803287152, 1.2612941520620715,
           1.2842072762451713, 1.3064916553530515, 1.3281159188721259, 1.3490495846858539, 1.3692631187449746,
           1.3887279928844511, 1.4074167406535292, 1.425331080209898, 1.4425264743104838, 1.4588671509564253,
           1.4742440263973844, 1.4887159320368621, 1.5022708661570106, 1.5148900875503482, 1.5265562815553746,
           1.5372535930173812, 1.5469676562185444, 1.5556856217098913, 1.5633961799851419, 1.5700895819440048,
           1.5757576561002236, 1.5803938224974654, 1.58397840591544, 1.5864805987909647, 1.587945830781585,
           1.588374036344425, 1.5877667446623256, 1.5861270734700739, 1.58345971959881, 1.5797709462653868,
           1.5750685671411842, 1.5693619272425681, 1.5626618806926877, 1.5549807654117667, 1.5463323748002464,
           1.5367319264862727, 1.5261960282158982, 1.5147426409710567, 1.5023910394068605, 1.4891617697059769,
           1.4750766049538302, 1.460158498144084, 1.4444315329292643, 1.4279208722365062, 1.4106527048732516,
           1.392654190252151, 1.3739526135633877, 1.354524399876925, 1.3344497505223758, 1.3137593555416747,
           1.2924845816483546, 1.2706574078233484, 1.248310360021524, 1.2254764451436575, 1.2021890844297181,
           1.1784820464301937, 1.1543893797125533, 1.1299453454599755, 1.1051843501191025, 1.0801163471361668,
           1.0547539360496792, 1.0291840052918737, 1.003529747920598, 0.97773020637976193, 0.95181918676147959,
           0.92583018491073377, 0.89979632514421304, 0.87375030034061452, 0.84772431353374578, 0.82175002113534357,
           0.79585847790981357, 0.77019555194624412, 0.74476115748836857, 0.71949194912590797, 0.69441564727016114,
           0.66955915112160858, 0.64494849733525983, 0.62060882105585635, 0.59656431939600429, 0.57294587835202726,
           0.54968258895190325, 0.52677477172055742, 0.50424240560951605, 0.48210440840403135, 0.46037861617835174,
           0.43902445802861856, 0.41740895001173822, 0.39630268131317442, 0.3757193263492144, 0.35567126806307164,
           0.3361695950276099, 0.31722410166913723, 0.2987592196211174, 0.28086410385157801, 0.26355454464305672,
           0.24683513900466519, 0.23070921652551674, 0.21516432718926534, 0.20012263877811695, 0.18568839784178828,
           0.17185983043400319, 0.15863398965330991, 0.14600678855430632, 0.13394609235799479, 0.12246185599458892,
           0.11156283303911887, 0.10124056091461821, 0.091485625132869786, 0.082288622348383411, 0.073638855578363083,
           0.065522520867644526, 0.057926892209298246, 0.050838537159590927, 0.044254686435731438, 0.038186122025487046,
           0.032568562602248351, 0.027387054752909982, 0.022626215909899682, 0.018276272478899635, 0.014341655398657224,
           0.010764138493021436, 0.0075284039984104077, 0.0046189613479988775, 0.0020209875812569784, 0.0, 0.0, 0.0,
           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def GetTransistorTransientThermalResistanceByTime(time):
    num1 = R1TrPerR0Value * (1.0 - math.exp(-1.0 * time / T1TrPerJ1Value))
    num2 = R2TrPerJ0Value * (1.0 - math.exp(-1.0 * time / T2TrPerT1Value))
    num3 = R3TrPerT0Value * (1.0 - math.exp(-1.0 * time / T3TrValue))
    num4 = R4TrPerR1Value * (1.0 - math.exp(-1.0 * time / T4TrValue))
    total_resistance = (num1 + num2 + num3 + num4) * rth_tr_value
    return total_resistance


def GetDiodeTransientThermalResistanceByTime(time):
    num1 = R1aDiPerRd0Value * (1.0 - math.exp(-1.0 * time / T1aDiPerJd1Value))
    num2 = R2aDiPerJd0Value * (1.0 - math.exp(-1.0 * time / T2aDiPerTd1Value))
    num3 = R3aDiPerTd0Value * (1.0 - math.exp(-1.0 * time / T3aDiValue))
    num4 = R4aDiPerRd1Value * (1.0 - math.exp(-1.0 * time / T4aDiValue))
    total_resistance = (num1 + num2 + num3 + num4) * rth_di_value
    return total_resistance


rth_tr_value = 0.048
rth_di_value = 0.076
thermal_contact_resistance_value = 0.0115

# tr_tc_max = tj_tr - delta_tj_tr
# fwd_tc_max = tj_fwd - delta_tj_fwd

tr_long_thermal_resistance = GetTransistorTransientThermalResistanceByTime(10.0)
fwd_long_thermal_resistance = GetDiodeTransientThermalResistanceByTime(10.0)
secondsPerCycleDegree = 1.0 / dtInputFo / 360.0
time1 = secondsPerCycleDegree / 2.0
timeStep = 0.0

TrFreqAndThermoDict = [0 for i in range(360)]
DiFreqAndThermoDict = [0 for i in range(360)]
TjIGBT = [0 for i in range(360)]
TjPIGBT = [0 for i in range(360)]
TjFWD = [0 for i in range(360)]
dtFRD = [0 for i in range(360)]
RthDiValue = [0 for i in range(360)]
RthTrValue = [0 for i in range(360)]
ThermalContactResistanceValue = [0 for i in range(360)]
TrInstPowerLoss = [0 for i in range(360)]
DiInstPowerLoss = [0 for i in range(360)]
lt_Temp_Time = [0 for i in range(360)]
lt_Temp_Rad = [0 for i in range(360)]
lt_Tr_Temp = [0 for i in range(360)]
lt_Tr_Temp_Powerloss = [0 for i in range(360)]
lt_Di_Temp = [0 for i in range(360)]
lt_Di_Temp_Powerloss = [0 for i in range(360)]

while time1 <= 10.0:
    timeStep += secondsPerCycleDegree * 360.0
    resistanceByTime3 = GetTransistorTransientThermalResistanceByTime(timeStep)
    resistanceByTime4 = GetDiodeTransientThermalResistanceByTime(timeStep)
    for index1 in range(0, 360):
        # TrFreqAndThermoDict[index1] += GetTransistorTransientThermalResistanceByTime(time1)
        # DiFreqAndThermoDict[index1] = GetDiodeTransientThermalResistanceByTime(time1)
        time1 += secondsPerCycleDegree
        if resistanceByTime3 / tr_long_thermal_resistance >= 0.99 and resistanceByTime4 / fwd_long_thermal_resistance >= 0.99:
            break
    for index1 in range(0, 360):
        for degree_count in range(0, 360):
            TjIGBT[degree_count] = dtInputCaseTemp + dtPIGBT[degree_count] * RthTrValue[degree_count] + \
                                   ThermalContactResistanceValue[degree_count] * (
                                           dtPIGBT[degree_count] + dtFRD[degree_count])
            TjFWD[degree_count] = dtInputCaseTemp + dtFRD[degree_count] * RthDiValue[degree_count] + \
                                  ThermalContactResistanceValue[degree_count] * (
                                          dtPIGBT[degree_count] + dtFRD[degree_count])
            TrFreqAndThermoDict[degree_count] += GetTransistorTransientThermalResistanceByTime(time1)
            DiFreqAndThermoDict[degree_count] += GetDiodeTransientThermalResistanceByTime(time1)
            TjIGBT[degree_count] -= (TrInstPowerLoss[degree_count] - dtPIGBT[degree_count]) * TrFreqAndThermoDict[
                degree_count]
            TjFWD[degree_count] -= (DiInstPowerLoss[degree_count] - dtFRD[degree_count]) * DiFreqAndThermoDict[
                degree_count]
            TjIGBT[degree_count] += (TrInstPowerLoss[degree_count] - dtPIGBT[degree_count]) * TrFreqAndThermoDict[
                degree_count]
            TjFWD[degree_count] += (DiInstPowerLoss[degree_count] - dtFRD[degree_count]) * DiFreqAndThermoDict[
                degree_count]
        time1 += secondsPerCycleDegree
        for degree_count in range(0, 360):
            TrPowerLossDelta = TrInstPowerLoss[degree_count] - TrInstPowerLoss[degree_count - 1]
            DiPowerLossDelta = DiInstPowerLoss[degree_count] - DiInstPowerLoss[degree_count - 1]
            TjIGBT[degree_count] += TrPowerLossDelta * TrFreqAndThermoDict[(360 + index1 - degree_count) % 360]
            TjFWD[degree_count] += DiPowerLossDelta * DiFreqAndThermoDict[(360 + index1 - degree_count) % 360]

        lt_Temp_Time.append(time1 / 1000.0)
        lt_Temp_Rad.append((index1 + 1))
        lt_Tr_Temp.append(TjIGBT)
        lt_Tr_Temp_Powerloss.append(TrInstPowerLoss[index1])
        lt_Di_Temp.append(TjFWD)
        lt_Di_Temp_Powerloss.append(DiInstPowerLoss[index1])

# CalculationCommonMethods.CalcTemperatureStatistics(modSimResult, moduleNum)
