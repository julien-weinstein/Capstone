# How To Run
Install virtualenv:

`$ pip install virtualenv`

Open a terminal in the project root directory and run:

`$ virtualenv env`

Then run the command:

`$ .\env\Scripts\activate`

Then install the dependencies:

`$ (env) pip install -r requirements.txt`

Finally start the web server:

`$ (env) python app.py`

This server will start on port 5000 by default. You can change this in app.py by changing the following line to this:

```
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
```

# Project Overview
This project offers users a Flask-leveraged web-based search engine to search for Wikipedia articles relating to the topic of health. The search engine queries our data set, which is an inverted index built from a corpus of ~500 Wikipedia articles. The documents are returned based on relevance to the query using the Okapi BM25 algorithm. Additionally, text summaries of each article are included in the search results as well as pagination for convenient browsing through results.

# Python Scripts
We leveraged several Python scripts to execute multiple different functions necessary for the search engine to run. First, the `focused_crawler.py` sources Wikipedia articles based on a seed URL and keyword. For our seed URL, we used https://en.wikipedia.org/wiki/Health, and the keyword we used was "health." Next, we set the depth parameter to 10 so that the crawler would go 10 levels deep in Wikipedia space by adding links to articles within the articles that contained the word "health," through 10 iterations of crawling.

The other key Python scripts include:


`inv_index.py`: Builds inverted index from corpus generated by the Focused Crawler


`search_engine.py`: Runs query against inverted index, ranks document results based on Okapi BM25 algorithm, and returns URL results.


`text_summarizer.py`: Provides most salient sentences in summary form from each URL present in the corpus.


`app.py`: Employs Flask library to generate search engine webpage, takes in user query and runs it through the Search Engine Python script, and contains important logic for appending the correct text summarizies to each URL result, as well as pagination information for use in the index.html file. Each result page should only contain 10 results, and the user should be able to proceed through pages individually until they reach the termination of the search results.

# HTML and CSS Files
The `index.html` and `base.html` files provide the back-end structure of the search engine webpage. The `index.html` file contains Jinja2 scripting to incorporate logic into the web page's layout dependent on certain conditions. For example, if a user reaches the last page of a certain query's results, they should not be able to click on the next page button since there wouldn't be a next page. Another instance of Jinja2 logic is modifying what is shown on the home page compared to post-search. The user does not need to see an empty section labeled with "No Search Results" on the homepage before they have even executed a query. The `base.html` file contains HTML code for visual aspects like font color and so forth.

# Integration with IDE and Heroku
To make all these scripts work together, we first ran locally the `inv_index.py` and `text_summarizer.py` files to generate pickle files of the inverted index and text summaries of all the documents in the corpus, and saved those to a local directory. Next, those pickle files were accessed by the `app.py` file run Visual Studio Code in the same directory as the pickle files, which also contained the `search_engine.py` file along with the HTML and CSS files. Finally, a Heroku account was setup and the webpage was generated via the Heroku CLI. It is recommended that, to successfully run this project, an IDE comparable to VS Code is used.
