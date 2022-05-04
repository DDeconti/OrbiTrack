% Daniel DeConti - Elementary Orbit/Trajectory Function Plotter(2022-05-03)
%syms x y
%
%x_vars = [8.025, 10.170, 11.202, 10.736, 9.092]
%y_vars = [8.310, 6.355, 3.212, 0.375, -2.267]
%
%x_min = min(x_vars)
%x_max = max(x_vars)
%y_min = min(y_vars)
%y_max = max(y_vars)

%A = [x^2 + y^2, x, y, 1; 50, 1, 7, 1; 40, 6, 2, 1; 52, 4, 6, 1]

%func = [x^2, x*y, y^2, x, y, 1]
 
%fimplicit(det(A) == 0, [x_min x_max y_min y_max]);

%conic_plot([1], [2])
function [] = conic_plot(x_vars, y_vars)
    syms x y
    x_vars = x_vars.';
    y_vars = y_vars.';
    x_min = min(x_vars)
    x_max = max(x_vars)
    y_min = min(y_vars)
    y_max = max(y_vars)
    ones = [1;1;1;1;1]; % improve later
    A = [x_vars.^2, x_vars.*y_vars, y_vars.^2, x_vars, y_vars, ones];
    func = [x^2, x*y, y^2, x, y, 1; A];
    disp(func)
    fimplicit(det(func) == 0, [x_min x_max y_min y_max]);
end

%conic_plot([1 2 3], [4 5 6])
    