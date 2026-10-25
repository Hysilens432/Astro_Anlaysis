% Ploting 3D data based on the galactic positions provided in harris I 


% constants

const r0_kpc = 8.0; % 8) "Distance from Galactic center (kpc), assuming R_0=8.0 kpc" Harris one





% Settings, Should be obvious w/ the names 
limitsKpc = [20, 100];
saveFigures = true;
style.widthCm = 24;
style.heightCm = 21;
style.fontSize = 10;
style.markerSize = 30;                  
style.colormap = parula(256);
style.noDataColour = [0.78 0.78 0.78]; % edge case, dataNA, grey
style.edgeColour = [0.20 0.20 0.20]; % outline of points
style.guideColour = [0.45 0.45 0.45]; % sun's orbit around smbh, mid grey
style.centreStyle = {'k+', 'MarkerSize', 10, 'LineWidth', 1.5}; % SMBH
style.sunStyle = {'o', 'MarkerSize', 7, 'MarkerFaceColor', [1 0.85 0], 'MarkerEdgeColor', 'k'}; % sun yellow
style.dpi = 300; % resolution 