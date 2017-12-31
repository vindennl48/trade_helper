
class Money:
    def __init__(self, amount=0, accuracy=8):
        self.amount = 0
        self.accuracy = int(accuracy)
        self.set(amount)

    def set(self, x):
        value = float(str(x))
        self.amount = int(value*(10**self.accuracy))

    def get_accuracy(self,x):
        if type(x) is Money:
            if self.accuracy > x.accuracy:
                return self.accuracy
            else:
                return x.accuracy
        else:
            return self.accuracy

    def __add__(self, x):
        accuracy = self.get_accuracy(x)
        a = self.float()
        x = float(str(x))
        return Money(a+x,accuracy)

    def __sub__(self, x):
        accuracy = self.get_accuracy(x)
        a = self.float()
        x = float(str(x))
        return Money(a-x,accuracy)

    def __mul__(self, x):
        accuracy = self.get_accuracy(x)
        a = self.float()
        x = float(str(x))
        return Money(a*x,accuracy)

    def __div__(self, x):
        accuracy = self.get_accuracy(x)
        a = self.float()
        x = float(str(x))
        return Money(a/x,accuracy)

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

    def __float__(self):
        return float(self.amount)/(10**self.accuracy)

    def float(self):
        return self.__float__()

    def __str__(self):
        result = float(self.amount) / (10**self.accuracy)
        accuracy = "{:." + str(self.accuracy) + "f}"
        return accuracy.format(result)

    def str(self):
        return self.__str__()


# if __name__ == "__main__":
#     a = Money(5)
#     b = Money(3)
#     c = (((a-(a*b))+b)*(a/b))
#     print(c)
# 
