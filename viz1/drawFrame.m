function d = drawFrame(x, y, bigDelta, color)
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

    % draw lines between the four points to form a square.
    line([x1,x2], [y1,y2], 'LineWidth', 1.5, 'Color', color);
    line([x2,x3], [y2,y3], 'LineWidth', 1.5, 'Color', color);
    line([x3,x4], [y3,y4], 'LineWidth', 1.5, 'Color', color);
    line([x4,x1], [y4,y1], 'LineWidth', 1.5, 'Color', color);

end