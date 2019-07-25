#!/usr/bin/python
import numpy as np

#Reading an avi file does not work on my computer, so I am not sure if this works.
writeMovie = False

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


def computeMinMax(f, h, x, d1, d2):
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
    mind = [mind1, mind2]
    maxd1 = max(d1)
    maxd2 = max(d2)
    maxd = [maxd1, maxd2]

    fforminh_temp = []
    for i in range(0, len(f)):
        if (h[i] == minh):
            fforminh_temp.append(f[i])
    minfforminh = min(fforminh_temp)

    if (minh == maxh):
        # We'll decide later what we do in this case - it's treatable.
        print("Warning: minh = maxh = " + str(minh))

    return [minf, maxf, minh, maxh, minfforminh, mind, maxd]
    #end computeMinMax


def findBestXFeasInf(minf, minh, minfforminh, f, h, x):
    # Find xbestfeas and xbestinf
    # xbestfeas is x for which f = minf and h = 0
    xbf_temp = []
    xbi_temp = []
    for i in range(0, len(f)):
        if (f[i] == minf and h[i] == 0):
            xbf_temp.append(x[i])
        elif (h[i] == minh and f[i] == minfforminh):
            xbi_temp.append(x[i])
    xbestfeas = np.array(xbf_temp)
    xbestinf  = np.array(xbi_temp)

    return [xbestfeas, xbestinf]
    #end findBestXFeasInf


def computeCenter1(listofpoints):
    if not len(listofpoints):
        print("Warning: Calling computeCenter1 with an empty list of points")
        return []

    sumx = 0
    sumy = 0
    for x in listofpoints:
        sumx += x[0]
        sumy += x[1]
    cx = sumx / len(listofpoints)
    cy = sumy / len(listofpoints)
    center = [cx, cy]

    return center
    #end computeCenter1


def computeCenter(xbestfeas, xbestinf):
    bestFeasCenter = []
    bestInfCenter = []
    center = []

    if xbestfeas.size:
        bestFeasCenter = computeCenter1(xbestfeas)
    if xbestinf.size:
        bestInfCenter  = computeCenter1(xbestinf)

    if bestFeasCenter and bestInfCenter:
        center = computeCenter1([bestFeasCenter, bestInfCenter])
    elif bestFeasCenter:
        center = bestFeasCenter
    elif bestInfCenter:
        center = bestInfCenter
    else:
        print("Warning: computeCenter could not compute... center")

    return center
    #end computeCenter


def writeFunc(outfile, xlim):
    # These are the bb constraints. We concentrate on this problem for now.
    if xlim[0] >= xlim[1]:
        return
    xlim0 = max(0,xlim[0]);
    step = (xlim[1]-xlim0)/100
    outfile.write("x = "+str(xlim0)+":"+str(step)+":"+str(xlim[1])+"\n")
    outfile.write("y1 = 0.9441./x\n")
    outfile.write("y2 = 15 - x\n")
    outfile.write("plot (x,y1,'b',x,y2,'r')\n")
    #end writeFunc


def writeHeader(outfile):
    if writeMovie:
        outfile.write("writerObj = VideoWriter('out.avi');\n")
        outfile.write("writerObj.FrameRate = 60;\n")
        outfile.write("open(writerObj);\n")
    outfile.write("fId = figure('units','normalized','outerposition',[0 0 1 1]);\n")
    outfile.write("hold on\n")

    #end writeHeader


def computeRescale(center, nbbbe, bbe, di, mind, maxd):
    # Depending on bbe, scale will go between A and B.
    A = [2*maxd[0], 2*maxd[1]]
    B = [100*mind[0], 100*mind[1]]
    # B must not be too small, or else in the end we get no valuable rescaling
    B[0] = max(1e-3, B[0])
    B[1] = max(1e-3, B[1])
    val = 2*[None]  # Lists with two values, to be filled next
    xlim = 2*[None]
    ylim = 2*[None]
    val[0] = (B[0]*bbe + A[0]*(nbbbe-bbe-1)) / (nbbbe-1)
    val[1] = (B[1]*bbe + A[1]*(nbbbe-bbe-1)) / (nbbbe-1)
    xlim[0] = round(center[0] - val[0], 6)
    xlim[1] = round(center[0] + val[0], 6)
    ylim[0] = round(center[1] - val[1], 6)
    ylim[1] = round(center[1] + val[1], 6)

    return [xlim, ylim]


def writeRescale(outfile, xlim, ylim):

    outfile.write("xlim(["+str(xlim[0])+" "+str(xlim[1])+"]);\n")
    outfile.write("ylim(["+str(ylim[0])+" "+str(ylim[1])+"]);\n")

    #end writeRescale


def writeDelay(outfile, delay):
    outfile.write("pause("+str(delay)+");\n")


