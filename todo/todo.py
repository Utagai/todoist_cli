from cli import TodoistCLI
from conf_schema import TodoConfig


def main():
    conf = TodoConfig.get_config()
    to = TodoistCLI(conf)

    # Start.
    to.do()


if __name__ == '__main__':
    main()
