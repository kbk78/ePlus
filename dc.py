import sys,os,subprocess
from shutil import copyfile
sys.path.append('C:\\Projects\\Tools\ePlus')
from importlib import reload
from copy import deepcopy as dc
import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np
import re


from runeplus import runeplus
import loadeso
import exml
import readidf
import parsetup

reload(parsetup)
reload(exml)
reload(readidf)

files = [
        'dc.idf',
        'dcb.idf',
        ]



#for ea in files:
#   idffile=os.getcwd()+'\\'+ea
#   for i in range(4,9):
#       subprocess.call(['C:\CustomSoftware\EnergyPlusV8-9-0\PreProcess\IDFVersionUpdater\Transition-V8-'+str(i)+'-0-to-V8-'+str(i+1)+'-0.exe',idffile],cwd='C:\CustomSoftware\EnergyPlusV8-9-0\PreProcess\IDFVersionUpdater')
#   subprocess.call(['C:\CustomSoftware\EnergyPlusV9-2-0\PreProcess\IDFVersionUpdater\Transition-V8-9-0-to-V9-0-0.exe',idffile],cwd='C:\CustomSoftware\EnergyPlusV9-2-0\PreProcess\IDFVersionUpdater')
#   subprocess.call(['C:\CustomSoftware\EnergyPlusV9-2-0\PreProcess\IDFVersionUpdater\Transition-V9-0-0-to-V9-1-0.exe',idffile],cwd='C:\CustomSoftware\EnergyPlusV9-2-0\PreProcess\IDFVersionUpdater')
#   subprocess.call(['C:\CustomSoftware\EnergyPlusV9-2-0\PreProcess\IDFVersionUpdater\Transition-V9-1-0-to-V9-2-0.exe',idffile],cwd='C:\CustomSoftware\EnergyPlusV9-2-0\PreProcess\IDFVersionUpdater')




#make cases
cases = files

# Basecase orientations------------------------------
idf = readidf.idf('dcb.idf')
for r in range(90,360,90):
    idf.t.loc['Building',:,1] = r
    idf.writeidf('dcb'+str(r)+'.idf')
    cases.append('dcb'+str(r)+'.idf')

