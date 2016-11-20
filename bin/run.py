from flask import Flask, request, redirect
from twilio import twiml
import os
import re
from twilio.rest import TwilioRestClient
from time import sleep

app = Flask(__name__)
caller_id = "YOUR_ID"
default_client = 'lendup'



twilio_client = TwilioRestClient(account='',
                              token='')

# add your Twilio phone number here
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '+12404398086')
# plug in your Ngrok Forwarding URL 
NGROK_BASE_URL = os.environ.get('NGROK_BASE_URL', 'https://lendbuzz-rkemburu.c9users.io:8080/')



@app.route("/", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = twiml.Response()

    # Start our <Gather> verb
    with resp.gather(finishOnKey="#", action='/gather') as gather:
        gather.say('Please enter a number, press pound when you are finished.')
    return str(resp)



@app.route('/gather', methods=['GET', 'POST'])
def gather():   
    """Processes results from the <Gather> prompt in /voice"""
    # Start our TwiML response
    resp = twiml.Response()

    # If Twilio's request to our app included already gathered digits,
    # process them

    if 'Digits' in request.values:
        # Get which digit the caller chose
        number = request.values['Digits']
        a = int(number)
        
        for x in xrange(a):
            if ((x+1) % 15 == 0):
                resp.say('FIZZBUZZ')
            elif ((x+1) % 3 == 0):
                resp.say('FIZZ')
            elif ((x+1) % 5 == 0):
                resp.say('BUZZ')
            else:
                resp.say(str(x+1))
    return str(resp)
    
@app.route('/dial-phone/<outbound_phone_number>/<delay>')
def outbound_call(outbound_phone_number, delay):
    
    """
        Uses the Twilio Python helper library to send a POST request to
        Twilio telling it to dial an outbound phone call from our specific
        Twilio phone number (that phone number must be owned by our
        Twilio account).
    """
    # the url must match the Ngrok Forwarding URL plus the route defined in
    # the previous function that responds with TwiML instructions
    
    print "LOG: CALL INITIATED TO  " + outbound_phone_number + " IN " + delay + " SECONDS "
    sleep(float(delay))
    print "LOG: CALL INITIATED TO  " + outbound_phone_number
    twilio_client.calls.create(to=outbound_phone_number, from_=caller_id,
                               url=NGROK_BASE_URL + '/twiml')
    return
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))