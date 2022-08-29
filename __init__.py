from flask import Flask, render_template, request, redirect, url_for, flash, session
from Forms import *
import shelve, User, Email, MealCombination, AddToCart, Order
#Login mail@mail.com
#password 12345

#Login2 nomail@mail.com
#password2 54321

app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('home.html')

@app.route('/')
def home():
    if 'user' in session:
        user = session['user']
        user = user[1]
        return render_template('home.html', first_name=user)
    else:
        return render_template('home.html')

# Ulys
@app.route('/faq')
def FAQ():
    return render_template('faq.html')

@app.route('/aboutUs')
def about_us():
    return render_template('aboutUs.html')

@app.route('/returnHome')
def return_home():
    return render_template('returnHome.html')

@app.route('/contactUs',methods=['GET','POST'])
def contact_us():
    create_email_form = CreateEmailForm(request.form)
    if request.method == 'POST' and create_email_form.validate():
        email_dict = {}
        db = shelve.open('storage.db','c')

        try:
            email_dict = db['Emails']
        except:
            print("Error in retrieving Emails from storage.db.")


        email_id = len(email_dict) +1
        email = Email.Email(email_id,name=create_email_form.name.data, email=create_email_form.email.data, subject=create_email_form.subject.data, message=create_email_form.message.data )
        # email = Email.Email(create_email_form.name.data, create_email_form.email.data, create_email_form.subject.data, create_email_form.message.data )
        email_dict[email.get_email_id()] = email
        db['Emails'] = email_dict


        db.close()

        return redirect(url_for('return_home'))
    return render_template('contactUs.html', form=create_email_form)

@app.route('/emails')
def emails():
    email_dict = {}
    db = shelve.open('storage.db', 'r')
    email_dict = db['Emails']
    db.close()

    emails_list =[]
    for key in email_dict:
        emails = email_dict.get(key)
        emails_list.append(emails)

    return render_template('emails.html', count=len(emails_list), emails_list=emails_list)


@app.route('/editEmail/<int:id>/', methods=['GET', 'POST'])
def edit_email(id):
    edit_email_form = CreateEmailForm(request.form)
    if request.method == 'POST' and edit_email_form.validate():
        email_dict = {}
        db = shelve.open('storage.db', 'w')
        email_dict = db['Emails']

        emails = email_dict.get(id)
        emails.set_name(edit_email_form.name.data)
        emails.set_email(edit_email_form.email.data)
        emails.set_subject(edit_email_form.subject.data)
        emails.set_message(edit_email_form.message.data)


        db['Emails'] = email_dict
        db.close()

        return redirect(url_for('emails'))
    else:
        email_dict = {}
        db = shelve.open('storage.db', 'r')
        email_dict = db['Emails']
        db.close()

        emails = email_dict.get(id)
        edit_email_form.name.data = emails.get_name()
        edit_email_form.email.data = emails.get_email()
        edit_email_form.subject.data = emails.get_subject()
        edit_email_form.message.data = emails.get_message()

        return render_template('editEmail.html', form=edit_email_form)

@app.route('/deleteEmail/<int:id>', methods=['POST'])
def delete_email(id):
    email_dict = {}
    db = shelve.open('storage.db', 'w')
    email_dict = db['Emails']

    email_dict.pop(id)

    db['Emails'] = email_dict
    db.close()

    return redirect(url_for('emails'))



# __________________________________________________________________________

# JiaJun
# Staff pages
@app.route('/stafflogin', methods=['GET', 'POST'])
def stafflogin():

    form = LogIn(request.form)
    if request.method == 'POST' and form.validate():
        if form.email.data == "staff@account" and form.password.data == 'staffpass':
            flash('Log in successfully!', 'success')
            session['staff'] = 'staff'
            return redirect(url_for("home"))
        else:
            flash('Log in unsuccessful, please try again!','danger')
    return render_template('stafflogin.html', title='Login', form=form)

@app.route('/accounts')
def accounts():
    accounts_dict = {}
    db = shelve.open('storage.db', 'r')
    accounts_dict = db['Users']
    db.close()

    accounts_list = []
    for key in accounts_dict:
        user = accounts_dict.get(key)
        accounts_list.append(user)

    return render_template('accounts.html', count=len(accounts_list), users_list=accounts_list)

#  Customer pages
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        accounts_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            accounts_dict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        user = User.User(create_user_form.first_name.data, create_user_form.last_name.data, create_user_form.birthday.data, create_user_form.gender.data, create_user_form.email.data, create_user_form.phone_number.data, create_user_form.password.data)
        accounts_dict[user.get_user_id()] = user
        db['Users'] = accounts_dict
        db.close()
        # flash(f'Account Created Successfully for {create_user_form.first_name.data}', category='success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=create_user_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    users_dict = {}
    db = shelve.open('storage.db','r')
    users_dict = db['Users']
    users_list = []

    # If there is no account in database, direct user to signup page
    if users_dict == {}:
        return redirect(url_for('signup'))

    else:
        for key in users_dict:
            user = users_dict.get(key)
            print(key)
            users_list.append(user)
            form = LogIn(request.form)
            if request.method == 'POST' and form.validate():
                for user in users_list:
                    if form.email.data == user.get_email() and form.password.data == user.get_password():
                        flash('Log in successfully!', 'success')

                        id = user.get_user_id()
                        first_name = user.get_first_name()
                        last_name = user.get_last_name()
                        birthday = user.get_birthday()
                        gender = user.get_gender()
                        email = user.get_email()
                        phone_number = user.get_phone_number()
                        password = user.get_password()

                        user_details = [id, first_name,last_name,birthday,gender,email,phone_number,password]
                        session['user'] = user_details

                        return redirect(url_for("home"))
                    else:
                        if "user" in session:
                            return render_template('login.html')
                        flash('Log in unsuccessful, please try again!','danger')
    return render_template('login.html', title='Login', form=form)


