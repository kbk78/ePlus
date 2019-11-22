"""
Bharath Karambakkam
--------------------
e-mail:Bharath.karambakkam@imegcorp.com
function: Load EnergyPlus output xml file (*.xml)
"""

from xml.etree.ElementTree import parse 
from numpy import array
import pandas as pd
import calendar
from xmljson import parker as pr

class exml(object):

 def __init__(self,fname):
     self.fname=fname
     tree = parse(self.fname)
     self.elem = tree.getroot()

 def reload(self):
     self.__init__(self.fname)

 def getprm(self):
     c=self.elem.find('AnnualBuildingUtilityPerformanceSummary')
     x=c.findall('EndUses')[:-1]
     cat= [e.find('name').text for e in x]
     elec  = pd.Series([e.find('Electricity').text for e in x],dtype=float,index=cat)/3.4144
     gas = pd.Series([e.find('NaturalGas').text for e in x],dtype=float,index=cat)/1e2
     distCl = pd.Series([e.find('DistrictCooling').text for e in x],dtype=float,index=cat)
     distHt = pd.Series([e.find('DistrictHeating').text for e in x],dtype=float,index=cat)
     additionalFuel = pd.Series([e.find('AdditionalFuel').text for e in x],dtype=float,index=cat)
     prm = pd.DataFrame({'elec[kWh]':elec,'gas[therm]':gas,'distCl[kBtu]':distCl,'distHt[kBtu]':distHt,'additionalFuel[kBtu]':additionalFuel})
     return prm.loc[prm.any(1),prm.any()]
 
 def getEUI(self):
     c=self.elem.find('AnnualBuildingUtilityPerformanceSummary')
     x=c.findall('SiteAndSourceEnergy')[1]
     return float(x.find('EnergyPerTotalBuildingArea').text)
     

 def getunmethours(self):
     x= self.elem.find('SystemSummary').findall('TimeSetpointNotMet')[-1]
     return pd.Series(pr.data(x))

 def getunmetzones(self):
     x= self.elem.find('SystemSummary').findall('TimeSetpointNotMet')[:-1]
     return pd.DataFrame(pr.data(x)['TimeSetpointNotMet'])[:-1].set_index('name')

 def getall(self):
     r = pr.data(self.elem)
     for ea in['BuildingName','EnvironmentName','WeatherFileLocationTitle'
             ,'ProgramVersion','SimulationTimestamp']:r.pop(ea,None)
     for ea in r:
         if not all([ea in ['monthly','TariffReport']]):  
             for j in ['for','note','footnote','General']: r[ea].pop(j,None)
             for j in r[ea]:
                 if type(r[ea][j]) is list:
                     self.__setattr__(ea+'1'+j,pd.DataFrame(r[ea][j]).set_index('name'))
                 else:
                     self.__setattr__(ea+'1'+j,pd.Series(r[ea][j]))


 def getmonthly(self):
     r = pr.data(self.elem)
     for ea in r:
         if 'monthly' in ea:
             if type(r[ea]) is list:
                 s = pd.DataFrame()
                 for j in r[ea]:
                     v=pd.DataFrame(j['CustomMonthlyReport'])
                     v['zone'] = j['for']
                     s=pd.concat([s,v],sort=True)
                 s=s.set_index(['zone','name'])     
                 self.__setattr__(ea,s)
             else:
                 pd.DataFrame(r[ea]['CustomMonthlyReport'])
                 self.__setattr__(ea,pd.DataFrame(r[ea]['CustomMonthlyReport']))


 def getLEEDprm(self):
     self.getall()

     prmres = self.LeedSummary1Eap245PerformanceRatingMethodCompliance * (1,1/1000,100,1/1000,1,1/1000,12,12,1,1/1000)

     idx = [('InteriorLightingGeneral','ElectricEnergyUse'),
            ('InteriorLightingGeneral','ElectricDemand'),
            ('ExteriorLightingGeneral','ElectricEnergyUse'),
            ('ExteriorLightingGeneral','ElectricDemand'),
            ('HeatingNotSubdivided','NaturalGasEnergyUse'),
            ('HeatingNotSubdivided','NaturalGasDemand'),
            ('CoolingNotSubdivided','ElectricEnergyUse'),
            ('CoolingNotSubdivided','ElectricDemand'),
            ('PumpsGeneral','ElectricEnergyUse'),
            ('PumpsGeneral','ElectricDemand'),
            ('HeatRejectionNotSubdivided','ElectricEnergyUse'),
            ('HeatRejectionNotSubdivided','ElectricDemand'),
            ('FansGeneral','ElectricEnergyUse'),
            ('FansGeneral','ElectricDemand'),
            ('ExteriorEquipmentNotSubdivided','ElectricEnergyUse'),
            ('ExteriorEquipmentNotSubdivided','ElectricDemand'),
            ('WaterSystemsGeneral','NaturalGasEnergyUse'),
            ('WaterSystemsGeneral','NaturalGasDemand'),
            ('InteriorEquipmentGeneral','ElectricEnergyUse'),
            ('InteriorEquipmentGeneral','ElectricDemand'),
            ('ExteriorEquipmentNotSubdivided','ElectricEnergyUse'),
            ('ExteriorEquipmentNotSubdivided','ElectricDemand'),
            ('ExteriorEquipmentNotSubdivided','ElectricEnergyUse'),
            ('ExteriorEquipmentNotSubdivided','ElectricDemand'),
            ('RefrigerationGeneral','ElectricEnergyUse'),
            ('RefrigerationGeneral','ElectricDemand'),
            ('ExteriorEquipmentNotSubdivided','ElectricEnergyUse'),
            ('ExteriorEquipmentNotSubdivided','ElectricDemand'),
            ('ExteriorEquipmentNotSubdivided','ElectricEnergyUse'),
            ('ExteriorEquipmentNotSubdivided','ElectricDemand'),
            ('ExteriorEquipmentNotSubdivided','ElectricEnergyUse'),
            ('ExteriorEquipmentNotSubdivided','ElectricDemand'),
            ('ExteriorEquipmentNotSubdivided','ElectricEnergyUse'),
            ('ExteriorEquipmentNotSubdivided','ElectricDemand'),
            ('ExteriorEquipmentNotSubdivided','ElectricEnergyUse'),
            ('ExteriorEquipmentNotSubdivided','ElectricDemand'),
            ('HeatingNotSubdivided','ElectricEnergyUse'),
            ('HeatingNotSubdivided','ElectricDemand')]

     return prmres.stack().loc[idx]


 def getstd(self):
     
     c = self.elem.find('AnnualBuildingUtilityPerformanceSummary')
     s = pd.DataFrame(pr.data(c)['EndUses'][:-1]).set_index('name') *[1/3.412,1/100,1,1/1000,1/1000,1] #kwh,therm,,MMBtu,MMBtu,
     s = s.reset_index().melt(id_vars='name')
     s = s[s['value']>0]
     s = s.set_index(s.name+'_'+s.variable)['value']
 
     c = self.elem.find('DemandEndUseComponentsSummary')
     sd = pd.DataFrame(pr.data(c)['EndUses'][:-1][1:]).set_index('name') *[1/3.412,1/100,1,1/1000,1/1000,1] #kwh,therm,,MMBtu,MMBtu,
     sd = sd.reset_index().melt(id_vars='name')
     sd = sd[sd['value']>0]
     sd = sd.set_index(sd.name+'_'+sd.variable+'Demand')['value']
     s = s.append(sd)

     c = self.elem.find('SystemSummary').findall('TimeSetpointNotMet')[-1]
     s=s.append(pd.Series(pr.data(c))[1:])
     
     s['EUI']=float(self.elem.find('AnnualBuildingUtilityPerformanceSummary').findall('SiteAndSourceEnergy')[1].find('EnergyPerTotalBuildingArea').text)
     
     coils=pr.data(self.elem.find('EquipmentSummary').findall('CoolingCoils'))['CoolingCoils']
     s['ClCoilSens']=pd.DataFrame(coils,index=range(max(1,isinstance(coils,list)*len(coils))))[['NominalSensibleCapacity']].sum()[0]
     
     coils=pr.data(self.elem.find('EquipmentSummary').findall('CoolingCoils'))['CoolingCoils']
     s['ClcoilLat']=pd.DataFrame(coils,index=range(max(1,isinstance(coils,list)*len(coils))))[['NominalLatentCapacity']].sum()[0]
     
     coils=pr.data(self.elem.find('EquipmentSummary').findall('HeatingCoils'))['HeatingCoils']
     s['HtCoil']=pd.DataFrame(coils,index=range(max(1,isinstance(coils,list)*len(coils))))[['NominalTotalCapacity']].sum()[0]
     
     s['clgCFM'] = pd.DataFrame(pr.data(self.elem.find('HvacSizingSummary').findall('ZoneSensibleCooling'))['ZoneSensibleCooling'])['UserDesignAirFlow'].sum()
     
     s['oaCFM'] = pd.DataFrame(pr.data(self.elem.find('HvacSizingSummary').findall('ZoneSensibleCooling'))['ZoneSensibleCooling'])['MinimumOutdoorAirFlowRate'].sum()
     
     s['htgCFM'] = pd.DataFrame(pr.data(self.elem.find('HvacSizingSummary').findall('ZoneSensibleHeating'))['ZoneSensibleHeating'])['UserDesignAirFlow'].sum()

     
     s['totalcl'] = pd.DataFrame(pr.data([list(ea)[3] for ea in self.elem.findall('Coilreportmonthly')])['CustomMonthlyReport'])['AnnualSumOrAverage'].sum()
     s['senscl'] = pd.DataFrame(pr.data([list(ea)[4] for ea in self.elem.findall('Coilreportmonthly')])['CustomMonthlyReport'])['AnnualSumOrAverage'].sum()
     s['totalht'] = pd.DataFrame(pr.data([list(ea)[1] for ea in self.elem.findall('Coilreportmonthly')])['CustomMonthlyReport'])['AnnualSumOrAverage'].sum()
     return s
 
