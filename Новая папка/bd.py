
from datetime import datetime
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import ElementNotVisibleException, ElementNotSelectableException
import html_to_json


option = webdriver.ChromeOptions()
#option.add_argument('headless')
option.add_argument("--disable-infobars")
browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', chrome_options=option)

temp = 0
after_id = ''
wait = WebDriverWait(browser, 10, poll_frequency=1,
                     ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])


class Users:
    all_users = dict()

    def __init__(self, user_id):
        self.name = None
        self.timer = None
        self.order = None
        self.data = None
        Users.add_user(user_id, self)

    @staticmethod
    def get_user(user_id):
        if Users.all_users.get(user_id) is None:
            new_user = Users(user_id)
            return new_user
        return Users.all_users.get(user_id)

    @classmethod
    def add_user(cls, user_id, user):
        cls.all_users[user_id] = user


def data_timer(user):
    brow = browser.current_url
    new_url = browser.get(browser.current_url + user.order[0][12:])
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wid-id-11"]/div/div/div[2]/div[3]/div')))
    sater = browser.find_element(By.XPATH, '//*[@id="wid-id-11"]/div/div/div[2]/div[3]/div').get_attribute('outerHTML')

    output_json = html_to_json.convert(sater)
    # user.timer = output_json['div'][0]['_values'][2].split()[5]
    print(output_json['div'][0]['_values'][2].split()[5])
    browser.get(brow)
    return output_json['div'][0]['_values'][2].split()[5]


def enter_list(root, *info):  # root, name or count_or_time, relxx, relyy, relheight

    index = Frame(root, bg='white')
    index.place(relx=f'{info[1]}', rely=f'{info[2]}', relwidth='1', relheight=f'{info[3]}')
    tittle = Label(index, text=f'{info[0]}', bg='white', font=('Comic Sans MS', 60), highlightcolor='white')
    tittle.pack(anchor='w', padx=50)


def timer_list(user):
    if isinstance(user.timer, str):
        if int(user.timer) // 60 >= 1:
            timering = datetime.strptime(f'{int(user.timer) // 60}:{int(user.timer) % 60}:0', '%H:%M:%S')
            user.timer = timering
            user.timer -= datetime.strptime('0:0:1', '%H:%M:%S')
        else:
            timering = datetime.strptime(f'0:{user.timer}:0', '%H:%M:%S')
            user.timer = timering
            user.timer -= datetime.strptime('0:0:1', '%H:%M:%S')
    else:
        user.timer = datetime.strptime(str(user.timer), '%H:%M:%S')
        user.timer -= datetime.strptime('0:0:1', '%H:%M:%S')
    return str(user.timer)[0:]


def tick(Dicty_browzer, root):
    global temp, after_id
    after_id, root.after(1000, renewal, browser, root)
    d, k = 0, 0

    for person, dfgsd in Users.all_users.items():
        if not person in str(Dicty_browzer):
            k += 1
    count = len(Dicty_browzer) + k
    one_count = round(1 / count, 2)
    for people in Users.all_users:
        if people not in str(Dicty_browzer):
            user = Users.get_user(people)
            if user.data is None:
                user.data = 1
                user.timer = data_timer(user)
            enter_list(root, user.name, 0.00, d, one_count)
            enter_list(root, timer_list(user), 0.70, d, one_count)
            if user.timer == '0:00:00':
                Users.all_users.pop(people)
            d += one_count

    for name, information in sorted(Dicty_browzer.items(), key=lambda count_order: len(count_order)):
        if Users.all_users.get(name, None) is None:
            user = Users.get_user(name)
            user.name = name
            user.order = information
            user.timer = str(len(user.order) * 23)
            enter_list(root, user.name, 0.00, d, one_count)
            enter_list(root, str(len(user.order)), 0.60, d, one_count)
            enter_list(root, timer_list(user), 0.70, d, one_count)
            d += one_count
        else:
            user = Users.get_user(name)
            if len(information) != len(user.order):
                user.data = None
                user.order = information
                user.timer = str(len(user.order) * 23)
            enter_list(root, user.name, 0.00, d, one_count)
            enter_list(root, str(len(user.order)), 0.60, d, one_count)
            enter_list(root, timer_list(user), 0.70, d, one_count)
            d += one_count


def time_couriers(n_n, n_o):
    user = Users.get_user(n_n)
    user.timer = n_o
    pass


def save_information(n_n, n_o, Dicty_browzer):
    try:
        if Dicty_browzer.get(n_n, None) is None:
            Dicty_browzer[n_n] = [n_o]
        else:
            Dicty_browzer[n_n].append(n_o)
    except:
        pass


def couriers(output_json, dicti):
    for i in range(len(output_json['tbody'][0]['tr'])):
        name_number = output_json['tbody'][0]['tr'][i]['td'][6]['div'][0]['a'][0]['span'][0]['_values']
        number_order = output_json['tbody'][0]['tr'][i]['td'][0]['div'][0]['a'][0]['_attributes']['href']
        save_information(name_number[0], number_order, dicti)


def renewal(browser, root):
    Dicty_browzer = dict()
    place_order = browser.find_element(By.XPATH, "//select/option[@value='1']")
    place_order.click()
    order_choice = browser.find_element(By.XPATH, "//select/option[@value='6']")
    order_choice.click()
    sater = browser.find_element(By.XPATH, "//*[@id='wid-id-18']/div/div/div[2]/table/tbody").get_attribute('outerHTML')
    output_json = html_to_json.convert(sater)
    try:
        couriers(output_json, Dicty_browzer)
    except:
        renewal(browser, root)
    tick(Dicty_browzer, root)


def main():
    try:

        browser.get('https://stapizza.superdostavka.net/login')
        time.sleep(1)

        email_input = browser.find_element(By.ID, "username")
        email_input.clear()
        email_input.send_keys('0160')
        pas_input = browser.find_element(By.ID, "password")
        pas_input.clear()
        pas_input.send_keys('12345')
        time.sleep(0.1)
        enter = browser.find_element(By.XPATH, "//button")
        enter.click()
        time.sleep(3)

        root = Tk()
        root['bg'] = '#fafafa'
        root.title('Таймер курьеров')
        root.state('zoomed')
        canvas = Canvas(root)
        canvas.pack()

        frame_one = Frame(root, bg='white')
        frame_one.place(relx='0.00', rely='0.00', relwidth='1', relheight='1')
        root.after(3000, renewal, browser, root)
        root.mainloop()
        time.sleep(3)
        time.sleep(100)


    except:
        main()


if __name__ == '__main__':
    main()
