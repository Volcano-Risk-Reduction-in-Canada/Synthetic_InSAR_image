function [num_fringes, detectable, max_disp, min_disp, disp_range] = count_fringes_from_los(los_grid)
    fringe_spacing = 0.028333;  % meters

    max_disp = max(los_grid(:));
    min_disp = min(los_grid(:));
    disp_range = max_disp - min_disp;

    num_fringes = disp_range / fringe_spacing;
    detectable = num_fringes >= 1.5;

end



