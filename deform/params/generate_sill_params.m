
%% Define Source Parameters
% Source_Type = 3. Rectangular Sills

function Sill = generate_sill_params()
    Sill.Strike = 180 * rand;                    % strike (orientation of Length dimension) in degrees [no different]
    Sill.Dip = 0 + (15 - 0) * rand;              % Dip in degrees (usually zero or near zero)
    Sill.Opening = 0.05 + (5 - 0.05) * rand;     % magnitude of opening (perpendincular to plane) in metres
    Sill.Depth = 2 + (8 - 2) * rand;             % depth (measured vertically) to top of dyke in kilometres
    Sill.Width = 0.5 + (8 - 0.5) * rand;         % depth (measured vertically) to bottom of dyke in kilometres
    Sill.Length = 0.5 + (12 - 0.5) * rand;       % dyke length in kilometres
end
