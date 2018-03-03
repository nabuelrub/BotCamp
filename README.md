# BotCamp

To run the program you will need four different Twitter Api keys 
Add them to the following files:
1. code/collector.py
2. code/user_listener.py
3. trends/collector.py
4. trends/get_trends.py


# REQUIREMENTS:

There are several dependencies:
* [Numpy](http://www.numpy.org/)
* [NLTK](https://spacy.io/)
* [Words Corpora](http://www.nltk.org/nltk_data/)
* [Pybloom](https://pypi.python.org/pypi/pybloom)
* [IGraph](https://pypi.python.org/pypi/python-igraph)
* [Scikit-learn](https://pypi.python.org/pypi/scikit-learn)

# Before running the code you need to:

1. Add keywords related to the topic you want find campaigns with bot activities (keywords.txt)
2. Place Twitter API keys in the four files
3. Run BotsFinder\(Debot\).sh to start detecting bots using [Debot](http://www.cs.unm.edu/~chavoshi/debot/) tool.
4. simultaneously, run keywords_generator.sh to add new keywords from the 50 trending hashtags (Optional).
5. After collecting data, run Campaign_Detector.sh to find campaigns, reported campaigns and bots are found in (Campaigns/CampaignDetection/ParsedData/campaigns.csv).


