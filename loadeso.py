
"""
Bharath Karambakkam
e-mail:Bharath.karambakkam@imegcorp.com
file: Load EnergyPlus Hourly output file (*.eso)
"""





from pylab import *
import pandas as pd
import re
import io


def loadeso_old(fname):
    """
    for 8760 data only
    """
    with open(fname,'r') as f: eso = f.read()
    vart = re.findall('([^,]+,[^,]+) !Hourly',eso)
    varn = re.findall('(\d+),([\d.eE-]+)\n',eso)
    s = pd.DataFrame(varn,columns=['var','val'],dtype='float64')
    s['dt']=repeat([datetime.datetime(2012,1,1,0)+datetime.timedelta(hours=i) for i in range(8760)],len(vart))
    eso=s.pivot(index='dt',columns='var',values='val')
    eso.columns=vart
    return eso


def loadeso(fname):
    """
    Works only if all hourly variables are of equal length 
    """ 
    with open(fname,'r') as f: varstr = f.read()
    colstr,datstr,end = varstr.split('End of')

    cols = pd.read_csv(io.StringIO(colstr),skiprows=6+int(colstr.find('Calendar Year')>0),header=None,names=['n','zone','value'])
    cols['zone']= cols.loc[:,'zone'].str.split(expand=True)[0]
    cols['value'] = cols.loc[:,'value'].str.split(' \[',expand=True)[0]
 
    d = pd.DataFrame(re.findall('2,[ 0-9]*,([ 0-9]*),([ 0-9]*),[ 0-1]*,([ 0-9]*),([ 0-9.]*),[ 0-9.]*,[A-Z]',datstr),dtype=np.float).astype(int)
    dtx=pd.to_datetime(2012*100000000 + d[0]*1000000 + d[1]*10000+(d[2]-1)*100+d[3], format='%Y%m%d%H%M')


    eso = pd.read_csv(io.StringIO(re.sub('^2,.*\n','',datstr,flags=re.M)),skiprows=2,header=None,dtype=np.float)
    eso['hrs'] = eso.groupby(0).cumcount()
    eso = eso.set_index(['hrs',0]).unstack()

    eso.index = dtx
    eso.columns = pd.MultiIndex.from_arrays(cols.loc[eso.columns.get_level_values(0).astype(int),['zone','value']].values.T)

#    eso.loc[:,('zone name',slice(None))] Sample referencing for columns
    return eso.sort_index(axis=1)

