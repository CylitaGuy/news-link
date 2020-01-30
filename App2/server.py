from flask import Flask, render_template, request

#Editing to upload working packages, etc.
import os
import pandas as pd
import numpy as np
import sys

#specifying local system path for remaining functions files
sys.path.insert(1, '/Users/Cylita/Desktop/insight-ds-project_news-link/scripts')

#self written functions and scripts that will be needed
import text_normalization_funs as TN
import similiarity_funcs as SIM


# Create the application object
app = Flask(__name__)

@app.route('/',methods=["GET","POST"]) #we are now using these methods to get user input
def home_page():
	return render_template('index.html')  # render a template

@app.route('/output')
def recommendation_output():

	# Pull input
	some_input = request.args.get('user_input')       	 
  	 
	# Case if empty
	if some_input =="'":
		return render_template("index.html",
                              	my_input = some_input,
                              	my_form_result="Empty")
	else:
		#Talking the comp text
		comptext = some_input

		#Cleaning the comptext to get it ready fo TF-IDF
		cleancomp = TN.normalize_Story(story = comptext)

		#Load in corpora for comparison
		corpus = pd.read_csv('/Users/Cylita/Desktop/insight-ds-project_news-link/data/processed/demo_corp.csv')

		#Computing similarity scores for given dataframe
		scores = SIM.SimCorpCreate (corpora = corpus['cleaned_text'], directory= '/Users/Cylita/Desktop/insight-ds-project_news-link/scripts/', querydoc = cleancomp)

		#Top Stores
		TopStories = SIM.StoryMatch(SimScores = scores, originalDF = corpus)

		#Only Display the first two
		TopStories2 = TopStories.iloc[0]

		#TopStories Titles
		some_output = TopStories2['title']
		some_number = round(TopStories2['sim_scores'],2)
		some_image="giphy.gif"
		return render_template("index.html",
                          	my_input=some_input,
                          	my_output = some_output,
                          	my_number=some_number,
                          	my_img_name=some_image,
                          	my_form_result="NotEmpty")

# start the server with the 'run()' method
if __name__ == "__main__":
	app.run(debug=True) #will run locally http://127.0.0.1:5000/
