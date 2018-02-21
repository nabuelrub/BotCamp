function calDTW(f_name,round_path,win,week,cexp)
f_name
sig = csvread(f_name);
tic
%win = 20;
dtws = zeros(length(sig(:,1)),length(sig(:,1)));
for i=1:length(sig(:,1))
   if (mod(i,100)==0)
       i
   end
   s = sig(i,:);
   for j=i+1:length(sig(:,1))
       t = sig(j,:);
       a = dtw(s,t,win);
       dtws(i,j) = a(1);
   end
end
str = strcat(round_path,'/w',int2str(week),'_exp',int2str(cexp),'_dtws.mat');
%eval(sprintf('rnd_%d_dtws = dtws;',r));
%m = strcat('rnd_',int2str(r),'_dtws');
save(str,'dtws');
toc
exit
