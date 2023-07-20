import tkinter
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import os
from tkinter import *
from tkinter import ttk


def start():

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver'

    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)

    options = Options()

    options.add_argument('--blink-settings=imagesEnabled=false')

    # 접속할 url
    url = "https://talk.naver.com/"

    # 접속 시도
    driver = webdriver.Chrome(driver_path, options=options)

    driver.get(url)

    time.sleep(5)

    login = {
        "id": user_id.get(),
        "pw": password.get()
    }

    def clipboard_input(id, user_input):
        temp_user_input = pyperclip.paste()  # 사용자 클립보드를 따로 저장

        pyperclip.copy(user_input)
        driver.find_element(By.ID, id).click()
        # driver.find_element_by_xpath(user_xpath).click()
        ActionChains(driver).key_down(Keys.COMMAND).send_keys(
            'v').key_up(Keys.COMMAND).perform()

        pyperclip.copy(temp_user_input)  # 사용자 클립보드에 저장 된 내용을 다시 가져 옴
        time.sleep(1)

    clipboard_input('id', login.get("id"))
    clipboard_input('pw', login.get("pw"))
    driver.find_element(By.XPATH, '//*[@id="log.login"]').click()

    time.sleep(1)

    new_window = Tk()

    def quit_all():
        new_window.destroy()

    def replace_tk():
        error_message = ''
        error_text = ''

        try:
            driver.find_element(By.CLASS_NAME, 'message_text')
            error_message = driver.find_element(
                By.CLASS_NAME, 'message_text').text
        except:
            print('아이디 비번 확인 필요')

        try:
            driver.find_element(By.ID, 'err_common')
            error_text = driver.find_element(By.ID, 'err_common').text

        except:
            print('자동 입력 방지 나옴')

        if len(error_text) or len(error_message) > 0:

            new_window.title("아이디랑 비번 확인 필요")
            new_window.geometry(
                f"{app_width}x{app_height}+{int(center_width)}+{int(center_height)}")
            btn = Button(new_window, text='종료하기', command=quit_all, width=20, height=3, fg='white', bg='white', cursor="coffee_mug").pack(
                side=TOP, expand=YES)

    # 브라우저 등록 클릭
    try:
        if driver.find_element(By.XPATH, '//*[@id="new.save"]'):
            driver.find_element(By.XPATH, '//*[@id="new.save"]').click()

    except:
        print('등록하기 버튼 없이 바로 네이버 톡톡 진입')

    try:
        scroll = driver.find_element(By.ID, 'talk_all_tabpanel')

    # 로그인 실패 시 처리
    except:
        print('에러')
        replace_tk()
        return
    # 스크롤 특정 엘리먼트로 이동
    ActionChains(driver).move_to_element(scroll).perform()

    verical_ordinate = 1000

    unselect_list = ['네이버쇼핑', '쇼핑몰', '캠핑·숙박·펜션',
                     '여행·레저', '의료', '전문가', '생활서비스', '네이버 인플루언서 센터', '네이버페이', '네이버회원', '네이버 광고', '네이버플러스 멤버십', '네이버플러스 멤버십 고객센터']

    fan_url = 'in.naver'

    stop = True

    total_chat_list = []

    while stop:

        text_wraps = driver.find_elements(By.CLASS_NAME, 'text_wrap')

        for text in text_wraps:
            if text not in total_chat_list:
                total_chat_list.append(text)

        driver.execute_script(
            "arguments[0].scrollTop = arguments[1]", scroll, verical_ordinate)
        verical_ordinate += 1000

        time.sleep(0.5)

        text_wraps = driver.find_elements(By.CLASS_NAME, 'text_wrap')

        if len(total_chat_list) == len(text_wraps):
            print('스크롤 끝')
            break

    time.sleep(3)

    print("next level")

    f = open('./already_fan.txt', mode='r')

    already_fan = []

    for fan in f:
        already_fan.append(fan.replace('\n', ''))

    f.close()

    new_fan = []

    for element in text_wraps:
        if element.find_element(By.CLASS_NAME, 'name').text not in unselect_list:
            if element.find_element(By.CLASS_NAME, 'name').text in already_fan:
                print(element.find_element(By.CLASS_NAME, 'name').text)
                continue
            if fan_url in element.find_element(By.CLASS_NAME, 'message').text:
                print(element.find_element(By.CLASS_NAME, 'name').text)
                try:
                    element.find_element(By.CLASS_NAME, 'count')
                except:
                    continue

                if element.find_element(
                        By.CLASS_NAME, 'message').text:

                    element.click()

                    time.sleep(7)

                    card = driver.find_element(
                        By.CLASS_NAME, 'widgetcard_wrap.type_og')

                    a_tags = card.find_elements(By.TAG_NAME, 'a')

                    href = ''

                    for attr in a_tags:
                        if fan_url in attr.get_attribute('href'):
                            href = attr.get_attribute('href')
                            print(href)
                            attr.click()
                            break

                    driver.switch_to.window(
                        driver.window_handles[1])

                    time.sleep(7)

                    fan_btn = driver.find_element(
                        By.CLASS_NAME, 'hm-component-homeCover-profile-btn-item.hm-component-homeCover-profile-btn-item-fan.hm-theme-color-homeCover-profile-btn-item-fan')
                    fan_btn.click()

                    time.sleep(3)
                    toggle_btn = driver.find_element(
                        By.CLASS_NAME, 'AnimatedToggleButton__button___MRfHn')
                    toggle_btn.click()

                    time.sleep(3)
                    driver.close()
                    driver.switch_to.window(
                        driver.window_handles[0])

                    time.sleep(6)

                    chat_input_area = driver.find_element(
                        By.CLASS_NAME, 'chat_input')
                    chat_input_area.click()

                    chat_input_area.send_keys(':-) 완료')

                    chat_input_area.send_keys(Keys.ENTER)

                    if element.find_element(By.CLASS_NAME, 'name').text not in already_fan:
                        new_fan.append(element.find_element(
                            By.CLASS_NAME, 'name').text)

    # a : 이어쓰기 모드
    f = open('./already_fan.txt', 'a', encoding='utf-8')

    for fan_name in new_fan:
        if fan_name != '':
            f.write(fan_name+'\n')

    f.close()
    driver.quit()
    print('맞팬하기 완료')


