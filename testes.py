



class Teste:
    def __init__(self, num, formatter = "{:05d}"):
        self.formatter = formatter
        self.num = num
        print(formatter.format(num))



a = Teste(10)