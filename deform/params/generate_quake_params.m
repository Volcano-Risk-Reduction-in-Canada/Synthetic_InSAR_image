
%% Define Source Parameters
% Source_Type = 1. Earthquakes

function Quake = generate_quake_params()
    Quake.Strike = 180 * rand;                                       % strike in degrees
    Quake.Dip = 30 + (90 - 30) * clamped_rand();                               % dip in degrees
    Quake.Rake = -180 + 360 * clamped_rand();                                  % rake in degrees
    Quake.Slip = 0.1 + (3.0 - 0.1) * clamped_rand();                           % magnitude of slip vector in metres
    Quake.Top_depth = 1 + (5 - 1) * clamped_rand();                            % depth (measured vertically) to top of fault in kilometres
    Quake.Bottom_depth = Quake.Top_depth + (2 + (10 - 2) * clamped_rand());    % depth (measured vertically) to bottom of fault in kilometres
    Quake.Length = 2 + (20 - 2) * clamped_rand();                              % fault length in kilometres
end


