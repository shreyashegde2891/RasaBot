from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk import Tracker
from typing import Any, Text, Dict, List, Union
from rasa_sdk.executor import CollectingDispatcher
import zomatopy
import json
import pandas as pd
import re
# Import the email modules
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def results_to_utterance(price_results):
	response = ''
	matching_results_found = False

	if len(price_results)==0:
		response = "Sorry couldn't find any restaurants in price range."
	else:
		matching_results_found = True
		i = 0
		for index, row in price_results.head(5).iterrows():
			i = i+1
			response = response + str( i ) + ". \"" + row['Restaurant_Name'] + "\" in \"" + row['Address'] + "\" has been rated "+str(row['Rating']) + ". And the average price for two people here is: " + str(row['Avg_budget']) + " Rs \n"

	return matching_results_found, response

def results_to_email(price_results):
	response = '<table border=1><tr><th>Name</th><th>Address</th><th>Rating</th><th>Average price for two</th></tr>'
	for index, row in price_results.head(10).iterrows():
		response = response + "<tr><td>" + row['Restaurant_Name'] + "</td><td>" + row['Address'] + "</td><td> Rated "+str(row['Rating']) + ".</td><td> " + str(row['Avg_budget']) + " Rs </td></tr>"

	return response + "</table>"

class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'


	def run(self, dispatcher, tracker, domain):

		config={ "user_key":"f207a84eb81c174a12735f568cffd505"}
		zomato = zomatopy.initialize_app(config)
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		price_range = tracker.get_slot('budget')
		print("Details:")
		print(loc)
		print(cuisine)
		print(price_range)
		location_detail=zomato.get_location(loc, 1)
		d1 = json.loads(location_detail)
		lat=d1["location_suggestions"][0]["latitude"]
		lon=d1["location_suggestions"][0]["longitude"]
		cuisines_dict={'chinese':25,'mexican':73,'south indian':85,'north indian':50,'american':1,'italian':55}

		dispatcher.utter_message("---------------------------------------")
		dispatcher.utter_message("Searching for restaurants...")

		results_df = pd.DataFrame(columns=['Restaurant_Name','Address','Avg_budget','Rating'])
		results = zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 0, 20, "rating", "desc")
		matching_results_found = False

		d = results
		response=""
		if d['results_found'] == 0:
			response= "no results"
		else:
			for restaurant in d['restaurants']:
				results_df = results_df.append({'Restaurant_Name':restaurant['restaurant']['name'],'Address': restaurant['restaurant']['location']['address'],'Avg_budget':restaurant['restaurant']['average_cost_for_two'],'Rating':restaurant['restaurant']['user_rating']['aggregate_rating']},ignore_index=True)
				#response=response+ "Restaurant Name: "+ restaurant['restaurant']['name']+ " Address: "+ restaurant['restaurant']['location']['address']+" Average budget for two people: "+restaurant['restaurant']['average_cost_for_two']+" Zomato user rating: "+ restaurant['restaurant']['user_rating']['aggregate_rating']+"\n"	

		if price_range=="<500" or price_range == "500":
			matching_results_found, response = results_to_utterance(results_df[results_df['Avg_budget'] <= 500])
		elif(price_range=="500-700"):
			price_results = results_df[(results_df['Avg_budget'] >500) & (results_df['Avg_budget'] < 700)]
			matching_results_found, response = results_to_utterance(price_results)
		else:
			price_results = results_df[(results_df['Avg_budget'] >=700)]
			matching_results_found, response = results_to_utterance(price_results)

		if matching_results_found:
			dispatcher.utter_message("Showing you top rated restaurants:")
			dispatcher.utter_message(response)
			dispatcher.utter_message("---------------------------------------")
		else:
			dispatcher.utter_message(response)
			dispatcher.utter_message("---------------------------------------")
			# dispatcher.utter_template("utter_ask_alternate_budget", tracker, domain)

		# cuisines_dict={'bakery':5,'chinese':25,'cafe':30,'italian':55,'biryani':7,'north indian':50,'south indian':85}
		if matching_results_found:
			return [SlotSet('search_results', results), SlotSet('found_results', matching_results_found)]
		else:
			return [SlotSet('search_results', None), SlotSet('found_results', matching_results_found)]

