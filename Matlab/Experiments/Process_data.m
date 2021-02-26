
info = Data.information;            % Experiment information
t = Data.time;                      % Time [Seconds]
p = Data.signals(1).values;         % Pressure [Bar]
curv = Data.signals(1).values;      % Python,OpenCv recored angle [Degree]
sens = Data.signals(2).values;      % Analog Sensor reading [Degree]
sim = Data.signals(3).values;       % Simulated-plant output [Degree]

plot_per = [0.0,1.0];                 % Percent of the time to plot

% Scale data to percent
[pks,p_ind] = findpeaks(curv);
[dip,d_ind] = findpeaks(max(curv)-curv);

curv = curv/max(curv);
sens = lowpass(sens,0.1);
sens = sens/max(sens);
%p = polyfit(t,sens,8);
%sens_p = p(1)*t.^8 + p(2)*t.^7 + p(3)*t.^6 + p(4)*t.^5 + p(5)*t.^4 + p(6)*t.^3 + p(7)*t.^2 + p(8)*t + p(9);
sim = sim/max(sim);

% Linearity error [Percent]
lin_err = mean(abs(curv-sens));

% Hysteresis error [Percent]
[pks,p_ind] = findpeaks(curv);
[dip,d_ind] = findpeaks(max(curv)-curv);
%%
dif=zeros(length(t),1);
for i=1:1:length(d_ind)
    for ind=p_ind(i):1:d_ind(i)
        dif(ind) = abs(curv(ind)-sens(ind))+abs(curv(ind+p_ind(i+1)-d_ind(i))-sens(ind+p_ind(i+1)-d_ind(i)));
        %dif = [dif; abs(curv(ind)-sens(ind))+abs(curv(ind+p_ind(i+1)-d_ind(i))-sens(ind+p_ind(i+1)-d_ind(i)))];
    end
end
%% Plots
t1=find(t>(max(t)*plot_per(1)), 1 );
t2=find((max(t)*plot_per(2))>t, 1, 'last' );
plot(t(t1:t2),[curv(t1:t2),sens(t1:t2),dif(t1:t2)])
