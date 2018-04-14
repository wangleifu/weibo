from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time

# 如果有操作太快的提示框，点击确定
def confirm(driver):
    try:
        confirm = WebDriverWait(driver, 1).until(lambda x: x.find_element_by_xpath('//*[@class="W_layer_btn S_bg1"]/a'))
        confirm.click()
        print(' ----处理提示框！')
        return True
    except:
        return False

# 点赞操作
def praise(driver, element):
    praise = WebDriverWait(element, 10).until(lambda x: x.find_element_by_xpath('div[@class="WB_feed_handle"]/div/ul/li[4]/a'))
    if praise.get_attribute('title') == '赞':
        confirm(driver)
        praise.click()
        while confirm(driver):
            praise.click()
        print(' -----成功点赞！')
    print('----已赞！')
    time.sleep(2)

# 转发操作
def repost(driver, element):
    repost = WebDriverWait(element, 10).until(lambda x: x.find_element_by_xpath('div[@class="WB_feed_handle"]/div/ul/li[2]/a'))
    confirm(driver)
    repost.click()
    while confirm(driver):
        repost.click()
    path = '//*[@class="W_layer "]/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[1]/a'
    post = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(path))
    post.click()
    print(' -----完成转发！')
    time.sleep(2)

def add(element, follows):
    href = element.find_element_by_xpath('div[1]/div[3]/div[3]/a').get_attribute('href')
    follows.append(href)
    print(' -----完成保存需要关注的微博！')

# 关注新用户操作
def follow(follows):
    print(' ----处理需要关注人列表！')
    if len(follows) == 0:
        print('----此次不需要关注操作！')
        return
    for follow in follows:
        ActionChains(browser).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()
        driver.get(follow)
        # handle = driver.window_handles[2]
        # driver.switch_to.window(handles)
        gz = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[4]/div/div[1]/a[1]'))
        gz.click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
        time.sleep(2)

def loop(driver, last_time):
    # 刷新出本页所有微博
    driver.refresh()
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        print('-----下拉加载页面！')
        time.sleep(2)

    # 获取当前页的所有用户微博
    elements = driver.find_elements_by_xpath('//*[@id="v6_pl_content_homefeed"]/div/div[3]/div')
    elements = elements[:len(elements)-2]
    print('---共获取到 %d 条原创微博---' % len(elements))

    # 爬取所有微博并对符合要求的微博（抽奖微博）进行相应的操作
    i = 0
    follows = []
    for element in elements:
        i += 1
        ActionChains(driver).move_to_element(element).perform()
        date = elements[0].find_element_by_xpath('//div[@class="WB_detail"]/div[2]/a[1]').get_attribute('date')
        if date > last_time:
            text = element.find_element_by_xpath('//div[@class="WB_detail"]/div[3]').text.strip()
            if (text.find('抽') != -1) or (text.find('送') != -1) or (text.find('开') != -1):
                time.sleep(1)
                print('---以前的抽奖微博，忽略！---')
                if text.find('赞') != -1:
                    print(' ------需要点赞！！！', i)
                    praise(driver, feed_handle)
                if text.find('转') != -1:
                    print(' ------需要转发！！！', i)
                    repost(driver, feed_handle)
                if text.find('关注') != -1:
                    print(' ------需要关注！！！', i)
                    add(element, follows)
        else:
            continue
        time.sleep(3)

    follow(follows)
    last_time = elements[0].find_element_by_xpath('//div[@class="WB_detail"]/div[2]/a[1]').get_attribute('date')
    print('执行结束, 休息10分钟')
    sleep(60*10)

# 用Chrome浏览器打开登录页面
driver = webdriver.Chrome()
driver.maximize_window()
login_url = "https://login.sina.com.cn/signup/signin.php?entry=sso"
driver.get(login_url)

# 登录页面
WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('username')).send_keys('18507138053')
WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('password')).send_keys('Ww,.941025')
WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('#vForm > div.main_cen > div > ul > li:nth-child(8) > div.btn_mod > input')).click()
print('---进入新浪个人中心---')

# 进入我的微首页
weibo = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/ul/li[1]/a'))
ActionChains(driver).move_to_element(weibo).perform() 
weibo.click()
print('---进入微博首页---')

# 切换窗口到微博首页
handles = driver.window_handles
wb = handles[1]
driver.switch_to.window(wb)

# 点击原创
original = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="v6_pl_content_homefeed"]/div/div[1]/div/ul/li[3]/a'))
original.click()
print('---进入原创页面---')
time.sleep(2)

# 初次启动，只抓取24小时内的微博
last_time = int(time.time()) - 60*60*24
while True:
    loop(driver, last_time)
