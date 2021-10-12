from bs4 import BeautifulSoup
import requests
import smtplib
import time
import datetime
from enum import Enum
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from colorama import Fore, Back, Style
import json

ticketsOnSale = False
passNumber = 0
thisYearsRelease = None
nextYearsRelease = None

# ask the user what movie he wants to monitor
# search for current year and (current year + 1) movies with that name
# user chooses a movie
moviesBaseURL = "http://www.omdbapi.com/?apikey=24712c16"
print(Fore.YELLOW + "Would you like to monitor a specific date (1) or search for a movie?")
monitoringChoice = input()
# for a date, skip all this movie shit, if not, execute the movie shit
print(Fore.YELLOW + "What movie would you like to monitor tickets for?" + Fore.BLUE)
movieToWatchInput = input()
print(Fore.LIGHTGREEN_EX + "Searching for movies with that name..." + Fore.RESET)

current_year = datetime.date.today().year
current_month = datetime.date.today().month
currentYearMovies = requests.request('GET', moviesBaseURL + '&t=' + movieToWatchInput + '&y=' +  str(current_year))
nextYearMovies 	  = requests.request('GET', moviesBaseURL + '&t=' + movieToWatchInput + '&y=' +  str(current_year + 1))
parsedCYMovie = json.loads(currentYearMovies.content)
print(json.dumps(parsedCYMovie, indent=4))
parsedNYMovie = json.loads(nextYearMovies.content)

if parsedCYMovie["Response"] == "True":
	thisYearsRelease = parsedCYMovie["Released"]
if parsedNYMovie["Response"] == "True":
	nextYearsRelease = parsedNYMovie["Released"]


movieFound = 1

while movieFound == 1 or movieFound == 2 or movieFound == 'n' or movieFound == 'N':

	if thisYearsRelease != "N/A" and nextYearsRelease != "N/A" and current_month >= 11 :
		print(Fore.YELLOW + "Which of these two movies are you looking to monitor? Enter '1' or '2'.")
		print(Fore.BLUE + "--> 1. " + parsedCYMovie["Title"] + " , coming out on " + Fore.RED + thisYearsRelease + ".")
		print(Fore.BLUE + "--> 2. '" + parsedNYMovie["Title"] + "', coming out on " + nextYearsRelease + ".")
		movieFound = input()
	elif thisYearsRelease != "N/A" and nextYearsRelease == "N/A":
		print(Fore.YELLOW + "Is this the movie you were looking for? Enter (Y/N)")
		print(Fore.BLUE + "--> '" + parsedCYMovie["Title"] + "', coming out on " + Fore.RED + thisYearsRelease + ".")
		movieFound = input()
	elif thisYearsRelease == "N/A" and nextYearsRelease != "N/A":
		print(Fore.YELLOW + "Is this the movie you were looking for? Enter (Y/N)")
		print(Fore.BLUE + "--> '" + parsedNYMovie["Title"] + "', coming out on " + Fore.RED + nextYearsRelease + ".")
		movieFound = input()
	else:
		print("Found no movies with that name. Press '1' to search a different movie. Press '3' to shutdown.")
		movieFound = input()
		exit()

# add a while
# put it all in a dictionary to keep things organized
# grab that movie's release date and use that for the request to Cineplex


exit()

print("Enter a date to watch tickets for in MM/DD/YYYY format: ")
dateToWatch = input()
ticketsPurchaseLink = "https://www.cineplex.com/Showtimes/any-movie/cinema-banque-scotia-montreal?Date=" + dateToWatch
# print("How do you want to be contacted? Press 1 for email, 2 for phone, 3 for both.")
# alertMethod = input()

# class AlertMethod(Enum):
#     EMAIL = 1
#     PHONE = 2
#     BOTH = 3
    
# def sendAlert(method):
    # if(method == AlertMethod.EMAIL):
    #     emailAlert()
    # elif(method == AlertMethod.PHONE):
    #     phoneAlert()
    # elif(method == AlertMethod.BOTH):
    #     totalAlert()
    # else:
    #     print("Alert method switch case failed.")
    #     print(method)
    #     for am in (AlertMethod):
    #         print(am)

def emailAlert():
	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Cineplex ' + dateToWatch + ' Tickets Alert'
	msg['From'] = "leonard.bonfils@gmail.com"
	msg['To'] = "l.92@icloud.com"

	text = 'Tickets are now available'
	html = '''
			<!DOCTYPE html>
			<html>
				<body>
					<div style="background-color:#eee;padding:10px 20px;">
						<h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;">Buy tickets now!</h2>
					</div>
					<div style="padding:20px 0px">
						<div style="height: 500px;width:400px">
							<img src="https://i.imgur.com/hxEGEPr.jpeg" style="height: 300px;">
							<div style="text-align:center;">
								<h3>Hurry!</h3>
								<p>Tickets are now on sale. Get them quick!</p>
								<a href={ticketsPurchaseLink}>Link to buy</a>
							</div>
						</div>
					</div>
				</body>
			</html>
		'''
  
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	msg.attach(part1)
	msg.attach(part2)

	# Send the message via our own SMTP server.
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("leonard.bonfils@gmail.com", "ssbqwssycfxmpchs")
	server.send_message(msg)
	server.quit()

def phoneAlert():
    print('Whatever')

def totalAlert():
    emailAlert()
    phoneAlert()

while(ticketsOnSale == False):
    ticketsResp = requests.get(ticketsPurchaseLink)
    html = ticketsResp.content
    soup = BeautifulSoup(html, "html.parser")

    # option_tags = soup.find_all("No movies are playing")
    div_1 = soup.find_all("div", {"class": "error-simple"})
    # print(option_tags)
    now = datetime.datetime.now()
    nowFormatted = now.strftime(("%m-%d-%Y %H:%M")) 
    
    passNumber += 1
    print(Fore.YELLOW + "Request #" + str(passNumber))
    
    if("No movies" in str(div_1)):
        ticketsOnSale = False
        print(Fore.BLUE + f"{nowFormatted}: " + Fore.LIGHTGREEN_EX + "Tickets are not on sale yet.")
    else:
        ticketsOnSale = True
        print(Fore.RED + f"TICKETS NOW ON SALE! - " + Fore.MAGENTA + f"Released at {nowFormatted}")

    time.sleep(60)
    
emailAlert()

quit()