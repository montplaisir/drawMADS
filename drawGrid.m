function d = drawGrid(point, bigDelta, color)
    x = point(1);
    y = point(2);
    smallDelta = min([bigDelta, bigDelta*bigDelta]);
    
    drawFrame(x, y, bigDelta, color);
    drawMesh(x, y, bigDelta, smallDelta, color);
    % we draw the current X later so it does not get overwritten
    % by another mesh.
    %drawPoint(x, y);
end