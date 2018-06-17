"""
Bharath Karambakkam
e-mail:Bharath.karambakkam@imegcorp.com
function: Load energyplus idf file into a pandas dataframe(*.idf)
"""


import re,io
import pandas as pd

class idf(object):

    def __init__(self,name=None):
        self.name=name
        self.t=None
        if name:self.readidf()

    def reload(self):
        None
#        self.__init__(self.name)
    def copy(self):
        idfc=idf()
#        idfc.t=self.t
#        idfc.name=self.name
        return idfc
        

    def readidf(self):
        with open(self.name,'r') as f: idf=re.sub('!.*|\t','',f.read()).replace('\n','')
        

        dstr = '(Output:Variable|Output:Surfaces:Drawing|Output:Meter)'
        idf  = re.sub(' *'+dstr+'.*?;','',idf)

        idf = re.sub(r'( *)(,|;)( *)',r'\2',idf)

        df = pd.DataFrame(idf.split(';')[:-1], columns=['col'])
        idfTable=pd.DataFrame(df['col'].str.split(',').tolist()).set_index([0,1])

        idfTable.columns=idfTable.columns-1
        idfTable[1].fillna('',inplace=True)
        self.t = idfTable.stack().sort_index(level=0)
        self.t.name='val'
        self.t.index.set_names(['class','name','par'],inplace=True)

    #Editing groups idfTable.loc['Building',slice(None),2]=3

    def setparnames(self):
        with open('parnames.csv') as f:n = pd.read_csv(f.read())
        self.t=pd.merge(n,self.t.reset_index(),how='outer').ffill(axis=1).drop('par',axis=1)
        self.t.set_index(['class','name','title'],inplace=True)
        self.t.soft_index(level=0)

    def writeidf(self,fname):
        s = io.StringIO()
        self.t.unstack().to_csv(s,header=False,line_terminator=',\n')
        s.seek(0)
        with open(fname,'w') as f: f.write(re.sub('[,\s]*\n',';\n',s.read()))

    def getzones(self):
        return self.t.loc['Zone',:,1].reset_index()['name']


    def getsyszones_old(self):
        sp = self.t.loc['AirLoopHVAC:ZoneSplitter',:,slice(2,1000)].reset_index()[['name','val']]
        
        zn = self.t[self.t.reset_index()['class'].str.contains('AirTerminal:.*Uncontrolled',regex=True).values].loc[:,:,2].reset_index()[['name','val']]
        zn = zn.append(self.t[self.t.reset_index()['class'].str.contains('AirTerminal:.*Reheat',regex=True).values].loc[:,:,3].reset_index()[['name','val']])
        sp['sys'] = pd.DataFrame(sp['name'].str.split(' Zone Splitter').tolist())[0]
        zn['zn'] = pd.DataFrame(zn['name'].str.split(' ').tolist())[0]   #may not work if there is space in zone name.
        sp = sp[['sys','val']]
        zn = zn[['zn','val']]
        return pd.merge(zn,sp)[['zn','sys']].set_index('sys').stack()


    def getsyszones(self):
        zn  = self.t.loc['ZoneHVAC:EquipmentConnections',:,[5]].reset_index()[['name','val']]
        s=lambda s: s.split(' Zone')[0]
        z=lambda z: ''.join(z.upper().split(':'))
        zn['name'] = zn['name'].apply(z)
        zn['val'] = zn['val'].apply(s)
        return zn

    def getclass(self):
        for i in self.t.index.get_level_values(0).unique():print(i)

    def getnames(self,classname):
        for i in self.t.loc[classname].index.get_level_values(0).unique():print(i) 

    def plotzones(self,floor=0,zdata=0):
        from matplotlib.patches import Polygon
        from matplotlib.collections import PatchCollection
        import matplotlib.pyplot as plt

        f = (self.t.loc['BuildingSurface:Detailed',:,1] =='Floor').reset_index()
        fl = f[f['val']]['name'].values
        nind=fl.repeat((self.t.loc['BuildingSurface:Detailed',fl,10:].groupby('name').size().values/3).astype('int'))
        s=pd.DataFrame(self.t.loc['BuildingSurface:Detailed',fl,10:].values.reshape(-1,3),columns=['x','y','z'],index=nind).apply(pd.to_numeric)

        zn = self.t.loc['BuildingSurface:Detailed',fl,[3]].values
        s['zn']=zn.repeat((self.t.loc['BuildingSurface:Detailed',fl,10:].groupby('name').size().values/3).astype('int'))


        if not zdata:
            zdata = s.groupby('zn').first().groupby('zn').ngroup()


        gr = s.groupby(s.index)
        ly = pd.DataFrame({'poly':gr.apply(lambda x:Polygon(x[['x','y']].values)),
                      'zn':gr.first()['zn'],
                      'z':gr.first()['z'],
                      'zdata':zdata.repeat(gr.first().groupby('zn').size()).values})


        fig, ax = plt.subplots(1)
        ax.set_aspect('equal')
        ax.set_xlim([s.min()['x'],s.max()['x']])
        ax.set_ylim([s.min()['y'],s.max()['y']])

        gr=ly.groupby('z')
        p = PatchCollection(gr.get_group(list(gr.groups.keys())[floor])['poly'].values)
        ax.add_collection(p)
        p.set_array(gr.get_group(list(gr.groups.keys())[floor])['zdata'].values)
        plt.colorbar(p)
        plt.show()


