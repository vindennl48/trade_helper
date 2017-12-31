
class Money:
    def __init__(self, amount=0, accuracy=8):
        self.amount = 0
        self.accuracy = int(accuracy)

        self.set_amount(amount)

    def set_amount(self, x):
        self.amount = int(float(x)*(10**self.accuracy))

#    def __add__(self, x):
#        if self.accuracy > x.accuracy:
#            m = Money(accuracy=self.accuracy)
#        else:
#            m = Money(accuracy=x.accuracy)
#        m.amount = int(self.amount + x.amount)
#        return m
#
#    def __sub__(self, x):
#        m = Money()
#        m.amount = int(self.amount - x.amount)
#        return m
#
#    def __mul__(self, x):
#        m = Money()
#        m.amount = int(self.amount * x.amount)
#        return m
#
#    def __div__(self, x):
#        m = Money()
#        m.amount = int(self.amount / x.amount * (10**self.accuracy))
#        return m

    def __gt__(self, x):
        return self.amount > x.amount

    def __ge__(self, x):
        return self.amount >= x.amount

    def __lt__(self, x):
        return self.amount < x.amount

    def __le__(self, x):
        return self.amount <= x.amount

    def __ne__(self, x):
        return self.amount != x.amount

    def __eq__(self, x):
        return self.amount == x.amount

    def __str__(self):
        result = float(float(self.amount) / (10**self.accuracy))
        return "{:.8f}".format(result)
