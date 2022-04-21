#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 06:48:05 2022

@author: kerstin
"""

# Post Charging Mode: noCharging,immediateCharging,surplusCharging
# Post Modell Settings: 
#       SOC start
#       SOC end
#       hysteresisTime start
#       hysteresisTime end
# Post Anlage

# import main Flask class and request object
from flask import Flask, request
from config import Config

#http://localhost:5000/appSettings?chargingMode=1
#http://localhost:5000/appSettings?chargingMode=1&surplusTimeOn=474744747
#http://localhost:5000/facilitySettings?pVManufacturer=E3DC


# create the Flask app
app = Flask(__name__)

allowedModes = Config.allowedChargingModes
knownManufacturers = Config.pVManufacturer
pVManufacturerEndpoint = Config.pVManufacturerEndpoint
endpointsChargingApp = Config.endpointsChargingApp
endpointsFacility = Config.endpointsFacility
chargingModeEndpoint = Config.chargingModeEndpoint
socStartEndpoint = Config.socStartEndpoint
socStopEndpoint = Config.socStopEndpoint

def readEndpoints(endpoints):
    redEndpoints = {}
    for endpoint in endpoints:
        redEndpoints[endpoint] = request.args.get(endpoint)
    redEndpoints = {k: v for k, v in redEndpoints.items() if v is not None}
    return redEndpoints

@app.route('/facilitySettings')
def facilitySettings():
    redEndpoints = readEndpoints(endpointsFacility)
    returnString = {}
    for endpoint,value in redEndpoints.items():      
        if endpoint == pVManufacturerEndpoint:
            if value not in knownManufacturers:
                returnString[endpoint] = "This manufacturer is not known, please refer to list: {knownManufacturers}".format(knownManufacturers=knownManufacturers)
            else:
                # todo implement influx write here
                returnString[endpoint] =  "Your parameter {endpoint} is set to {value}".format(endpoint=endpoint,value=value)
        else:
            # todo implement influx write here
            returnString[endpoint] =  "Your parameter {endpoint} is set to {value}".format(endpoint=endpoint,value=value)
      
    return returnString

@app.route('/appSettings')
def appSettings():
    redEndpoints = readEndpoints(endpointsChargingApp)
    for endpoint,value in redEndpoints.items():
        try: 
            redEndpoints[endpoint] = int(value)
        except:
            redEndpoints[endpoint] = None
    returnString = {}
    for endpoint,value in redEndpoints.items():      
        if value is not None:
            if endpoint == chargingModeEndpoint:
                if value not in allowedModes:
                    returnString[endpoint] = "Please check boundary conditions for {endpoint}, the given value is not available. Possible values are {allowedModes}".format(endpoint=endpoint,allowedModes=allowedModes)
                else:
                    # todo implement influx write here
                    returnString[endpoint] =  "Your parameter {endpoint} is set to {value}".format(endpoint=endpoint,value=value)
            elif endpoint == socStartEndpoint or endpoint == socStopEndpoint:
                if value <0 or value>100:
                    returnString[endpoint] = "Please check boundary conditions for {endpoint}, the given value is not available. Possible values are 0 to 100".format(endpoint=endpoint,allowedModes=allowedModes)
                else:
                    # todo implement influx write here
                    returnString[endpoint] =  "Your parameter {endpoint} is set to {value}".format(endpoint=endpoint,value=value)
            else:
                # todo implement influx write here
                returnString[endpoint] =  "Your parameter {endpoint} is set to {value}".format(endpoint=endpoint,value=value)
        else:
            returnString[endpoint] = "Please check boundary conditions for {endpoint}".format(endpoint=endpoint)
    return returnString

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
