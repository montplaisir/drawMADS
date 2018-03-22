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
    % vertical lines
    ptWidth = 0.75;
    for v = xmin:smallDelta:xmax
    %    line([v,v], [ymin,ymax], 'Color', color);
        % Instead of drawing the whole grid, only indicate the points on
        % the grid that are interesting for us. The inside of the grid is
        % never used.
        line([v,v], [ymin-ptWidth,ymin+ptWidth], 'Color', color);
        line([v,v], [ymax-ptWidth,ymax+ptWidth], 'Color', color);      
    end
    %horizontal lines
    for h = ymin:smallDelta:ymax
        %line([xmin,xmax], [h,h], 'Color', color)
        line([xmin-ptWidth,xmin+ptWidth], [h,h], 'Color', color)
        line([xmax-ptWidth,xmax+ptWidth], [h,h], 'Color', color)

    end
end