outputs =  [#'Output:VariableDictionary, IDF;',
#            'Output:Variable,Basement:Gathering,Zone Heating Setpoint Not Met Time,hourly; !- Zone Sum [hr]',
#            'Output:Variable,Ground:Ninja,Zone Heating Setpoint Not Met While Occupied Time,hourly; !- Zone Sum [hr]',
#            'Output:Variable,Ground:Delivery,Zone Heating Setpoint Not Met While Occupied Time,hourly; !- Zone Sum [hr]',
#            'Output:Variable,Level2:Auditorium,Zone Heating Setpoint Not Met While Occupied Time,hourly; !- Zone Sum [hr]',
#            'Output:Variable,L1:DataCenter,Zone Cooling Setpoint Not Met While Occupied Time,hourly; !- Zone Sum [hr]',
#            'Output:Variable,LEVEL2:OFFICE11,Zone Mean Air Temperature,hourly; !- Zone Average [C]',
#            'Output:Variable,*,Air System Mixed Air Mass Flow Rate,hourly; !- HVAC Average [kg/s]',
            'Output:Variable,*,Air System Outdoor Air Mass Flow Rate,hourly; !- HVAC Average [kg/s]',
#            'Output:Variable,Level1 FCU DOAS AHU Supply Fan,Fan Electric Power,hourly; !- HVAC Average [W]'
#            'Output:Variable,*,Zone Air Terminal Outdoor Air Volume Flow Rate,hourly; !- HVAC Average [m3/s]'
#            'Output:Variable,*,Zone Heating Setpoint Not Met While Occupied Time,hourly; !- Zone Sum [hr]',
#            'Output:Variable,*,Zone Cooling Setpoint Not Met While Occupied Time,hourly; !- Zone Sum [hr]',
#            'Output:Variable,*,Zone Mechanical Ventilation Mass Flow Rate,hourly; !- HVAC Average [kg/s]',
#            'Output:Variable,*,Air System Total Heating Energy,hourly; !- HVAC Sum [J]',
#            'Output:Variable,*,Zone Air System Sensible Heating Energy,hourly; !- HVAC Sum [J]',
#            'Output:Variable,*,District Heating Hot Water Energy,hourly; !- HVAC Sum [J]',
#            'Output:Variable,*,Fan Electric Power,hourly; !- HVAC Average [W]',
#            'Output:Variable,*,District Heating Hot Water Energy,hourly; !- HVAC Sum [J]',
#            'Output:Variable,*,District Cooling Chilled Water Energy,hourly; !- HVAC Sum [J]',
#            'Output:Variable,*,Plant Component Distributed Demand Rate,hourly; !- HVAC Average [W]',
#            'Output:Variable,*,Plant Supply Side Cooling Demand Rate,hourly; !- HVAC Average [W]',
#            'Output:Variable,*,Plant Supply Side Heating Demand Rate,hourly; !- HVAC Average [W]',
#            'Output:Variable,*,Water to Water Heat Pump Electric Energy,hourly; !- HVAC Sum [J]',
#
#            'Output:Variable,BelowGrade:1 PTAC Outdoor Air Node Name,System Node Mass Flow Rate,hourly; !- HVAC Average [kg/s]',
#            'Output:Variable,Roof:1 PTAC Outdoor Air Node Name,System Node Mass Flow Rate,hourly; !- HVAC Average [kg/s]',     
#            'Output:Variable,Core:1 PTAC Outdoor Air Node Name,System Node Mass Flow Rate,hourly; !- HVAC Average [kg/s]',    
#            'Output:Variable,East:1 PTAC Outdoor Air Node Name,System Node Mass Flow Rate,hourly; !- HVAC Average [kg/s]',   
#            'Output:Variable,North:1 PTAC Outdoor Air Node Name,System Node Mass Flow Rate,hourly; !- HVAC Average [kg/s]', 
#            'Output:Variable,West:1 PTAC Outdoor Air Node Name,System Node Mass Flow Rate,hourly; !- HVAC Average [kg/s]', 
#            'Output:Variable,South:1 PTAC Outdoor Air Node Name,System Node Mass Flow Rate,hourly; !- HVAC Average [kg/s]',
#
#            'Output:Variable,*,Zone Air Heat Balance System Air Transfer Rate,hourly; !- HVAC Average [W]',
#            'Output:Variable,*,System Node Temperature,hourly; !- HVAC Average [C]',
#            'Output:Variable,*,Heating Coil Air Heating Energy,hourly; !- HVAC Sum [J]',
#            'Output:Variable,*,Cooling Coil Total Cooling Energy,hourly; !- HVAC Sum [J]',
#            'Output:Variable,*,Cooling Coil Sensible Cooling Energy,hourly; !- HVAC Sum [J]'

#            'Output:Variable,*,Air System Mixed Air Mass Flow Rate,hourly; !- HVAC Average [kg/s]',

#            'Output:Variable,*,Zone Air Temperature,hourly; !- HVAC Average [C]',
#            'Output:Variable,*,Zone Predicted Sensible Load to Setpoint Heat Transfer Rate,hourly; !- HVAC Average [W]',
#            'Output:Variable,*,System Node Temperature,hourly; !- HVAC Average [C]',
#            'Output:Variable,MEMORIALSTADIUM_OCC,Schedule Value,hourly; !- Zone Average []',
#            'Output:Variable,MEMORIALSTADIUM_EQ,Schedule Value,hourly; !- Zone Average []',
#            'Output:Variable,MEMORIALSTADIUM_LT,Schedule Value,hourly; !- Zone Average []',
#            'Output:Variable,MEMORIALSTADIUM_FAN,Schedule Value,hourly; !- Zone Average []',
]

for ea in cases:
    idf = readidf.idf(ea)
#    infiltration 0.15 cfm/sqft =0.15*0.00508 m3/s/m2
    idf.t.loc['ZoneInfiltration:DesignFlowRate',:,3] ='Flow/ExteriorWallArea'
    idf.t.loc['ZoneInfiltration:DesignFlowRate',:,6] = 0.000402

#    idf.t.loc['ElectricEquipment',:,10] = 'IntEquip'
#    idf.t.loc['Lights',:,11] = 'IntLights'
#
#    idf.t.loc['AvailabilityManager:NightCycle',:,7] = ''
#    idf.t.loc['AvailabilityManager:NightCycle',:,5] = 'Thermostat'
#
#    idf.t.loc['RunPeriod',:,[3,4]] = [1,2]
#    idf.t.loc['Controller:MechanicalVentilation',:,2]='No'   
#    idf.t.loc['Controller:OutdoorAir',:,5] = 'Autosize'
#    idf.t.loc['Controller:OutdoorAir',:,7] = 'NoEconomizer'

    idf.writeidf(ea)
    idf = readidf.idf(ea)
    with open(ea,'r') as f: idft=f.read().replace('CommaAndHTML','XMLandHTML')
    for ei in outputs:idft=idft+ei+'\n'
    with open(ea,'w') as w:w.write(idft)

