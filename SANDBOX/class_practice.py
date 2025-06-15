def function(x, y):
    if type(x) is not int or type(y) is not int:
        raise TypeError("Both arguments must be integers")
    else: 
        return x*y


class Multiply:
    def __init__(self, x, y):
        if type(x) is not int or type(y) is not int:
            raise TypeError("Both arguments must be integers")
        self.x = x
        self.y = y

    def multiply(self):
        return self.x * self.y

    def __str__(self):
        return f"Multipy({self.x}, {self.y})"
    
multiplication = Multiply(2, 4)
#print(multiplication)  # Output: 8
#print(multiplication.multiply())



