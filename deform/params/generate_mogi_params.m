
%% Define Source Parameters
% Source_Type = 4. Magma Chamber - point pressure

function Mogi = generate_mogi_params(d_bin, v_bin, number_bins)
    depth_bins = linspace(2, 6, number_bins + 1);
    volume_bins = logspace(6, 8, number_bins + 1);

    % Depth of Mogi Source (2-6 km)
    Mogi.Depth = depth_bins(d_bin) + ...
        (depth_bins(d_bin + 1) - depth_bins(d_bin)) * rand;

    % Volume in m^3 (1e6-1e8)
    Mogi.Volume = volume_bins(v_bin) * ...
        (volume_bins(v_bin + 1) / volume_bins(v_bin))^rand;

end