#sys.path.append('C:\\Projects\\Tools\ePlus')
#from importlib import reload
#from copy import deepcopy as al
#import pandas as pd
##import matplotlib.pyplot as plt
#import numpy as np
#import re
#
#from runeplus import runeplus
#import loadeso
#import exml
#import readidf
#import parsetup
#
#reload(parsetup)
#reload(exml)
#reload(readidf)
#
#f = (idf.t.loc['BuildingSurface:Detailed',:,1] =='Floor').reset_index()
#fl = f[f['val']]['name'].values
#nind=fl.repeat((idf.t.loc['BuildingSurface:Detailed',fl,10:].groupby('name').size().values/3).astype('int'))
#
#zn = idf.t.loc['BuildingSurface:Detailed',fl,[3]].values
#s['zn']=zn.repeat((idf.t.loc['BuildingSurface:Detailed',fl,10:].groupby('name').size().values/3).astype('int')))
#
#
#s=pd.DataFrame(idf.t.loc['BuildingSurface:Detailed',fl,10:].values.reshape(-1,3),columns=['x','y','z'],index=nind).apply(pd.to_numeric)
#lev = s.groupby('z')
#lev1 = lev.get_group(list(lev.groups.keys())[floor])
#zn = pd.DataFrame(idf.t.loc['BuildingSurface:Detailed',fl,[3]].values,columns=['zones'])
#lev1['n'] = lev1.groupby('zn').ngroup().values
#
#
#
#
#znpoly = []
#for c,ea in lev1.groupby(lev1.index):
#    znpoly.append(Polygon(ea[['x','y']].values, linewidth=0,edgecolor="none"))
#
#
#fig, ax = plt.subplots(1)
#ax.set_aspect('equal')
#ax.set_xlim([s.min()['x'],s.max()['x']])
#ax.set_ylim([s.min()['y'],s.max()['y']])
#p = PatchCollection(znpoly)
#ax.add_collection(p)
#p.set_array(zn['n'].values)
#plt.colorbar(p)
#plt.show()
#
#import shapely.geometry as sg
#import shapely.ops as so
#import matplotlib.pyplot as plt
#
##constructing the first rect as a polygon
#r1 = sg.Polygon([(0,0),(0,1),(1,1),(1,0),(0,0)])
#
##a shortcut for constructing a rectangular polygon
#r2 = sg.box(0.5,0.5,1.5,1.5)
#
##cascaded union can work on a list of shapes
#new_shape = so.cascaded_union([r1,r2])
#
##exterior coordinates split into two arrays, xs and ys
## which is how matplotlib will need for plotting
#xs, ys = new_shape.exterior.xy
#
##plot it
#fig, axs = plt.subplots()
#axs.fill(xs, ys, alpha=0.5, fc='r', ec='none')
#plt.show() #if not interactive
