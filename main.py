from .request import login, followMember

def login():
    username = "lxy15020712608"
    password = "910216"
    cookie = login(username, password)
    list = followMember(cookie=cookie, page=1)

if __name__ == '__main__':
    login()