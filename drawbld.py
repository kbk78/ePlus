import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np

coord = [[0,0,0],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1],[1,-1,0],[1,0,-1]]
colors = [["Green"],["Blue"],["Green"],["Green"],["Red"],["Green"],["Green"]]
labels = [['yes'],['no'],['yes'],['no'],['yes'],['no'],['no']]

# Horizontal cartesian coords
hcoord = [c[0] for c in coord]

# Vertical cartersian coords
vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) /3. for c in coord]

fig, ax = plt.subplots(1)
ax.set_aspect('equal')

# Add some coloured hexagons
for x, y, c, l in zip(hcoord, vcoord, colors, labels):
    color = c[0].lower()  # matplotlib understands lower case words for colours
    hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3., 
                         orientation=np.radians(30), 
                         facecolor=color, alpha=0.2, edgecolor='k')
    ax.add_patch(hex)
    # Also add a text label
    ax.text(x, y+0.2, l[0], ha='center', va='center', size=20)

# Also add scatter points in hexagon centres
ax.scatter(hcoord, vcoord, c=[c[0].lower() for c in colors], alpha=0.5)

plt.show()


import matplotlib
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt


fig, ax = plt.subplots()

resolution = 50 # the number of vertices
N = 3
x       = np.random.rand(N)
y       = np.random.rand(N)
radii   = 0.1*np.random.rand(N)
patches = []
for x1,y1,r in zip(x, y, radii):
    circle = Circle((x1,y1), r)
    patches.append(circle)

x       = np.random.rand(N)
y       = np.random.rand(N)
radii   = 0.1*np.random.rand(N)
theta1  = 360.0*np.random.rand(N)
theta2  = 360.0*np.random.rand(N)
for x1,y1,r,t1,t2 in zip(x, y, radii, theta1, theta2):
    wedge = Wedge((x1,y1), r, t1, t2)
    patches.append(wedge)

# Some limiting conditions on Wedge
patches += [
    Wedge((.3,.7), .1, 0, 360),             # Full circle
    Wedge((.7,.8), .2, 0, 360, width=0.05), # Full ring
    Wedge((.8,.3), .2, 0, 45),              # Full sector
    Wedge((.8,.3), .2, 45, 90, width=0.10), # Ring sector
]

for i in range(N):
    polygon = Polygon(np.random.rand(N,2), True)
    patches.append(polygon)

colors = 100*np.random.rand(len(patches))
p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
p.set_array(np.array(colors))
ax.add_collection(p)
plt.colorbar(p)

plt.show()

