from flask import Flask, render_template, request

#Editing to upload working packages, etc.
import os
import pandas as pd
import numpy as np
import sys
import json 

#specifying local system path for remaining functions files
sys.path.insert(1, '/Users/Cylita/Desktop/insight-ds-project_news-link/scripts')

#self written functions and scripts that will be needed
import text_normalization_funs as TN
import similiarity_funcs as SIM

#Load in corpora for comparison
corpus = pd.read_csv('/Users/Cylita/Desktop/insight-ds-project_news-link/data/processed/Final_Cleaned_Corpus.csv')

#Computing important story cutoffs


# Create the application object
app = Flask(__name__)

@app.route('/',methods=["GET","POST"]) #we are now using these methods to get user input
def home_page():
	return render_template('index.html')  # render a template

@app.route('/output')
def recommendation_output():

	# Pull input
	some_input = request.args.get('user_input')       	 
  	 
	# If the input is empty
	if some_input =="":
		return render_template("index.html",
                              	my_input = some_input,
                              	my_form_result="Empty")
	
	elif len(some_input) >= SIM.percentile_85:
		
		#Talking the comp text
		comptext = some_input

		#Cleaning the comptext to get it ready fo TF-IDF
		cleancomp = TN.normalize_Story(story = comptext)

		#Obtaining the first 30% of the comp text for longform story separation
		#first30 = TN.Clean30(text = cleancomp)


		############################################
		####Performing 30% Story Similarity
		#Computing similarity scores for given dataframe
		#scores = SIM.SimCorpCreate (corpora = corpus['cleaned_text'], 
			#directory= '/Users/Cylita/Desktop/insight-ds-project_news-link/scripts/', 
			#querydoc = first30)

		#Top Stories
		#Top_30_Stories = SIM.StoryMatch(SimScores = scores, originalDF = corpus)
		
		#Renaming the column headings of top stories
		#Top_30_Stories.rename(columns={'title':'Article Title',
                          #'mainurl':'Link',
                          #'sim_scores':'Cosine Similarity'}, 
                 #inplace=True)
		
		############################################
		####Performing Whole Story Similarity
		
		#Computing similarity scores for given dataframe
		scores = SIM.SimCorpCreate (corpora = corpus['cleaned_text'], 
			directory= '/Users/Cylita/Desktop/insight-ds-project_news-link/scripts/', 
			querydoc = cleancomp)

		#Top Stories
		Top_Whole_Stories = SIM.StoryMatch(SimScores = scores, originalDF = corpus)

		#Renaming the column headings of top stories
		Top_Whole_Stories.rename(columns={'title':'Article Title',
                          'mainurl':'Link',
                          'sim_scores':'Cosine Similarity'}, 
                 inplace=True)


		return render_template("index.html",
                              	tables=[#Top_30_Stories.to_html(index= False, classes='display',
                              		#escape = False, render_links = True),
                              	Top_Whole_Stories.to_html(index = False, 
									classes='display', escape = False,
									render_links = True)],
                              	#Titles = ["For the Beginning of Your Article", "For the End"],
                         		my_input = comptext,
                              	my_form_result="Long")

	else:
		#Talking the comp text
		comptext = some_input

		#Cleaning the comptext to get it ready fo TF-IDF
		cleancomp = TN.normalize_Story(story = comptext)


		#Computing similarity scores for given dataframe
		scores = SIM.SimCorpCreate (corpora = corpus['cleaned_text'], 
			directory= '/Users/Cylita/Desktop/insight-ds-project_news-link/scripts/', 
			querydoc = cleancomp)

		#Top Stores
		TopStories = SIM.StoryMatch(SimScores = scores, originalDF = corpus)

		#Renaming the column headings of top stories
		TopStories.rename(columns={'title':'Article Title',
                          'mainurl':'Link',
                          'sim_scores':'Cosine Similarity'}, 
                 inplace=True)
		
		#Return my rendered template with the output
		return render_template("index.html",
							#my output
							tables=[TopStories.to_html(index = False, 
									classes='display', escape = False,
									render_links = True)],
                         	my_input = comptext,
                         	my_form_result="NotEmpty")

# start the server with the 'run()' method
if __name__ == "__main__":
	app.run(debug=True) #will run locally http://127.0.0.1:5000/
