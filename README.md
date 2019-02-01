# Goals of the project
Focussing on the seven biggest UK supermarket brands on Facebook and using natural language processing and supervised classification modelling, can we train a machine to distinguish the different supermarket brands' social content from one another on Facebook?

# Why you created the project 
Facebook pages are a significant brand asset for thousands of companies and organisations worldwide. Companies invest heavily into developing social content to engage with customers and prospects in a two way 'conversation’. The impact of social media on business success is widely debated (often with very differing views) however one thing that most marketers agree on is that brand differentiation is a key aspect of any 'healthy' brand. Brands need to stand out from one another in their category. Not just in terms of what they offer but also in terms of how they communicate - across all media channels, including social media. Which leads to the focus of this project – are brands doing enough to differentiate their social content on Facebook?

Why supermarkets? Well, having worked somewhere that was responsible for one of these brands’ social content, I was curious to see if their work was effective,

# Methodology & Approach

Seven of the UK's leading supermarket brands were chosen for the study: Sainsbury's, Tesco, Lidl, ASDA, Morrisons, M&S and Waitrose. I intend to scrape their social content from Facebook using automated web scraping (Selenium). 
Web scraping can be quite tricky – especially on a site like Facebook which has quite complicated and varying html code. However, there are no other ways of obtaining page content. Using Facebook’s social graph API would have been the ideal, however because of the Cambridge Analytica scandal, developer approval is very hard to get. 
In addition to the raw content scraped online, I’ll integrate this with some secondary data sources to add a few metrics that I can’t scrape

The diagram below summarises the data streams I intend to obtain and how I intend them to work with one another.

Once I’ve scraped, cleaned and integrated all these data streams into a final .csv file, I can then begin to look at analyzing and start building some models.

The project in its current state splits into seven stages and for ease of reading I’ve split this across seven notebooks. For those that want a quick overview of the project I would recommend exploring the '0_Summary & Technical Reporting', for those who want something less technical - I have created a powerpoint slideshow talking through the project in '6_Presentation'

0_Summary & Technical Reporting	

1_Data Acquisition	cleanedup

2_Data Preparation & Cleaning

3_Feature Engineering

4_EDA

5_Modelling

6_Presentation


# How to install the project

Feel free to fork and clone this project. You’ll need a github account and a python environment to run the code, Jupyter notebook might make sense seeing as that’s what I wrote in.

Some key libraries are required in order to run this project in its entirety:

Selenium
Chromedriver / Webdriver
TQDM Notebook (not essential, but helps to see progress)
All the standard Data Science libraries (e.g. SKLearn, Seaborn, Pandas, NumPy...)

# How to run the project
I've set up each stage of the project in its own folder with various sub folder containing all the data you need so you can download individual folders and run them seperately and they should all run smoothly. If you have any problems, let me know through here and I can try and assist you. 

# Observations and improvements


# Link to your Jupyter Notebook






