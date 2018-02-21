function [] = get_cluster(round_path,week,cexp)
Current = [];
Current_name = [];
e = [];
DTWClustering = 1;
tt = load(sprintf('%s/w%d_exp%d_dtws.mat',round_path,week,cexp));
eval(sprintf('e = tt.dtws;'));
e_name = textread(sprintf('%s/w%d_exp%d_name.txt',round_path,week,cexp),'%s\n');



n = size(e);
for i = 1:n
    for j = i+1:n
        if DTWClustering == 0
        e(i,j) = 1 - e(i,j);
        end
        e(j,i) = e(i,j);
    end
    e(i,i) = 0;
end

P = squareform(e);
D = linkage(P,'single');

if DTWClustering == 0
C = cluster(D,'cutoff',0.1);
else
C = cluster(D,'cutoff',0.1);
end


Current = [Current ;C + length(Current)];
Current_name = [Current_name ;e_name];




nnn = length(Current_name);
[junk ind] = sort(Current_name);
old_Current = Current;
i = 1;
while i <= nnn
    for j = i+1:nnn
        if strcmp(Current_name(ind(i)),Current_name(ind(j)))
            j
            Current_name(ind(i))
            Current_name(ind(j))
            ind1 = find(Current==Current(ind(j)));
            Current(ind1) = Current(ind(i));
        else
            i = j;
            break;
        end
    end
    i = j;
end


m = max(Current);
len(1:m) = 0;
for i = 1:m
    len(i) = length(find(Current==i));
end

[slen ii]  = sort(len);

length(unique(Current_name(find(Current == ii(end-1)))))


unique(Current_name(find(Current == ii(end-1))))

file_name = strcat(round_path,'/clstrs_exp',int2str(cexp),'_ge_2.txt')
fileID = fopen(file_name,'w');
length(ii)
for i=1:length(ii)
   %i
    a = unique(Current_name(find(Current == ii(end-(i-1)))));
    if(length(a) >=2)
        for j=1:length(a)-1
        %j
        fprintf(fileID,'%s,',a{j});   
        end
    fprintf(fileID,'%s\n',a{end});   
    end
end

exit