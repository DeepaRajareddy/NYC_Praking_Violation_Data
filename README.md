# Analyzing Millions of NYC Parking Violations

## Description:

The NYC Open Data project makes available freely data published by NYC agencies and other partners. These datasets range from a few thousand rows to millions, depending on department and time frame. For the really large datasets, attempting to download is unfeasible as some of these files are upwards of 5-10 Gbs in size. As such, this service offers an Application Programming Interface - known colloquially as an API - for ease of querying and loading the data via web requests in terminal (via curl) or code (via python, javascript, etc). Furthermore, these APIs are made available via the Socrata Open Data API, which provides a well established and easy to use set of conventions for querying public datasets such as the one we will be using. For this project, we will leverage a python client of the Socrata API to connect to the Open Parking and Camera Violations (OPCV) API, load all the data into an ElasticSearch instance, and visualize / analyze with Kibana. To accomplish this, we will leverage our knowledge of containerization, working with the terminal and python scripting. 

## Dataset
The dataset used in the project is the Open Parking and Camera Violations (OPCV) data from NYC Open Data (https://opendata.cityofnewyork.us/).

## Outline
This project hasfour parts:

1:  Python Scripting
2:  Loading into ElasticSearch
3:  Visualizing and Analysis on Kibana
4:  Deploying code into Docker Container

## Python Scripting
I have developed a python command line interface that can connect to the OPCV API and demonstrate that the data is accessible via python.
Also script can able to run within docker but take parameters from the command line. Each line of data consumed by our script must then be passed appropriately into Elasticsearch.
I have determined fe fileds from the API also I have pushed into our Elasticsearch instance.

## Inputs/Outputs
Here are all the command line arguments our script supports:

$ docker run -e APP_KEY={YOUR_APP_KEY} -t bigdata1:1.0 python main.py --page_size=1000 --num_pages=4

## Some key arguments here:
●	APP_KEY: This is how a user can pass along an APP_KEY for the API in a safe manner. APP_KEY is not been “hardcoded” anywhere in my source code.
●	bigdata1: This is the name of your docker image. 
●	--page_size: This command line argument is required. It will ask for how many records to request from the API per call.
●	--num_pages: This command line argument is optional. If not provided, our script continue requesting data until the entirety of the content has been exhausted. If this argument is provided, continue querying for data num_pages times.


## Libraries

In order to accommodate the command line arguments (like the --page_size, etc), I have used the argparse library. 
All libraries that I used can be tracked in the requirements.txt file.
For this script, you must use PyPI’s sodapy module. This module makes it seamless to connect to your Socrata API and provides a high-level interface for providing additional parameters such as page offsets.
Your project should have a src folder containing functions for interacting with the OPCV API and for managing the API response. Your main.py script should live in the src folder at the same level as your Dockerfile and requirements.txt

## Visualizing and Analysis on Kibana

In order to properly index information on kibana, we will want to properly define a time field. The OPCV dataset does contain an issue_date  field that would be a good candidate for this definition. As part of this exercise, I have come up with a way to parse this field - which is stored as text - into a python datetime field.As far as output goes, I have configured Kibana to pull items from the index defined when loading data into Elasticsearch. This should load up the resulting data into the Kibana API and allow us to do some interesting analysis. I have created 4 visualizations in Kibana that analyze the data loaded and present analysis in graphical form. 


