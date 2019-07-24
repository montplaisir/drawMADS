#!/usr/bin/python
import numpy as np

def readInfile(statsFileName, syntax):
    infile = open("stats.txt", "r")
    # We are interested in: f (OBJ), h (CONS_H), x (SOL), d (MESH_SIZE).
    # We assume x and d are of dimension 2.
    f_read  = []
    h_read  = []
    x1_read = []
    x2_read = []
    x_read  = []
    d1_read = []
    d2_read = []
    d_read  = []

    # Compute indices
    indexF = syntax.index("OBJ")
    indexH = syntax.index("CONS_H")
    indexX = syntax.index("SOL")
    indexD = syntax.index("MESH_SIZE")
    # Need to adjust considering that SOL and MESH_SIZE have 2 elements
    if (indexF > indexX):
        indexF += 1
    if (indexH > indexX):
        indexH += 1
    if (indexD > indexX):
        indexD += 1
    if (indexF > indexD):
        indexF += 1
    if (indexH > indexD):
        indexH += 1
    if (indexX > indexD):
        indexX += 1

    #Read line by line and fill arrays.
    # Use temporary arrays and then convert them to numpy arrays.
    for line in infile:
        word = line.split()
        f_read.append(float(word[indexF]))
        h_read.append(float(word[indexH]))
        x1_read.append(float(word[indexX]))
        x2_read.append(float(word[indexX+1]))
        newx = [x1_read[len(x1_read)-1], x2_read[len(x2_read)-1]]
        x_read.append(newx)
        d1_read.append(float(word[indexD]))
        d2_read.append(float(word[indexD+1]))
        newd = [d1_read[len(d1_read)-1], d2_read[len(d2_read)-1]]
        d_read.append(newd)

    # Done reading
    infile.close()

    f  = np.array(f_read)
    h  = np.array(h_read)
    x1 = np.array(x1_read)
    x2 = np.array(x2_read)
    x  = np.array(x_read)
    d1 = np.array(d1_read)
    d2 = np.array(d2_read)
    d  = np.array(d_read)
    nbbbe = len(f)

    return [f, h, x1, x2, x, d1, d2, d, nbbbe]
    #end readInfile


def computeMinMax(f, h, x, d):
    # hnonzero is the list of non-zero h. Used to compute minh
    hnonzero = h[np.nonzero(h)]

    # feasiblef is the list of f for which h is 0. Used to compute minf and maxf.
    # VRM there must be a more elegant way to compute this
    ff_temp = []
    for i in range(0, len(f)):
        if (h[i] == 0):
            ff_temp.append(f[i])
    feasiblef = np.array(ff_temp)

    # Compute min and max for arrays
    minf = min(feasiblef)
    maxf = max(feasiblef)
    minh = min(hnonzero)
    maxh = max(hnonzero)
    mind1 = min(d1)
    mind2 = min(d2)
    maxd1 = max(d1)
    maxd2 = max(d2)

    fforminh_temp = []
    for i in range(0, len(f)):
        if (h[i] == minh):
            fforminh_temp.append(f[i])
    minfforminh = min(fforminh_temp)

    if (minh == maxh):
        # We'll decide later what we do in this case - it's treatable.
        print("Warning: minh = maxh = " + str(minh))
    #print("VRM: minf = " + str(minf))
    #print("VRM: maxf = " + str(maxf))
    #print("VRM: minh = " + str(minh))
    #print("VRM: maxh = " + str(maxh))
    #print("VRM: mind1 = " + str(mind1))
    #print("VRM: maxd1 = " + str(maxd1))
    #print("VRM: mind2 = " + str(mind2))
    #print("VRM: maxd2 = " + str(maxd2))

    return [minf, maxf, minh, maxh, minfforminh]
    #end computeMinMax


def findBestXFeasInf(minf, minh, minfforminh):
    # Find xbestfeas and xbestinf
    # xbestfeas is x for which f = minf and h = 0
    xbf_temp = []
    xbi_temp = []
    #print("VRM: minh = " + str(minh) + " minfforminh = " + str(minfforminh))
    for i in range(0, len(f)):
        if (f[i] == minf and h[i] == 0):
            xbf_temp.append(x[i])
        elif (h[i] == minh and f[i] == minfforminh):
            xbi_temp.append(x[i])
    xbestfeas = np.array(xbf_temp)
    xbestinf  = np.array(xbi_temp)
    #print(xbestfeas)
    #print(xbestinf)

    return [xbestfeas, xbestinf]
    #end findBestXFeasInf




def writeHeader(outfile):
    outfile.write("writerObj = VideoWriter('out.avi');\n")
    outfile.write("writerObj.FrameRate = 60;\n")
    outfile.write("open(writerObj);\n")
    outfile.write("fId = figure;\n")
    outfile.write("hold\n")

    # These are the bb constraints. We concentrate on this problem for now, so
    # do not move them.
    outfile.write("x = -2:.05:18\n")
    outfile.write("y1 = 0.9441./x\n")
    outfile.write("y2 = 15 - x\n")
    outfile.write("plot (x,y1,x,y2)\n")
    outfile.write("xlim([-2 40])\n")
    outfile.write("ylim([-2 30])\n")


def computeColorFeas(f, minf, maxf):
    # Feasible color is between [0.5, 0.5, 0.5] (grey - worse f) and [1, 0, 0] (red - best f).
    if (f < minf):
        print("Warning: f (" + str(f) + ") < minf (" + str(minf) + "). This should not happen.")
        f = minf
    elif (f > maxf):
        print("Warning: f (" + str(f) + ") > maxf (" + str(maxf) + "). This should not happen.")
        f = maxf

    val = (maxf-f) / (2*(maxf-minf));
    r = val + 0.5;
    g = 0.5 - val;
    b = 0.5 - val;

    return [r, g, b]
    

def computeColorInf(h, minh, maxh):
    # Color for infeasible point is between [0, 0, 0] (black - worse h) and [0.5, 0.5, 0.5] (grey - best nonzero h).
    if (h < minh):
        print("Warning: h (" + str(h) + ") < minh (" + str(minh) + "). This should not happen.")
        h = minh
    elif (h > maxh):
        print("Warning: h (" + str(h) + ") > maxh (" + str(maxh) + "). This should not happen.")
        h = maxh


# Input: stats file with format: OBJ CONS_H SOL MESH_SIZE
# MESH_SIZE and SOL each have 2 values (DIMENSION=2).
[f, h, x1, x2, x, d1, d2, d, nbbbe] = readInfile("stats.txt", ["OBJ", "CONS_H", "SOL", "MESH_SIZE"]);
[minf, maxf, minh, maxh, minfforminh] = computeMinMax(f, h, x, d)
[xbestfeas, xbestinf] = findBestXFeasInf(minf, minh, minfforminh)

color = computeColorFeas(-0.0005, minf, maxf)
print(color)




outfile = open("v2.m", "w")

writeHeader(outfile)

outfile.close()



