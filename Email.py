class Email:

    # count_id = 0
    def __init__(self, email_id, name, email, subject, message):
        # Email.count_id += 1
        # self.__email_id = Email.count_id
        self.__email_id = email_id
        self.__name = name
        self.__email = email
        self.__subject = subject
        self.__message = message

    def get_email_id(self):
        return self.__email_id
    def get_name(self):
        return self.__name
    def get_email(self):
        return self.__email
    def get_subject(self):
        return self.__subject
    def get_message(self):
        return self.__message


    def set_email_id(self, email_id):
        self.__email_id = email_id
    def set_name(self, name):
        self.__name = name
    def set_email(self, email):
        self.__email = email
    def set_subject(self, subject):
        self.__subject = subject
    def set_message(self, message):
        self.__message= message


