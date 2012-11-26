#from django.db import models

class SafeFloat(float):
    def __new__(self, a):
        try:
            return super(SafeFloat, self).__new__(float, a)
        except ValueError:
            return None

