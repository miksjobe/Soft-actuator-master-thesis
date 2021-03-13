function T = SplitStruct(Data, Condition, TrimL, TrimU)
% Split the struct into the different input references. Use TrimLower and
% Upper to shift the Condition.
if nargin < 4
    TrimU = 20;
end
if nargin < 3
    TrimL = 20;
    TrimU = 20;
end
trim = find(Condition);
Condition( min(trim) : min(trim)+TrimL)=0;
Condition( max(trim)-TrimU : max(trim)) =0;
clear trim
T.time = Data.time(Condition);

for i = 1:numel(Data.signals)
    T.signals(i).values=Data.signals(i).values(Condition);
    T.signals(i).dimensions = Data.signals(i).dimensions;
    T.signals(i).label = Data.signals(i).label;
    T.signals(i).title = Data.signals(i).title;
    T.signals(i).plotStyle = Data.signals(i).plotStyle;
end

T.blockName = Data.blockName;
T.information = Data.information;
end

