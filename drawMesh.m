function d = drawMesh(x, y, bigDelta, smallDelta, color)
    % upper left corner
    x1 = x-bigDelta;
    y1 = y+bigDelta;
    % upper right corner
    x2 = x+bigDelta;
    y2 = y1;
    % lower right corner
    y3 = y-bigDelta;
    x3 = x2;
    % lower left corner
    y4 = y3;
    x4 = x1;
    
    % min and max
    xmin = x1;
    xmax = x2;
    ymin = y3;
    ymax = y1;

    % draw lines to form a mesh.
    % points on vertical frame lines
    ptWidth = 0.75;
    for v = xmin:smallDelta:xmax
        % Instead of drawing the whole grid, only indicate the points on
        % the grid that are interesting for us. The inside of the grid is
        % never used.
        drawMeshPoint(v, ymin, color);
        drawMeshPoint(v, ymax, color);
    end
    %points on horizontal frame lines
    for h = ymin:smallDelta:ymax
        drawMeshPoint(xmin, h, color);
        drawMeshPoint(xmax, h, color);
    end
end