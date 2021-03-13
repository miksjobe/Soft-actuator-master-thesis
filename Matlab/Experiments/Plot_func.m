function [] = Plot_func(data)
if isempty(data.time)
    return
end
% Plots the inputed struct, only works with the setup from Extract.m

% Colors
% #DEDBD3 - Light Grey
% #E8BD58 - Orange
% #4BA3EB - Turqoise
% #964BEB - Violet
subplot(2,1,1);
area(data.time,data.pressure,'FaceColor','#DEDBD3','EdgeColor','#DEDBD3','LineWidth',0.1);
axis([min(data.time) max(data.time) -0.2 1.2])
hold on;
plot(data.time,data.recorded,'Color','#E8BD58','LineWidth',1);
plot(data.time,data.sensor,'Color','#4BA3EB','LineWidth',1);
%plot(data.time,data.simulated,'b');
xlabel('time [Seconds]')
ylabel('Normalized values [%Pa, %Degree]')
legend('pressure (reference)','recorded (camera)','sensor');
hold off;

subplot(2,1,2);
t=rescale(data.time);
%plot(data.recorded,data.sensor,'Color','#4BA3EB','LineWidth',1);
%scatter(data.simulated,data.sensor,10,data.time,'filled');
hold on;
plot3(data.simulated,data.sensor,t);
c = 1:numel(t);
h = surface([data.simulated(:),data.simulated(:)],[data.sensor(:),data.sensor(:)],[t(:),t(:)],[c(:),c(:)],'EdgeColor','flat','FaceColor','none','LineWidth',1.5);
colormap([0.6 0.9 0.85
    0.55 0.87 0.85
    0.5 0.85 0.85
    0.35 0.7 0.78
    0.2 0.6 0.7
    0.25 0.55 0.7
    0.3 0.5 0.7
    0.25 0.4 0.65]);
%plot(data.recorded,data.recorded,'Color','#E8BD58','LineWidth',1.5);
hold on;
plot(data.simulated,data.simulated,'Color','#111111','LineWidth',1.5);

axis([-0.2 1.2 -0.2 1.2])
%legend('Recorded','1:1 line');
%xlabel('Simulated Curvature [%Degree]')
%ylabel('Curvature [%Degree]')
hold off;

end

