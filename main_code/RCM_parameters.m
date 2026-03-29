%% RCM (RADARSAT Constellation Mission) Geometry Parameters
% Use this file to configure synthetic interferogram generation for RCM
% Copy/replace values into runGenDeformation.m, runGenTurbulent.m, runGenStratified.m

%% ========== RCM SENSOR SPECIFICATIONS ==========
% C-band wavelength (RCM: 5.405 cm)
wavelength = 0.05405;   % metres (RCM); original Sentinel-1 used 0.055465
m2rad = 4*pi/wavelength;
rad2m = wavelength/(4*pi);

% Satellite geometry - choose based on RCM beam mode
% Ascending orbit (typical): heading ~192 deg
% Descending orbit: heading ~12 deg
Heading = 192;          % degrees, azimuth clockwise from North
Incidence = 35;         % degrees (e.g. SC30MC, 16M8, 5M10 - mid-swath)

%% ========== SPATIAL RESOLUTION & FOOTPRINT ==========
% Choose ONE of these modes. Grid matches RCM pixel spacing.
% 500x500 grid (cropped to 227x227) - adjust if needed.

% Option A: Medium Resolution 30 m (125 km swath, 30m res)
RCM_mode = 'MR30';
pixelSpacing = 30;      % metres (RCM MR 30m mode)
halfExtent_m = 7500;    % 500/2 * 30m -> 7.5 km half-extent, 15 km total
x = -halfExtent_m:pixelSpacing:(halfExtent_m - pixelSpacing);
y = x;
% Cropped 227x227 patch = 6.81 km x 6.81 km

% Option B: Medium Resolution 16 m (30 km swath) - uncomment to use
% RCM_mode = 'MR16';
% pixelSpacing = 16;
% halfExtent_m = 4000;    % 500/2 * 16m -> 8 km total
% x = -halfExtent_m:pixelSpacing:(halfExtent_m - pixelSpacing);
% y = x;
% Cropped 227x227 = 3.63 km x 3.63 km

% Option C: Low Resolution 100 m (500 km swath) - uncomment to use
% RCM_mode = 'LR100';
% pixelSpacing = 100;
% halfExtent_m = 25000;   % 50 km total (matches original code)
% x = -halfExtent_m:pixelSpacing:(halfExtent_m - pixelSpacing);
% y = x;
% Cropped 227x227 = 22.7 km x 22.7 km

%% ========== OUTPUT PATCH SIZE ==========
% 227x227 for AlexNet; adjust if using different CNN input size
imageSize = 500;        % full grid before crop (must be >= 227)
halfcrop = floor(227/2);  % 113 -> crop 227x227 from centre

%% ========== TARGET SAMPLE COUNTS ==========
totalSamples = 10000;
samplesPerClass = 10000;

%% ========== DEFORMATION SOURCE (for defaultParameters / runGenDeformation) ==========
% Mogi (magma chamber) - common for volcanic deformation
Source_Type = 4;
Mogi.Depth  = 5;           % km
Mogi.Volume = 10*1e6;      % m^3

%% ========== OUTPUT PATHS ==========
% Update for your system (Windows / Mac / Linux)
outputRoot = '/path/to/your/output/synthesised_patches/';
inputRoot  = '/path/to/GACOS/stratify/volcano_2018/';  % for stratified only
