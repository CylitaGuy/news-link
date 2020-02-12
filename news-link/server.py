from flask import Flask, render_template, request

#Editing to upload working packages, etc.
import os
import pandas as pd
import numpy as np
import sys
import json 

#specifying local system path for remaining functions files

#self written functions and scripts that will be needed
import scripts.text_normalization_funs as TN
import scripts.similiarity_funcs as SIM

#Load in corpora for comparison
corpus = pd.read_csv(r'data/Final_Cleaned_Corpus_test.txt')

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
	
	else:
		#Taking the comptext and cleaning it to get ready for TF-IDF
		comptext = some_input
		cleancomp = TN.normalize_Story(story = comptext)

		#Compute similarity scores
		scores = SIM.SimCorpCreate (corpora = corpus['cleaned_text'], 
									directory= '/Users/Cylita/Desktop/insight-ds-project_news-link/news-link/scripts/', 
									querydoc = cleancomp)
		#Give me Top Stories, rounded
		Top_Whole_Stories = round(SIM.StoryMatch(SimScores = scores, originalDF = corpus),2)

		#Renaming the column headings of top stories
		Top_Whole_Stories.rename(columns={'title':'Article Title',
                          'mainurl':'Link',
                          'sim_scores':'Cosine Similarity'}, 
                 			inplace=True)

		if len(cleancomp) >= SIM.percentile_85:
			return render_template("index.html",
                              	tables=[Top_Whole_Stories.to_html(index = False, 
									classes='display', escape = False,
									render_links = True)],
                         		my_input = comptext,
                              	my_form_result="Long")

		if len(cleancomp) < SIM.percentile_85:	
			#Return my rendered template with the output
			return render_template("index.html",
							#my output
							tables=[Top_Whole_Stories.to_html(index = False, 
									classes='display', escape = False,
									render_links = True)],
                         	my_input = comptext,
                         	my_form_result="NotEmpty")

# start the server with the 'run()' method
if __name__ == "__main__":
	app.run(debug=True) #will run locally http://127.0.0.1:5000/
