
%% Define Source Parameters
% Source_Type = 2. Dykes

function Dyke = generate_dyke_params()
    Dyke.Strike = 180 * clamped_rand();                                      % strike in degrees [0-180]
    Dyke.Dip = 80 + (90 - 80) * clamped_rand();                              % dip in degrees (usually 90 or near 90)
    Dyke.Opening = 0.05 + (1.5 - 0.05) * clamped_rand();                     % magnitude of opening (perpendincular to plane) in metres
    Dyke.Top_depth = 1 + (4 - 1) * clamped_rand();                           % depth (measured vertically) to top of dyke in kilometres
    Dyke.Bottom_depth = Dyke.Top_depth + (1 + (6 - 1) * clamped_rand());     % depth (measured vertically) to bottom of dyke in kilometres
    Dyke.Length = 2 + (15 - 2) * clamped_rand();                             % dyke length in kilometres
end
