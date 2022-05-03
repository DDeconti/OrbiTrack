% Daniel DeConti - Elementary Orbit/Trajectory Function Plotter(2022-05-03)
syms x y

x_vars = [8.025, 10.170, 11.202, 10.736, 9.092]
y_vars = [8.310, 6.355, 3.212, 0.375, -2.267]

x_min = min(x_vars)
x_max = max(x_vars)
y_min = min(y_vars)
y_max = max(y_vars)

%A = [x^2 + y^2, x, y, 1; 50, 1, 7, 1; 40, 6, 2, 1; 52, 4, 6, 1]

func = [x^2, x*y, y^2, x, y, 1]
 
fimplicit(det(A) == 0, [x_min x_max y_min y_max]);
