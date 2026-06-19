clear all
runConfig;

% parameters
samplesPerClass = 10000;

% input directories
patchDirWrap   = [rootDir, 'all/wrap/'];
patchDirUnwrap = [rootDir, 'all/unwrap/'];
deformList     = dir([patchDirUnwrap,'deform/*.mat']);
turbulentList  = dir([patchDirUnwrap,'turbulent/*.mat']);
stratifiedList = dir([patchDirUnwrap,'stratified/*.mat']);
% use minimum available to avoid errors
nAvailable = min([length(deformList), length(turbulentList), length(stratifiedList)]);
nSamples = min(samplesPerClass, nAvailable);
if nSamples == 0, error('No data in one or more component directories.'); end
% get shuffled index for combination
indDeform     = randperm(length(deformList),     nSamples);
indTurbulent  = randperm(length(turbulentList),  nSamples);
indStratified = randperm(length(stratifiedList), nSamples);
% output directories
outputDirWrap   = [patchDirWrap,   'combine/'];
outputDirUnwrap = [patchDirUnwrap, 'combine/'];
mkdir(outputDirWrap);
mkdir(outputDirUnwrap);
% merging process
for k = 1:nSamples
    % get deformation
    load([patchDirUnwrap, 'deform/',     deformList(indDeform(k)).name(1:end-3),      'mat']);
    load([patchDirUnwrap, 'turbulent/',  turbulentList(indTurbulent(k)).name(1:end-3), 'mat']);
    load([patchDirUnwrap, 'stratified/', stratifiedList(indStratified(k)).name(1:end-3),'mat']);
    if range(los_grid(:))<=15
        los_grid = los_grid*18/range(los_grid(:));
        save([patchDirUnwrap, 'deform/', deformList(indDeform(k)).name(1:end-3),'mat'],'los_grid');
    elseif range(los_grid(:))>=50
        los_grid = los_grid*40/range(los_grid(:));
        save([patchDirUnwrap, 'deform/', deformList(indDeform(k)).name(1:end-3),'mat'],'los_grid');
    end
    insarImg  = los_grid + curTur + atmo;
    mask      = imerode(atmo~=0,strel('disk',3));
    insarWrap = (wrapTo2Pi(insarImg)-pi);
    insarWrap = (insarWrap-min(insarWrap(:)))/range(insarWrap(:)).*mask;
    outputName = ['comb_', sprintf('%05d', k)];
    imwrite(insarWrap, [outputDirWrap, outputName, '.png']);
    save([outputDirUnwrap, outputName, '.mat'], 'insarImg', 'mask');
end
