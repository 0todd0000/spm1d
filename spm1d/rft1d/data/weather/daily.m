%  add path to data and functions

addpath ('../..')

%  Last modified 22 September 2009

%  -----------------------------------------------------------------------
%                     Daily Weather Data
%  -----------------------------------------------------------------------

%  -----------------------  input the raw data  -----------------------

fid    = fopen('dailtemp.dat','rt');
tempav = fscanf(fid,'%f');
tempav = reshape(tempav, [365,35]);

fid    = fopen('dailprec.dat','rt');
precav = fscanf(fid,'%f');
precav = reshape(precav, [365,35]);

%  set up the times of observation at noon

daytime   = (1:365)'-0.5;
dayrange  = [0,365];
dayperiod = 365;

%  day values roughly in weeks

weeks = linspace(0,365,53)';   

%  define 8-character names for stations

place = [ ...
    'Arvida     '; ...
    'Bagottville'; ...
    'Calgary    '; ...
    'Charlottown'; ...
    'Churchill  '; ...
    'Dawson     '; ...
    'Edmonton   '; ...
    'Fredericton'; ...
    'Halifax    '; ...
    'Inuvik     '; ...
    'Iqaluit    '; ...
    'Kamloops   '; ...
    'London     '; ...
    'Montreal   '; ...
    'Ottawa     '; ...
    'Pr. Albert '; ...
    'Pr. George '; ...
    'Pr. Rupert '; ...
    'Quebec     '; ...
    'Regina     '; ...
    'Resolute   '; ...
    'Scheffervll'; ...
    'Sherbrooke '; ...
    'St. Johns  '; ...
    'Sydney     '; ...
    'The Pas    '; ...
    'Thunder Bay'; ...
    'Toronto    '; ...
    'Uranium Cty'; ...
    'Vancouver  '; ...
    'Victoria   '; ...
    'Whitehorse '; ...
    'Winnipeg   '; ...
    'Yarmouth   '; ...
    'Yellowknife'];

%  set up indices that order the stations from east to west to north

geogindex = [24,  9, 25, 34,  4,  8, 22,  1,  2, 19, 23, 14, 15, 28, 13, ...
             27, 33, 26,  5, 20, 16, 29,  7,  3, 12, 30, 31, 17, 18, 32, ...
              6, 35, 11, 10, 21];
         
place  = place(geogindex,:);
tempav = tempav(:,geogindex);
precav = precav(:,geogindex);

%  define 1-character names for months

monthletter = ['J'; 'F'; 'M'; 'A'; 'M'; 'J'; 'J'; 'A'; 'S'; 'O'; 'N'; 'D'];

%  load the data from file daily.mat.  The stations in this file have
%  been rearranged to run from east to west to north.

load daily

%  -------------  set up fourier basis  ---------------------------
%  Here it was decided that 65 basis functions captured enough of
%  the detail in the temperature data: about one basis function
%  per week.  However, see below for smoothing with a saturated
%  basis (365 basis functions) where smoothing is defined by the
%  GCV criterion.

nbasis     = 65;
daybasis65 = create_fourier_basis(dayrange, nbasis);

%  ----  set up the harmonic acceleration operator  -------

Lbasis  = create_constant_basis(dayrange);  %  create a constant basis
Lcoef   = [0,(2*pi/365)^2,0];    %  set up three coefficients
wfd     = fd(Lcoef,Lbasis);      % define an FD object for weight functions
wfdcell = fd2cell(wfd);          % convert the FD object to a cell object
harmaccelLfd = Lfd(3, wfdcell);  %  define the operator object

%  ---------  create fd objects for temp. and prec. ------------

daytempfd = smooth_basis(daytime, tempav, daybasis65);
daytempfd_fdnames{1} = 'Day';
daytempfd_fdnames{2} = 'Station';
daytempfd_fdnames{3} = 'Deg C';
daytempfd = putnames(daytempfd, daytempfd_fdnames);

dayprecfd = smooth_basis(daytime, precav, daybasis65);
dayprecfd_fdnames{1} = 'Day';
dayprecfd_fdnames{2} = 'Station';
dayprecfd_fdnames{3} = 'mm';
dayprecfd = putnames(dayprecfd, dayprecfd_fdnames);

%  Plot temperature curves and values

plotfit_fd(tempav, daytime, daytempfd, place)

%  Plot residuals for three best fits and three worst fits

casenames = place;
varnames  = 'Temperature';
rng       = dayrange;
index     = [1,2,3,33,34,35];
residual  = 1;
sortwrd   = 1;

plotfit_fd(tempav, daytime, daytempfd, casenames, varnames, ...
           residual, sortwrd, rng, index)

%  Plot precipitation curves and values

plotfit_fd(precav, daytime, dayprecfd, place)

%  Assessment: the functions are definitely too rough with
%  this many basis functions, and especially for precip. which
%  has a much higher noise level.

