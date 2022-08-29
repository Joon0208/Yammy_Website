from wtforms import Form, StringField, IntegerField, DateField, RadioField, SelectField, TextAreaField, validators
from wtforms.validators import InputRequired, Email

class CreateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    birthday = DateField('Birthday', [validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    phone_number = StringField('Phone Number',[validators.Length(min=1,max=20)])
    password = StringField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])

class LogIn(Form):
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = StringField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])

class CreateEmailForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField("Email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    subject = StringField('Subject', [validators.Length(min=1, max=150), validators.DataRequired()])
    message = TextAreaField('Message', [validators.DataRequired()])


class CreateMealCombination(Form):
    preference = RadioField('Choose Preference', choices=[('Low Carb', 'Low Carb'), ('Muscle Building', 'Muscle Building'), ('Vegetarian', 'Vegetarian')], default='Low Carb')
    combination = RadioField('Choose Combination',
                            choices=[('All', 'All Combination'),('L&D', 'Lunch & Dinner')], default='All')

class AddShoppingCartAll_LowCarb(Form):
    Preference = SelectField('Preference', choices=[('Low Carb', 'Low Carb')],default='Low Carb')
    Combination = SelectField('Combination',choices=[('All', 'All Combination')], default='All')
    MondayB = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    MondayL = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    MondayD = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    TuesdayB = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    TuesdayL = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    TuesdayD = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    WednesdayB = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    WednesdayL = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    WednesdayD = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    ThursdayB = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    ThursdayL = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    ThursdayD = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    FridayB = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    FridayL = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    FridayD = SelectField('Quantity', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')


class AddShoppingCartNoBreakfast_LowCarb(AddShoppingCartAll_LowCarb):
    Combination = SelectField('Combination',choices=[('L&D', 'Lunch & Dinner')], default='L&D')
    MondayB = SelectField('Quantity', choices=[('0', '0')], default='0')
    TuesdayB = SelectField('Quantity', choices=[('0', '0')], default='0')
    WednesdayB = SelectField('Quantity', choices=[('0', '0')], default='0')
    ThursdayB = SelectField('Quantity', choices=[('0', '0')], default='0')
    FridayB = SelectField('Quantity', choices=[('0', '0')], default='0')


class AddShoppingCartAll_MuscleBuilding(AddShoppingCartAll_LowCarb):
    Preference = SelectField('Preference', choices=[('Muscle Building', 'Muscle Building')], default='Muscle Building')


class AddShoppingCartNoBreakfast_MuscleBuilding(AddShoppingCartNoBreakfast_LowCarb):
    Preference = SelectField('Preference', choices=[('Muscle Building', 'Muscle Building')], default='Muscle Building')


class AddShoppingCartAll_Vegetarian(AddShoppingCartAll_LowCarb):
    Preference = SelectField('Preference', choices=[('Vegetarian', 'Vegetarian')], default='Vegetarian')


class AddShoppingCartNoBreakfast_Vegetarian(AddShoppingCartNoBreakfast_LowCarb):
    Preference = SelectField('Preference', choices=[('Vegetarian', 'Vegetarian')], default='Vegetarian')



class Order_Comfirmation_Form(Form):
    # user_id = StringField('UserID', [validators.Length(min=1, max=150), validators.DataRequired()])
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    phone_number = StringField('Phone Number', [validators.Length(min=1, max=20)])
    address = StringField('Address', [validators.Length(min=1, max=150), validators.DataRequired()])
    region = SelectField('Region', choices=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West'), ('Central', 'Central')], default='North')
    rating = SelectField('Rating', choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')], default='5')