runeplus(cases,'C:\\ProgramData\\DesignBuilder\\Weather Data\\USA_IL_University.of.Illinois-Willard.AP.725315_TMY3.epw',rem=True,showprogress=True,ver = 'EnergyPlusV8-9-0') 
elec=pd.DataFrame()
gas=pd.DataFrame()
cost=pd.DataFrame()

ut=pd.Series([0.1067,0.606,0.00758,0.0113],index=['elec[kWh]','gas[therm]','distCl[kBtu]','distHt[kBtu]'])# Utility rates
for r in cases:
    ca=r.split('.idf')[0]
    xml = exml.exml(ca+'Table.xml')
    vars()['x'+ca]= xml
    eso=loadeso.loadeso(ca+'.eso')
    vars()['e'+ca]=eso
    print(ca+'- EUI: '+str(xml.getEUI()))
    elec[ca] = xml.getprm()['elec[kWh]']
    cost[ca] = (xml.getprm() * ut).dropna(axis=1).sum(axis=1)
    print(ca+str(xml.getunmethours()))
print(cost)
xdc.getall()
xdcb.getall()

print("savings: {0:0.1f} %".format(((1-cost['dc'].sum()/cost['dcb'].sum())*100)))


#------ PRM Outputs
prmrow  =  ['InteriorLightingGenerallights',
            'ExteriorLightingExteriorLights',
            'HeatingNotSubdivided',
            'CoolingNotSubdivided',
            'PumpsGeneral',
            'HeatRejectionNotSubdivided',
            'FansGeneral',
            'ExteriorEquipmentNotSubdivided',
            'WaterSystemsWaterHeater',
            'InteriorEquipmentGeneralequipment']

prmcol = ['ElectricEnergyUse', 'ElectricDemand']

prmbavg  =  (xgab.getLEEDprm(prmcol,prmrow) + \
            xgab90.getLEEDprm(prmcol,prmrow) + \
            xgab180.getLEEDprm(prmcol,prmrow) + \
            xgab270.getLEEDprm(prmcol,prmrow))/4

prm = xga.getLEEDprm(prmcol,prmrow)


prmbavg.to_clipboard(index=False)

#-------------


#------ EUI Graphs
#enduses = xdc.AnnualBuildingUtilityPerformanceSummary1EndUses
#enduses.drop('Water',inplace=True,axis=1)
#enduses.drop('TotalEndUses',inplace=True)
#enduses = enduses.reset_index().melt(id_vars=['name']).replace(0.00,np.nan).dropna()
#
#enduses.rename(columns={'variable':'Source','name':'Category'},inplace=True)
#enduses['value']= enduses['value']/109891
#enduses.to_clipboard()
#-------------


#print('WindowtowallRatio')
#xdc.InputVerificationAndResultsSummary1WindowWallRatio

#print('Verification')
#prm = xdc.AnnualBuildingUtilityPerformanceSummary1EndUses
#prm = prm.loc[prm.any(axis=1),prm.any()][:-1].replace(0.0,np.nan)
#prmd =xdc.DemandEndUseComponentsSummary1EndUses
#prmd = prmd.loc[prmd.any(axis=1),prmd.any()][:-1].replace(0.0,np.nan)
#runhours = prm/prmd

#print('Wall/RoofU')
#xdc.EnvelopeSummary1OpaqueExterior['UFactorWithFilm'].value_counts()
#xdcb.EnvelopeSummary1OpaqueExterior['UFactorWithFilm'].value_counts()

#print('WindowU')
xdc.EnvelopeSummary1ExteriorFenestration['GlassUFactor'].value_counts()
#xdcb.EnvelopeSummary1ExteriorFenestration['GlassUFactor'].value_counts()

#print('WindowSHGC')
#xdc.EnvelopeSummary1ExteriorFenestration['GlassShgc'].value_counts()
#xdcb.EnvelopeSummary1ExteriorFenestration['GlassShgc'].value_counts()
#
#print('WindowTransmittance')
#xdc.EnvelopeSummary1ExteriorFenestration['GlassVisibleTransmittance'].value_counts()
#xdcb.EnvelopeSummary1ExteriorFenestration['GlassVisibleTransmittance'].value_counts()
#
#print('Process')
#(xdc.InputVerificationAndResultsSummary1ZoneSummary['Area']*xdc.InputVerificationAndResultsSummary1ZoneSummary['PlugAndProcess']/3.412).dropna()[:-2].sum()
#(xdcb.InputVerificationAndResultsSummary1ZoneSummary['Area']*xdcb.InputVerificationAndResultsSummary1ZoneSummary['PlugAndProcess']/3.412).dropna()[:-2].sum()

#print('Lighting')
#(xdc.InputVerificationAndResultsSummary1ZoneSummary['Lighting']/3.412).value_counts()
#(xdcb.InputVerificationAndResultsSummary1ZoneSummary['Lighting']/3.412).value_counts()

