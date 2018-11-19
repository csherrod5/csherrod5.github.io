from flask import render_template, url_for, flash, redirect, request
from garbageRO import app, bcrypt, db
from garbageRO.forms import LoginForm, DumpsterForm, UpdateDumpsterForm
from garbageRO.models import Dumpster, Pickup, User
from flask_login import login_user, current_user, logout_user, login_required

#Boolean array
onRoute = [];
for dump in Dumpster.query.all():
	onRoute.append(dump.onRoute);

@app.route("/home")
@app.route("/")
def home():
	page = request.args.get('page', 1, type=int)
	dumpsters = Dumpster.query.paginate(page=page, per_page=5)
	all_dumpsters = Dumpster.query.all()
	return render_template('home.html', dumpsters=dumpsters, all_dumpsters=all_dumpsters)

@app.route("/pickup")
@login_required
def pickup():
	for dump in Dumpster.query.all():
		if dump.onRoute:
			pickup = Pickup(dumpster=dump)
			dump.full = False
			dump.onRoute = False
			db.session.add(pickup)
			db.session.commit()
	return redirect(url_for('home'))

@app.route("/history")
def history():
	page = request.args.get('page', 1, type=int)
	pickups = Pickup.query.order_by(Pickup.date.desc()).paginate(page=page, per_page=7)
	return render_template('pickupHistory.html', title='History', pickups=pickups, dumpsters=Dumpster.query.all())

@app.route("/history/<id>")
def filtered_history(id):
	page = request.args.get('page', 1, type=int)
	dump = Dumpster.query.get(id)
	pickups = Pickup.query.filter_by(dumpster=dump).order_by(Pickup.date.desc()).paginate(page=page, per_page=6)
	return render_template('pickupHistory.html', title='History', pickups=pickups, dumpsters=Dumpster.query.all())

@app.route("/history/<id>/delete", methods=['GET', 'POST'])
@login_required
def delete_pickup(id):
	pickup = Pickup.query.get_or_404(id)
	db.session.delete(pickup)
	db.session.commit()
	reassignArrayIDs(Pickup.query.all())
	return redirect(url_for('history'))

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = LoginForm()
	if form.validate_on_submit():
		#Currently, there is only one 'admin' user
		#This will change if there needs to be an account registration and login system
		user = User.query.first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=False)

			#If the user arrived at the login screen because they tried to access a restricted page, then redirect them to their desired page if they successfully log in
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Incorrect Password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/dumpster/toggle/<id>")
@login_required
def toggle_dumpster(id):
	dump = Dumpster.query.get(id)
	if dump:
		if dump.onRoute:
			dump.onRoute = False
		else:
			dump.onRoute = True
		db.session.commit()
	else: flash('That dumpster does not exist!', 'danger')
	return redirect(url_for('home'))

@app.route("/dumpster/new")
@login_required
def new_dumpster():
	#Every new dumpster is assumed to be empty and off the route by default
	dump = Dumpster(location="New Dumpster", full=False, onRoute=False, lat=30.612725, lng=-96.339578)
	db.session.add(dump)
	db.session.commit()
	flash("Successfully created new dumpster. Please update its name and location", 'success')
	return redirect(url_for('home'))

@app.route("/dumpster/<id>", methods=['GET', 'POST'])
@login_required
def update_dumpster(id):
	dump = Dumpster.query.get_or_404(id)
	form = UpdateDumpsterForm()
	if form.validate_on_submit():
		#Update the dumpster information
		dump.location = form.location.data
		dump.lat = form.lat.data
		dump.lng = form.lng.data
		dump.full = form.full.data
		db.session.commit()
		flash("Dumpster: '" + dump.location + "' successfully updated!", 'success')
		return redirect(url_for('home'))
	elif request.method == 'GET':
		#Load current dumpster data into the form fields
		form.location.data = dump.location
		form.lat.data = dump.lat
		form.lng.data = dump.lng
		form.full.data = dump.full
	return render_template('update_dumpster.html', title=dump.location, dumpster=dump, form=form)

@app.route("/dumpster/<id>/location")
@login_required
def update_dumpster_location(id):
	dump = Dumpster.query.get_or_404(id)
	return render_template('update_dumpster_location.html', title=dump.location, dumpster=dump)

@app.route("/dumpster/<id>/location/<lat>/<lng>", methods=['GET', 'POST'])
@login_required
def update_dumpster_latlng(id, lat, lng):
	dump = Dumpster.query.get_or_404(id)
	#Update the dumpster information
	dump.lat = lat
	dump.lng = lng
	db.session.commit()
	flash("Lattitude and Longitude values have been updated below. Click 'Update Dumpster' to finalize", 'secondary')
	return redirect(url_for('update_dumpster', id=dump.id))

@app.route("/dumpster/<id>/delete", methods=['POST'])
@login_required
def delete_dumpster(id):
	dump = Dumpster.query.get_or_404(id)
	db.session.delete(dump)
	db.session.commit()
	flash("Dumpster: '" + dump.location + "' successfully deleted!", 'success')
	reassignArrayIDs(Dumpster.query.all())
	return redirect(url_for('home'))

def reassignArrayIDs(array):
	i = 1
	for element in array:
		element.id = i
		db.session.commit()
		i = i + 1
