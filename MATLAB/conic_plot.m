% Daniel DeConti - Elementary Orbit/Trajectory Function Plotter(2022-05-03)

% Takes determinant of 6x6 matrix to find symbolic equation for conic
% section of 5 points. Automatically plots on [min, max] range from inputs,
% need to add in better autofitting.
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
    disp(det(func))
    disp(collect(det(func), x^2))
    fimplicit(det(func) == 0, [x_min x_max y_min y_max]);
end
    