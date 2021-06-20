import os


def installer():
    os.system('pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint')
    os.system('python3 db_init.py')


if __name__ == '__main__':
    installer()
