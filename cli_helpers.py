import re
import readline

def parse(func):
    def split_arg(self, arg):
        func(self, arg.split())

    return split_arg

def state(func):
    def set_state(self, args):
        self.state.set_state(func(self, args))

    return set_state

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

def inject(func):
    inject_base_pat = '%{}:({}\\b)*'
    hint_base = '%{}'
    def inject_arg(self, args):
        for i in range(len(args)):
            arg = args[i]
            if '%p:' in arg:
                pat = inject_base_pat.format('p', '\d+')
                hint = hint_base.format('p')
            elif '%s:' in arg:
                pat = inject_base_pat.format('s', '\w+')
                hint = hint_base.format('s')
            elif '%:' in arg:
                pat = inject_base_pat.format('', '\w+')
                hint = hint_base.format('')
            else:
                continue

            val = re.compile(pat).search(arg).group(1)
            inject_id = str(self.state.fetch(val, hint=hint).obj_id)
            args[i] = re.sub(pat, inject_id, arg)

        func(self, args)
        readline_inject(args)

    return inject_arg

def readline_inject(args):
    # Inject into readline to use the injected command.
    history_len = readline.get_current_history_length()
    last_item = readline.get_history_item(history_len)
    cmd = ' '.join([last_item.split()[0]] + args)
    readline.replace_history_item(history_len-1, cmd)

def print_listing(items, pos):
    for offset, item in enumerate(items):
        print('{}. {}'.format(pos+offset, item))

    return pos + len(items)
