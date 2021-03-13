% Log situational parameters; temperature, date, timestamp

clear Data
Data=Experiment_Data;

fprintf('\n')
Data.information.temperature = input('What is the temperature?: ');
Data.information.experiment_number = input('Which numbered experiment is this?: ');
Data.information.configuration = input('What configuration? [pp pm mp mm nn] ');
c = clock;
Data.information.date = c(1:3);
Data.information.timestamp = fix(c(4:6));
fprintf('\n')
disp(Data.information);

filename = ['Experiment_#', num2str(Data.information.experiment_number),'_', num2str(Data.information.date(1)),'-',num2str(Data.information.date(2)),'-',num2str(Data.information.date(3)),'.mat'];
if isfile(filename)
    fprintf('Caution: File already exists. \nAre you sure you want to override \nthis file?  1=YES  any=NO  \n')
    if input('Answer: ')==1
        save(filename, 'Data')
        fprintf(['Struct saved to the MAT-file called: \n"', num2str(filename),'"\n\n'])
    else
        fprintf('No action was done.\n\n')
    end
else
    save(filename, 'Data')
    fprintf(['Struct saved to the MAT-file called: \n"', num2str(filename),'"\n\n'])
end
clear c filename


