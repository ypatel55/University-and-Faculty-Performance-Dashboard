
# University and Faculty Performance Dashboard
## By: Yogi Patel

## Purpose
The University and Faculty Performance Dashboard is designed to allow user exploration of academic data encompassing universities, faculty members, publications, research interests, and more.
\
The target users of this dashboard are students, researchers, and anyone else interested in exploring academic data. The dashboard serves as a valuable resource for evaluating the performance of universities and their faculty members so users can find information best suited for their needs.
\
The main objectives of this dashboard are to provide insights into the performance of universities and their faculty members based on metrics such as publication count, faculty collaboration, faculty expertise, and university quality data sourced from [ratemyprofessors.com](https://www.ratemyprofessors.com/). The dashboard also aims to provide visualization and analysis tools for users to understand trends at universities and make informed decisions for their academic interests.

## Installation
* Clone the repository to local machine
* Set up the MySQL, Neo4j, and MongoDB databases accordingly
* Open terminal and run `python3 app.py`

## Usage
Usage of Application: After running `python3 app.py` in your terminal, navigate to the dash app using the http link returned. 

Usage of Dashboard: Start by selecting a University from the dropdown at the top of the dashboard. After selecting a University, certain widgets will be auto populated and certain widgets will require user input. Here is a explanation of each widget and how to use them:

- **Widget 1:** This will be auto populated with the logo of the University you chose. It will also display some metrics about the university. (MySQL)

- **Widget 2:** This widget will also be auto populated. It will display 11 different ratings for the university chosen which are pulled from [ratemyprofessors.com](https://www.ratemyprofessors.com/)

- **Widget 3:** This widget allows you to explore co-publications of a faculty member. Select a faculty member from the drop down and a graph will be displayed with nodes to other faculty they have ever co-published with. (Neo4j)
  
- **Widget 4:** This will also be auto populated. It will display the top 10 keywords at the given university and users can hover over the graph for additional information. (MySQL)

- **Widget 5:** This widget takes an input of a keyword and returns faculty members associated with that keyword. The data will be displayed in a table and users can hover over the name of the faculty member to see an image of them if it is available in the database. (MongoDB)

- **Widget 6:** This widget allows users to select a faculty member from the dropdown and will display all publications by that faculty member. (MongoDB)

- **Widget 7:** This widget is auto populated and shows the number of publications per year for the selected university. The user can hover over the graph to see additional data. (Neo4j)

- **Widget 8:** This widget will be auto populated if there is research interest data available for the selected university. If there isn’t, it will simply display a message saying so. If there is available data, the widget will show a graph of the top 10 research interests by faculty members at that university. (MySQL)

- **Widget 9:** This widget is also only available if there is research interest data available for the selected university (similar to widget 8). If there isn’t, it will simply display a message saying so and the drop down selection will be empty. If there is available data, the widget will allow the user to select a research interest and will display faculty members who have the given research interest. The data is again returned as a table and has the option to hover over the faculty members name to see their image if available. (MySQL)

- **Widgets 10 & 11:** These widgets allow users to enter their name or any username to save their results. Users can choose to save faculty members in one widget and keywords in the other. They can use the provided buttons to add or delete to their favorites or simply view what’s in their favorites for each. These widgets both perform updates of the backend database. (MySQL)

Overall, the dashboard is easy to navigate and use through the visually pleasing layout and informative labels given. The different sections allow users to explore and interact with the data. 

## Design
The application has an architecture with separate components for data retrieval. The main app.py file uses the backend python scripts [mysql_utils.py](mysql_utils.py), [mongodb_utils.py](mongodb_utils.py), [neo4j_utils.py](neo4j_utils.py), and [ratemyprofessor.py](ratemyprofessor.py) to query data from the respective databases. The frontend of this application is built using HTML, CSS, Python, and Dash for visualization and user interaction.

## Implementation
The dashboard is implemented using Python for scripting. I used MySQL, Neo4j, and MongoDB Databases by connecting with mysql.connector, neo4j GraphDatabase, and pymongo respectively. I also utilized HTTP requests, urllib, and BeautifulSoup to pull data from [ratemyprofessors.com](https://www.ratemyprofessors.com/). For the overall implementation of the dashboard, I used Dash, dash_bootstrap_components, plotly.express,  dash_cytoscape, dash_dependencies, HTML, CSS, and Pandas.
