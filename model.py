class User:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
    
    def get_username(self):
        return self.__username
    
    def get_password(self):
        return self.__password

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

class Student:
    def __init__(self, fullname, id, gender, dob, absent_count, atttedance=None):
        self.__fullname = fullname
        self.__id = id
        self.__gender = gender
        self.__dob = dob
        self.__absent_count = absent_count
        self.__atttedance = atttedance

    def get_fullname(self):
        return self.__fullname
    
    def get_id(self):
        return self.__id

    def get_gender(self):
        return self.__gender

    def get_dob(self):
        return self.__dob
    
    def get_absent_count(self):
        return self.__absent_count

    def get_atttedance(self):
        return self.__atttedance

    def set_fullname(self, fullname):
        self.__fullname = fullname

    def set_id(self, id):
        self.__id = id

    def set_gender(self, gender):
        self.__gender = gender
    
    def set_dob(self, dob):
        self.__dob = dob

    def set_absent_count(self, absent_count):
        self.__absent_count = absent_count

    def set_atttedance(self, atttedance):
        self.__atttedance = atttedance