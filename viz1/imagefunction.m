function f = imagefunction()
% general: random entre 0.3 et 0.6.
mat = rand(33)/5.0+0.4;
% 2eme creux: entre 0.2 et 0.3.
mat(20:26,4:6) = rand(7,3)/10.0+0.2; 
% 2eme creux: ravin entre 0.1 et 0.2.
mat(21:25, 5) = rand(5,1)/10.0+0.1;

% X0
mat(9,9) = 0.5;

% X1 disons
mat(9, 13) = 0.2;
% Autour de X1 mettre des points a faible valeur pour une meilleure
% visualisation
mat(8, 13) = 0.21;
mat(9, 12) = 0.21;
mat(8, 14) = 0.23;
mat(10, 14) = 0.21;
mat(7, 13) = 0.22;

% 1er creux: entre 0.1 et 0.3.
mat(16:22,16:22) = rand(7,7)/5.0+0.1;
mat(15,22) = 0.31;
mat(15,23) = 0.34;
mat(16,22) = 0.36;
mat(15,24) = 0.33;
mat(14,24) = 0.33;
mat(17,17) = 0.1;
mat(19,18) = 0.0; % solution optimale

royalBlue = [0, 0, 0.8];
royalBlue1 = [0, 0, 0.9];
royalBlue2 = [0.1, 0.1, 0.9];
lightBlue = [0, 0.4, 0.8];
greyBlue = [0.4, 0.4, 0.5];
tropicalBlue = [0, 0.45, 0.4];
tropicalBlue1 = [0, 0.5, 0.4];
greyOrange = [0.6, 0.5, 0.3];
orange = [0.8, 0.6, 0.1];
canary2 = [0.82, 0.7, 0.15];
canary1 = [0.88, 0.82, 0.19];
canary = [0.9, 0.85, 0.2];

map = [ canary
        canary1
        canary1
        orange
        greyOrange
        greyBlue
        tropicalBlue
        tropicalBlue1
        royalBlue1
        royalBlue1
        royalBlue];

colormap(map);
contourf(mat, 'LineStyle', 'none');
% hide axes
ax = gca;
ax.Visible = 'off';

end

