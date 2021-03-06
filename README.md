# News-Link: Saving Journalists Time for What Matters

Website: http://cguy.pythonanywhere.com/

## The Problem:

Large digital news publishers, like many on-line services, want to increase audience engagement with their content. While there are a variety of strategies that publishers may use to accomplish this, one approach commonly employed is to insert links that direct readers to additional, related news stories on that publisher's website. While these links serve to increase the time readers spend interacting with a publisher's news content, currently these links are often curated manually by journalists. As a result, journalists may spend a significant portion of their day searching for related stories to include in a story they are working on. Where these links are generated automatically, it is often based on content popularity. This can be frustrating for the reader who, as a result, may be provided with links to stories that - although popular in their area - are unrelated to an article they are reading.

## The Solution:

**News-Link** is web application that uses natural language processing to quickly recommend journalists links to stories that are similar in content to the one they are writing. Ultimately, by automating the process of searching for similar news stories, **News-Link** saves journalists time. Importantly, by using NLP it also ensures that recommended articles are similar to a story of interest - reducing frustration on the part of the user when compared to recommendation systems based solely on popularity.

## Setting up News-Link

After cloning this repository, run the following code to set up **News-Link**:

```python
cd news-link
pip install -r requirements.txt
```

Once this has been completed, you can explore the **News-Link** server script and process notebook (*News_Link_Process.ipynb*) to get a sense of how the application works. 

## How Does News-Link Work?

#### 1) The Data

To create **News-Link** I scraped news articles from the CBC.ca landing pages (see *webscrapting_articles.py* in the scripts folder) daily for a week. In addition to scraping the titles, authors, date, and main text of each news story, I also scraped all of the related story links inserted manually by journalists. Given that this application is a tool meant to be used internally by a news organization I chose to focus on the articles from a single digital publisher. This scraping resulted in the creation of a corpus that contains >1500 news articles. While for the purposes of this project the corpus is static, the functions written could be easily combined to produce a pipeline that scrapes the web daily and updates the corpus (see more in **5) Next Steps/Future Directions** below). 

#### 2) Computing Article Similarity

Prior to computing news article similarity, all text is cleaned (*i.e.* converted to lowercase, stop words removed, contractions removed, lemmetization). The **News-Link** app computes TF-IDF vectors for each story and then uses these vectors to compute cosine similarity. Given that TF-IDF is a fairly simple method to represent unstructured text and may not adequately capture semantics, I also explored using GloVe embeddings to compute cosine similarity and using GloVe embeddings to calculate word mover's distance. Ultimately, given that TF-IDF did a reasonable job at returning similar news articles from the corpus (see **4) Approaches to Validating News-Link** below) and that word embeddings are computationally expensive, the app is built using TF-IDF and cosine similarity. To learn more about the other embedding and similarity metrics applied, see the *Data_Viz_Exploration.ipynb*.

#### 3) The Web Application

**User Input**: For **News-Link** to work, a journalist inputs the title and main body of a story they are writing. 

**On the Server**: For a given story entered by a journalist, **News-Link** cleans said story in the same way all corpus stories were cleaned, computes TF-IDF vectors, and then compares the story of interest to all stories in the corpus using cosine similarity. 

**Output**: The **News-Link** web application returns the original text entered to the journalist. If a story entered by a journalist is on the longer side (see *Data_Viz_Exploration.ipynb* for determination), it notifies the journalist that they should consider dispersing links throughout their story (rather than at just the end) as readership tends to drop off for thse longer articles. Finally, **News-Link** returns a table that displays the 10 most similar news articles in the corpus. The table contains article titles, click-able urls, and the cosine similarity score for these articles.

#### 4) Approaches to Validating News-Link

Validating NLP approaches that compute similarity (which is subjective in and of itself) can be challenging. Considering this I decided to approach validation in four ways:

*1) Does **News-Link** do as good of a job as journalists at returning similar articles?*

The links inserted manually by journalists were a reasonable first place to start in trying to understand if the application I built was doing a "good" job at returning similar news stories. To accomplish this, I used the similar links gathered during initial story scraping to scrape the full text of these articles inserted by journalists (see *Cleaning Raw Data.ipynb and webscraping_related_links.py*). For an article of interest I then computed the cosine similarity score for the news article inserted by a journalist and compared that to the cosine similarity score for the top (*i.e.* most similar) article identified by **News-Link**. These were the results:

![image](https://github.com/CylitaGuy/news-link/blob/master/notebooks/figures/png/News_Scatter.jpg)

**Fig 1. Comparison of cosine similarity scores (computed from TF-IDF vectors) for the top similar story identified by News-Link and stories selected by journalists.**

In ~30% of cases, **News-Link** identified articles that had the same similarity score as those inserted manually by journalists. The rest of the time, my application was able to pull out stories that were more similar than those inserted by journalists from the corpus. While this comparison is not perfect (*e.g.* my approach can never do worse than a journalist because the similar articles they inserted are included in the corpus), overall it would suggest that the articles identified by **News-Link** are similar enough to a story of interest to be considered by journalists. 

It is also worth noting that while the application is built using TF-IDF and cosine similarity, I also repeated this validation process using GloVe embeddings and cosine similarity and GloVe embeddings and word mover's distance. The results of these comparisons can be found in *Data_Viz_Exploration.ipynb*. 

*2) Do news readers feel that the articles returned by **News-Link** are similar to the stories they are reading?*

In order to understand how the average reader might feel about the similarity of selected links, I put together a short survey which I administered to the Insight Data Science Toronto Office. As part of this survey, participants were asked to read three short news stories. After reading the stories they were provided with several possible related headlines. Each one of these headlines for "similar" news stories was selected using a different method: journalist heuristic, TF-IDF and cosine similarity, GloVe embeddings and cosine similarity, and GloVe embeddings and word mover's distance. Given that only 20 individuals completed this survey, I did not analyze the results for statistical significance, but present a graphical representation of pooled results below:

![image](https://github.com/CylitaGuy/news-link/blob/master/notebooks/figures/png/Pie_Chart_Survey4.jpg)

**Fig 2. Summarized results of preference survey (n=20) from three test stories.**

While 50% of individuals thought links inserted by journalists were the most similar to the story, it is worth noting that these links were also often returned by **News-Link**. Further, ~20% of people thought TF-IDF selected links were the most similar. Given that it is hard to draw reasonable conclusions from such a small sample, replicating this survey approach with more stories and readers would be benificial. 

*3) Does **News-Link** work for the stakeholder*

Given that **News-Link** is a tool that was created to save journalists time, the next step would be to take this prototype to the stakeholder for them to try. Conducting focused interviews with journalists who have tried **News-Link** would help me to understand if this application accomplishes its automation and improved work flow goals. These interviews would also give me a sense of how it could be improved upon to help it increase efficiency. 

*4) Does **News-Link** increase audience engagement?*

If this were a tool that was eventually scaled for use at a digital publisher it would likely be worthwhile to test if similar links selected using this new approach alter audience engagement. This could be accomplished through simple A/B Testing.  

#### 5) Next Steps / Future Improvements

**News-Link** was built during a short (~3 week) time period as part of the [Insight Data Science Program](https://www.insightdatascience.com/). While the first version of **News-Link** accomplishes its task well, with more time several improvements could be made. Namely:

* A pipeline that continually updates the news corpus
* Incorporating date and article topic into the selection of similar links (*i.e.* returning relevant recent links)
* Creating an additional module that gives journalists options for related links, but in a different topic area to help diversify what readers are seeing
* Incorporating article popularity in the model
