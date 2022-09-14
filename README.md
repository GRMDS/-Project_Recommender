# Dataset Recommender of RMDS LAB
RMDS Lab is aiming to make its work more public to let data scientists enjoy the charm in algorithms. This is one of its open-source projects, project recommender, which
is deployed on the [RMDS LAB](https://grmds.org).

## Introduction
RMDS wants to recommend RMDS datasets to RMDS users customly based on datasets similarity and popularity. We would calculate out a recommendation score for each dataset and recommend those datasets with high recommendation scores to user. For public demonstration purpose, this project used generated data instead of read data. The process of fake data generation data is included as well.

The Dataset Recommender consists data generation, dataset similarity calculation and dataset recommendation.
1.	text_gen.py(optional)
•	generate fake dataset using aitextgen(original data not provided)
•	input: NA(trained models)
•	output: JSON format of list of projects and JSON format of dataset’s title and description
2.	top_click.py
•	generate most popular projects click history by user
•	input: NA
•	output: csv format of project click history for each user
3.	file_gen.py
•	generate project records and user upload history
•	input: project title and description
•	output: csv format of project with description, list of project and upload history
4.	recom_table.py
•	generate data for dataset including dataset information, view and download
•	input: NA
•	output: csv format of basic dataset information
5.	recom.py
•	recommend 5 datasets to each user based on user similarity and datasets similarity
•	input: project record, dataset record
•	output: csv format of recommendation for each user
6.	dataset_fake.ipynb
This is a Jupyter notebook of the complete process of the recommendation system(except text gen). It could be used as an overview of the project.


## Requirements of development environment
- pyjarowinkler 1.8
- scikit-learn 0.24.0
## License
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-green.svg)](https://www.gnu.org/licenses/agpl-3.0)
