class MealCombination:
    count_id = 1

    def __init__(self, preference, combination):
        # User.count_id += 1
        self.__meal_combination_id = MealCombination.count_id
        self.__preference= preference
        self.__combination = combination

    def get_meal_combination_id(self):
        return self.__meal_combination_id

    def get_preference(self):
        return self.__preference


    def get_combination(self):
        return self.__combination


    def set_meal_combination_id(self, meal_combination_id):
        self.__meal_combination_id = meal_combination_id

    def set_preference(self, preference):
        self.__preference = preference


    def set_combination(self, combination):
        self.__combination = combination

