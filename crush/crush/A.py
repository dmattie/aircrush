class A:
    def __init__(self):
        pass
    def __enter__(self):
        print("in __enter__")
        print(self.X)
        return self
    def __exit__(self, exception_type, exception_value, traceback):
        print("in __exit__")
        print(self.X)

with A() as a:
    
    X=1
    Y=2
