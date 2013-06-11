"""
This application does not create models. It parses the csv files found in the data directory on demand
"""
import locale


class SafeFloat(float):
    def __new__(self, a=0):
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
            a = locale.atof(a)
            return super(SafeFloat, self).__new__(float, a)
        except ValueError:
            return None

    def __add__(self, rhs):
        print "yo"
        return self.value

