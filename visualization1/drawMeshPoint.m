function d = drawMeshPoint(x, y, color)
    w = 0.75;
    line([x,x],[y-w/2,y+w/2], 'LineWidth', w, 'Color', color);
    line([x-w/2,x+w/2],[y,y], 'LineWidth', w, 'Color', color);