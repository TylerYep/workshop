class Sample:
    def __init__(self, secret, read_only):
        self._secret = secret
        self.__read_only = read_only

    @property
    def secret(self):
        return self._secret

    @property
    def read_only(self):
        return self.__read_only

    @property
    def backdoor(self):
        return self._secret


sample = Sample(200, 50)
print(sample.read_only)
sample.__read_only = 30
print(sample.read_only)
print(sample.__read_only)
print(vars(sample))

