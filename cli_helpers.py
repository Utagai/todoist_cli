def parse(func):
    def split_arg(self, arg):
        func(self, arg.split())

    return split_arg

class arglen:
    def __init__(self, min, max = None):
        self.min = min
        if not max:
            self.max = self.min
        else:
            self.max = max

    def __call__(self, func):
        def arglen_check(func_self, arg):
            if self.min <= len(arg) and len(arg) <= self.max:
                return func(func_self, arg)
            else:
                print("The '{}' command takes between [{}, {}] args.".format(
                    func.__name__.split('_')[1], self.min, self.max))

        return arglen_check

def print_listing(items, pos):
    for offset, item in enumerate(items):
        print('{}. {}'.format(pos+offset, item))

    return pos + len(items)
