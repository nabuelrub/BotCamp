#!/bin/bash

MYPWD=${PWD}

cd $MYPWD/CampaignDetection

#Parse bot tweets
python "parse_1.py" $MYPWD
python "parse_2.py" $MYPWD
python "text_dynamics.py" $MYPWD
python "parse_step1.py" $MYPWD
python "parse_step2.py" $MYPWD

#Find graph edges
python "hashtags_edges.py" $MYPWD
python "mentions_edges.py"
python "media_edges.py"
python "retweets_edges.py"

#Create graphs and cluster bots
python "hashtags.py"
python "mention.py"
python "media.py"
python "retweets.py"
python "temporal_clusters.py"

#Find distance between each pair of bots and ensemble
python "Dissimilarity_matrix.py"
cd ParsedData
matlab -nodisplay -nosplash -nodesktop -r "run hierarchical_clustering.m;exit;"
cd ..

#Report campaigns and bot membership
python "campaignsFinder.py"


