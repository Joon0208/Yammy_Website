class AddToCart:
    count_id = 0

    def __init__(self, preference,combination, MondayB, MondayL, MondayD, TuesdayB, TuesdayL, TuesdayD, WednesdayB, WednesdayL, WednesdayD
                 , ThursdayB, ThursdayL, ThursdayD, FridayB, FridayL, FridayD):
        AddToCart.count_id += 1
        self.__cart_id = AddToCart.count_id
        self.__preference = preference
        self.__combination = combination
        self.__MondayB= MondayB
        self.__MondayL = MondayL
        self.__MondayD = MondayD
        self.__TuesdayB= TuesdayB
        self.__TuesdayL = TuesdayL
        self.__TuesdayD = TuesdayD
        self.__WednesdayB= WednesdayB
        self.__WednesdayL = WednesdayL
        self.__WednesdayD = WednesdayD
        self.__ThursdayB= ThursdayB
        self.__ThursdayL = ThursdayL
        self.__ThursdayD = ThursdayD
        self.__FridayB= FridayB
        self.__FridayL = FridayL
        self.__FridayD = FridayD
        self.__total_price = 0

    def get_cart_id(self):
        return self.__cart_id

    def get_preference(self):
        return self.__preference

    def get_combination(self):
        return self.__combination

    def get_MondayB(self):
        return self.__MondayB

    def get_MondayL(self):
        return self.__MondayL

    def get_MondayD(self):
        return self.__MondayD

    def get_TuesdayB(self):
        return self.__TuesdayB

    def get_TuesdayL(self):
        return self.__TuesdayL

    def get_TuesdayD(self):
        return self.__TuesdayD

    def get_WednesdayB(self):
        return self.__WednesdayB

    def get_WednesdayL(self):
        return self.__WednesdayL

    def get_WednesdayD(self):
        return self.__WednesdayD

    def get_ThursdayB(self):
        return self.__ThursdayB

    def get_ThursdayL(self):
        return self.__ThursdayL

    def get_ThursdayD(self):
        return self.__ThursdayD

    def get_FridayB(self):
        return self.__FridayB

    def get_FridayL(self):
        return self.__FridayL

    def get_FridayD(self):
        return self.__FridayD

    def get_total_price(self):
        return self.__total_price



    def set_cart_id(self, cart_id):
        self.__cart_id = cart_id

    def set_preference(self, preference):
        self.__preference = preference

    def set_combination(self, combination):
        self.__combination = combination

    def set_MondayB(self, MondayB):
        self.__MondayB = MondayB

    def set_MondayL(self, MondayL):
        self.__MondayL = MondayL

    def set_MondayD(self, MondayD):
        self.__MondayD = MondayD

    def set_TuesdayB(self, TuesdayB):
        self.__TuesdayB = TuesdayB

    def set_TuesdayL(self, TuesdayL):
        self.__TuesdayL = TuesdayL

    def set_TuesdayD(self, TuesdayD):
        self.__TuesdayD = TuesdayD

    def set_WednesdayB(self, WednesdayB):
        self.__WednesdayB = WednesdayB

    def set_WednesdayL(self, WednesdayL):
        self.__WednesdayL = WednesdayL

    def set_WednesdayD(self, WednesdayD):
        self.__WednesdayD = WednesdayD

    def set_ThursdayB(self, ThursdayB):
        self.__ThursdayB = ThursdayB

    def set_ThursdayL(self, ThursdayL):
        self.__ThursdayL = ThursdayL

    def set_ThursdayD(self, ThursdayD):
        self.__ThursdayD = ThursdayD

    def set_FridayB(self, FridayB):
        self.__FridayB = FridayB

    def set_FridayL(self, FridayL):
        self.__FridayL = FridayL

    def set_FridayD(self, FridayD):
        self.__FridayD = FridayD

    def calc_total_plan(self):
        total=int(self.__MondayB)+int(self.__MondayL)+int(self.__MondayD)+int(self.__TuesdayB)+int(self.__TuesdayL)+int(self.__TuesdayD)+int(self.__WednesdayB)+int(self.__WednesdayL) + int(self.__WednesdayD)+int(self.__ThursdayB) + int(self.__ThursdayL) + int(self.__ThursdayD)+int(self.__FridayB) + int(self.__FridayL) + int(self.__FridayD)

        self.__total_price=total*5

        return self.__total_price





