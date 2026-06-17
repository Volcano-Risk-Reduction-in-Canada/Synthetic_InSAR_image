function rgb = applyEVPhaseColorRamp(phase)
% Apply the EV phase cyclic color ramp to a wrapped phase image in [-pi, pi].
% Returns a uint8 H×W×3 RGB image.
    stops = [-pi, -2.35619, -1.57080, -0.78540, 0, 0.78540, 1.57080, 2.35619, pi];
    R_vals = uint8([0,   0, 102, 217, 255, 212,  98,   0,   0]);
    G_vals = uint8([191, 60,   0,   0,   0, 142, 236, 253, 191]);
    B_vals = uint8([169, 248, 234, 133,   0,   0,   0,  35, 169]);

    phase = max(-pi, min(pi, phase));
    rgb = cat(3, interp1(stops, single(R_vals), phase, 'linear'), ...
                 interp1(stops, single(G_vals), phase, 'linear'), ...
                 interp1(stops, single(B_vals), phase, 'linear'));
    rgb = uint8(round(rgb));
end
