from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from pyquery import PyQuery as py
import time

# 开始
chrome_options = Options()
# chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options = chrome_options)
browser.set_window_size(800, 600)

time.sleep(1)
wait = WebDriverWait(browser, 5)

def log_in(usrname, password, course, num_kc):
    try:
        browser.get('http://passport2.chaoxing.com/login?fid=22169&refer=http://i.mooc.chaoxing.com')
        input_usrname = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#unameId'))
        )
        input_password = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#passwordId'))
        )
        input_numcode = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#numcode'))
        )

        input_usrname.send_keys(usrname)
        input_password.send_keys(password)
        look_numcode()
        numcode = get_numcode()
        print(numcode)
        input_numcode.send_keys(numcode)
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#form > table > tbody > tr.zl_tr_top18_2 > td:nth-child(2) > label > input'))
        )
        submit.click()

        browser.switch_to.frame('frame_content')
        if course ==1:
            kccss = 'body > div > div:nth-child(3) > div.ulDiv > ul > li:nth-child(2) > div.Mcon1img.httpsClass > a:nth-child(1) > img'
        else:
            kccss = 'body > div > div:nth-child(3) > div.ulDiv > ul > li:nth-child(1) > div.Mcon1img.httpsClass > a:nth-child(1) > img'
        kc = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, kccss))
        )
        kc.click()

        browser.switch_to.window(browser.window_handles[-1])
        tk = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.main > div.left > div.content1.roundcorner > div.timeline > div:nth-child(1) > div:nth-child(2) > h3 > span.articlename > a'))
        )
        tk.click()
        kc_list = get_kc_list()
    except Exception:
        print('登录失败重新登了！')
        log_in(usrname=usrname, password=password, course=course)

    # cur102435926
    print(kc_list)
    for kcid in kc_list[num_kc:]:
        kc_btn = browser.find_element(By.CSS_SELECTOR, '#'+kcid)
        browser.execute_script("arguments[0].scrollIntoView(true);", kc_btn)
        kc_btn.click()
        start_tk()
        time.sleep(3)
        num_kc = num_kc+1
        with open ('log.txt','w') as f:
            f.write(str(num_kc))

def look_numcode():
    vercode = browser.find_element(By.CSS_SELECTOR, '#numVerCode')
    browser.get_screenshot_as_file('vercode.png')


def start_tk():

    click_shipin()
    time.sleep(2)
    #切换iframe
    browser.switch_to.frame('iframe')
    video_frame = browser.find_element_by_tag_name('iframe')
    browser.switch_to.frame(video_frame)

    #点击视频
    ksp = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#reader'))
    )
    browser.execute_script("arguments[0].scrollIntoView(true);", ksp)

    #点击视频动作
    actions = ActionChains(browser)
    actions.move_to_element(ksp)
    actions.click()
    actions.perform()
    #等待视频结束

    time_wait()
    browser.switch_to.default_content()
    print('本节课结束！')


def time_wait():

    time.sleep(3)
    try:
        dic = py(browser.page_source)
        wait_time_str = dic('.vjs-duration-display').text()
        now_time = dic('.vjs-current-time-display').text()
        now_mn = now_time.split(':')
        min_sec = wait_time_str.split(':')
        print(now_mn, min_sec)
        wait_time = (int(min_sec[0])-int(now_mn[0]))*60 + int(min_sec[1])-int(now_mn[1])
        print(wait_time)

        tanchuang = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ans-videoquiz-opts'))
        )
        #wait !!!!!!!
        selectors = tanchuang.find_elements_by_tag_name('input')
        for btn in selectors:
            try:
                btn.click()
                submit = wait.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'ans-videoquiz-submit'))
                )
                submit.click()
                time.sleep(1)
                btn.click()
            except UnexpectedAlertPresentException:
                time.sleep(1)
                browser.switch_to.alert.accept()
                time.sleep(1)
        time.sleep(wait_time)
    except Exception:
        try:
            if wait_time < 2:
                time.sleep(5)
            else:
                time_wait()
        except Exception:
            browser.refresh()


def click_shipin():

    time.sleep(3)
    shipin = browser.find_element_by_class_name('tabtags')
    btns = shipin.find_elements_by_tag_name('span')
    for btn in btns:
        if btn.get_attribute('title') == '':
            sp = btn
    sp.click()

def get_kc_list():
    kc_list = []
    zhangjie = browser.find_elements_by_class_name('ncells')
    for kc in zhangjie:
        kc_list.append(kc.find_element_by_tag_name('h4').get_attribute('id'))
    return kc_list

def get_numcode():
    numcode = browser.find_element(By.CSS_SELECTOR, '#numVerCode')
    img_url = numcode.get_attribute('src')
    numcode = input('请输入验证码：')
    return numcode

def main():
    usrname = ''
    password = ''
    with open('log.txt', 'r') as f:
        num_kc = f.read()
    num_kc = int(num_kc)
    log_in(usrname, password, 1, num_kc)

if __name__ == '__main__':

    main()