%  these smoothing parameter values probably undersmooth the data,
%  but we can impose further smoothness on the results of analyses

%  set up the functional parameter objects to define smoothing

templambda = 1e1;
preclambda = 1e5;

tempfdPar  = fdPar(daybasis65, harmaccelLfd, templambda);
precfdPar  = fdPar(daybasis65, harmaccelLfd, preclambda);

daytempfd = smooth_fd(daytempfd, tempfdPar);
dayprecfd = smooth_fd(dayprecfd, precfdPar);

%  plot each pair of functions along with raw data

tempmat = eval_fd(daytempfd, daytime);
precmat = eval_fd(dayprecfd, daytime);

index = 1:35;
for i = index
  subplot(2,1,1)
  plot(daytime,tempav(:,i),'ro',daytime,tempmat(:,i),'-')
  axis([0 365 -35 25])
  xlabel('Day')
  ylabel('Temperature (deg. C)')
  title(place(i,:))
  subplot(2,1,2)
  plot(daytime,precav(:,i),'ro',daytime,precmat(:,i),'-')
  axis([0 365 0 13])
  xlabel('Day')
  ylabel('Precipitation (mm)')
  pause
end

%  plot all the functions

figure(1)
subplot(1,1,1)
plot(daytempfd);
  axis([0 365 -35 25])
xlabel('\fontsize{12} Day')
title('\fontsize{16} Mean Temperature')

figure(2)
subplot(1,1,1)
plot(dayprecfd);
  axis([0 365 0 13])
xlabel('\fontsize{12} Day')
title('\fontsize{16} Mean Precipitation')

%  -------------------------------------------------------------
%                 Choose level of smoothing using 
%          the generalized cross-validation criterion
%              with smoothing function smooth_basis.
%  -------------------------------------------------------------

% set up a saturated basis capable of interpolating the data

nbasis      = 365;  
daybasis365 = create_fourier_basis(dayrange, nbasis);

%  --------------------  smooth temperature  ------------------

%  set up range of smoothing parameters in log_10 units

loglam = (-5:1)';
nlam   = length(loglam);

dfsave  = zeros(nlam,1);
gcvsave = zeros(nlam,1);

%  loop through smoothing parameters

for ilam=1:length(loglam)
    lambda = 10^loglam(ilam);
    display(['lambda = ',num2str(lambda)])
    fdParobj = fdPar(daybasis365, harmaccelLfd, lambda);
    [fdobj, df, gcv] = smooth_basis(daytime, tempav, fdParobj);
    dfsave(ilam)  = df;
    gcvsave(ilam) = sum(gcv);
end

%  display and plot degrees of freedom and GCV criterion

disp('Log lambda    df          gcv')
disp([loglam, dfsave, gcvsave])

figure(1)
subplot(2,1,1)
plot(loglam, gcvsave, 'o-')
ylabel('\fontsize{16} GCV Criterion')
title('\fontsize{16} Temperature Smoothing')
subplot(2,1,2)
plot(loglam, dfsave, 'o-')
xlabel('\fontsize{16} log_{10} \lambda')
ylabel('\fontsize{16} Degrees of Freedom')

%  Do final smooth with minimum GCV value

lambda   = 0.01;  %  minimum GCV estimate, corresponding to 255 df
fdParobj = fdPar(daybasis365, harmaccelLfd, lambda);

[daytempfd, df, gcv, coef, SSE] = ...
             smooth_basis(daytime, tempav, fdParobj);

disp(['Degrees of freedom = ',num2str(df)])
disp(['Generalized cross-validation = ',num2str(sum(gcv))])

%  estimate standard error of fit

stderr = sqrt(sum(SSE)/(35*(365-df)));  %  0.26 deg C

disp(['standard error of fit = ',num2str(stderr)])

%  plot data and fit

subplot(1,1,1)
plotfit_fd(tempav, daytime, daytempfd, place)

%  --------------------  smooth precipitation  ------------------

%  set up range of smoothing parameters in log_10 units

loglam = (4:9)';
nlam = length(loglam);

dfsave  = zeros(nlam,1);
gcvsave = zeros(nlam,1);

%  loop through smoothing parameters
for ilam=1:nlam
    lambda = 10^loglam(ilam);
    display(['lambda = ',num2str(lambda)])
    fdParobj = fdPar(daybasis365, harmaccelLfd, lambda);
    [fdobj, df, gcv] = smooth_basis(daytime, precav, fdParobj);
    dfsave(ilam)  = df;
    gcvsave(ilam) = sum(gcv);
end

%  display and plot degrees of freedom and GCV criterion

disp('Log lambda    df          gcv')
disp([loglam, dfsave, gcvsave])

