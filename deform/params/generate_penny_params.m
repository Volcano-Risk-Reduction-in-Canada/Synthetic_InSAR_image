
%% Define Source Parameters
% Source_Type = 5. Pressurized Penny-shaped Horizontal Crack (Fialko) - Sill
% Note, this is the slowest to calculate of the various sources

function Penny = generate_penny_params()
    Penny.Depth = 2 + (8 - 2) * rand;               % Depth of crack in km^3
    Penny.Pressure = 10^(5 + (7 - 5) * rand);       % Pressure of crack in Pa
    Penny.Radius = 1 + (8 - 1) * rand;              % Radius of crack in km^3
end
