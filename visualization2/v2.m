writerObj = VideoWriter('out.avi');
writerObj.FrameRate = 60;
open(writerObj);
fId = figure;
hold
x = -2:.05:18
y1 = 0.9441./x
y2 = 15 - x
plot (x,y1,x,y2)
xlim([-2 40])
ylim([-2 30])
