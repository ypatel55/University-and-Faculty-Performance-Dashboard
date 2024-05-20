# University ratings pulled from ratemyprofessor.com

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Python dictionary with ratemyprofessor codes for each university in the data
university_codes = {
    "University of California--Berkeley": "1072",  "University of illinois at Urbana Champaign": "1112", "College of William Mary": "269", "University of Rochester": "1331", "Emory University": "340",
    "Carnegie Mellon University": "181", "Harvard University": "399", "Northwestern University": "709", "Cornell University": "298", "Case Western Reserve University": "186", "Yale University": "1222",
    "Johns Hopkins University": "464", "University of California--Los Angeles": "1075", "University of Florida": "1100", "Wake Forest University": "1130", "University of California--San Diego": "1079",
    "University of California--Irvine": "13221", "Boston University": "124", "New York University": "675", "Lehigh University": "509", "Georgetown University": "355", "University of Southern California": "1381",
    "Tufts University": "1040", "University of Notre Dame": "1576", "University of Wisconsin--Madison": "18418", "University of Chicago": "1085", "Tulane University": "1041", "Stanford University": "953",
    "University of Pennsylvania": "1275", "Brandeis University": "129", "Northeastern University": "696", "Columbia University": "278", "Duke University": "1350", "Massachusetts Institute of Technology": "580", 
    "University of Virginia": "1277", "Dartmouth College": "1339", "Vanderbilt University": "4002", "University of Texas at Austin": "1255", "University of North Carolina at Chapel Hill": "1232", "Rice University": "799",
    "Georgia Institute of Technology": "361", "Washington University in St Louis": "1147", "Boston College": "122", "University of Michigan": "1258", "California Institute of Technology": "148",
    "Brown University": "137", "University of California--Santa Barbara": "1077", "University of Georgia": "1101", "University of California--Davis": "1073", "Princeton University": "780", "Auburn University": "60",
    "Fordham University": "1325", "University of Maryland--College Park": "1270", "Howard University": "421", "University at Buffalo--SUNY": "960", "Texas A&M University": "1003","University of Massachusetts--Amherst": "1513",
    "Stony Brook University--SUNY": "971", "Purdue University--West Lafayette": "783", "George Washington University": "353", "Indiana University--Bloomington": "440", "University of Iowa": "1115", 
    "University of California--Santa Cruz": "1078", "Pepperdine University": "759", "American University": "32", "Villanova University": "1236", "Florida State University": "1237",
    "University of Minnesota--Twin Cities": "1257", "University of San Diego": "1340", "Virginia Tech": "1349", "Santa Clara University": "882", "Brigham Young University--Provo": "135", 
    "University of California--Merced": "4767", "University of California--Riverside": "1076", "Clemson University": "242", "Michigan State University": "601", "Worcester Polytechnic Institute": "1220", 
    "University of Denver": "1095", "Pennsylvania State University--University Park": "758", "Colorado School of Mines": "274", "Binghamton University--SUNY": "958", "Texas Christian University": "1008", 
    "Gonzaga University": "370", "Elon University": "333", "Baylor University": "90", "Rutgers University--New Brunswick": "825", "Stevens Institute of Technology": "982", "Southern Methodist University": "927",
    "North Carolina State University": "685", "University of Pittsburgh--Pittsburgh Campus": "1247", "Yeshiva University": "1223", "Rensselaer Polytechnic Institute": "795", "University of Miami": "1241",
    "University of Arizona": "1402", "University of Washington": "1530", "Syracuse University": "992", "Marquette University": "565"
}

# Returns ratemyprofessor given university id
def get_university_id(university_name):
    return university_codes.get(university_name, None)

# Extracts all university ratings from ratemyprofessor.com (11 types of ratings for each univesity)
def get_university_ratings(university_name):
    university_id = get_university_id(university_name)
    all_ratings = {}

    if university_id:
        search_url = f"https://www.ratemyprofessors.com/school/{university_id}"
        response = urlopen(search_url).read()
        soup = BeautifulSoup(response, features="lxml")

        overall = soup.find('div',attrs={'class':'OverallRating__Number-y66epv-3 dXoyqn'}).get_text(strip=True)
        all_ratings["Overall Rating"] = overall

        summary_ratings_container = soup.find_all('div', class_='GradeSquare__ColoredSquare-sc-6d97x2-0', limit=10)
        for summary in summary_ratings_container:
            container = summary.find_parent('div', class_='CategoryGrade__CategoryGradeContainer-sc-17vzv7e-0 ivOAGg')
            title = container.find('div', class_='CategoryGrade__CategoryTitle-sc-17vzv7e-1 XKroK').get_text(strip=True)
            rating = summary.get_text(strip=True)
            all_ratings[title] = rating

        return all_ratings


# Example usage:
#print(get_university_ratings("University of illinois at Urbana Champaign"))