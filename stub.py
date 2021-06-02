#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from PIL import Image, ImageDraw, ImageFont
import uuid

UPLOAD_FOLDER = '/home/hoyd/Development/ticketstub'
#UPLOAD_FOLDER = '/var/www/apps/ticketstub'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['POST', 'GET'])
def createTicket():
    myname = "YOUR NAME HERE"
    mycolor = "orange"
    if request.method == "POST":
        try:
            myname = request.form.get('myname')
            if not myname:
                myname = "YOUR NAME HERE"
        except:
            error = "didn't work"
            myname = "YOUR NAME HERE"
        try:
            mycolor = request.form.get('mycolor')
            if not mycolor:
                mycolor = "orange"
        except:
            mycolor = "orange"

    ticket_name = myname #.upper()

    if mycolor == "orange":
        image = Image.open('ticket-stub-orange.png')
    elif mycolor == "green":
        image = Image.open('ticket-stub-green.png')    
    elif mycolor == "blue":
        image = Image.open('ticket-stub-blue.png')
    else:
        image = Image.open('ticket-stub-orange.png')
        
    draw = ImageDraw.Draw(image)
    font_name = ImageFont.truetype('fonts/Roboto-Regular.ttf', size=100, encoding="utf-8")

    # calculate the starting position of name
    name_start_pos = font_name.getsize(ticket_name)[0] / 2
    ticket_middle = 960 - name_start_pos

    if font_name.getsize(ticket_name)[0] <= 900:
        (x, y) = (ticket_middle, 550)
        color = 'rgb(255, 255, 255)'
        draw.text((x, y), ticket_name, fill=color, font=font_name)
    elif 900 < font_name.getsize(ticket_name)[0] < 1200:
        font_name = ImageFont.truetype('fonts/Roboto-Regular.ttf', size=80, encoding="utf-8")
        name_start_pos = font_name.getsize(ticket_name)[0] / 2
        ticket_middle = 960 - name_start_pos
        (x, y) = (ticket_middle, 550)
        color = 'rgb(255, 255, 255)'
        draw.text((x, y), ticket_name, fill=color, font=font_name)
    elif font_name.getsize(ticket_name)[0] >= 1200:
        font_name = ImageFont.truetype('fonts/Roboto-Regular.ttf', size=60, encoding="utf-8")
        name_start_pos = font_name.getsize(ticket_name)[0] / 2
        ticket_middle = 960 - name_start_pos
        (x, y) = (ticket_middle, 550)
        color = 'rgb(255, 255, 255)'
        draw.text((x, y), ticket_name, fill=color, font=font_name)

    stub_filename = 'stub-'+ uuid.uuid4().hex +'.png'

    # save the edited image
    image.save(stub_filename, optimize=True, quality=20)
    return render_template('index.html', stub_filename=stub_filename)


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)