subplot(2,1,1)
plot(loglam, gcvsave, 'o-')
ylabel('\fontsize{16} GCV Criterion')
title('\fontsize{16} Precipitation Smoothing')
subplot(2,1,2)
plot(loglam, dfsave, 'o-')
xlabel('\fontsize{16} log_{10} \lambda')
ylabel('\fontsize{16} Degrees of Freedom')

%  Do final smooth with minimum GCV value

lambda = 1e7;  %  minimum GCV estimate, corresponding to 8.5 df
fdParobj = fdPar(daybasis365, harmaccelLfd, lambda);

[dayprecfd, df, gcv, coef, SSE] = ...
            smooth_basis(daytime, precav, fdParobj);

disp(['Degrees of freedom = ',num2str(df)])
disp(['Generalized cross-validation = ',num2str(sum(gcv))])

%  estimate standard error of fit

stderr = sqrt(sum(SSE)/(35*(365-df)));  %  0.94 mm

disp(['standard error of fit = ',num2str(stderr)])

%  plot data and fit

subplot(1,1,1)
plotfit_fd(precav, daytime, dayprecfd, place)

%  Assessment: the temperature curves are still pretty rough,
%  although the data themselves show that there are very
%  high frequency effects in the mean temperature, especially
%  early in the year. 
%  The precip. curves may be oversmoothed for some weather
%  stations. 

%  smooth precipitation in Prince Rupert

PRprecfd = smooth_basis(daytime, precav(:,18), fdParobj);

PRprecvec = eval_fd(daytime, PRprecfd);

subplot(1,1,1)

plot(daytime, precav(:,18), '.', ...
     daytime, PRprecvec,    '-')
ylabel('\fontsize{19} Precipitation (mm)')
axis([0,365,0,18])

%  -----------------------------------------------------------------
%                     PCA of temperature  
%  -----------------------------------------------------------------

lambda = 1e4;
fdParobj = fdPar(daytempfd, harmaccelLfd, lambda);

%  principal components analysis of temperature

nharm  = 4;
daytemppcastr = pca_fd(daytempfd, nharm, fdParobj);
daytemppcastr_new = pca_fd_new(daytempfd, nharm, fdParobj);

figure(1)
subplot(1,1,1)
plot_pca_fd(daytemppcastr, 1)

%  Varimax rotation

daytemprotpcastr = varmx_pca(daytemppcastr);

%  plot rotated harmonics

figure(1)
subplot(1,1,1)
plot_pca_fd(daytemprotpcastr, 1)

%  plot log eigenvalues

daytempharmeigval = daytemppcastr.values;
x = ones(16,2);
x(:,2) = reshape((5:20),[16,1]);
y = log10(daytempharmeigval(5:20));
c = x\y;
subplot(1,1,1)
plot(1:20,log10(daytempharmeigval(1:20)),'-o', ...
     1:20, c(1)+ c(2).*(1:20), ':')
xlabel('Eigenvalue Number')
ylabel('Log10 Eigenvalue')

%  plot factor scores

harmscr = daytemprotpcastr.harmscr;

plot(harmscr(:,1), harmscr(:,2), 'o')
xlabel('Harmonic I')
ylabel('Harmonic II')
text(harmscr(:,1)+5, harmscr(:,2), place)

%  ------------------------------------------------------------------
%               Functional linear models 
%  ------------------------------------------------------------------

%  ---------------------------------------------------------------
%             Predicting temperature from climate region 
%  ---------------------------------------------------------------

%  set up a smaller basis using only 65 Fourier basis functions
%  to save some computation time

smallnbasis = 65;
smallbasis  = create_fourier_basis(dayrange, smallnbasis);
tempfd      = smooth_basis(daytime, tempav, smallbasis);

%  names for climate regions

region_names = [ ...
'Canada  '; 'Atlantic'; 'Pacific '; 'Contintl'; 'Arctic  '];

%  indices for weather stations in each of four climate regions

atlindex = [1,2,4,8,9,13,14,15,19,22,23,24,25,28,34];
pacindex = [12,17,18,30,31];
conindex = [3,5,6,7,16,20,26,27,29,32,33,35];
artindex = [10,11,21];

%  Set up a design matrix having a column for the grand mean, and
%    a column for each climate region effect. Add a dummy contraint
%    observation

zmat = zeros(35,5);
zmat(:       ,1) = 1;
zmat(atlindex,2) = 1;
zmat(pacindex,3) = 1;
zmat(conindex,4) = 1;
zmat(artindex,5) = 1;

%  attach a row of 0, 1, 1, 1, 1 to force region
%  effects to sum to zero, and define first regression
%  function as grand mean for all stations

z36    = ones(1,5);
z36(1) = 0;
zmat   = [zmat; z36];

%  revise YFDOBJ by adding a zero function

coef   = getcoef(tempfd);  
coef36 = [coef,zeros(smallnbasis,1)];  
tempfd = putcoef(tempfd, coef36);  