class SendEmail(Action):
	def name(self):
		return 'action_email'
		
	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		price_range = tracker.get_slot('budget')
		email = tracker.get_slot('email')
		print("Inside email")
		print(email)
		results = tracker.get_slot('search_results')
		results_df = pd.DataFrame(columns=['Restaurant_Name','Address','Avg_budget','Rating'])

		dispatcher.utter_message("Sending email ... ")

		msg = MIMEMultipart()
		msg['From']=""  # Enter your email address here
		msg['To']=email 
		msg['Subject']="Your recommendations from rasa bot"

		d = results

		try:
			if d['results_found'] == 0:
				response= "no restaurants found!!"
			else:
				for restaurant in d['restaurants']:
					results_df = results_df.append({'Restaurant_Name':restaurant['restaurant']['name'],'Address': restaurant['restaurant']['location']['address'],'Avg_budget':restaurant['restaurant']['average_cost_for_two'],'Rating':restaurant['restaurant']['user_rating']['aggregate_rating']},ignore_index=True)

			response = "Hello,<br><br><b>The Top (upto 10) restaurants for your search for {} food in {} with a price range of {} </b> <br><br>".format(cuisine, loc, price_range)

			if price_range=="<500" or price_range == "500":
				response = response + results_to_email(results_df[results_df['Avg_budget'] <= 500])
			elif(price_range=="500-700"):
				price_results = results_df[(results_df['Avg_budget'] >500) & (results_df['Avg_budget'] < 700)]
				response = response + results_to_email(price_results)
			else:
				price_results = results_df[(results_df['Avg_budget'] >=700)]
				response = response + results_to_email(price_results)

			# print(response)
			msg.attach(MIMEText(response,'html'))
			msg.attach(MIMEText('<br><br>Bon Appetit!!','html'))
			
			try:
			
				server = smtplib.SMTP('smtp.gmail.com:587')
				server.starttls()
				server.login(msg['From'], '<Password>')
				server.sendmail(msg['From'], msg['To'], msg.as_string())
				server.quit()
			except asyncio.TimeoutError: 
				dispatcher.utter_message("Smtplib asyncio error")

			dispatcher.utter_message("Sent!")
		except Exception as inst:
			print(type(inst))    # the exception instance
			print(inst.args)     # arguments stored in .args
			print(inst)          # __str__ allows args to be printed directly,
			dispatcher.utter_message("Sorry, I failed to send email. I'm not going to retry.")

		return [SlotSet('email_sent', True)]

