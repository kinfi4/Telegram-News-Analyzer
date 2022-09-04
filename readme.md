# Propaganda Analyzer

This project was created by me in May 2022, three months have passed since Russia attacked Ukraine and started the most brutal, most terrible war since 1939.

This is the first war in the world that is taking place not only on earth, but also in the minds of millions and even billions of people.
The information war is very important, so I decided to create a special system that will analyze news from both Ukrainian and Russian sources (Telegram channels).

----------------------------------------

The system has two main purposes: classify news into four categories and give the sentiment coloring of the news

Four categorical classes are:   
        
* Shelling - everything that is connected with fighting and shelling.
* Economic - news about sanctions, economic situation and so on.
* Humanitarian - everything that is connected with a life of an ordinary people
* Political - sayings, comments and estimations of politicians

For classification, I created 6 models: **Decision Tree, Support Vector Classifier, Gaussian Naive Bayes, LSTM Neuron Network, 1D CNN Neuron Network, KNN.

-----------------------

<b><h4 style="color:#fcc">All the data needed for training I gathered by myself and can be found <a href="https://github.com/kinfi4/Telegram-News-Analyzer/blob/master/src/data/training-data/news-for-training.csv">here</a></h4></b>

-------------------------------------
## You can find the whole research report here:  
### https://datastudio.google.com/reporting/c76dd534-e89d-4153-a2d9-82d6e5776b6a
-------------------------------------

Ok, now let's take a look at what do we have:

<img src="https://github.com/kinfi4/Telegram-News-Analyzer/blob/master/screenshots/Screenshot%20from%202022-05-29%2018-57-34.png?raw=true" alt=""/> <br>  

-------------------

Let's take a look at how did the news changed during the time. As we can see, there was a explosion at 24th February 2022.

--------------------------

<img src="https://github.com/kinfi4/Telegram-News-Analyzer/blob/master/screenshots/Screenshot%20from%202022-05-29%2018-59-59.png?raw=true" alt=""/>

---------------------------------------

It is also interesting to take a look at `Shelling` category before 24th. As we can see russian propagandistic channels
posted and news in category `Shelling` before 24th. That is because russian propaganda was trying to create a pretext for
intervention by saying that Ukraine is shelling and trying to occupy Donbass region.

---------------------------------------

<img src="https://github.com/kinfi4/Telegram-News-Analyzer/blob/master/screenshots/Screenshot%20from%202022-05-29%2019-00-50.png?raw=true" alt=""/>

---------------------------------------

Now let's take a look at sentiment coloring of the News during this war. It's quite unexpected that there are so many 
"Positive" news there. But, as we go deeper we can explain it.  

First things first, as we already saw, most of the news are in the category `Political`. Almost all politicians
from both sides of conflict is trying to say positive things, in order to support their people.  

Second things second, it's clear, that russian propagandistic channels have much more positive coloring than
ukrainian ones. You can see it on the right up diagram. That happens because russians invented their own language
called "Nonayaz". The was no "Explosion" but a "Cotton", the ship didn't sink, but dived underwater and so on and so forth.

---------------------------------------

<img src="https://github.com/kinfi4/Telegram-News-Analyzer/blob/master/screenshots/Screenshot%20from%202022-05-29%2019-02-53.png?raw=true" alt=""/>

--------------------------------------

Finally, here we can see the visualization of news in category `Shelling`. Here we can see the explosion in popularity
of this category after 24th of February. We also can see (on the left hand), what are the most popular words appear in 
posts of this category.

-------------------------------------

<img src="https://github.com/kinfi4/Telegram-News-Analyzer/blob/master/screenshots/Screenshot%20from%202022-05-29%2019-09-44.png?raw=true" alt=""/>


-------------------------------------
@kinfi4

