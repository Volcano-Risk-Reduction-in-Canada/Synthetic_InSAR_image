function cmap = phase_colormap(n)
    %phase_colormap Generate a custom colormap with n points
    % Usage:
    %   cmap = phase_colormap();        % Default 256 points
    %   cmap = phase_colormap(128);     % Custom number of points
    
    if nargin < 1
        n = 256; % Default to 256 points
    end
    
    % Define the input data for the colormap
    x = [-3.14159, -2.35619, -1.57080, -0.78540, 0.00000, ...
          0.78540, 1.57080, 2.35619, 3.14159];
    colors = [
        0/255, 191/255, 169/255;  % Corresponding RGB for -3.14159
        0/255, 60/255, 248/255;   % Corresponding RGB for -2.35619
        102/255, 0/255, 234/255;  % Corresponding RGB for -1.57080
        217/255, 0/255, 133/255;  % Corresponding RGB for -0.78540
        255/255, 0/255, 0/255;    % Corresponding RGB for 0.00000
        212/255, 142/255, 0/255;  % Corresponding RGB for 0.78540
        98/255, 236/255, 0/255;   % Corresponding RGB for 1.57080
        0/255, 253/255, 35/255;   % Corresponding RGB for 2.35619
        0/255, 191/255, 169/255;  % Corresponding RGB for 3.14159
    ];

    % Interpolate the colors over n points
    interp_points = linspace(-3.14159, 3.14159, n);
    red_interp = interp1(x, colors(:,1), interp_points, 'linear');
    green_interp = interp1(x, colors(:,2), interp_points, 'linear');
    blue_interp = interp1(x, colors(:,3), interp_points, 'linear');
    
    % Combine into colormap
    cmap = [red_interp(:), green_interp(:), blue_interp(:)];
end