class ValidateLocation(Action):
	def name(self):
		return 'action_validate_location'
	
	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('location')	
		print("Inside ValidateLocation")
		print(loc)
		known_invalid_locs = ['Achhnera', 'Adalaj', 'Adoni', 'Adoor', 'Adra', 'Adyar', 'Afzalpur', 'Agartala', 'Ahmednagar', 
		'Aizawl', 'Akola', 'Akot', 'Alappuzha', 'Alipurduar', 'Alirajpur', 'Almora', 'Aluva', 'Alwar', 'Amalapuram', 
		'Amalner', 'Amaravathi', 'Amaravati', 'Ambala', 'Ambattur', 'Ambejogai', 'Ambernath', 'Amroha', 'Anakapalle', 
		'Anand', 'Anantapur', 'Angul', 'Anjangaon', 'Anjar', 'Ankleshwar', 'Arakkonam', 'Arambagh', 'Araria', 'Arrah', 
		'Arsikere', 'Aruppukkottai', 'Arvi', 'Arwal', 'Asarganj', 'Ashok Nagar', 'Athni', 'Attingal', 'Avadi', 
		'BIHAR', 'Badrinath', 'Bageshwar', 'Bagha Kusmar', 'Baharampur', 'Bahraich', 'Bajpur', 'Balaghat', 'Balangir', 
		'Bally', 'Banaganipalli', 'Bapatla', 'Baranagar', 'Barasat', 'Barauli', 'Barbigha', 'Barbil', 'Bardhaman', 
		'Bargarh', 'Barkot', 'Barpeta', 'Bathinda', 'Begusarai', 'Bellampalle', 'Bellary', 'Belonia', 'Berhampur', 
		'Bettiah', 'Bhabua', 'Bhadrachalam', 'Bhagalpur', 'Bhainsa', 'Bhaiseena', 'Bhalswa Jahangir Pur', 'Bharatpur', 
		'Bhatapara', 'Bhatpara', 'Bhawanipatna', 'Bheemunipatnam', 'Bhilai', 'Bhilwara', 'Bhimavaram', 'Bhimtal', 
		'Bhind', 'Bhiwani', 'Bhongir', 'Bhowali', 'Bhusawal', 'Bhusawar', 'Bidar', 'Bidhan Nagar', 'Bihar Sharif', 
		'Bilaspur', 'Bobbili', 'Bodhan', 'Bokaro', 'Bongaigaon City', 'Bulandshahr', 'Burhanpur', 'Buxar', 'Byasanagar', 
		'Chaibasa', 'Chalakudy', 'Chamba', 'Chamoli Gopeshwar', 'Champawat', 'Chandpara', 'Chandrapur', 'Changanassery', 
		'Chapra', 'Charkhi Dadri', 'Chatra', 'Chengannur', 'Cherthala', 'Chhapra', 'Chidambaram', 'Chirala', 'Chirkunda', 
		'Chirmiri', 'Chittoor', 'Chittur-Thathamangalam', 'Cooch Behar', 'Dalli-Rajhara', 'Danapur', 'Darbhanga', 
		'Davanagere', 'Degana', 'Dehri', 'Deoghar', 'Devprayag', 'Dewas', 'Dhamtari', 'Dharchula', 'Dharmanagar', 
		'Dharmavaram', 'Dhenkanal', 'Dhone,', 'Dhoraji', 'Dhubri', 'Dhule', 'Dhuri', 'Didihat', 'Dindigul', 'Dineshpur', 
		'Diphu', 'Dogadda', 'Doiwala', 'Dumka', 'Dumraon', 'Durg', 'Dwarahat', 'Ellenabad', 'Eluru', 'English Bazar', 
		'Etawah', 'EtawahMumbai', 'Faizabad', 'Faridkot', 'Farooqnagar', 'Farrukhabad', 'Fatehabad', 'Fatehpur', 'Fazilka', 
		'Firozpur Cantt.', 'Forbesganj', 'Gadarpur', 'Gadwal', 'Gandhidham', 'Gandhinagar', 'Gangarampur', 'Gangotri', 
		'Gangtok', 'Gavaravaram', 'Gaya', 'Goalpara', 'Gobichettipalayam', 'Gobindgarh', 'Gochar', 'Gohana', 'Gokak', 
		'Golaghat', 'Gooty', 'Gopalganj', 'Gopalpur', 'Gudivada', 'Gudur', 'Gumia', 'Guna', 'Guntakal', 'Gunupur', 
		'Gurdaspur', 'Guruvayoor', 'Hajipur', 'Haldia', 'Hansi', 'Hapur', 'Haridwar', 'Herbertpur', 'Hindupur', 'Hospet', 
		'Howrah', 'Hubballi-Dharwad', 'Hugli and Chinsurah', 'Ichalkaranji', 'Imphal', 'Itarsi', 'Jaggaiahpet', 'Jagraon', 
		'Jagtial', 'Jalandhar Cantt.', 'Jalgaon', 'Jalna', 'Jamalpur', 'Jammalamadugu', 'Jamui', 'Jangaon', 'Jaspur', 
		'Jatani', 'Jaunpur', 'Jehanabad', 'Jhabrera', 'Jhargram', 'Jharsuguda', 'Jhumri Tilaiya', 'Jorhat', 'Joshimath', 
		'Junagadh', 'Kadapa', 'Kadi', 'Kadiri', 'Kagaznagar', 'Kailasahar', 'Kaladhungi', 'Kalimpong', 'Kallakurichi', 
		'Kalpi', 'Kalyan-Dombivali', 'Kamareddy', 'Kamarhati', 'Kandukur', 'Kanhangad', 'Kanigiri', 'Kapadvanj', 'Karaikal', 
		'Karaikudi', 'Karawal Nagar', 'Karimganj', 'Karimnagar', 'Karjat', 'Karnal', 'Karnaprayag', 'Karur', 'Kasaragod', 
		'Kathua', 'Katihar', 'Kavali', 'Kayamkulam', 'Kedarnath', 'Kela Khera', 'Kendrapara', 'Kendujhar', 'Keshod', 
		'Khambhat', 'Khammam', 'Khanda', 'Khandwa', 'Kharagpur', 'Kharar', 'Khatima', 'Khodargama', 'Khowai', 'Kichha', 
		'Kirari Suleman Nagar', 'Kirtinagar', 'Kishanganj', 'Kodungallur', 'Kohima*', 'Koratla', 'Korba', 'Kot Kapura', 
		'Kotdwar', 'Kothagudem', 'Kovvur', 'Koyilandy', 'Kulti', 'Kumarganj', 'Kumbakonam', 'Kunnamkulam', 'Kyathampalle', 
		'Lachhmangarh', 'Ladnu', 'Ladwa', 'Lahar', 'Laharpur', 'Lakheri', 'Lakhisarai', 'Laksar', 'Lakshmeshwar', 
		'Lal Gopalganj Nindaura', 'Lalganj', 'Lalgudi', 'Lalkuan', 'Lalsot', 'Landhaura', 'Lanka', 'Lar', 'Lathi', 
		'Latur', 'Lilong', 'Limbdi', 'Lingsugur', 'Loha', 'Lohaghat', 'Lohardaga', 'Lonar', 'Lonavla', 'Longowal', 
		'Loni', 'Losal', 'Lumding', 'Lunawada', 'Lunglei', 'MUZAFFARPUR', 'Macherla', 'Machilipatnam', 'Madanapalle', 
		'Maddur', 'Madhepura', 'Madhubani', 'Madhugiri', 'Madhupur', 'Madhyamgram', 'Madikeri', 'Magadi', 'Mahaboobnagar', 
		'Mahad', 'Mahalingapura', 'Maharajganj', 'Maharajpur', 'Mahasamund', 'Mahe', 'Mahemdabad', 'Mahendragarh', 
		'Mahesana', 'Maheshtala', 'Mahnar Bazar', 'Mahua Dabra Haripura', 'Mahua Kheraganj', 'Maihar', 'Mainaguri', 
		'Makhdumpur', 'Makrana', 'Malaj Khand', 'Malavalli', 'Malda', 'Malegaon', 'Malkangiri', 'Malkapur', 'Malout', 
		'Malpura', 'Malur', 'Manachanallur', 'Manasa', 'Manavadar', 'Manawar', 'Mandalgarh', 'Mandamarri', 'Mandapeta', 
		'Mandawa', 'Mandi Dabwali', 'Mandideep', 'Mandla', 'Mandvi', 'Manendragarh', 'Maner Sharif', 'Mangaldoi', 
		'Mangalvedhe', 'Manglaur', 'Mango', 'Mangrol', 'Mangrulpir', 'Manihari', 'Manjlegaon', 'Mankachar', 'Manmad', 
		'Mansa', 'Manuguru', 'Manvi', 'Manwath', 'Mapusa', 'Margao', 'Margherita', 'Marhaura', 'Mariani', 'Marigaon', 
		'Markapur', 'Masaurhi', 'Mathabhanga', 'Mattannur', 'Mau', 'Mauganj', 'Mavelikkara', 'Mavoor', 'Mayang Imphal', 
		'Medak', 'Medininagar', 'Medinipur', 'Mehkar', 'Memari', 'Merta City', 'Mhaswad', 'Mhow Cantonment', 'Mhowgaon', 
		'Mihijam', 'Mira-Bhayandar', 'Mirganj', 'Miryalaguda', 'Mirzapur', 'Modasa', 'Mokameh', 'Mokokchung', 'Monoharpur', 
		'Morbi', 'Morena', 'Morinda, India', 'Morshi', 'Motihari', 'Motipur', 'Mount Abu', 'Mudabidri', 'Mudalagi', 
		'Muddebihal', 'Mudhol', 'Mukerian', 'Mukhed', 'Muktsar', 'Mul', 'Mulbagal', 'Multai', 'Mundargi', 'Mundi', 
		'Mungeli', 'Munger', 'Muni Ki Reti', 'Murliganj', 'Murshidabad', 'Murtijapur', 'Murwara', 'Musabani', 'Mussoorie', 
		'Muvattupuzha', 'Muzaffarnagar', 'Muzaffarpur', 'Nabarangapur', 'Nabha', 'Nadbai', 'Nadiad', 'Nagar', 'Nagari', 
		'Nagarkurnool', 'Nagercoil', 'Nagina', 'Nagla', 'Nagpur', 'Nahan', 'Naharlagun', 'Naidupet', 'Naihati', 
		'Naila Janjgir', 'Nainital', 'Nainpur', 'Najibabad', 'Nakodar', 'Nakur', 'Nalbari', 'Namagiripettai', 'Namakkal', 
		'Nandaprayag', 'Nandgaon', 'Nandivaram-Guduvancheri', 'Nandura', 'Nandyal', 'Nangal', 'Nangloi Jat', 'Nanjangud', 
		'Nanjikottai', 'Nanpara', 'Narasapuram', 'Narasaraopet', 'Naraura', 'Narayanpet', 'Narendranagar', 'Nargund', 
		'Narkatiaganj', 'Narkhed', 'Narnaul', 'Narsinghgarh', 'Narsipatnam', 'Narwana', 'Nasirabad', 'Natham', 'Nathdwara', 
		'Naugachhia', 'Naugawan Sadat', 'Naura', 'Nautanwa', 'Navalgund', 'Navi Mumbai', 'Navi Mumbai Panvel Raigad', 'Nawabganj', 
		'Nawada', 'Nawanshahr', 'Nawapur', 'Nedumangad', 'Nedumbassery', 'Neem-Ka-Thana', 'Nehtaur', 'Nelamangala', 'Nellikuppam', 
		'Nepanagar', 'New Delhi', 'Neyyattinkara', 'Nidadavole', 'Nilambur', 'Nilanga', 'Nimbahera', 'Nirmal', 'Niwai', 
		'Niwari', 'Nizamabad', 'Nohar', 'Nokha', 'Nongstoin', 'Noorpur', 'North Dumdum', 'North Lakhimpur', 'Nowgong', 
		'Nowrozabad', 'Nuzvid', 'Obra', 'Oddanchatram', 'Ongole', 'Orai', 'Ottappalam', 'Owk', 'Ozar', 'Ozhukarai', 
		'P.N.Patti', 'Pachora', 'Pachore', 'Pacode', 'Padmanabhapuram', 'Padra', 'Padrauna', 'Paithan', 'Pakaur', 'Palai', 
		'Palampur', 'Palani', 'Palasa Kasibugga', 'Palghar', 'Pali', 'Palia Kalan', 'Palitana', 'Palladam', 'Pallapatti', 
		'Pallavaram', 'Pallikonda', 'Palwancha', 'Panagar', 'Panagudi', 'Panaji', 'Panamattom', 'Panchkula', 'Panchla', 
		'Pandharkaoda', 'Pandharpur', 'Pandhurna', 'Pandua', 'Panihati', 'Panipat', 'Panna', 'Panniyannur', 'Panruti', 
		'Panvel', 'Pappinisseri', 'Paradip', 'Paramakudi', 'Parangipettai', 'Parasi', 'Paravoor', 'Parbhani', 'Pardi', 
		'Parlakhemundi', 'Parli', 'Partur', 'Parvathipuram', 'Pasan', 'Paschim Punropara', 'Pasighat', 'Pathanamthitta', 
		'Pathardi', 'Pathri', 'Patiala', 'Patratu', 'Pattamundai', 'Patti', 'Pattran', 'Pattukkottai', 'Patur', 'Pauni', 
		'Pauri', 'Pavagada', 'Pedana', 'Peddapuram', 'Pehowa', 'Pen', 'Perambalur', 'Peravurani', 'Peringathur', 'Perinthalmanna', 
		'Periyakulam', 'Periyasemur', 'Pernampattu', 'Perumbavoor', 'Petlad', 'Phagwara', 'Phalodi', 'Phaltan', 'Phillaur', 
		'Phulabani', 'Phulera', 'Phulpur', 'Pihani', 'Pilani', 'Pilibanga', 'Pilkhuwa', 'Pimpri-Chinchwad', 'Pindwara', 
		'Pipar City', 'Piriyapatna', 'Piro', 'Pithampur', 'Pithapuram', 'Pithoragarh', 'Polur', 'Ponnani', 'Ponneri', 
		'Ponnur', 'Poonch', 'Porsa', 'Port Blair', 'Powayan', 'Prantij', 'Pratapgarh', 'Prithvipur', 'Proddatur', 
		'Pudupattinam', 'Pukhrayan', 'Pulgaon', 'Puliyankudi', 'Punalur', 'Punganur', 'Punjaipugalur', 'Puranpur', 
		'Purna', 'Purnia', 'Purquazi', 'Purwa', 'Pusad', 'Puthuppally', 'Puttur', 'Qadian', 'Rabkavi Banhatti', 
		'Radhanpur', 'Rae Bareli', 'Rafiganj', 'Raghogarh-Vijaypur', 'Raghunathpur', 'Rahatgarh', 'Rahuri', 'Raichur', 
		'Raiganj', 'Raikot', 'Rairangpur', 'Raisen', 'Raisinghnagar', 'Rajagangapur', 'Rajakhera', 'Rajaldesar', 'Rajam', 
		'Rajauri', 'Rajesultanpur', 'Rajgarh', 'Rajgir', 'Rajpipla', 'Rajpur Sonarpur', 'Rajpura', 'Rajsamand', 'Rajula', 
		'Rajura', 'Ramachandrapuram', 'Ramagundam', 'Ramanagaram', 'Ramanathapuram', 'Ramdurg', 'Rameshwaram', 
		'Ramganj Mandi', 'Ramnagar', 'Ramngarh', 'Rampur', 'Rampur Maniharan', 'Rampura Phul', 'Rampurhat', 'Ramtek', 
		'Ranavav', 'Rangiya', 'Rania', 'Ranibennur', 'Rapar', 'Rasipuram', 'Rasra', 'Ratangarh', 'Rath', 'Ratia', 
		'Ratlam', 'Ratnagiri', 'Rau', 'Raurkela Industrial Township', 'Raver', 'Rawatbhata', 'Rawatsar', 'Raxaul Bazar', 
		'Rayachoti', 'Rayadurg', 'Rayagada', 'Reengus', 'Rehli', 'Renigunta', 'Renukoot', 'Reoti', 'Repalle', 'Revelganj', 
		'Rewa', 'Rishikesh', 'Risod', 'Robertsganj', 'Rohtak', 'Ron', 'Roorkee', 'Rosera', 'Rudauli', 'Rudraprayag', 
		'Rudrapur', 'Rupnagar', 'Sabalgarh', 'Sadabad', 'Sadasivpet', 'Sadri', 'Sadulshahar', 'Safidon', 'Safipur', 
		'Sagar', 'Sagara', 'Sagwara', 'Saharanpur', 'Saharsa', 'Sahaspur', 'Sahaswan', 'Sahawar', 'Sahibganj', 
		'Sahjanwa', 'Saidpur', 'Saiha', 'Sailu', 'Sainthia', 'Sakaleshapura', 'Sakti', 'Salaya', 'Salur', 'Samalkha', 
		'Samalkot', 'Samana', 'Samastipur', 'Sambalpur', 'Sambhal', 'Sambhar', 'Samdhan', 'Samthar', 'Sanand', 'Sanawad', 
		'Sanchore', 'Sandi', 'Sandila', 'Sanduru', 'Sangamner', 'Sangareddy', 'Sangaria', 'Sangli-Miraj & Kupwad', 
		'Sangole', 'Sangrur', 'Sanivarapupeta', 'Sankarankovil', 'Sankari', 'Sankeshwara', 'Sarangpur', 'Sardarshahar', 
		'Sardhana', 'Sarni', 'Sarsawa', 'Sarsod', 'Sasaram', 'Sasvad', 'Satana', 'Satara', 'Sathyamangalam', 'Satna', 
		'Satrampadu', 'Sattenapalle', 'Sattur', 'Saunda', 'Saundatti-Yellamma', 'Sausar', 'Savanur', 'Savarkundla', 
		'Savner', 'Sawantwadi', 'Secunderabad', 'Sedam', 'Sehore', 'Sendhwa', 'Seohara', 'Seoni', 'Seoni-Malwa', 
		'Serampore', 'Shahabad', 'Shahade', 'Shahbad', 'Shahdol', 'Shahganj', 'Shahjahanpur', 'Shahpur', 'Shahpura', 
		'Shajapur', 'Shaktigarh', 'Shamgarh', 'Shamli', 'Shamsabad, Farrukhabad', 'Shegaon', 
		'Sheikhpura', 'Shendurjana', 'Shenkottai', 'Sheoganj', 'Sheohar', 'Sheopur', 'Sherghati', 'Sherkot', 
		'Shiggaon', 'Shikaripur', 'Shikarpur', 'Shikohabad', 'Shimla', 'Shirdi', 'Shirpur-Warwade', 'Shirur', 
		'Shishgarh', 'Shivamogga', 'Shivpuri', 'Sholavandan', 'Sholingur', 'Shoranur', 'Shrigonda', 'Shrirampur', 
		'Shrirangapattana', 'Shujalpur', 'Siana', 'Sibsagar', 'Siddipet', 'Sidhi', 'Sidhpur', 'Sidlaghatta', 'Sihor', 
		'Sihora', 'Sikanderpur', 'Sikandra Rao', 'Sikandrabad', 'Sikar', 'Silao', 'Silapathar', 'Sillod', 'Silvassa*', 
		'Simdega', 'Sindagi', 'Sindhagi', 'Sindhnur', 'Singrauli', 'Sinnar', 'Sira', 'Sircilla', 
		'Sirhind Fatehgarh Sahib', 'Sirkali', 'Sirohi', 'Sironj', 'Sirsa', 'Sirsaganj', 'Sirsi', 'Siruguppa', 
		'Sitamarhi', 'Sitarganj', 'Sivaganga', 'Sivagiri', 'Siwan', 'Sohagpur', 'Sohna', 'Sojat', 'Solan', 'Sonamukhi', 
		'Sonepur', 'Songadh', 'Sonipat', 'Sopore', 'Soro', 'Soron', 'South Dumdum', 'Soyagaon', 'Sri Ganganagar', 
		'Sri Madhopur', 'Srikakulam', 'Srikalahasti', 'Srinivaspur', 'Srirampore', 'Srisailam', 'Srivilliputhur', 
		'Suar', 'Sugauli', 'Sujangarh', 'Sujanpur', 'Sullurpeta', 'Sultan Pur Majra', 'Sultanganj', 'Sumerpur', 
		'Sunabeda', 'Sunam', 'Sundargarh', 'Sundarnagar', 'Supaul', 'Surandai', 'Surapura', 'Suratgarh', 
		'Surendranagar Dudhrej', 'Suri', 'Suriyampalayam', 'Suryapet', 'Tadepalligudem', 'Tadipatri', 'Takhatgarh', 
		'Taki', 'Talaja', 'Talcher', 'Talegaon', 'Talikota', 'Taliparamba', 'Talode', 'Talwara', 'Tamluk', 'Tanakpur', 
		'Tanda', 'Tandur', 'Tanuku', 'Tarakeswar', 'Tarana', 'Taranagar', 'Taraori', 'Tarbha', 'Tarikere', 'Tarn Taran', 
		'Tasgaon', 'Tehri', 'Tekkalakote', 'Tenali', 'Tenkasi', 'Tenu dam-cum-Kathhara', 'Terdal', 'Tezpur', 
		'Thakurdwara', 'Thammampatti', 'Thana Bhawan', 'Thane', 'Thangadh', 'Thanjavur', 'Tharad', 'Tharamangalam', 
		'Tharangambadi', 'Theni Allinagaram', 'Thirumangalam', 'Thirupuvanam', 'Thiruthuraipoondi', 'Thiruvalla', 
		'Thiruvallur', 'Thiruvarur', 'Thodupuzha', 'Thoothukudi', 'Thoubal', 'Thrippunithura', 'Thuraiyur', 'Tikamgarh', 
		'Tilda Newra', 'Tilhar', 'Tindivanam', 'Tinsukia', 'Tiptur', 'Tirora', 'Tiruchendur', 'Tiruchengode', 
		'Tiruchirapalli', 'Tirukalukundram', 'Tirukkoyilur', 'Tirupathur', 'Tirupati', 'Tirur', 'Tiruttani', 
		'Tiruvethipuram', 'Tiruvottiyur', 'Tiruvuru', 'Tirwaganj', 'Titlagarh', 'Tittakudi', 'Todabhim', 
		'Todaraisingh', 'Tohana', 'Tuensang', 'Tuljapur', 'Tulsipur', 'Tumkur', 'Tumsar', 'Tundla', 'Tuni', 'Tura', 
		'Uchgaon', 'Udaipur', 'Udaipurwati', 'Udhagamandalam', 'Udhampur', 'Udumalaipettai', 'Udupi', 'Ujhani', 
		'Ulhasnagar', 'Uluberia', 'Umarga', 'Umaria', 'Umarkhed', 'Umbergaon', 'Umred', 'Umreth', 'Una', 'Unjha', 
		'Unnamalaikadai', 'Unnao', 'Upleta', 'Uran', 'Uran Islampur', 'Uravakonda', 'Urmar Tanda', 'Usilampatti', 
		'Uthamapalayam', 'Uthiramerur', 'Utraula', 'Uttarakhand', 'Uttarkashi', 'Vadakkuvalliyur', 'Vadalur', 
		'Vadgaon Kasba', 'Vadipatti', 'Vadnagar', 'Vaijapur', 'Vaikom', 'Valparai', 'Vandavasi', 'Vaniyambadi', 
		'Vapi', 'Varandarappilly', 'Varkala', 'Vasai-Virar', 'Vatakara', 'Vedaranyam', 'Vellakoil', 'Venkatagiri', 
		'Vijainagar, Ajmer', 'Vijapur', 'Vijayanagaram', 'Vijaypur', 'Vikarabad', 'Vikasnagar', 'Vikramasingapuram', 
		'Viluppuram', 'Vinukonda', 'Viramgam', 'Virudhachalam', 'Virudhunagar', 'Vishakapatnam', 'Visnagar', 
		'Viswanatham', 'Vita', 'Vrindavan', 'Vyara', 'Wadgaon Road', 'Wadhwan', 'Wadi', 'Wai', 'Wanaparthy', 'Wani', 
		'Wankaner', 'Wara Seoni', 'Warhapur', 'Warisaliganj', 'Warora', 'Warud', 'Washim', 'Wokha', 'Yadgir', 
		'Yamunanagar', 'Yanam', 'Yawal', 'Yellandu', 'Yemmiganur', 'Yerraguntla', 'Yevla', 'Zaidpur', 'Zamania', 
		'Zira', 'Zirakpur', 'Zunheboto']

		valid_locs = ["Bangalore","Chennai","Delhi","Hyderabad","Kolkata","Mumbai",
			"Agra","Ajmer","Aligarh","Amravati","Amritsar","Asansol","Aurangabad","Ahmedabad","Allahabad",
			"Bareilly","Belgaum","Bhavnagar","Bhiwandi","Bhopal","Bhubaneswar","Bikaner","Bokaro Steel City",
			"Chandigarh","Coimbatore","nagpur","Cuttack",
			"Dehradun","Dhanbad","Durg-Bhilai Nagar","Durgapur","Erode","Faridabad","Firozabad",
			"Ghaziabad","Goa","Gorakhpur","Gulbarga","Guntur","Gurgaon","Guwahati","Gwalior",
			"Hubli-Dharwad","Indore","Jabalpur","Jaipur","Jalandhar","Jammu","Jamnagar","Jamshedpur","Jhansi","Jodhpur",
			"Kannur","Kanpur","Kakinada","Kochi","Kottayam","Kolhapur","Kollam","Kota","Kozhikode","Kurnool",
			"Lucknow","Ludhiana","Madurai","Malappuram","Mathura","Mangalore","Meerut","Moradabad","Mysore",
			"Nanded","Nashik","Nellore","Noida","Palakkad","Patna","Pondicherry","Prayagraj","Pune", 
			"Raipur","Rajkot","Rajahmundry","Ranchi","Rourkela",
			"Salem","Sangli","Siliguri","Solapur","Srinagar","Sultanpur","Surat",
			"Thiruvananthapuram","Thrissur","Tiruchirappalli","Tirunelveli","Tiruppur","Tiruvannamalai",
			"Ujjain","Bijapur","Vadodara","Varanasi","Vasai-Virar City","Vijayapura","Vijayawada","Visakhapatnam","Vellore","Warangal"]

		valid_locs = [name.casefold() for name in valid_locs]
		known_invalid_locs = [name.casefold() for name in known_invalid_locs]

		if loc.casefold() in valid_locs: 
			return [SlotSet('valid_location', True)]
		elif loc.casefold() in known_invalid_locs:
			dispatcher.utter_message("Sorry, we don't operate in that city.")
			# dispatcher.utter_template("utter_ask_alternate_city", tracker, domain)
			return [SlotSet('location', None), SlotSet('valid_location', False)]
		else:
			dispatcher.utter_message("Sorry, I couldn't find any such location.")
			# dispatcher.utter_template("utter_ask_alternate_city", tracker, domain)
			return [SlotSet('location', None), SlotSet('valid_location', None)]


class ResetSlot(Action):

    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("location", None), SlotSet("cuisine", None),
			SlotSet("budget", None), SlotSet("email", None), SlotSet("valid_location", False),
			SlotSet("search_results", None), SlotSet("found_results", None), SlotSet("email_sent", None)]

def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
		return {
				"location": self.from_text(intent=None),
			}	