# Customer have to log out after logging in their account
# One disadvantage is customer have to logout of their account to see their edits
@app.route('/customer_profile', methods = ['GET', 'POST'])
def customer_profile():
    if 'user' in session:
        user = session["user"]
        accounts_list = user[1:8]
        id = user[0]
        return render_template('customer_profile.html', accounts_list=accounts_list, id=id)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("staff", None)
    cart_dict = {}
    db = shelve.open('storage.db', 'c')
    cart_dict = db['Cart']
    cart_dict.clear()
    db['Cart'] = cart_dict
    db.close()

    return redirect(url_for('login'))


@app.route('/customer_update/<int:id>/', methods=['GET', 'POST'])
def customer_update(id):
    if 'user' in session:

        update_user_form = CreateUserForm(request.form)
        if request.method == 'POST' and update_user_form.validate():
            accounts_dict = {}
            db = shelve.open('storage.db', 'w')
            accounts_dict = db['Users']
            user = accounts_dict.get(id)
            user.set_first_name(update_user_form.first_name.data)
            user.set_last_name(update_user_form.last_name.data)
            user.set_birthday(update_user_form.birthday.data)
            user.set_gender(update_user_form.gender.data)
            user.set_email(update_user_form.email.data)
            user.set_phone_number(update_user_form.phone_number.data)
            user.set_password(update_user_form.password.data)
            # Update session's new list to show on customer's profile
            id = user.get_user_id()
            first_name = user.get_first_name()
            last_name = user.get_last_name()
            birthday = user.get_birthday()
            gender = user.get_gender()
            email = user.get_email()
            phone_number = user.get_phone_number()
            password = user.get_password()
            session['user'] = [id,first_name,last_name,birthday,gender,email,phone_number,password]
            # Update new details to the database
            db['Users'] = accounts_dict
            db.close()
            return redirect(url_for('customer_profile'))
        else:
            accounts_dict = {}
            db = shelve.open('storage.db', 'r')
            accounts_dict = db['Users']
            db.close()
            user = accounts_dict.get(id)
            update_user_form.first_name.data = user.get_first_name()
            update_user_form.last_name.data = user.get_last_name()
            update_user_form.birthday.data = user.get_birthday()
            update_user_form.gender.data = user.get_gender()
            update_user_form.email.data = user.get_email()
            update_user_form.phone_number.data = user.get_phone_number()
            update_user_form.password.data = user.get_password()
        return render_template('account.html', form=update_user_form)
    else:
        return redirect(url_for('login'))

@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        accounts_dict = {}
        db = shelve.open('storage.db', 'w')
        accounts_dict = db['Users']

        user = accounts_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_birthday(update_user_form.birthday.data)
        user.set_gender(update_user_form.gender.data)
        user.set_email(update_user_form.email.data)
        user.set_phone_number(update_user_form.phone_number.data)
        user.set_password(update_user_form.password.data)

        db['Users'] = accounts_dict
        db.close()

        return redirect(url_for('accounts'))
    else:
        accounts_dict = {}
        db = shelve.open('storage.db', 'r')
        accounts_dict = db['Users']
        db.close()

        user = accounts_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.birthday.data = user.get_birthday()
        update_user_form.gender.data = user.get_gender()
        update_user_form.email.data = user.get_email()
        update_user_form.phone_number.data = user.get_phone_number()
        update_user_form.password.data = user.get_password()

    return render_template('account.html', form=update_user_form)

