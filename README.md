# About
The required corpus for research in the article: Public Sentiment Diffusion over COVID-19 Related Tweets Posted by Major Public Health Agency in the United States.

# File Description
<p>tweetTongji-final.xlsx: the result and diagram of handling the corpus in the article.</p>
<p>id_network.csv: the interaction record of tweet with id extarcted from tweets posted by HHS, NIH, FDA and CDC in the COVID-19-TweetIds dataset.</p>
<p><pre>for example, the file 1221623107397595137_network.csv store the interaction record of tweed whose id is 1221623107397595137.</pre></p> 
<p>extraction.py:  script for interaction extraction from mongodb collection.</p>
<p>moreinfo.py:  script for extract more information about the interaction tweets from the COVID-19-TweetIds dataset.</p>
<p>allinfowithemotion.py：script for emerge emotion intensity and polarity of tweets.</p>

# Fileds of Interaction record
<p>FromNodeId: the id of father tweet,</p>
<p>ToNodeId: the id of child tweet,</p>
<p>Weight: the type of interaction. 1 represents retweet, 2 represents reply, 3 represents quote,</p>
<p>Level: the level of sentiment diffusion network.</p>