p = 5;
xfdcell = cell(1,p);
for j=1:p
    xfdcell{j} = zmat(:,j);
end

%  set up the basis for the regression functions

nbetabasis = 13;
betabasis  = create_fourier_basis(dayrange, nbetabasis);

%  set up the functional parameter object for the regression fns.

betafd    = fd(zeros(nbetabasis,p), betabasis);
estimate  = 1;
lambda    = 0;
betafdPar = fdPar(betafd, harmaccelLfd, lambda, estimate);
betacell = cell(1,p);
for j=1:p
    betacell{j} = betafdPar;
end

%  compute regression coefficient functions and 
%  predicted functions

fRegressStruct = fRegress(tempfd, xfdcell, betacell);

betaestcell = fRegressStruct.betahat;
yhatfdobj   = fRegressStruct.yhat;

%  plot regression functions

for j=1:p
    subplot(2,3,j)
    plot(getfd(betaestcell{j}))
    title(['\fontsize{16} ',region_names(j,:)])
end

%  plot predicted functions

subplot(2,3,6)
plot(yhatfdobj)
title('Predicted values')

%  compute mapping from data y to coefficients in c

smallbasismat = eval_basis(daytime, smallbasis);
y2cMap = (smallbasismat'*smallbasismat)\smallbasismat';

%  compute residual matrix and get covariance of residuals

yhatmat  = eval_fd(daytime, yhatfdobj);
ymat     = eval_fd(daytime, tempfd);
tempresmat = ymat(:,1:35) - yhatmat(:,1:35);
SigmaE   = cov(tempresmat');

%  plot covariance surface for errors

subplot(1,1,1)
contour(SigmaE)
hold on
plot(dayrange,dayrange,'--')
hold off
colorbar

%  plot standard deviation of errors

stddevE = sqrt(diag(SigmaE));
plot(daytime, stddevE, '-')
xlabel('\fontsize{19} Day')
ylabel('\fontsize{19} Deg C')

%  Repeat regression, this time outputting results for
%  confidence intervals

stderrStruct = fRegress_stderr(fRegressStruct, y2cMap, SigmaE);

betastderrcell = stderrStruct.betastderr;

%  plot regression functions

subplot(1,1,1)
for j=1:p
    plot(daytime, eval_fd(daytime, betastderrcell{j}))
    title(['\fontsize{16} ',region_names(j,:)])
    pause
end

%  plot regression functions with confidence limits

subplot(1,1,1)
for j=1:p
    plotbeta(betaestcell{j}, betastderrcell{j}, weeks)
    xlabel('\fontsize{19} Day')
    ylabel('\fontsize{19} deg C')
    title(['\fontsize{16} ',region_names(j,:)])
    axis([0,365,-25,20])
    pause
end
     
%  set up a functional data object for the temperature residuals

lambda     = 1e5;
fdParobj   = fdPar(smallbasis, harmaccelLfd, lambda);

tempresfdobj = smooth_basis(daytime, tempresmat, fdParobj);

%  plot temperature residuals

plot(tempresfdobj)

%  -----------------------------------------------------------------------
%    predict log precipitation from climate region and temperature
%  -----------------------------------------------------------------------

%  Now repeat all this for log precipitation.  

smallnbasis = 65;
smallbasis  = create_fourier_basis(dayrange, smallnbasis);
precfd      = smooth_basis(daytime, precav, smallbasis);

%  set up functional data object for log precipitation

logprecmat = log10(eval_fd(daytime,precfd));

lnprecfd = smooth_basis(daytime, logprecmat, smallbasis);

lnprecfd_fdnames{1} = 'Months';
lnprecfd_fdnames{2} = 'Station';
lnprecfd_fdnames{3} = 'log_{10} mm';
lnprecfd = putnames(lnprecfd, lnprecfd_fdnames);

%  plot log precipitation functions

plot(lnprecfd);
title('Log Precipitation Functions')

%  Be sure to run previous analysis predicting temperature from
%  climate region before running this example.

%  revise LOGPREDFD by adding a zero function

coef   = getcoef(lnprecfd);  
nbasis = getnbasis(smallbasis);
coef36 = [coef,zeros(nbasis,1)];  
lnprecfd = putcoef(lnprecfd, coef36);  

%  extend temperature residual functions to include
%  zero function

coef   = getcoef(tempresfdobj); 
nbasis = size(coef,1);
coef36 = [coef,zeros(nbasis,1)];  
tempresfdobj = putcoef(tempresfdobj, coef36);  

%  add TEMPRFDOBJ to the set of predictors

p = 5;
xfdcell = cell(1,p+1);
for j=1:p
    xfdcell{j} = zmat(:,j);
end
xfdcell{6}  = tempresfdobj;

%  set up the basis for the regression functions

nbetabasis = 13;
betabasis  = create_fourier_basis(dayrange, nbetabasis);

%  set up the functional parameter object for the regression fns.

betafd    = fd(zeros(nbetabasis,p), betabasis);
estimate  = 1;
lambda    = 0;
betafdPar = fdPar(betafd, harmaccelLfd, lambda, estimate);
betacell = cell(1,p+1);
for j=1:p
    betacell{j} = betafdPar;
end
betacell{6} = betafdPar;

%  compute regression coefficient functions and 
%  predicted functions

fRegressStruct = fRegress(lnprecfd, xfdcell, betacell);

betaestcell = fRegressStruct.betahat; 
yhatfdobj   = fRegressStruct.yhat;

%  plot regression functions

prednames = [region_names; 'tempres '];
for j=1:p+1
    plot(getfd(betaestcell{j}))
    title(['\fontsize{16} ',prednames(j,:)])
    pause
end  

%  plot predicted functions

plot(yhatfdobj)

%  compute residual matrix and get covariance of residuals

yhatmat    = eval_fd(daytime, yhatfdobj);
ymat       = eval_fd(daytime, lnprecfd);
lnprecrmat = ymat(:,1:35) - yhatmat(:,1:35);
SigmaE  = cov(lnprecrmat');

contour(SigmaE)
colorbar

%  get confidence intervals

stderrStruct = fRegress_stderr(fRegressStruct, y2cMap, SigmaE);

betastderrcell = stderrStruct.betastderr;

%  plot regression functions

for j=1:p+1
    plotbeta(betaestcell{j}, betastderrcell{j}, weeks)
    xlabel('\fontsize{19} Day')
    ylabel('\fontsize{19} log_{10} mm')
    title(['\fontsize{16} ',prednames(j,:)])
    pause
end

%  ---------------------------------------------------------------
%      log annual precipitation predicted by temperature profile
%  ---------------------------------------------------------------

%  set up log10 total precipitation 

annualprec = log10(sum(precav))';

%  set up a smaller basis using only 65 Fourier basis functions
%  to save some computation time

smallnbasis = 65;
smallbasis  = create_fourier_basis(dayrange, smallnbasis);
tempfd      = smooth_basis(daytime, tempav, smallbasis);

smallbasismat = eval_basis(daytime, smallbasis);
y2cMap = (smallbasismat'*smallbasismat)\smallbasismat';

%  set up the covariates, the first the constant, and the second
%  temperature

p = 2;
constantfd = fd(ones(1,35), create_constant_basis(dayrange));
xfdcell = cell(1,p);
xfdcell{1} = constantfd;
xfdcell{2} = tempfd;

%  set up the functional parameter object for the regression fns.
%  the smoothing parameter for the temperature function
%  is obviously too small here, and will be revised below by
%  using cross-validation.

betacell = cell(1,p);
%  set up the first regression function as a constant
betabasis1 = create_constant_basis(dayrange);
betafd1    = fd(0, betabasis1);
betafdPar1 = fdPar(betafd1);
betacell{1} = betafdPar1;
%  set up the second with same basis as for temperature
%  35 basis functions would permit a perfect fit to the data
nbetabasis  = 35;
betabasis2  = create_fourier_basis(dayrange, nbetabasis);
betafd2     = fd(zeros(nbetabasis,1), betabasis2);
lambda      = 10;
betafdPar2  = fdPar(betafd2, harmaccelLfd, lambda);
betacell{2} = betafdPar2;

%  carry out the regression analysis

fRegressStruct = fRegress(annualprec, xfdcell, betacell);

betaestcell   = fRegressStruct.betahat; 
annualprechat = fRegressStruct.yhat;

%  constant term

intercept = getcoef(getfd(betaestcell{1}));

disp(['Constant term = ',num2str(intercept)])

%  plot the coefficient function for temperature
               
plot(getfd(betaestcell{2}))
title('\fontsize{16} Regression coefficient for temperature')

%  plot the fit

plot(annualprechat, annualprec,    'o', ...
     annualprechat, annualprechat, '--')

%  compute cross-validated SSE's for a range of smoothing parameters

loglam = (5:0.5:15)';
nlam   = length(loglam);
SSE_CV = zeros(nlam,1);
for ilam = 1:nlam;
    lambda       = 10^loglam(ilam);
    betacelli    = betacell;
    betacelli{2} = putlambda(betacell{2}, lambda);
    SSE_CV(ilam) = fRegress_CV(annualprec, xfdcell, betacelli);
    fprintf('%3.f %6.2f %10.4f\n', ilam, loglam(ilam), SSE_CV(ilam));
end

plot(loglam, SSE_CV, 'bo-')
xlabel('\fontsize{19} log_{10} smoothing parameter \lambda')
ylabel('\fontsize{19} Cross-validation score')

%  analysis with minimum CV smoothing

lambda      = 10^12.5;
betafdPar2  = fdPar(betafd2, harmaccelLfd, lambda);
betacell{2} = betafdPar2;

%  carry out the regression analysis

fRegressStruct  = fRegress(annualprec, xfdcell, betacell);
betaestcell   = fRegressStruct.betahat; 
annualprechat = fRegressStruct.yhat;

%  constant term

intercept = getcoef(getfd(betaestcell{1}));

disp(['Constant term = ',num2str(intercept)])

%  plot the coefficient function for temperature
               
plot(getfd(betaestcell{2}))
title('\fontsize{16} Regression coefficient for temperature')

%  plot the fit

plot(annualprechat, annualprec, 'o', ...
     annualprechat, annualprechat, '--')
xlabel('\fontsize{16} Predicted log precipitation')
ylabel('\fontsize{16} Observed log precipitation')

%  compute squared multiple correlation

covmat = cov([annualprec, annualprechat]);
Rsqrd = covmat(1,2)^2/(covmat(1,1)*covmat(2,2));

disp(['R-squared = ',num2str(Rsqrd)])

%  compute sigmae

resid = annualprec - annualprechat;
SigmaE = mean(resid.^2);

%  recompute the analysis to get confidence limits

%  get confidence intervals

stderrStruct = fRegress_stderr(fRegressStruct, y2cMap, SigmaE);

betastderrcell = stderrStruct.betastderr;

%  constant  coefficient standard error:

intercept = getcoef(betastderrcell{1});

%  plot the temperature coefficient function
               
plotbeta(betaestcell{2}, betastderrcell{2})
title('\fontsize{16} Regression coefficient for temperature')

%  ---------------------------------------------------------------
%         predict log precipitation from temperature
%  ---------------------------------------------------------------

%  change 0's to 0.05 mm in precipitation data

prectmp = precav;
for j=1:35
    index = find(prectmp(:,j)==0);
    prectmp(index,j) = 0.05;
end

%  set up functional data object for log precipitation

logprecmat = log10(eval_fd(daytime,dayprecfd));

lnprecfd = smooth_basis(daytime, logprecmat, smallbasis);
lnprecfd_fdnames{1} = 'Months';
lnprecfd_fdnames{2} = 'Station';
lnprecfd_fdnames{3} = 'log_{10} mm';
lnprecfd = putnames(lnprecfd, lnprecfd_fdnames);

%  plot precipitation functions

plot(lnprecfd);
title('Log Precipitation Functions')

%  set up smoothing levels for s (xLfd) and for t (yLfd)

xLfd = harmaccelLfd;
yLfd = harmaccelLfd;
xlambda = 1e9;
ylambda = 1e7;

%  compute the linear model

wtvec = ones(35,1);
linmodstr = linmod(daytempfd, lnprecfd, wtvec, ...
                   xLfd, yLfd, xlambda, ylambda);

afd = linmodstr.alpha;   %  The intercept function
bfd = linmodstr.reg;     %  The bivariate regression function

%  plot the intercept function

plot(afd);

%  plot the regression function as a surface

bfdmat = eval_bifd(bfd, weeks, weeks);

subplot(1,1,1)
contour(weeks, weeks, bfdmat)
xlabel('\fontsize{12} Day(t)')
ylabel('\fontsize{12} Day(s)')

%  Get fitted functions

lnprechatfd = linmodstr.yhat;

% Compute mean function as a benchmark for comparison

lnprecmeanfd = mean(lnprecfd);
lnprechat0 = eval_fd(weeks, lnprecmeanfd);

%  Plot actual observed, fitted, and mean log precipitation for
%      each weather station, 

for i=1:35
    lnpreci    = eval_fd(lnprecfd(i),    weeks);
    lnprechati = eval_fd(lnprechatfd(i), weeks);
    SSE = sum((lnpreci-lnprechati).^2);
    SSY = sum((lnpreci-lnprechat0).^2);
    RSQ = (SSY-SSE)/SSY;
    plot(weeks, lnpreci, 'o', weeks, lnprechati, '-')
    xlabel('\fontsize{12} Day')
    ylabel('\fontsize{12} Log Precipitation')
    title(['\fontsize{16}', place(i,:),'  R^2 = ',num2str(RSQ)])
    pause
end

%  -------------------------------------------------------------------
%              Smooth Vancouver's precipitation with a 
%                       positive function.
%  -------------------------------------------------------------------

%  select Vancouver's precipitation

VanPrec  = precav(:,30);

%  smooth the data using 65 basis functions

lambda    = 1e4;
fdParobj  = fdPar(smallbasis, harmaccelLfd, lambda);
VanPrecfd = smooth_basis(daytime, VanPrec, fdParobj);
                      
%  Plot temperature curves and values

plotfit_fd(VanPrec, daytime, VanPrecfd)

%  set up the functional parameter object for positive smoothing

dayfdPar = fdPar(smallbasis, harmaccelLfd, lambda);

%  smooth the data with a positive function

Wfd1 = smooth_pos(daytime, VanPrec, dayfdPar);

%  plot both the original smooth and positive smooth

VanPrecvec    = eval_fd(daytime, VanPrecfd);
VanPrecposvec = eval_pos(daytime, Wfd1);

plot(daytime, VanPrec, '.', daytime, VanPrecposvec, 'b-', ...
     daytime, VanPrecvec, 'r--')
legend('Observed', 'Positive smooth', 'Unrestricted smooth')
 
%  plot the residuals

VanPrecres = VanPrec - VanPrecposvec;
plot(daytime, VanPrecres.^2, '.', dayrange, [0,0], ':')
title('Residuals from positive fit')

%  compute a postive smooth of the squared residuals

lambda = 1e3;
dayfdPar = fdPar(smallbasis, harmaccelLfd, lambda);
Wfd = smooth_pos(daytime, VanPrecres.^2, dayfdPar);

%  plot the square root of this smooth along with the residuals

VanPrecvarhat = eval_pos(daytime, Wfd);
VanPrecstdhat = sqrt(VanPrecvarhat);
plot(daytime, VanPrecres.^2, '.', daytime, VanPrecvarhat, 'b-', ...
     dayrange, [0,0], ':')

%  set up a weight function for revised smoothing

wtvec = 1./VanPrecvarhat;
 
lambda   = 1e3;
dayfdPar = fdPar(smallbasis, harmaccelLfd, lambda);
Wfd2 = smooth_pos(daytime, VanPrec, dayfdPar, wtvec);

%  plot the two smooths, one with weighting, one without

VanPrecposvec2 = eval_pos(daytime, Wfd2);

plot(daytime, VanPrec, '.', daytime, VanPrecposvec2, 'b-', ...
     daytime, VanPrecposvec, 'r--')
legend('Observed', 'Weighted', 'Unweighted')

%  ------------------------------------------------------------------
%                PCA of log precipitation
%  -----------------------------------------------------------------

%  change 0's to 0.05 mm for precipitation

prectmp = precav;
for j=1:35
    index = find(prectmp(:,j)==0);
    prectmp(index,j) = 0.05;
end

%  work with log base 10 precipitation

logprec = log10(prectmp);

%  set up a fourier basis with 13 basis functions

logprecbasis = create_fourier_basis([0,365], 13);

%  smooth the data with unpenalized regression splines

logprecfd = smooth_basis(daytime, logprec, logprecbasis);

%  PCA with four principal components

nharm = 4;
logprecpca = pca_fd(logprecfd, nharm);

%  proportion of variance accounted for

disp('Proportions of variance accounted for:')
disp(logprecpca.varprop)
disp(['Total proportion of variance = ', ...
      num2str(sum(logprecpca.varprop))])

%  plot the unrotated principal components

plot_pca(logprecpca)

%  rotate the principal components

logprecpca = varmx_pca(logprecpca);

%  plot the rotated principal components

plot_pca(logprecpca)
plot_pca(logprecpca, 365, 0, 0)

%  plot log eigenvalues

x = ones(9,2);
x(:,2) = reshape((5:13),[9,1]);
y = log10(logprecpca.values(5:13));
c = x\y;
subplot(1,1,1)
phdl = plot(1:9,log10(logprecpca.values(1:9)),'o-', ...
            1:9, c(1)+ c(2).*(1:9), ':');
set(phdl, 'LineWidth', 2)
xlabel('\fontsize{13} Eigenvalue Number')
ylabel('\fontsize{13} Log_{10} Eigenvalue')
axis([0.9,9.1,-1.5,2])

%  ------------------------------------------------------------------
%  smoothing log precipitation with estimation of residual density
%  -----------------------------------------------------------------

%  change 0's to 0.05 mm for precipitation

prectmp = precav;
for j=1:35
    index = find(prectmp(:,j)==0);
    prectmp(index,j) = 0.05;
end

%  work with log base 10 precipitation

logprec = log10(prectmp);

%  set up the harmonic acceleration operator

Lbasis  = create_constant_basis([0,365]);  %  create a constant basis
Lcoef   = [0,(2*pi/365)^2,0];    %  set up three coefficients
wfd     = fd(Lcoef,Lbasis);      % define an FD object for weight functions
wfdcell = fd2cell(wfd);          % convert the FD object to a cell object
harmaccelLfd = Lfd(3, wfdcell);  %  define the operator object

%  set up logprecfd 

ynbasis  = 11;
logprecbasis = create_fourier_basis([0,365], ynbasis);

%  smooth the data with this basis

logprecfd = smooth_basis(daytime, logprec, logprecbasis);

%  set up design matrix  

zmat   = eval_basis(daytime, logprecbasis);

%  set up the range

rng    = [-4.5,3];
nbasis = 13;
norder =  6;
wbasis = create_bspline_basis(rng, nbasis, norder);

%  estimate the coefficients assuming normality

args  = linspace(rng(1),rng(2),101)';
coef0 = getcoef(smooth_basis(args, -(args.^2)./2, wbasis));
Wfd0  = fd(coef0, wbasis);

%  iteration control parameters for LMdens_fd

conv    = 1e-2;
iterlim = 10;
active  = 2:nbasis;
dbglev  = 1;

lambda  = 1e-4;
Wfd0Par = fdPar(Wfd0, 3, lambda);

coefsave = zeros(nbasis,  35);
betasave = zeros(ynbasis, 35);

stations = 1:35;

% stations = [5,30];

for istn = stations    
    disp([num2str(istn), '  ',place(istn,:)])    
    stnfd = logprecfd(istn);    
    %  compute the residual vector   
    stnprec = logprec(:,istn);
    stnfit  = eval_fd(daytime, stnfd);
    stnres  = stnprec - stnfit;
    sigma0  = sqrt(cov(stnres));
    %  standarize the residuals
    stnstdres = stnres./sigma0;
    %  set up initial regression coefficients     
    beta0  = getcoef(stnfd);    
    [Wfd, beta] = LMdens_fd(stnprec, Wfd0Par, zmat, beta0, sigma0, ...
                            conv, iterlim, dbglev);
    betasave(:,istn) = beta;
    coefsave(:,istn) = getcoef(Wfd);   
    figure(1)
    subplot(2,1,1)
    plot(Wfd)
    xlabel('')
    ylabel('W(t)')
    title(['\fontsize{16} ', place(istn,:)])
    subplot(2,1,2)
    Wvec = eval_fd(args, Wfd);
    dens = exp(Wvec);
    plot(args, dens);
    xlabel('')
    ylabel('p(t)')    
    stnfit2 = zmat*beta;
    figure(2)
    subplot(1,1,1)
    plot(daytime, stnprec, '.', daytime, stnfit2, '-', ...
         daytime, stnfit, '--')
    title(['\fontsize{16} ', place(istn,:)])    
    stnres2 = stnprec - stnfit2;  
    figure(3)
    subplot(2,1,1)
    plot(daytime, stnres./sigma0, '.')
    title(['\fontsize{16} ', place(istn,:)])
    subplot(2,1,2)
    plot(daytime, stnres2./sigma0, '.')    
    pause    
end

%  functional ANOVA of Wfd's

stations = 1:35;

for istn = stations    
    disp([num2str(istn), '  ',place(istn,:)])    
    stnfd = logprecfd(istn);    
    %  compute the residual vector    
    stnprec = logprec(:,istn);
    stnfit  = eval_fd(daytime, stnfd);
    stnres  = stnprec - stnfit;
    sigma0  = sqrt(cov(stnres));    
    %  standarize the residuals    
    stnstdres = stnres./sigma0;    
    %  set up initial regression coefficients 
    beta0  = getcoef(stnfd);    
    [Wfd, beta] = LMdens_fd(stnprec, Wfd0Par, zmat, beta0, sigma0, ...
        conv, iterlim, dbglev);    
    betasave(:,istn) = beta;
    coefsave(:,istn) = getcoef(Wfd);    
end

%  set up design matrix

zmat2 = zeros(35,5);
zmat2(:       ,1) = 1;
zmat2(atlindex,2) = 1;
zmat2(pacindex,3) = 1;
zmat2(conindex,4) = 1;
zmat2(artindex,5) = 1;

%  attach a row of 0, 1, 1, 1, 1

z36    = ones(1,5);
z36(1) = 0;
zmat2   = [zmat2; z36];

%  revise YFDOBJ by adding a zero function

coef36   = [coefsave,zeros(nbasis,1)];  
W36fd = putcoef(Wfd, coef36);  

p = 5;
clear xfdcell
for j=1:p
    xfdcell{j} = zmat2(:,j);
end

%  set up the functional parameter object for the regression fns.

betabasis  = wbasis;
betafd    = fd(zeros(nbasis,p), betabasis);
estimate  = 1;
lambda    = 0;
betafdPar = fdPar(betafd, harmaccelLfd, lambda);
betacell = cell(1,p);
for j=1:p
    betacell{j} = betafdPar;
end

%  set up FDPAR object for response

W36fdPar = fdPar(W36fd);

%  carry out the functional ANOVA

fRegressStruct = fRegress(W36fd, xfdcell, betacell);
betaestcell = fRegressStruct.betahat;
W36hatfd    = fRegressStruct.yhat;

%  a quick plot of the regression functions

subplot(1,1,1)
plotbeta(betaestcell)

plot(W36hatfd)

W36hatmat = eval_fd(args, W36hatfd);

plot(args, exp(W36hatmat), '-')

 