@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('storage.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    if 'user' in session:
        return redirect(url_for('logout'))
    elif 'staff' in session:
        return redirect(url_for('accounts'))

    return redirect(url_for('logout'))


app.config['SECRET_KEY'] = "Yammy_key"


# __________________________________________________________________________
# Terruce
# Transaction processing

@app.route('/meal_combination',methods=['GET', 'POST'])
def meal_combination():

    if 'user' in session:

        create_meal_combination = CreateMealCombination(request.form)
        if request.method == 'POST':

            temp_mealcombination = {}
            db = shelve.open('storage.db', 'c')

            try:
                temp_mealcombination = db['Meal_Combination']
            except:
                print("Error in retrieving MealCombination from storage.db.")

            meal_combination = MealCombination.MealCombination(
                create_meal_combination.preference.data,
                create_meal_combination.combination.data
            )

            temp_mealcombination[meal_combination.get_meal_combination_id()] = meal_combination
            db['Meal_Combination'] = temp_mealcombination

            db.close()

            combination_list = []
            for key in temp_mealcombination:
                combination = temp_mealcombination.get(key)
                combination_list.append(combination)

            if combination_list[0].get_preference() == 'Low Carb':
                return redirect(url_for('addtocartlowcarb'))
            elif combination_list[0].get_preference() == 'Muscle Building':
                return redirect(url_for('addtocartmusclebuilding'))
            elif combination_list[0].get_preference() == 'Vegetarian':
                return redirect(url_for('addtocartvegetarian'))
        return render_template('meal_combination.html', form=create_meal_combination)
    else:
         return redirect(url_for('login'))


@app.route('/LowCarb', methods=['GET', 'POST'])
def addtocartlowcarb():
    temp_mealcombination = {}
    db = shelve.open('storage.db', 'r')
    temp_mealcombination = db['Meal_Combination']
    db.close()

    combination_list = []
    for key in temp_mealcombination:
        combination = temp_mealcombination.get(key)
        combination_list.append(combination)

    if MealCombination.MealCombination.get_combination(combination_list[0])=='All':
        add_to_cart_low_carb = AddShoppingCartAll_LowCarb(request.form)
        if request.method == 'POST':

            cart_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                cart_dict = db['Cart']
            except:
                print("Error in retrieving Cart from storage.db.")

            cart = AddToCart.AddToCart(
                add_to_cart_low_carb.Preference.data,
                add_to_cart_low_carb.Combination.data,
                add_to_cart_low_carb.MondayB.data,
                add_to_cart_low_carb.MondayL.data,
                add_to_cart_low_carb.MondayD.data,
                add_to_cart_low_carb.TuesdayB.data,
                add_to_cart_low_carb.TuesdayL.data,
                add_to_cart_low_carb.TuesdayD.data,
                add_to_cart_low_carb.WednesdayB.data,
                add_to_cart_low_carb.WednesdayL.data,
                add_to_cart_low_carb.WednesdayD.data,
                add_to_cart_low_carb.ThursdayB.data,
                add_to_cart_low_carb.ThursdayL.data,
                add_to_cart_low_carb.ThursdayD.data,
                add_to_cart_low_carb.FridayB.data,
                add_to_cart_low_carb.FridayL.data,
                add_to_cart_low_carb.FridayD.data)


            cart_dict[cart.get_cart_id()] = cart
            db['Cart'] = cart_dict

            db.close()

            return redirect(url_for('cart'))
        return render_template('LowCarb.html', form = add_to_cart_low_carb,combination_list=combination_list)

    elif MealCombination.MealCombination.get_combination(combination_list[0])=='L&D':
        add_to_cart_low_carb = AddShoppingCartNoBreakfast_LowCarb(request.form)
        if request.method == 'POST':

            cart_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                cart_dict = db['Cart']
            except:
                print("Error in retrieving Cart from storage.db.")


            cart = AddToCart.AddToCart(
                add_to_cart_low_carb.Preference.data,
                add_to_cart_low_carb.Combination.data,
                add_to_cart_low_carb.MondayB.data,
                add_to_cart_low_carb.MondayL.data,
                add_to_cart_low_carb.MondayD.data,
                add_to_cart_low_carb.TuesdayB.data,
                add_to_cart_low_carb.TuesdayL.data,
                add_to_cart_low_carb.TuesdayD.data,
                add_to_cart_low_carb.WednesdayB.data,
                add_to_cart_low_carb.WednesdayL.data,
                add_to_cart_low_carb.WednesdayD.data,
                add_to_cart_low_carb.ThursdayB.data,
                add_to_cart_low_carb.ThursdayL.data,
                add_to_cart_low_carb.ThursdayD.data,
                add_to_cart_low_carb.FridayB.data,
                add_to_cart_low_carb.FridayL.data,
                add_to_cart_low_carb.FridayD.data)

            cart_dict[cart.get_cart_id()] = cart
            db['Cart'] = cart_dict

            db.close()

            return redirect(url_for('cart'))
        return render_template('LowCarb.html', form=add_to_cart_low_carb, combination_list=combination_list)


@app.route('/MuscleBuilding', methods=['GET', 'POST'])
def addtocartmusclebuilding():
    temp_mealcombination = {}
    db = shelve.open('storage.db', 'r')
    temp_mealcombination = db['Meal_Combination']
    db.close()

    combination_list = []
    for key in temp_mealcombination:
        combination = temp_mealcombination.get(key)
        combination_list.append(combination)

    if MealCombination.MealCombination.get_combination(combination_list[0])=='All':
        add_to_cart_muscle_building = AddShoppingCartAll_MuscleBuilding(request.form)
        if request.method == 'POST':

            cart_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                cart_dict = db['Cart']
            except:
                print("Error in retrieving Cart from storage.db.")


            cart = AddToCart.AddToCart(
                add_to_cart_muscle_building.Preference.data,
                add_to_cart_muscle_building.Combination.data,
                add_to_cart_muscle_building.MondayB.data,
                add_to_cart_muscle_building.MondayL.data,
                add_to_cart_muscle_building.MondayD.data,
                add_to_cart_muscle_building.TuesdayB.data,
                add_to_cart_muscle_building.TuesdayL.data,
                add_to_cart_muscle_building.TuesdayD.data,
                add_to_cart_muscle_building.WednesdayB.data,
                add_to_cart_muscle_building.WednesdayL.data,
                add_to_cart_muscle_building.WednesdayD.data,
                add_to_cart_muscle_building.ThursdayB.data,
                add_to_cart_muscle_building.ThursdayL.data,
                add_to_cart_muscle_building.ThursdayD.data,
                add_to_cart_muscle_building.FridayB.data,
                add_to_cart_muscle_building.FridayL.data,
                add_to_cart_muscle_building.FridayD.data)


            cart_dict[cart.get_cart_id()] = cart
            db['Cart'] = cart_dict

            db.close()

            return redirect(url_for('cart'))
        return render_template('MuscleBuilding.html', form = add_to_cart_muscle_building,combination_list=combination_list)

    elif MealCombination.MealCombination.get_combination(combination_list[0])=='L&D':
        add_to_cart_muscle_building = AddShoppingCartNoBreakfast_MuscleBuilding(request.form)
        if request.method == 'POST':

            cart_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                cart_dict = db['Cart']
            except:
                print("Error in retrieving Cart from storage.db.")


            cart = AddToCart.AddToCart(
                add_to_cart_muscle_building.Preference.data,
                add_to_cart_muscle_building.Combination.data,
                add_to_cart_muscle_building.MondayB.data,
                add_to_cart_muscle_building.MondayL.data,
                add_to_cart_muscle_building.MondayD.data,
                add_to_cart_muscle_building.TuesdayB.data,
                add_to_cart_muscle_building.TuesdayL.data,
                add_to_cart_muscle_building.TuesdayD.data,
                add_to_cart_muscle_building.WednesdayB.data,
                add_to_cart_muscle_building.WednesdayL.data,
                add_to_cart_muscle_building.WednesdayD.data,
                add_to_cart_muscle_building.ThursdayB.data,
                add_to_cart_muscle_building.ThursdayL.data,
                add_to_cart_muscle_building.ThursdayD.data,
                add_to_cart_muscle_building.FridayB.data,
                add_to_cart_muscle_building.FridayL.data,
                add_to_cart_muscle_building.FridayD.data)

            cart_dict[cart.get_cart_id()] = cart
            db['Cart'] = cart_dict

            db.close()

            return redirect(url_for('cart'))
        return render_template('MuscleBuilding.html', form=add_to_cart_muscle_building, combination_list=combination_list)

@app.route('/Vegetarian', methods=['GET', 'POST'])
def addtocartvegetarian():
    temp_mealcombination = {}
    db = shelve.open('storage.db', 'r')
    temp_mealcombination = db['Meal_Combination']
    db.close()

    combination_list = []
    for key in temp_mealcombination:
        combination = temp_mealcombination.get(key)
        combination_list.append(combination)

    if MealCombination.MealCombination.get_combination(combination_list[0])=='All':
        add_to_cart_vegetarian = AddShoppingCartAll_Vegetarian(request.form)
        if request.method == 'POST':

            cart_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                cart_dict = db['Cart']
            except:
                print("Error in retrieving Cart from storage.db.")


            cart = AddToCart.AddToCart(
                add_to_cart_vegetarian.Preference.data,
                add_to_cart_vegetarian.Combination.data,
                add_to_cart_vegetarian.MondayB.data,
                add_to_cart_vegetarian.MondayL.data,
                add_to_cart_vegetarian.MondayD.data,
                add_to_cart_vegetarian.TuesdayB.data,
                add_to_cart_vegetarian.TuesdayL.data,
                add_to_cart_vegetarian.TuesdayD.data,
                add_to_cart_vegetarian.WednesdayB.data,
                add_to_cart_vegetarian.WednesdayL.data,
                add_to_cart_vegetarian.WednesdayD.data,
                add_to_cart_vegetarian.ThursdayB.data,
                add_to_cart_vegetarian.ThursdayL.data,
                add_to_cart_vegetarian.ThursdayD.data,
                add_to_cart_vegetarian.FridayB.data,
                add_to_cart_vegetarian.FridayL.data,
                add_to_cart_vegetarian.FridayD.data)


            cart_dict[cart.get_cart_id()] = cart
            db['Cart'] = cart_dict

            db.close()

            return redirect(url_for('cart'))
        return render_template('Vegetarian.html', form = add_to_cart_vegetarian, combination_list=combination_list)

    elif MealCombination.MealCombination.get_combination(combination_list[0])=='L&D':
        add_to_cart_vegetarian = AddShoppingCartNoBreakfast_Vegetarian(request.form)
        if request.method == 'POST':

            cart_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                cart_dict = db['Cart']
            except:
                print("Error in retrieving Cart from storage.db.")


            cart = AddToCart.AddToCart(
                add_to_cart_vegetarian.Preference.data,
                add_to_cart_vegetarian.Combination.data,
                add_to_cart_vegetarian.MondayB.data,
                add_to_cart_vegetarian.MondayL.data,
                add_to_cart_vegetarian.MondayD.data,
                add_to_cart_vegetarian.TuesdayB.data,
                add_to_cart_vegetarian.TuesdayL.data,
                add_to_cart_vegetarian.TuesdayD.data,
                add_to_cart_vegetarian.WednesdayB.data,
                add_to_cart_vegetarian.WednesdayL.data,
                add_to_cart_vegetarian.WednesdayD.data,
                add_to_cart_vegetarian.ThursdayB.data,
                add_to_cart_vegetarian.ThursdayL.data,
                add_to_cart_vegetarian.ThursdayD.data,
                add_to_cart_vegetarian.FridayB.data,
                add_to_cart_vegetarian.FridayL.data,
                add_to_cart_vegetarian.FridayD.data)

            cart_dict[cart.get_cart_id()] = cart
            db['Cart'] = cart_dict

            db.close()

            return redirect(url_for('cart'))
        return render_template('Vegetarian.html', form=add_to_cart_vegetarian, combination_list=combination_list)


@app.route('/Cart')
def cart():
    if 'user' in session:

        cart_dict = {}
        temp_mealcombination = {}
        db = shelve.open('storage.db', 'r')
        cart_dict = db['Cart']
        temp_mealcombination = db['Meal_Combination']
        db.close()

        cart_list = []
        for key in cart_dict:
            cart = cart_dict.get(key)
            cart_list.append(cart)

        combination_list = []
        for key in temp_mealcombination:
            combination = temp_mealcombination.get(key)
            combination_list.append(combination)

        return render_template('Cart.html', count=len(cart_list), cart_list=cart_list, combination_list=combination_list)
    else:
        return redirect(url_for('login'))

@app.route('/UpdateCart/<int:id>/<preference>/<combination>/', methods=['GET', 'POST'])
def update_cart(id,preference,combination):
    if preference=='Low Carb' and combination=='All':
        update_cart_form = AddShoppingCartAll_LowCarb(request.form)
        if request.method == 'POST':
            cart_dict = {}
            db = shelve.open('storage.db', 'w')
            cart_dict = db['Cart']

            cart = cart_dict.get(id)
            cart.set_preference(update_cart_form.Preference.data)
            cart.set_combination(update_cart_form.Combination.data)
            cart.set_MondayB(update_cart_form.MondayB.data)
            cart.set_MondayL(update_cart_form.MondayL.data)
            cart.set_MondayD(update_cart_form.MondayD.data)
            cart.set_TuesdayB(update_cart_form.TuesdayB.data)
            cart.set_TuesdayL(update_cart_form.TuesdayL.data)
            cart.set_TuesdayD(update_cart_form.TuesdayD.data)
            cart.set_WednesdayB(update_cart_form.WednesdayB.data)
            cart.set_WednesdayL(update_cart_form.WednesdayL.data)
            cart.set_WednesdayD(update_cart_form.WednesdayD.data)
            cart.set_ThursdayB(update_cart_form.ThursdayB.data)
            cart.set_ThursdayL(update_cart_form.ThursdayL.data)
            cart.set_ThursdayD(update_cart_form.ThursdayD.data)
            cart.set_FridayB(update_cart_form.FridayB.data)
            cart.set_FridayL(update_cart_form.FridayL.data)
            cart.set_FridayD(update_cart_form.FridayD.data)

            db['Cart'] = cart_dict
            db.close()

            return redirect(url_for('cart'))
        else:
            cart_dict = {}
            db = shelve.open('storage.db', 'r')
            cart_dict = db['Cart']
            db.close()

            cart = cart_dict.get(id)
            update_cart_form.Preference.data = cart.get_preference()
            update_cart_form.Combination.data = cart.get_combination()
            update_cart_form.MondayB.data = cart.get_MondayB()
            update_cart_form.MondayL.data = cart.get_MondayL()
            update_cart_form.MondayD.data = cart.get_MondayD()
            update_cart_form.TuesdayB.data = cart.get_TuesdayB()
            update_cart_form.TuesdayL.data = cart.get_TuesdayL()
            update_cart_form.TuesdayD.data = cart.get_TuesdayD()
            update_cart_form.WednesdayB.data = cart.get_WednesdayB()
            update_cart_form.WednesdayL.data = cart.get_WednesdayL()
            update_cart_form.WednesdayD.data = cart.get_WednesdayD()
            update_cart_form.ThursdayB.data = cart.get_ThursdayB()
            update_cart_form.ThursdayL.data = cart.get_ThursdayL()
            update_cart_form.ThursdayD.data = cart.get_ThursdayD()
            update_cart_form.FridayB.data = cart.get_FridayB()
            update_cart_form.FridayL.data = cart.get_FridayL()
            update_cart_form.FridayD.data = cart.get_FridayD()

            return render_template('UpdateLowCarb.html', form=update_cart_form)

    elif preference=='Low Carb' and combination=='L&D':
        update_cart_form = AddShoppingCartNoBreakfast_LowCarb(request.form)
        if request.method == 'POST':
            cart_dict = {}
            db = shelve.open('storage.db', 'w')
            cart_dict = db['Cart']

            cart = cart_dict.get(id)
            cart.set_preference(update_cart_form.Preference.data)
            cart.set_combination(update_cart_form.Combination.data)
            cart.set_MondayB(update_cart_form.MondayB.data)
            cart.set_MondayL(update_cart_form.MondayL.data)
            cart.set_MondayD(update_cart_form.MondayD.data)
            cart.set_TuesdayB(update_cart_form.TuesdayB.data)
            cart.set_TuesdayL(update_cart_form.TuesdayL.data)
            cart.set_TuesdayD(update_cart_form.TuesdayD.data)
            cart.set_WednesdayB(update_cart_form.WednesdayB.data)
            cart.set_WednesdayL(update_cart_form.WednesdayL.data)
            cart.set_WednesdayD(update_cart_form.WednesdayD.data)
            cart.set_ThursdayB(update_cart_form.ThursdayB.data)
            cart.set_ThursdayL(update_cart_form.ThursdayL.data)
            cart.set_ThursdayD(update_cart_form.ThursdayD.data)
            cart.set_FridayB(update_cart_form.FridayB.data)
            cart.set_FridayL(update_cart_form.FridayL.data)
            cart.set_FridayD(update_cart_form.FridayD.data)

            db['Cart'] = cart_dict
            db.close()

            return redirect(url_for('cart'))
        else:
            cart_dict = {}
            db = shelve.open('storage.db', 'r')
            cart_dict = db['Cart']
            db.close()

            cart = cart_dict.get(id)
            update_cart_form.Preference.data = cart.get_preference()
            update_cart_form.Combination.data = cart.get_combination()
            update_cart_form.MondayB.data = cart.get_MondayB()
            update_cart_form.MondayL.data = cart.get_MondayL()
            update_cart_form.MondayD.data = cart.get_MondayD()
            update_cart_form.TuesdayB.data = cart.get_TuesdayB()
            update_cart_form.TuesdayL.data = cart.get_TuesdayL()
            update_cart_form.TuesdayD.data = cart.get_TuesdayD()
            update_cart_form.WednesdayB.data = cart.get_WednesdayB()
            update_cart_form.WednesdayL.data = cart.get_WednesdayL()
            update_cart_form.WednesdayD.data = cart.get_WednesdayD()
            update_cart_form.ThursdayB.data = cart.get_ThursdayB()
            update_cart_form.ThursdayL.data = cart.get_ThursdayL()
            update_cart_form.ThursdayD.data = cart.get_ThursdayD()
            update_cart_form.FridayB.data = cart.get_FridayB()
            update_cart_form.FridayL.data = cart.get_FridayL()
            update_cart_form.FridayD.data = cart.get_FridayD()

            return render_template('UpdateLowCarb.html', form=update_cart_form)

    elif preference=='Low Carb' and combination=='L&D':
        update_cart_form = AddShoppingCartNoBreakfast_LowCarb(request.form)
        if request.method == 'POST':
            cart_dict = {}
            db = shelve.open('storage.db', 'w')
            cart_dict = db['Cart']

            cart = cart_dict.get(id)
            cart.set_preference(update_cart_form.Preference.data)
            cart.set_combination(update_cart_form.Combination.data)
            cart.set_MondayB(update_cart_form.MondayB.data)
            cart.set_MondayL(update_cart_form.MondayL.data)
            cart.set_MondayD(update_cart_form.MondayD.data)
            cart.set_TuesdayB(update_cart_form.TuesdayB.data)
            cart.set_TuesdayL(update_cart_form.TuesdayL.data)
            cart.set_TuesdayD(update_cart_form.TuesdayD.data)
            cart.set_WednesdayB(update_cart_form.WednesdayB.data)
            cart.set_WednesdayL(update_cart_form.WednesdayL.data)
            cart.set_WednesdayD(update_cart_form.WednesdayD.data)
            cart.set_ThursdayB(update_cart_form.ThursdayB.data)
            cart.set_ThursdayL(update_cart_form.ThursdayL.data)
            cart.set_ThursdayD(update_cart_form.ThursdayD.data)
            cart.set_FridayB(update_cart_form.FridayB.data)
            cart.set_FridayL(update_cart_form.FridayL.data)
            cart.set_FridayD(update_cart_form.FridayD.data)

            db['Cart'] = cart_dict
            db.close()

            return redirect(url_for('cart'))
        else:
            cart_dict = {}
            db = shelve.open('storage.db', 'r')
            cart_dict = db['Cart']
            db.close()

            cart = cart_dict.get(id)
            update_cart_form.Preference.data = cart.get_preference()
            update_cart_form.Combination.data = cart.get_combination()
            update_cart_form.MondayB.data = cart.get_MondayB()
            update_cart_form.MondayL.data = cart.get_MondayL()
            update_cart_form.MondayD.data = cart.get_MondayD()
            update_cart_form.TuesdayB.data = cart.get_TuesdayB()
            update_cart_form.TuesdayL.data = cart.get_TuesdayL()
            update_cart_form.TuesdayD.data = cart.get_TuesdayD()
            update_cart_form.WednesdayB.data = cart.get_WednesdayB()
            update_cart_form.WednesdayL.data = cart.get_WednesdayL()
            update_cart_form.WednesdayD.data = cart.get_WednesdayD()
            update_cart_form.ThursdayB.data = cart.get_ThursdayB()
            update_cart_form.ThursdayL.data = cart.get_ThursdayL()
            update_cart_form.ThursdayD.data = cart.get_ThursdayD()
            update_cart_form.FridayB.data = cart.get_FridayB()
            update_cart_form.FridayL.data = cart.get_FridayL()
            update_cart_form.FridayD.data = cart.get_FridayD()

            return render_template('UpdateLowCarb.html', form=update_cart_form)

    elif preference=='Muscle Building' and combination=='All':
        update_cart_form = AddShoppingCartAll_MuscleBuilding(request.form)
        if request.method == 'POST':
            cart_dict = {}
            db = shelve.open('storage.db', 'w')
            cart_dict = db['Cart']

            cart = cart_dict.get(id)
            cart.set_preference(update_cart_form.Preference.data)
            cart.set_combination(update_cart_form.Combination.data)
            cart.set_MondayB(update_cart_form.MondayB.data)
            cart.set_MondayL(update_cart_form.MondayL.data)
            cart.set_MondayD(update_cart_form.MondayD.data)
            cart.set_TuesdayB(update_cart_form.TuesdayB.data)
            cart.set_TuesdayL(update_cart_form.TuesdayL.data)
            cart.set_TuesdayD(update_cart_form.TuesdayD.data)
            cart.set_WednesdayB(update_cart_form.WednesdayB.data)
            cart.set_WednesdayL(update_cart_form.WednesdayL.data)
            cart.set_WednesdayD(update_cart_form.WednesdayD.data)
            cart.set_ThursdayB(update_cart_form.ThursdayB.data)
            cart.set_ThursdayL(update_cart_form.ThursdayL.data)
            cart.set_ThursdayD(update_cart_form.ThursdayD.data)
            cart.set_FridayB(update_cart_form.FridayB.data)
            cart.set_FridayL(update_cart_form.FridayL.data)
            cart.set_FridayD(update_cart_form.FridayD.data)

            db['Cart'] = cart_dict
            db.close()

            return redirect(url_for('cart'))
        else:
            cart_dict = {}
            db = shelve.open('storage.db', 'r')
            cart_dict = db['Cart']
            db.close()

            cart = cart_dict.get(id)
            update_cart_form.Preference.data = cart.get_preference()
            update_cart_form.Combination.data = cart.get_combination()
            update_cart_form.MondayB.data = cart.get_MondayB()
            update_cart_form.MondayL.data = cart.get_MondayL()
            update_cart_form.MondayD.data = cart.get_MondayD()
            update_cart_form.TuesdayB.data = cart.get_TuesdayB()
            update_cart_form.TuesdayL.data = cart.get_TuesdayL()
            update_cart_form.TuesdayD.data = cart.get_TuesdayD()
            update_cart_form.WednesdayB.data = cart.get_WednesdayB()
            update_cart_form.WednesdayL.data = cart.get_WednesdayL()
            update_cart_form.WednesdayD.data = cart.get_WednesdayD()
            update_cart_form.ThursdayB.data = cart.get_ThursdayB()
            update_cart_form.ThursdayL.data = cart.get_ThursdayL()
            update_cart_form.ThursdayD.data = cart.get_ThursdayD()
            update_cart_form.FridayB.data = cart.get_FridayB()
            update_cart_form.FridayL.data = cart.get_FridayL()
            update_cart_form.FridayD.data = cart.get_FridayD()

            return render_template('UpdateMuscleBuilding.html', form=update_cart_form)

    elif preference=='Muscle Building' and combination=='L&D':
        update_cart_form = AddShoppingCartNoBreakfast_MuscleBuilding(request.form)
        if request.method == 'POST':
            cart_dict = {}
            db = shelve.open('storage.db', 'w')
            cart_dict = db['Cart']

            cart = cart_dict.get(id)
            cart.set_preference(update_cart_form.Preference.data)
            cart.set_combination(update_cart_form.Combination.data)
            cart.set_MondayB(update_cart_form.MondayB.data)
            cart.set_MondayL(update_cart_form.MondayL.data)
            cart.set_MondayD(update_cart_form.MondayD.data)
            cart.set_TuesdayB(update_cart_form.TuesdayB.data)
            cart.set_TuesdayL(update_cart_form.TuesdayL.data)
            cart.set_TuesdayD(update_cart_form.TuesdayD.data)
            cart.set_WednesdayB(update_cart_form.WednesdayB.data)
            cart.set_WednesdayL(update_cart_form.WednesdayL.data)
            cart.set_WednesdayD(update_cart_form.WednesdayD.data)
            cart.set_ThursdayB(update_cart_form.ThursdayB.data)
            cart.set_ThursdayL(update_cart_form.ThursdayL.data)
            cart.set_ThursdayD(update_cart_form.ThursdayD.data)
            cart.set_FridayB(update_cart_form.FridayB.data)
            cart.set_FridayL(update_cart_form.FridayL.data)
            cart.set_FridayD(update_cart_form.FridayD.data)

            db['Cart'] = cart_dict
            db.close()

            return redirect(url_for('cart'))
        else:
            cart_dict = {}
            db = shelve.open('storage.db', 'r')
            cart_dict = db['Cart']
            db.close()

            cart = cart_dict.get(id)
            update_cart_form.Preference.data = cart.get_preference()
            update_cart_form.Combination.data = cart.get_combination()
            update_cart_form.MondayB.data = cart.get_MondayB()
            update_cart_form.MondayL.data = cart.get_MondayL()
            update_cart_form.MondayD.data = cart.get_MondayD()
            update_cart_form.TuesdayB.data = cart.get_TuesdayB()
            update_cart_form.TuesdayL.data = cart.get_TuesdayL()
            update_cart_form.TuesdayD.data = cart.get_TuesdayD()
            update_cart_form.WednesdayB.data = cart.get_WednesdayB()
            update_cart_form.WednesdayL.data = cart.get_WednesdayL()
            update_cart_form.WednesdayD.data = cart.get_WednesdayD()
            update_cart_form.ThursdayB.data = cart.get_ThursdayB()
            update_cart_form.ThursdayL.data = cart.get_ThursdayL()
            update_cart_form.ThursdayD.data = cart.get_ThursdayD()
            update_cart_form.FridayB.data = cart.get_FridayB()
            update_cart_form.FridayL.data = cart.get_FridayL()
            update_cart_form.FridayD.data = cart.get_FridayD()

            return render_template('UpdateMuscleBuilding.html', form=update_cart_form)

    elif preference=='Vegetarian' and combination=='All':
        update_cart_form = AddShoppingCartAll_Vegetarian(request.form)
        if request.method == 'POST':
            cart_dict = {}
            db = shelve.open('storage.db', 'w')
            cart_dict = db['Cart']

            cart = cart_dict.get(id)
            cart.set_preference(update_cart_form.Preference.data)
            cart.set_combination(update_cart_form.Combination.data)
            cart.set_MondayB(update_cart_form.MondayB.data)
            cart.set_MondayL(update_cart_form.MondayL.data)
            cart.set_MondayD(update_cart_form.MondayD.data)
            cart.set_TuesdayB(update_cart_form.TuesdayB.data)
            cart.set_TuesdayL(update_cart_form.TuesdayL.data)
            cart.set_TuesdayD(update_cart_form.TuesdayD.data)
            cart.set_WednesdayB(update_cart_form.WednesdayB.data)
            cart.set_WednesdayL(update_cart_form.WednesdayL.data)
            cart.set_WednesdayD(update_cart_form.WednesdayD.data)
            cart.set_ThursdayB(update_cart_form.ThursdayB.data)
            cart.set_ThursdayL(update_cart_form.ThursdayL.data)
            cart.set_ThursdayD(update_cart_form.ThursdayD.data)
            cart.set_FridayB(update_cart_form.FridayB.data)
            cart.set_FridayL(update_cart_form.FridayL.data)
            cart.set_FridayD(update_cart_form.FridayD.data)

            db['Cart'] = cart_dict
            db.close()

            return redirect(url_for('cart'))
        else:
            cart_dict = {}
            db = shelve.open('storage.db', 'r')
            cart_dict = db['Cart']
            db.close()

            cart = cart_dict.get(id)
            update_cart_form.Preference.data = cart.get_preference()
            update_cart_form.Combination.data = cart.get_combination()
            update_cart_form.MondayB.data = cart.get_MondayB()
            update_cart_form.MondayL.data = cart.get_MondayL()
            update_cart_form.MondayD.data = cart.get_MondayD()
            update_cart_form.TuesdayB.data = cart.get_TuesdayB()
            update_cart_form.TuesdayL.data = cart.get_TuesdayL()
            update_cart_form.TuesdayD.data = cart.get_TuesdayD()
            update_cart_form.WednesdayB.data = cart.get_WednesdayB()
            update_cart_form.WednesdayL.data = cart.get_WednesdayL()
            update_cart_form.WednesdayD.data = cart.get_WednesdayD()
            update_cart_form.ThursdayB.data = cart.get_ThursdayB()
            update_cart_form.ThursdayL.data = cart.get_ThursdayL()
            update_cart_form.ThursdayD.data = cart.get_ThursdayD()
            update_cart_form.FridayB.data = cart.get_FridayB()
            update_cart_form.FridayL.data = cart.get_FridayL()
            update_cart_form.FridayD.data = cart.get_FridayD()

            return render_template('UpdateVegetarian.html', form=update_cart_form)

    elif preference=='Vegetarian' and combination=='L&D':
        update_cart_form = AddShoppingCartNoBreakfast_Vegetarian(request.form)
        if request.method == 'POST':
            cart_dict = {}
            db = shelve.open('storage.db', 'w')
            cart_dict = db['Cart']

            cart = cart_dict.get(id)
            cart.set_preference(update_cart_form.Preference.data)
            cart.set_combination(update_cart_form.Combination.data)
            cart.set_MondayB(update_cart_form.MondayB.data)
            cart.set_MondayL(update_cart_form.MondayL.data)
            cart.set_MondayD(update_cart_form.MondayD.data)
            cart.set_TuesdayB(update_cart_form.TuesdayB.data)
            cart.set_TuesdayL(update_cart_form.TuesdayL.data)
            cart.set_TuesdayD(update_cart_form.TuesdayD.data)
            cart.set_WednesdayB(update_cart_form.WednesdayB.data)
            cart.set_WednesdayL(update_cart_form.WednesdayL.data)
            cart.set_WednesdayD(update_cart_form.WednesdayD.data)
            cart.set_ThursdayB(update_cart_form.ThursdayB.data)
            cart.set_ThursdayL(update_cart_form.ThursdayL.data)
            cart.set_ThursdayD(update_cart_form.ThursdayD.data)
            cart.set_FridayB(update_cart_form.FridayB.data)
            cart.set_FridayL(update_cart_form.FridayL.data)
            cart.set_FridayD(update_cart_form.FridayD.data)

            db['Cart'] = cart_dict
            db.close()

            return redirect(url_for('cart'))
        else:
            cart_dict = {}
            db = shelve.open('storage.db', 'r')
            cart_dict = db['Cart']
            db.close()

            cart = cart_dict.get(id)
            update_cart_form.Preference.data = cart.get_preference()
            update_cart_form.Combination.data = cart.get_combination()
            update_cart_form.MondayB.data = cart.get_MondayB()
            update_cart_form.MondayL.data = cart.get_MondayL()
            update_cart_form.MondayD.data = cart.get_MondayD()
            update_cart_form.TuesdayB.data = cart.get_TuesdayB()
            update_cart_form.TuesdayL.data = cart.get_TuesdayL()
            update_cart_form.TuesdayD.data = cart.get_TuesdayD()
            update_cart_form.WednesdayB.data = cart.get_WednesdayB()
            update_cart_form.WednesdayL.data = cart.get_WednesdayL()
            update_cart_form.WednesdayD.data = cart.get_WednesdayD()
            update_cart_form.ThursdayB.data = cart.get_ThursdayB()
            update_cart_form.ThursdayL.data = cart.get_ThursdayL()
            update_cart_form.ThursdayD.data = cart.get_ThursdayD()
            update_cart_form.FridayB.data = cart.get_FridayB()
            update_cart_form.FridayL.data = cart.get_FridayL()
            update_cart_form.FridayD.data = cart.get_FridayD()

            return render_template('UpdateVegetarian.html', form=update_cart_form)

@app.route('/deleteCart/<int:id>', methods=['POST'])
def delete_cart(id):
    cart_dict = {}
    db = shelve.open('storage.db', 'w')
    cart_dict = db['Cart']

    cart_dict.pop(id)

    db['Cart'] = cart_dict
    db.close()

    return redirect(url_for('cart'))

@app.route('/Checkout', methods=['GET', 'POST'])
def checkout():

    if 'user' in session:
        user = session["user"]
        accounts_list = user[1:8]
        id = user[0]

        cart_dict = {}
        db = shelve.open('storage.db', 'r')
        cart_dict = db['Cart']
        db.close()

        cart_list = []
        for key in cart_dict:
            cart = cart_dict.get(key)
            cart_list.append(cart)



        order_comfirmation_form = Order_Comfirmation_Form(request.form)

        if request.method == 'POST' and order_comfirmation_form.validate():
            order_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                order_dict = db['Orders']
            except:
                print("Error in retrieving Orders from storage.db.")



            for cart in cart_list:
                order_id = len(order_dict) + 1

                order = Order.Order(order_id,
                                    user[0],
                                    order_comfirmation_form.first_name.data,
                                    order_comfirmation_form.last_name.data,
                                    order_comfirmation_form.gender.data,
                                    order_comfirmation_form.email.data,
                                    order_comfirmation_form.phone_number.data,
                                    order_comfirmation_form.address.data,
                                    order_comfirmation_form.region.data,
                                    order_comfirmation_form.rating.data,
                                    cart.get_preference(),
                                    cart.get_combination(),
                                    cart.get_MondayB(),
                                    cart.get_MondayL(),
                                    cart.get_MondayD(),
                                    cart.get_TuesdayB(),
                                    cart.get_TuesdayL(),
                                    cart.get_TuesdayD(),
                                    cart.get_WednesdayB(),
                                    cart.get_WednesdayL(),
                                    cart.get_WednesdayD(),
                                    cart.get_ThursdayB(),
                                    cart.get_ThursdayL(),
                                    cart.get_ThursdayD(),
                                    cart.get_FridayB(),
                                    cart.get_FridayL(),
                                    cart.get_FridayD(),
                                    AddToCart.AddToCart.calc_total_plan(cart)
                                    )

                order_dict[order.get_order_id()] = order

            db['Orders'] = order_dict

            cart_dict = {}

            cart_dict = db['Cart']

            cart_dict.clear()

            db['Cart'] = cart_dict

            db.close()

            return redirect(url_for('order_confirmation'))
        else:
            # order_comfirmation_form.user_id.data = user.get_user_id()
            order_comfirmation_form.first_name.data = user[1]
            order_comfirmation_form.last_name.data = user[2]
            order_comfirmation_form.gender.data = user[4]
            order_comfirmation_form.email.data = user[5]
            order_comfirmation_form.phone_number.data = user[6]


            return render_template('Checkout.html', form=order_comfirmation_form, cart_list=cart_list, count=len(cart_list))


@app.route('/retrieveOrders')
def retrieve_orders():
    if 'user' in session:
        user = session["user"]

        id = user[0]

        order_dict = {}
        db = shelve.open('storage.db', 'r')
        order_dict = db['Orders']
        db.close()
        order_list = []


        for key in order_dict:
            order = order_dict.get(key)
            if order.get_user_id() == id:
                order_list.append(order)

        return render_template('retrieveOrders.html', count=len(order_list), order_list=order_list)


# @app.route('/deleteOrder/<int:id>', methods=['POST'])
# def delete_order(id):
#     order_dict = {}
#     db = shelve.open('storage.db', 'w')
#     order_dict = db['Orders']
#
#     order_dict.pop(id)
#
#     db['Orders'] = order_dict
#     db.close()
#
#     return redirect(url_for('retrieve_orders'))

@app.route('/deleteOrder_Staff/<int:id>', methods=['POST'])
def delete_order_all(id):
    order_dict = {}
    db = shelve.open('storage.db', 'w')
    order_dict = db['Orders']

    order_dict.pop(id)

    db['Orders'] = order_dict
    db.close()

    return redirect(url_for('retrieve_orders_all'))

@app.route('/OrderComfirmation')
def order_confirmation():
    return render_template('OrderConfirmation.html')

# __________________________________________________________________________
# Abinaya
# Report Generation

@app.route('/retrieveOrders_All')
def retrieve_orders_all():

    order_dict = {}
    db = shelve.open('storage.db', 'r')
    order_dict = db['Orders']
    db.close()
    order_list = []


    for key in order_dict:
        order = order_dict.get(key)
        order_list.append(order)

    return render_template('retrieveOrders_All.html', count=len(order_list), order_list=order_list)

if __name__ == '__main__':
    app.run()

