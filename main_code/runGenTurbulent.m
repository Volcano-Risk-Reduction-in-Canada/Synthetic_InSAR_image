% This code is for generate turbu atmospheric delay

clear all
runConfig;

addpath(fullfile(fileparts(mfilename('fullpath')), '..', 'turbulent'));
SAVEWRAP = 0;
mkdir([outputRoot, 'set1/unwrap/turbulent/']);
mkdir([outputRoot, 'set2/unwrap/turbulent/']);
if SAVEWRAP == 1
    mkdir([outputRoot, 'set1/wrap/turbulent/']);
    mkdir([outputRoot, 'set2/wrap/turbulent/']);
end
% parameters
rows = 100;
cols = 100;
psizex = 1;
psizey = 1;
covmodel_type = 0;
N = 20000/25;
% chipSize and halfcrop come from runConfig
imageSize = chipSize + 200;  % resize target before crop; 200px margin (~1.5km at 15m)

for maxvar = 7.5+[-2 -1 0 0.75 1.5]
    for alpha = 0.008*[0.5 0.75 1 1.5 2]
        disp([sprintf('%0.2f',maxvar),'_', sprintf('%0.4f',alpha)]);
        % generate turbulent atmosphere
        atm_pets = pcmc_atm(rows,cols,maxvar,alpha,covmodel_type,N,psizex,psizey);
        for k = 1:N
            curTur = imresize(atm_pets(:,:,k),[imageSize imageSize]);
            curTur = curTur(round(size(curTur,1)/2) + (-halfcrop:halfcrop-1),round(size(curTur,2)/2) + (-halfcrop:halfcrop-1));
            
            outputDir = [outputRoot, 'set', num2str(2-rem(k,2)),'/unwrap/turbulent/'];
            save([outputDir, 'turb_', sprintf('%0.2f',maxvar),'_', sprintf('%0.4f',alpha), '_', sprintf('%03d', k), '.mat'],'curTur');
            if SAVEWRAP == 1
                curTur = wrapTo2Pi(curTur)-pi;
                curTur = (curTur-min(curTur(:)))/range(curTur(:));
                outputDir = [outputRoot, 'set', num2str(2-rem(k,2)),'/wrap/turbulent/'];
                imwrite(curTur, [outputDir, 'turb_', sprintf('%0.2f',maxvar),'_', sprintf('%0.4f',alpha), '_', sprintf('%03d', k), '.png']);
            end
        end
    end
end

