#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from PIL import Image, ImageDraw, ImageFont, ImageOps
import uuid
import random

UPLOAD_FOLDER = 'uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['POST', 'GET'])
def createTicket():
    myname = "YOUR NAME HERE"
    mycolor = "grey"
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
                mycolor = "grey"
        except:
            mycolor = "grey"

    ticket_name = myname #.upper()

    if mycolor == "orange":
        image = Image.open('static/ticket-stub-orange.png')
    elif mycolor == "blue":
        image = Image.open('static/ticket-stub-blue.png')    
    elif mycolor == "brown":
        image = Image.open('static/ticket-stub-brown.png')
    elif mycolor == "grey":
        image = Image.open('static/ticket-stub-grey.png')    
    elif mycolor == "green":
        image = Image.open('static/ticket-stub-green.png')
    elif mycolor == "pink":
        image = Image.open('static/ticket-stub-pink.png')    
    elif mycolor == "red":
        image = Image.open('static/ticket-stub-red.png')
    elif mycolor == "yellow":
        image = Image.open('static/ticket-stub-yellow.png')
    else:
        image = Image.open('static/ticket-stub-grey.png')
        
    draw = ImageDraw.Draw(image)
    font_name = ImageFont.truetype('fonts/Roboto-Italic.ttf', size=100, encoding="utf-8")

    # calculate the starting position of name and draw it
    name_start_pos = font_name.getsize(ticket_name)[0] / 2
    ticket_middle = 800 - name_start_pos

    if font_name.getsize(ticket_name)[0] <= 900:
        (x, y) = (ticket_middle, 450)
        color = 'rgb(255, 255, 255)'
        draw.text((x, y), ticket_name, fill=color, font=font_name)
    elif 900 < font_name.getsize(ticket_name)[0] < 1200:
        font_name = ImageFont.truetype('fonts/Roboto-Italic.ttf', size=80, encoding="utf-8")
        name_start_pos = font_name.getsize(ticket_name)[0] / 2
        ticket_middle = 800 - name_start_pos
        (x, y) = (ticket_middle, 450)
        color = 'rgb(255, 255, 255)'
        draw.text((x, y), ticket_name, fill=color, font=font_name)
    elif font_name.getsize(ticket_name)[0] >= 1200:
        font_name = ImageFont.truetype('fonts/Roboto-Italic.ttf', size=60, encoding="utf-8")
        name_start_pos = font_name.getsize(ticket_name)[0] / 2
        ticket_middle = 800 - name_start_pos
        (x, y) = (ticket_middle, 450)
        color = 'rgb(255, 255, 255)'
        draw.text((x, y), ticket_name, fill=color, font=font_name)


    # generate random ticket number and draw it
    rand_num = str(random.randrange(10**12, 10**13))
    font_name = ImageFont.truetype('fonts/Roboto-Regular.ttf', size=40, encoding="utf-8")
    rot_num = Image.new('L', (480, 50))
    draw2 = ImageDraw.Draw(rot_num)
    draw2.text((0, 0), str('T-'+rand_num), fill=255, font=font_name)
    rot_im = rot_num.rotate(90, expand=1)
    image.paste(ImageOps.colorize(rot_im, (0,0,0), (255,255,255)), (220,75), rot_im)

    # save the edited image with layers
    stub_filename = 'stub-'+ uuid.uuid4().hex +'.png'
    image.save(UPLOAD_FOLDER+stub_filename, optimize=True, quality=20)
    return render_template('index.html', stub_filename=stub_filename)


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)

