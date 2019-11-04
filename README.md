# RasaBot
Rasabot for food recommendation system using zomato api's using Rasa NLU Framework.

Installation :

pip install rasa-x --extra-index-url https://pypi.rasa.com/simple

Packages versions:
Package version details are added in requirements.txt

Running action server : 
rasa run actions

Training the model:
rasa train

Running the command line bot:
rasa shell

Screenshots:
Sample screenshots present in screenshot folder

Note: 'SpacyNLP-en' might add to some delay in training and shell startup

For email :

In action server (actions.py), make the following changes in the below function

	class SendEmail(Action):
		msg['From']=""  # Enter Bots email address here
		server.login(msg['From'], "password") # Enter the password
