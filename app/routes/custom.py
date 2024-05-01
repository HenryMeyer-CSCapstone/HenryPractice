from app import app
from flask_login.utils import login_required
from flask import render_template, redirect, flash, url_for
from app.classes.data import CustomLine
from app.classes.forms import CustomLineForm
from flask_login import current_user
import datetime as dt

@app.route('/lines')
@login_required

def lines():
    lines = CustomLine.objects()
    return render_template("lines.html",lines=lines)

@app.route('/custom/<customLineId>')
@login_required

def custom(customLineId):
    thisCustomLine = CustomLine.objects.get(id=customLineId)
    return render_template("customline.html",customLine=thisCustomLine)

@app.route('/custom/create', methods=['GET','POST'])
@login_required
def customCreate():
    form = CustomLineForm()
    if form.validate_on_submit():
        currCustomLine = CustomLine(
            line = form.line.data,
            stations = form.stations.data,
            length = form.length.data,
            nightservice = form.nightservice.data,
            fstop = form.fstop.data,
            lstop = form.lstop.data,
            creator = current_user,
        )
        currCustomLine.save()
        return redirect(url_for('custom',customLineId=currCustomLine.id))

    return render_template('customlineform.html', form=form)

@app.route('/custom/edit/<customLineId>', methods=['GET','POST'])
@login_required
def lineEdit(customLineId):
    form = CustomLineForm()
    editLine = CustomLine.objects.get(id=customLineId)

    if editLine.creator != current_user:
        flash("You can't edit a sleep you don't own.")
        return redirect(url_for('lines'))
    
    if form.validate_on_submit():

        editLine.update(
            line = form.line.data,
            stations = form.stations.data,
            length = form.length.data,
            nightservice = form.nightservice.data,
            fstop = form.fstop.data,
            lstop = form.lstop.data,
            creator = current_user,
        )
        return redirect(url_for("custom",customLineId=editLine.id))
    
    form.line.data = editLine.line
    form.stations.data = editLine.stations
    form.length.data = editLine.length
    form.nightservice.data = editLine.nightservice
    form.fstop.data = editLine.fstop
    form.lstop.data = editLine.lstop
    return render_template("customlineform.html",form=form)

@app.route('/custom/delete/<customLineId>')
@login_required

def sleepDelete(customLineId):
    delCustom = CustomLine.objects.get(id=customLineId)
    delCustom.delete()
    flash(f"Your Custom Line has been deleted.")
    return redirect(url_for('lines'))