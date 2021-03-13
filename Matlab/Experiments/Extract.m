function struct_extract = Extract(in)
% Extract the different data and rescale them to their local percentages.

struct_extract.pressure = rescale(in.signals(1).values);
struct_extract.recorded = rescale(in.signals(3).values);
struct_extract.sensor = rescale(in.signals(4).values);
struct_extract.sensor = struct_extract.sensor(:);
struct_extract.simulated = rescale(in.signals(5).values);
struct_extract.time = in.time;
end

