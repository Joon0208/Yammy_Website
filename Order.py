from AddToCart import AddToCart

class Order(AddToCart):
    # count_order_id = 0

    def __init__(self,order_id, user_id, first_name, last_name, gender, email, phone_number, address, region, rating,
                 preference, combination, MondayB, MondayL, MondayD, TuesdayB, TuesdayL, TuesdayD, WednesdayB,
                 WednesdayL, WednesdayD, ThursdayB, ThursdayL, ThursdayD, FridayB, FridayL, FridayD, total_price
                 ):

        AddToCart.__init__(self, preference, combination, MondayB, MondayL, MondayD, TuesdayB, TuesdayL, TuesdayD, WednesdayB, WednesdayL, WednesdayD
             , ThursdayB, ThursdayL, ThursdayD, FridayB, FridayL, FridayD)

        self.__order_id = order_id
        self.__user_id = user_id
        # Order.count_order_id += 1
        # self.__order_id = Order.count_order_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__email = email
        self.__phone_number = phone_number
        self.__address = address
        self.__region = region
        self.__rating = rating
        self.__total_price = total_price

    def get_user_id(self):
        return self.__user_id

    def get_order_id(self):
        return self.__order_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    # def get_birthday(self):
    #     return self.__birthday

    def get_gender(self):
        return self.__gender

    def get_email(self):
        return self.__email

    def get_phone_number(self):
        return self.__phone_number

    def get_address(self):
        return self.__address

    def get_region(self):
        return self.__region

    def get_rating(self):
        return self.__rating

    def get_total_price(self):
        return self.__total_price


    def set_order_id(self,order_id):
        self.__order_id = order_id

    def set_user_id(self,user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    # def set_birthday(self, birthday):
    #     self.__birthday = birthday

    def set_gender(self, gender):
        self.__gender = gender

    def set_email(self, email):
        self.__email = email

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_address(self, address):
        self.__address = address

    def set_region(self, region):
        self.__region = region

    def set_rating(self, rating):
        self.__rating = rating

    def set_total_price(self, total_price):
        self.__total_price = total_price




