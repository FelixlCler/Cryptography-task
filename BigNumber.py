class LongNumber:
    HEX_CHARS = "0123456789ABCDEF"

    def __init__(self, num_str):
        self.num_str = num_str.upper()
        self.num_list = self.str_to_list(num_str)

    def __str__(self):
        return self.num_str

    def __repr__(self):
        return f"LongNumber({self.num_str})"

    def str_to_list(self, num_str):
        return [self.HEX_CHARS.index(c) for c in num_str]

    def list_to_str(self, num_list):
        return "".join([self.HEX_CHARS[i] for i in num_list])

    def add(self, other):
        if len(self.num_list) > len(other.num_list):
            num1 = self.num_list
            num2 = other.num_list
        else:
            num1 = other.num_list
            num2 = self.num_list

        res = []
        carry = 0
        while num1 or carry:
            n1 = num1.pop() if num1 else 0
            n2 = num2.pop() if num2 else 0
            s = n1 + n2 + carry
            carry, s = divmod(s, 16)
            res.insert(0, s)

        self.num_list = res
        self.num_str = self.list_to_str(res)

    def subtract(self, other):
        if self.num_list < other.num_list:
            raise ValueError("Can't subtract larger number from smaller number")

        num1 = self.num_list.copy()
        num2 = other.num_list.copy()

        res = []
        carry = 0
        while num1:
            n1 = num1.pop()
            n2 = num2.pop() if num2 else 0
            if carry:
                n1 -= 1
                carry = 0
            if n1 < n2:
                n1 += 16
                carry = 1
            res.insert(0, n1 - n2)

        while res[0] == 0 and len(res) > 1:
            res.pop(0)

        self.num_list = res
        self.num_str = self.list_to_str(res)

    def mod(self, other):
        if self.num_list < other.num_list:
            return self

        num1 = self.num_list.copy()
        num2 = other.num_list.copy()

        while len(num1) >= len(num2):
            shift = len(num1) - len(num2)
            for i, digit in enumerate(num2):
                num1[i + shift] -= digit
            while num1 and num1[-1] == 0:
                num1.pop()

        return LongNumber(self.list_to_str(num1))

    def bitwise_not(self):
        res = []
        for digit in self.num_list:
            res.append(15 - digit)
        return LongNumber(self.list_to_str(res))

    def bitwise_xor(self, other):
        if len(self.num_list) > len(other.num_list):
            num1 = self.num_list
            num2 = other.num_list
        else:
            num1 = other.num_list
            num2 = self.num_list

        res = []
        while num1:
            n1 = num1.pop()
            n2 = num2.pop() if num2 else 0
            res.insert(0, n1 ^ n2)

        return LongNumber