def writeIter(outfile, xi, di, color, delay):
    prec = 0.0001
    # r1 and r2: half-length and half-height of the rectangle to draw around point
    r1 = round(di[0]+prec, 5)
    r2 = round(di[1]+prec, 5)
    # px and py: position of the point
    px = round(xi[0], 6);
    py = round(xi[1], 6);

    outfile.write("color=" + str(color)+";")
    outfile.write(" r1="+str(r1)+"; r2="+str(r2)+";")
    outfile.write(" px="+str(px)+"; py="+str(py)+";")
    outfile.write(" rectangle('Position',[px-r1 py-r2 r1*2 r2*2], 'FaceColor', color, 'EdgeColor', color);")
    writeDelay(outfile, delay)
    if writeMovie:
        outfile.write(" figure(fId); frame = getframe(gcf); writeVideo(writerObj,frame);\n")

    #end writeIter


def writeEnd(outfile, xbestfeas, xbestinf, mind, delay):
    # At the end, re-write the best feasible and infeasible points
    # infeasible first, so the feasible appear on top.
    #delay = 0
    color = [0.0, 0.0, 0.2]
    for xbest in xbestinf:
        writeIter(outfile, xbest, mind, color, delay)
    color = [0.95, 0.4, 0.7]
    for xbest in xbestfeas:
        writeIter(outfile, xbest, mind, color, delay)

    #outfile.write("hold\n")


def computeColorFeas(f, minf, maxf):
    # Feasible color is between [0.5, 0.5, 0.5] (grey - worse f) and [1, 0, 0] (red - best f).
    if (f < minf):
        print("Warning: f (" + str(f) + ") < minf (" + str(minf) + "). This should not happen.")
        f = minf
    elif (f > maxf):
        print("Warning: f (" + str(f) + ") > maxf (" + str(maxf) + "). This should not happen.")
        f = maxf

    val = (maxf-f) / (2*(maxf-minf))
    r = round(val + 0.5, 2)
    g = round(0.5 - val, 2)
    b = round(0.5 - val, 2)

    return [r, g, b]
    #end computeColorFeas
    

def computeColorInf(h, minh, maxh):
    # Color for infeasible point is between [0, 0, 0] (black - worse h) and [0.5, 0.5, 0.5] (grey - best nonzero h).
    if (h < minh):
        print("Warning: h (" + str(h) + ") < minh (" + str(minh) + "). This should not happen.")
        h = minh
    elif (h > maxh):
        print("Warning: h (" + str(h) + ") > maxh (" + str(maxh) + "). This should not happen.")
        h = maxh
    val = (maxh-h) / (2*(maxh-minh))
    r = round(val, 2)
    g = round(val, 2)
    b = round(val, 2)

    return [r, g, b]
    #end computeColorInf


def doMadsFile():
    # Input: stats file with format: OBJ CONS_H SOL MESH_SIZE
    # MESH_SIZE and SOL each have 2 values (DIMENSION=2).
    [f, h, x1, x2, x, d1, d2, d, nbbbe] = readInfile("stats.txt", ["OBJ", "CONS_H", "SOL", "MESH_SIZE"])
    [minf, maxf, minh, maxh, minfforminh, mind, maxd] = computeMinMax(f, h, x, d1, d2)
    [xbestfeas, xbestinf] = findBestXFeasInf(minf, minh, minfforminh, f, h, x)

    center = computeCenter(xbestfeas, xbestinf)

    filename = "v2.m"
    outfile = open(filename, "w")

    writeHeader(outfile)

    [xlim, ylim] = computeRescale(center, nbbbe, 0, d[0], mind, maxd)
    writeFunc(outfile, xlim)

    delay = max(0.005, 10 / nbbbe)

    for bbe in range(0, nbbbe):
        xi = x[bbe]
        di = d[bbe]
        if (h[bbe] == 0):
            color = computeColorFeas(f[bbe], minf, maxf)
        else:
            color = computeColorInf(h[bbe], minh, maxh)

        [xlim, ylim] = computeRescale(center, nbbbe, bbe, di, mind, maxd)
        writeRescale(outfile, xlim, ylim)
        # Rewrite functions once in a while.
        if bbe % round(nbbbe / 20) == 0:
            writeFunc(outfile, xlim)
        writeIter(outfile, xi, di, color, delay)

    writeEnd(outfile, xbestfeas, xbestinf, mind, delay)
    writeDelay(outfile, 1)

    # Zoom out
    # Not quite working yet. Problem with writeFunc (see in loop above),
    # among other things.
    for k in range(1,nbbbe-200,((nbbbe-200)/20)):
        bbe = nbbbe-k
        writeDelay(outfile, 0.01);
        [xlim, ylim] = computeRescale(center, nbbbe, bbe, d[bbe], mind, maxd)
        writeRescale(outfile, xlim, ylim)
        writeFunc(outfile, xlim)
        writeEnd(outfile, xbestfeas, xbestinf, [k*max(1e-4,mind[0]), k*max(1e-4,mind[1])], delay)

    outfile.close()


doMadsFile()



