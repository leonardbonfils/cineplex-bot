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

ticketsOnSale = False
passNumber = 0

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
								<a href=f{ticketsPurchaseLink}>Link to buy</a>
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
	server.login("your email", "your email's password")
	server.send_message(msg)
	server.quit()

def phoneAlert():
    print('Whatever')

def totalAlert():
    emailAlert()
    phoneAlert()

while(ticketsOnSale == False):
    resp = requests.get(ticketsPurchaseLink)
    html = resp.content
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
        print(Fore.RED + "TICKETS NOW ON SALE! - " + Fore.MAGENTA + f"Released at {nowFormatted}")

    time.sleep(60)
    
emailAlert()

quit()
