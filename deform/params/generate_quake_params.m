
%% Define Source Parameters
% Source_Type = 1. Earthquakes

function Quake = generate_quake_params()
    Quake.Strike = 180 * rand;                                       % strike in degrees
    Quake.Dip = 30 + (90 - 30) * rand;                               % dip in degrees
    Quake.Rake = -180 + 360 * rand;                                  % rake in degrees
    Quake.Slip = 0.1 + (3.0 - 0.1) * rand;                           % magnitude of slip vector in metres
    Quake.Top_depth = 1 + (5 - 1) * rand;                            % depth (measured vertically) to top of fault in kilometres
    Quake.Bottom_depth = Quake.Top_depth + (2 + (10 - 2) * rand);    % depth (measured vertically) to bottom of fault in kilometres
    Quake.Length = 2 + (20 - 2) * rand;                              % fault length in kilometres
end


