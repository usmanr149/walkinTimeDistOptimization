from flask import Flask, render_template, flash, request,redirect, url_for, jsonify
from flask_wtf import Form
from wtforms import validators, RadioField

from bs4 import BeautifulSoup
from urllib.request import urlopen
#import requests

# import things
from flask_table import Table, Col

import http.client

app = Flask(__name__)

app.secret_key = 'TEST'

class TestForm(Form):
    choice_switcher = RadioField(
        'Choice?',
        [validators.Required()],
        choices=[('Walk', 'Walk'), ('Transit', 'Transit')], default='Walk'
    )

@app.route('/getHospitalWaitTimes')
def getHospitalWaitTimes():
    url = "http://www12.albertahealthservices.ca/repacPublic/SnapShotController?direct=displayEdmonton"
    page = urlopen(url).read()
    soup = BeautifulSoup(page, "lxml")

    hospital_wait_times = {}
    for hit in soup.find_all("tr"):
        if len(hit.find_all("td", class_="publicRepacSiteCell")) > 0:
            time = ''
            # print(hit.find("td", class_="publicRepacSiteCell").text)
            for img in hit.find_all("img", attrs={"alt": True}):
                # print(img.get("alt"))
                time += img.get("alt")
            hospital_wait_times[hit.find("td", class_="publicRepacSiteCell").text] = time

    return hospital_wait_times

@app.route('/updateTimes')
def updateTimes(url="http://www12.albertahealthservices.ca/repacPublic/SnapShotController?direct=displayEdmonton"):
    page = urlopen(url).read()
    soup = BeautifulSoup(page, "lxml")
    now_time = soup.find_all("div", class_="publicRepacDate")[0].findAll(text=True)[1].replace("\n", "").replace("\r",
                                                                                                                 "").replace(
        " ", "")
    print("now time: " + str(now_time))
    hospital_wait_times = getHospitalWaitTimes()
    table = getHTML(hospital_wait_times)
    return jsonify(table=table, result=now_time)#, jsonify(result=now_time),

def getHTML(data):

    html = []
    for key, value in data.items():
        html.append("<tr>")
        html.append("<td> {0} </td>".format(key))
        html.append("<td> {0} </td>".format(value))
        html.append("</tr>")

    return "\n".join(html)

@app.route('/waitTimes')
def waitTimes(url="http://www12.albertahealthservices.ca/repacPublic/SnapShotController?direct=displayEdmonton"):
    page = urlopen(url).read()
    soup = BeautifulSoup(page)#, "lxml")
    now_time = soup.find_all("div", class_="publicRepacDate")[0].findAll(text=True)[1].replace("\n", "").replace("\r",
                                                                                                                 "").replace(
        " ", "")
    hospital_wait_times = getHTML(getHospitalWaitTimes())
    return render_template('waitTimes.html', table=hospital_wait_times, result=now_time)

@app.route('/getLastUpdateTime')
def getLastUpdateTime(url="http://www12.albertahealthservices.ca/repacPublic/SnapShotController?direct=displayEdmonton"):
    # query the website and get the time we last update the wait times
    time = request.args.get('time', 0, type=str)
    print("time : " + str(time))
    page = urlopen(url).read()
    soup = BeautifulSoup(page, "lxml")
    now_time = soup.find_all("div", class_="publicRepacDate")[0].findAll(text=True)[1].replace("\n", "").replace("\r",
                                                                                                                 "").replace(
        " ", "")
    return jsonify(result=now_time)

@app.route('/youtube',  methods=['GET', 'POST'])
def iframe():
    if request.method == "POST":
        flash('Hello ' + request.form['options'])
        #return redirect(url_for('iframe'))
    return render_template('layout.html')

@app.route('/radiobuttons')
def radiobuttons():
    testform = TestForm()

    #flash('Hello ' + testform.form['options'])

    return render_template('test_form.html', form=testform)

@app.route('/base')
def index():
    return render_template('addition.html')

@app.route('/getTime')
def getTime():
    return render_template('getTime.html')

@app.route('/hospitalWaitTimes')
def getWaitTimes():
    url = "http://www12.albertahealthservices.ca/repacPublic/SnapShotController?direct=displayEdmonton"
    page = urlopen(url).read()
    soup = BeautifulSoup(page, "lxml")

    print(type(getLastUpdateTime()))

    hospital_wait_times = {}
    for hit in soup.find_all("tr"):
        if len(hit.find_all("td", class_="publicRepacSiteCell")) > 0:
            time = ''
            #print(hit.find("td", class_="publicRepacSiteCell").text)
            for img in hit.find_all("img", attrs={"alt": True}):
                #print(img.get("alt"))
                time += img.get("alt")
            hospital_wait_times[hit.find("td", class_="publicRepacSiteCell").text] = time

    return render_template('getTimeAndWaitTimes.html', item = hospital_wait_times)

if __name__ == '__main__':
   app.run(debug=True)