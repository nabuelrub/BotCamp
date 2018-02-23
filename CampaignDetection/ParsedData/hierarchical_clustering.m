
dis = csvread('dissimilarity_matrix.csv');
P = squareform(dis);
dis = dis';
D = linkage(dis,'average');
cutoff = unique(D(:,3))
cutoffR = round(cutoff,15)
C = cluster(D,'criterion','distance','cutoff',cutoff(find(cutoffR>0.8,1)-1));
csvwrite('Clusters.csv',C);

dendrogram(D,0)