#print('People')
#(xdc.InputVerificationAndResultsSummary1ZoneSummary['Area']/xdc.InputVerificationAndResultsSummary1ZoneSummary['People']).dropna().sum()
#(xdcb.InputVerificationAndResultsSummary1ZoneSummary['Area']/xdcb.InputVerificationAndResultsSummary1ZoneSummary['People']).dropna().sum()

#print('SystemAirFlow')
#xdcb.EquipmentSummary1Fans[['MaxAirFlowRate','RatedElectricPower']]
#xdc.EquipmentSummary1Fans.groupby('Type').get_group('Fan:ConstantVolume')[['MaxAirFlowRate','RatedElectricPower']]
#xdc.EquipmentSummary1Fans.groupby('Type').get_group('Fan:VariableVolume')[['MaxAirFlowRate','RatedElectricPower']]

#print('Outdoorair')
#idf = readidf.idf('dc.idf')
#sz=idf.getsyszones().set_index('name')
#sc = xdc.HvacSizingSummary1ZoneSensibleCooling
#sc.index = sc.index.str.upper()
#oa = sc.merge(sz,left_index=True,right_index=True).groupby('val').sum()['MinimumOutdoorAirFlowRate']
#
#idf = readidf.idf('dcb.idf')
#sz=idf.getsyszones().set_index('name')
#sc = xdcb.HvacSizingSummary1ZoneSensibleCooling
#sc.index = sc.index.str.upper()
#oab = sc.merge(sz,left_index=True,right_index=True).groupby('val').sum()['MinimumOutdoorAirFlowRate']

#print('CoolingCapacitykBtu')
#xdcb.EquipmentSummary1CoolingCoils.iloc[:,1:3]/1000
#xdcb.EquipmentSummary1CoolingCoils.loc['HydrotherapyPszAhuCoolingCoil',['DesignCoilLoad','NominalSensibleCapacity','NominalLatentCapacity']]

#print('HeatingCapcitykBtu')
#xdcb.EquipmentSummary1HeatingCoils.iloc[-9:,1:3]/1000

#print('Pumps')
#xdc.EquipmentSummary1Pumps
#xdcb.EquipmentSummary1Pumps

#for i in ['','90','180','270']:
#    vars()['xdcb'+i].getall()
#    vars()['prmb'+i] = vars()['xdcb'+i].LeedSummary1Eap245PerformanceRatingMethodCompliance
#prmbavg=((prmb+prmb90+prmb180+prmb270)/4).stack()
#prmbavg[prmbavg>0].to_clipboard()

basecost=pd.Series([prmbavg.loc[:,'ElectricEnergyUse'].sum(),
                    prmbavg.loc[:,'NaturalGasEnergyUse'].sum(),
                    prmbavg.loc['CoolingNotSubdivided','DistrictCoolingUse']*12,
                    0],
                    index=['elec[kWh]','gas[therm]','distCl[kBtu]','distHt[kBtu]'])*ut

#prmbavg = prmbavg[prmbavg>0]
#prmbavg.loc[:,'ElectricDemand']=(prmbavg.loc[:,'ElectricDemand']).values/1000
#prmbavg.loc[:,'AdditionalDemand']=(prmbavg.loc[:,'AdditionalDemand']).values/1000

#prm = xdc.LeedSummary1Eap245PerformanceRatingMethodCompliance.stack()
#prm[prm>0].to_clipboard()

propcost=pd.Series([prm.loc[:,'ElectricEnergyUse'].sum(),
                    prm.loc[:,'NaturalGasEnergyUse'].sum(),
                    prm.loc['CoolingNotSubdivided','DistrictCoolingUse']*12,
                    0],
                    index=['elec[kWh]','gas[therm]','distCl[kBtu]','distHt[kBtu]'])*ut

#propcost=pd.Series([
#                    prm.loc[:,'ElectricEnergyUse'][:-1].sum(),
#                    prm.loc[:,'NaturalGasEnergyUse'][:-1].sum(),
#                    prm.loc['SpaceCooling','AdditionalEnergyUse'],
#                    prm.loc[['SpaceHeating','ServiceWaterHeating'],'AdditionalEnergyUse'].sum()],
#                    index=['elec[kWh]','gas[therm]','distCl[kBtu]','distHt[kBtu]'])*ut
#
#fuelcostb = (xdcb.getprm() * ut).dropna(axis=1).sum()

#xdv.getall()
#print(xdc.AnnualBuildingUtilityPerformanceSummary1EndUsesBySubcategory.iloc[[0,1,6,7],[1,4,5]])