# tkinter 객체 생성
window = Tk()

window.title("맞팬하는 프로그램")

windows_width = window.winfo_screenwidth()
windows_height = window.winfo_screenheight()

app_width = 350
app_height = 200

center_width = (windows_width / 2) - (app_width / 2)
center_height = (windows_height / 2) - (app_height / 2)

window.geometry(
    f"{app_width}x{app_height}+{int(center_width)}+{int(center_height)}")


def check_id_pw():
    if user_id.get() == '' or password.get() == '':

        return ttk.Label(window, text="아이디와 비밀번호를 확인해주세요").grid(
            row=3, column=1, padx=10, pady=10)
    else:
        window.destroy()
        start()


# 사용자 id와 password를 저장하는 변수 생성
user_id, password = StringVar(), StringVar()


# id와 password, 그리고 확인 버튼의 UI를 만드는 부분
ttk.Label(window, text="Username : ").grid(row=0, column=0, padx=10, pady=10)
ttk.Label(window, text="Password : ").grid(row=1, column=0, padx=10, pady=10)
ttk.Entry(window, textvariable=user_id).grid(row=0, column=1, padx=10, pady=10)
ttk.Entry(window, textvariable=password).grid(
    row=1, column=1, padx=10, pady=10)
ttk.Button(window, text="맞팬하기", command=check_id_pw).grid(
    row=2, column=1, padx=10, pady=10)

window.mainloop()
