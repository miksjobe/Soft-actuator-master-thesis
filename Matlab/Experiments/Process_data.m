close all

Sine     =   SplitStruct(Data, Data.signals(2).values == 1);
Square   =   SplitStruct(Data, Data.signals(2).values == 2);
Sawtooth =   SplitStruct(Data, Data.signals(2).values == 3);
Step     =   SplitStruct(Data, Data.signals(2).values == 4);
Random   =   SplitStruct(Data, Data.signals(2).values == 5);
Still    =   SplitStruct(Data, Data.signals(2).values == 6);

%----------------------------------------------------------------------%
info = Data.information;           % Experiment information
t = Data.time;                     % Time [Seconds]
p = Data.signals(1).values;        % Pressure [Bar]
inpt = Data.signals(2).values;     % Input reference integer []
curv = Data.signals(3).values;     % Python,OpenCv recored angle [Degree]
sens = Data.signals(4).values;     % Analog Sensor reading [Degree]
sim = Data.signals(5).values;      % Simulated-plant output [Degree]
% Plot all values over whole experiment
%figure('Name','All values')
%plot(t, [p, inpt, curv, sim])
%legend('presure','input','curvature','simulated')

%----------------------------------------------------------------------%
sin = Extract(Sine);
sqre = Extract(Square);
saw = Extract(Sawtooth);
stp = Extract(Step);
randm = Extract(Random);
still = Extract(Still);
%sin.lin_err = mean(abs(sin.recorded-sin.sensor));

%----------------------------------------------------------------------%
if isempty(sin.time)==0
    figure('Name','Sinewave motion');
    Plot_func(sin);
end
if isempty(sqre.time)==0
    figure('Name','Squarewave motion');
    Plot_func(sqre);
end
if isempty(saw.time)==0
    figure('Name','Sawtooth motion');
    Plot_func(saw);
end
if isempty(randm.time)==0
    figure('Name','(Not-so)Random motion');
    Plot_func(randm);
end


%dif=zeros(length(t),1);
%for i=1:1:length(d_ind)
%    for ind=p_ind(i):1:d_ind(i)
%        dif(ind) = abs(curv(ind)-sens(ind))+abs(curv(ind+p_ind(i+1)-d_ind(i))-sens(ind+p_ind(i+1)-d_ind(i)));
%        %dif = [dif; abs(curv(ind)-sens(ind))+abs(curv(ind+p_ind(i+1)-d_ind(i))-sens(ind+p_ind(i+1)-d_ind(i)))];
%    end
%end




