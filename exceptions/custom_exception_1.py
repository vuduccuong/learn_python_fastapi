#  author = "Vũ Đức Cường"
#  date = 9/22/22, 11:18 PM


class CustomExceptionOne(Exception):
    def __init__(self, custom_field):
        self.custom_field = custom_field
