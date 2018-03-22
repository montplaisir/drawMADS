function d = drawImage()
    color = [0.95, 0.85, 0.85];
    pt1 = [9, 9]; bigDelta = 4.0;
    drawGrid(pt1, bigDelta, color);
    drawX(pt1(1), pt1(2));
    
    pt2 = [pt1(1)+bigDelta, pt1(2)];
    % bigDelta increments because point has changed (success)
    bigDelta = 2.0 * bigDelta;
    %color(2) = color(2) + 0.05;
    %color(3) = color(3) + 0.1;
    drawGrid(pt2, bigDelta, color);

    pt3 = [pt2(1)+(bigDelta/2.0), pt2(2)+bigDelta];
    bigDelta = 2.0 * bigDelta;
    %color(2) = color(2) + 0.05;
    %color(3) = color(3) + 0.1;
    drawGrid(pt3, bigDelta, color);

    pt4 = pt3;
    % bigDelta decrements because point is the same (failure)
    bigDelta = 0.5 * bigDelta;
    %color(2) = color(2) + 0.05;
    %color(3) = color(3) + 0.1;
    drawGrid(pt4, bigDelta, color);

    pt5 = pt4;
    bigDelta = 0.5 * bigDelta;
    %color(2) = color(2) + 0.05;
    %color(3) = color(3) + 0.1;
    drawGrid(pt5, bigDelta, color);

    pt6 = pt5;
    bigDelta = 0.5 * bigDelta;
    %color(2) = color(2) + 0.05;
    %color(3) = color(3) + 0.1;
    drawGrid(pt6, bigDelta, color);
    
    pt7 = [pt6(1)+(bigDelta/2.0), pt6(2)+bigDelta];
    bigDelta = 2.0 * bigDelta;
    %color(2) = color(2) + 0.05;
    %color(3) = color(3) + 0.1;
    drawGrid(pt7, bigDelta, color);

    pt8 = pt7;
    bigDelta = 0.5 * bigDelta;
    %color(2) = color(2) + 0.05;
    %color(3) = color(3) + 0.1;
    drawGrid(pt8, bigDelta, color);
    
    pt9 = pt8;
    bigDelta = 0.5 * bigDelta;
    %color(2) = color(2) + 0.05;
    %color(3) = color(3) + 0.1;
    drawGrid(pt9, bigDelta, color);
    
    % draw points again, because we don't see them so well.
    drawX(pt1(1), pt1(2));
    drawPoint(pt2(1), pt2(2));
    drawPoint(pt3(1), pt3(2));
    drawStar(pt7(1), pt7(2));
end