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
course_url = "http://study.enaea.edu.cn"
chrome_options = Options()
# chrome_options.add_argument('--headless')

prefs = {
    "profile.managed_default_content_settings.images": 1,
    "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
    "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,

}
chrome_options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(options=chrome_options)
# browser.set_window_size(800, 600)

# 进入
time.sleep(1)
wait = WebDriverWait(browser, 5)
browser.get("http://study.enaea.edu.cn/login.do")

# 输入账号和密码
input_usrname = wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#pc-form > div.form-body > div:nth-child(1) > div:nth-child(1) > input'))
)
input_password = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR,
                                    '#pc-form > div.form-body > div:nth-child(1) > div.input-control.input-control-second > input'))
)
login_btn = wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#pc-form > div.form-body > div:nth-child(1) > div.btn-row.mb15 > button'))
)
# 账号和密码
input_usrname.send_keys("")
input_password.send_keys("")
login_btn.click()

# 进入学习
login_study_btn = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#J_submitReg'))
)
login_study_btn.click()


def jump_course():
    # 直接跳转到学习界面
    time.sleep(5)
    browser.get(
        'http://study.enaea.edu.cn/circleIndexRedirect.do?action=toNewMyClass&type=course&circleId=35018&syllabusId=178761&isRequired=true&studentProgress=0')

    # 点击进入学习？
    # 这里需要解析一下观看哪个网站
    time.sleep(2)
    doc = py(browser.page_source)
    url_doc = doc('.golearn.ablesky-colortip.saveStuCourse')
    pro_doc = doc('.progressvalue')
    process = []
    urls = []
    for i in pro_doc.items():
        process.append(i.text())

    for i in url_doc.items():
        t_url = i.attr("data-vurl")
        urls.append(course_url + t_url)

    print(process, urls)

    # 找到需要进入的章节
    for p,url in zip(process,urls):
        if p!="100%":
            # 直接请求这个网站，不用跳转
            browser.get(url)
            start_look()

def start_look():
    # 这里需要检测一下看到了哪一章节了,测试发现不用
    time.sleep(2)
    doc = py(browser.page_source)
    # 查看历史观看进程
    process = []
    tags = []
    kc = doc(".cvtb-MCK-CsCt-studyProgress")
    for kc in kc.items():
        process.append(kc.text())
        tags.append(kc.attr('id'))

    print(process)
    print(tags)
    # 继续观看
    for p, idx in zip(process, tags):
        if p != '100%':
            btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#' + idx)))
            btn.click()
            break
    # 本章看完了？
    if process[-1] == "100%":
        time.sleep(5)
        jump_course()
    # 如果没看完我们就重新检测一下
    else:
        time.sleep(5 * 60)
        start_look()


if __name__ == '__main__':
    jump_course()

    # shutdown the browser
    time.sleep(3)
    browser.quit()
