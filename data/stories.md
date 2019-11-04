## Simple stories
## Greet
* greet
    - utter_greet
    - export

## Greet and Goodbye
* greet
    - utter_greet
* goodbye
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Bye
* goodbye
    - utter_goodbye
    - action_reset_slot
    - export

## No Input
* 
    - utter_default
    - export

## No Input
* 
    - utter_default
* 
    - utter_default
* 
    - utter_default
    - export


## Generated Story 3610933134170833992
* greet
    - utter_greet
* search_restaurant
    - utter_ask_location
* search_restaurant{"location": "bangalore"}
    - slot{"location": "bangalore"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_cuisine
* search_restaurant{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_budget
* search_restaurant{"budget": ">1000"}
    - slot{"budget": ">1000"}
    - action_restaurant
    - slot{"search_results": "has_text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* send_details{"email": "somename@gmail.com"}
    - slot{"email": "abc@def.com"}
    - action_email
    - utter_goodbye
    - action_reset_slot
    - export

## Generated Story 388558728549701728
* greet
    - utter_greet
* search_restaurant{"location": "rishikesh"}
    - slot{"location": "rishikesh"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": false}
    - utter_ask_alternate_city
* search_restaurant{"location": "jaipur"}
    - slot{"location": "jaipur"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_cuisine
* search_restaurant{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_budget
* search_restaurant{"budget": ">1000"}
    - slot{"budget": ">1000"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* deny
    - utter_goodbye
    - action_reset_slot
    - export

## Generated Story 9189546364870490612
* greet
    - utter_greet
* search_restaurant{"location": "rishikesh"}
    - slot{"location": "rishikesh"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": false}
    - utter_ask_alternate_city
* search_restaurant{"location": "Delhi"}
    - slot{"location": "Delhi"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_cuisine
* search_restaurant{"cuisine": "Chinese"}
    - slot{"cuisine": "Chinese"}
    - utter_ask_budget
* search_restaurant{"budget": "<500"}
    - slot{"budget": "<500"}
    - action_restaurant
    - slot{"search_results": null}
    - slot{"found_results": false}
    - utter_ask_alternate_budget
* search_restaurant{"budget": "500-1000"}
    - slot{"budget": "500-1000"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export


## Generated Story 3819246282420587981
* greet
    - utter_greet
* search_restaurant{"location": "kolkata"}
    - slot{"location": "kolkata"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_cuisine
* search_restaurant{"cuisine": "american"}
    - slot{"cuisine": "american"}
    - utter_ask_budget
* search_restaurant{"budget": "500-1000"}
    - slot{"budget": "500-1000"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* affirm
    - utter_ask_email
* send_details{"email": "someone@yahoo.com"}
    - slot{"email": "someone@somewhere.com"}
    - action_email
    - slot{"email_sent": true}
    - utter_goodbye
    - action_reset_slot
    - export

## Generated Story 5952315894912500283
* greet
    - utter_greet
* search_restaurant
    - utter_ask_location
* search_restaurant{"location": "mubaim"}
    - slot{"location": "mubaim"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": null}
    - utter_ask_alternate_city
* search_restaurant{"location": "mumbai"}
    - slot{"location": "mumbai"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_cuisine
* search_restaurant{"cuisine": "american"}
    - slot{"cuisine": "american"}
    - utter_ask_budget
* search_restaurant{"budget": ">1000"}
    - slot{"budget": ">1000"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* affirm
    - utter_ask_email
* send_details{"email": "email@outlook.com"}
    - slot{"email": "email@someserver.com"}
    - action_email
    - slot{"email_sent": true}
    - utter_goodbye
    - action_reset_slot
    - export

## Generated Story -5001997364761453290
* greet
    - utter_greet
* search_restaurant{"cuisine": "chinese", "location": "chandigarh"}
    - slot{"cuisine": "chinese"}
    - slot{"location": "chandigarh"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_budget
* search_restaurant{"budget": ">1000"}
    - slot{"budget": ">1000"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* deny
    - utter_goodbye
    - action_reset_slot
    - export

## Not providing budget
* search_restaurant{"cuisine": "chinese", "location": "chandigarh"}
    - slot{"cuisine": "chinese"}
    - slot{"location": "chandigarh"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_budget
* 
    - utter_default
* 
    - utter_default
    - export


## Generated Story -4831472538080396003
* greet
    - utter_greet
* 
    - utter_default
* search_restaurant
    - utter_ask_location
* 
    - utter_default
* search_restaurant{"location": "pune"}
    - slot{"location": "pune"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_cuisine
* 
    - utter_default
* search_restaurant{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_budget
* 
    - utter_default
* search_restaurant{"budget": "500-1000"}
    - slot{"budget": "500-1000"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": false}
    - utter_ask_alternate_budget
* search_restaurant{"budget": ">1000"}
    - slot{"budget": ">1000"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* deny
    - utter_goodbye
    - action_reset_slot
    - export

## Generated Story 5286903957715011224
* greet
    - utter_greet
* search_restaurant
    - utter_ask_location
* search_restaurant{"location": "Bangalore"}
    - slot{"location": "Bangalore"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_cuisine
* search_restaurant{"cuisine": "south indian"}
    - slot{"cuisine": "south indian"}
    - utter_ask_budget
* search_restaurant{"budget": "500-1000"}
    - slot{"budget": "500-1000"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": false}
    - utter_ask_alternate_budget
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Generated Story 7916779628815241742
* greet
    - utter_greet
* search_restaurant{"cuisine": "chinese", "location": "chandigarh"}
    - slot{"cuisine": "chinese"}
    - slot{"location": "chandigarh"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_budget
* search_restaurant{"budget": "<500"}
    - slot{"budget": "<500"}
    - action_restaurant
    - slot{"search_results": null}
    - slot{"found_results": false}
    - utter_ask_alternate_budget
* search_restaurant{"budget": ">1000"}
    - slot{"budget": ">1000"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Generated Story -3333502339638337872
* greet
    - utter_greet
* search_restaurant{"cuisine": "chinese", "location": "chandigarh", "budget": "<500"}
    - slot{"budget": "<500"}
    - slot{"cuisine": "chinese"}
    - slot{"location": "chandigarh"}
    - action_validate_location
    - slot{"valid_location": true}
    - action_restaurant
    - slot{"search_results": null}
    - slot{"found_results": false}
    - utter_ask_alternate_budget
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Generated Story 5699950204708172850
* greet
    - utter_greet
* search_restaurant
    - utter_ask_location
* search_restaurant
    - utter_default
* search_restaurant{"location": "Delhi"}
    - slot{"location": "Delhi"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_cuisine
* search_restaurant
    - utter_default
* search_restaurant{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_budget
* search_restaurant{"budget": "<500"}
    - slot{"budget": "<500"}
    - action_restaurant
    - slot{"search_results": null}
    - slot{"found_results": false}
    - utter_ask_alternate_budget
* search_restaurant{"budget": "500-1000"}
    - slot{"budget": "500-1000"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* affirm
    - utter_ask_email
* send_details{"email": "help@me.com"}
    - slot{"email": "help@me.com"}
    - action_email
    - slot{"email_sent": true}
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Generated Story -2373924488948642431
* greet
    - utter_greet
* search_restaurant{"cuisine": "italian", "location": "Mumbai", "budget": "<500"}
    - slot{"budget": "<500"}
    - slot{"cuisine": "italian"}
    - slot{"location": "Mumbai"}
    - action_validate_location
    - slot{"valid_location": true}
    - action_restaurant
    - slot{"search_results": null}
    - slot{"found_results": false}
    - utter_ask_alternate_budget
* search_restaurant{"budget": "500-1000"}
    - slot{"budget": "500-1000"}
    - action_restaurant
    - slot{"search_results": null}
    - slot{"found_results": false}
    - utter_ask_alternate_budget
* search_restaurant{"budget": "<500"}
    - slot{"budget": "<500"}
    - action_restaurant
    - slot{"search_results": null}
    - slot{"found_results": false}
    - utter_ask_alternate_budget
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Generated Story 6061993100952186407
* greet
    - utter_greet
* search_restaurant{"budget": "<500", "cuisine": "Mexican"}
    - slot{"budget": "<500"}
    - slot{"cuisine": "Mexican"}
    - utter_ask_location
* search_restaurant{"location": "Chennai"}
    - slot{"location": "Chennai"}
    - action_validate_location
    - slot{"valid_location": true}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Generated Story 5850808719902654095
* greet
    - utter_greet
* search_restaurant{"budget": ">1000", "cuisine": "italian", "location": "gurgaon"}
    - slot{"budget": ">1000"}
    - slot{"cuisine": "italian"}
    - slot{"location": "gurgaon"}
    - action_validate_location
    - slot{"valid_location": true}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Generated Story 6061993100952186407
* greet
    - utter_greet
* search_restaurant{"budget": "<500", "cuisine": "Mexican"}
    - slot{"budget": "<500"}
    - slot{"cuisine": "Mexican"}
    - utter_ask_location
* search_restaurant{"location": "Chennai"}
    - slot{"location": "Chennai"}
    - action_validate_location
    - slot{"valid_location": true}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Generated Story 5203668936517469404
* greet
    - utter_greet
* search_restaurant
    - utter_ask_location
* search_restaurant{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_location
* search_restaurant{"location": "Jaipur"}
    - slot{"location": "Jaipur"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_budget
* search_restaurant{"budget": "<500"}
    - slot{"budget": "<500"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Generated Story 3800648596020791957
* greet
    - utter_greet
* search_restaurant{"location": "almora"}
    - slot{"location": "almora"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": false}
    - utter_ask_alternate_city
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
* greet
    - utter_greet
* search_restaurant{"location": "paris"}
    - slot{"location": "paris"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": null}
    - utter_ask_alternate_city
* search_restaurant{"location": "hyderabad"}
    - slot{"location": "hyderabad"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_cuisine
* search_restaurant{"cuisine": "south indian"}
    - slot{"cuisine": "south indian"}
    - utter_ask_budget
* search_restaurant{"budget": "<500"}
    - slot{"budget": "<500"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Generated Story 2508725302789212799
* search_restaurant{"location": "shimla"}
    - slot{"location": "shimla"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": false}
    - utter_ask_alternate_city
* search_restaurant{"location": "srinagar"}
    - slot{"location": "srinagar"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_cuisine
* search_restaurant{"cuisine": "american"}
    - slot{"cuisine": "american"}
    - utter_ask_budget
* search_restaurant{"budget": ">1000"}
    - slot{"budget": ">1000"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* affirm
    - utter_ask_email
* send_details{"email": "abc@def.com"}
    - slot{"email": "abc@def.com"}
    - action_email
    - slot{"email_sent": true}
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
* search_restaurant{"location": "rourkela"}
    - slot{"location": "rourkela"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_cuisine
* search_restaurant{"cuisine": "south indian"}
    - slot{"cuisine": "south indian"}
    - utter_ask_budget
* search_restaurant{"budget": "500-1000"}
    - slot{"budget": "500-1000"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Generated Story -6156717076256734887
* search_restaurant{"cuisine": "Italian", "location": "panaji"}
    - slot{"cuisine": "Italian"}
    - slot{"location": "panaji"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": false}
    - utter_ask_alternate_city
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
* search_restaurant{"cuisine": "Mexican", "location": "panaji"}
    - slot{"cuisine": "Mexican"}
    - slot{"location": "panaji"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": false}
    - utter_ask_alternate_city
* affirm
    - utter_ask_location
* search_restaurant{"location": "goa"}
    - slot{"location": "goa"}
    - action_validate_location
    - slot{"valid_location": true}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Generated Story -9108298330462338250
* search_restaurant{"location": "alwar"}
    - slot{"location": "alwar"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": false}
    - utter_ask_alternate_city
* affirm
    - utter_ask_location
* search_restaurant{"location": "ajmer"}
    - slot{"location": "ajmer"}
    - action_validate_location
    - slot{"valid_location": true}
    - utter_ask_cuisine
* search_restaurant{"cuisine": "Chinese"}
    - slot{"cuisine": "Chinese"}
    - utter_ask_budget
* search_restaurant{"budget": "<500"}
    - slot{"budget": "<500"}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* affirm
    - utter_ask_email
* send_details{"email": "rasabot@gmail.com"}
    - slot{"email": "rasabot@gmail.com"}
    - action_email
    - slot{"email_sent": true}
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Generated Story 6153973767140398492
* search_restaurant{"budget": "<500", "location": "Alwar"}
    - slot{"budget": "<500"}
    - slot{"location": "Alwar"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": false}
    - utter_ask_alternate_city
* search_restaurant{"location": "ajmer"}
    - slot{"location": "ajmer"}
    - action_validate_location
    - slot{"valid_location": true}
    - action_restaurant
    - slot{"search_results": "text"}
    - slot{"found_results": true}
    - utter_query_ask_email
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
* search_restaurant{"location": "seattle"}
    - slot{"location": "seattle"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": null}
    - utter_ask_alternate_city
* search_restaurant{"location": "bharatpur"}
    - slot{"location": "bharatpur"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": false}
    - utter_ask_alternate_city
* search_restaurant{"location": "singapore"}
    - slot{"location": "singapore"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": null}
    - utter_ask_alternate_city
* search_restaurant{"location": "bhilai"}
    - slot{"location": "bhilai"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": false}
    - utter_ask_alternate_city
* search_restaurant{"budget": ">1000", "location": "london"}
    - slot{"budget": ">1000"}
    - slot{"location": "london"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": null}
    - utter_ask_alternate_city
* search_restaurant{"budget": "500-1000", "location": "austin"}
    - slot{"budget": "500-1000"}
    - slot{"location": "austin"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": null}
    - utter_ask_alternate_city
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Handwritten story 1 
* search_restaurant{"budget": ">1000", "location": "seattle"}
    - slot{"budget": ">1000"}
    - slot{"location": "seattle"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": null}
    - utter_ask_alternate_city
* search_restaurant{"location": "bharatpur"}
    - slot{"location": "bharatpur"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": false}
    - utter_ask_alternate_city
* search_restaurant{"location": "singapore"}
    - slot{"location": "singapore"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": null}
    - utter_ask_alternate_city
* search_restaurant{"location": "bhilai"}
    - slot{"location": "bhilai"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": false}
    - utter_ask_alternate_city
* search_restaurant{"budget": ">1000", "location": "london"}
    - slot{"budget": ">1000"}
    - slot{"location": "london"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": null}
    - utter_ask_alternate_city
* search_restaurant{"budget": "500-1000", "location": "austin"}
    - slot{"budget": "500-1000"}
    - slot{"location": "austin"}
    - action_validate_location
    - slot{"location": null}
    - slot{"valid_location": null}
    - utter_ask_alternate_city
* deny
    - utter_goodbye
    - action_reset_slot
    - slot{"location": null}
    - slot{"cuisine": null}
    - slot{"budget": null}
    - slot{"email": null}
    - slot{"valid_location": false}
    - slot{"search_results": null}
    - slot{"found_results": null}
    - slot{"email_sent": null}
    - export

## Thank you
* thankyou
	- utter_thankyou