from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time

def confirm(driver):
    print(' ----处理提示框！')
    try:
        # confirm = driver.find_element_by_xpath('//*[@class="W_layer_btn S_bg1"]/a')
        confirm = WebDriverWait(driver, 1).until(lambda x: x.find_element_by_xpath('//*[@class="W_layer_btn S_bg1"]/a'))
        confirm.click()
    except:
        pass
    time.sleep(1)

def follow(follows):
    print(' ----处理需要关注人列表！')
    for follow in follows:
        driver.get(follow)
        gz = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[4]/div/div[1]/a[1]'))
        time.sleep(2)

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

# 获取当前页的所有用户微博
for i in range(3):
    js = "window.scrollTo(0, document.body.scrollHeight)"
    driver.execute_script(js)
    time.sleep(2)
elements = driver.find_elements_by_xpath('//*[@id="v6_pl_content_homefeed"]/div/div[3]/div')
elements = elements[:len(elements)-2]
print('---共获取到 %d 条原创微博---' % len(elements))
i = 0
follows = []
for element in elements:
    i += 1
    feed_handle = element.find_element_by_xpath('//div[@class="WB_feed_handle"]')
    # driver.execute_script("arguments[0].scrollIntoView();", element)
    ActionChains(driver).move_to_element(element).perform()
    # ActionChains(driver).move_to_element(feed_handle).perform()
    date = element.find_element_by_xpath('//div[@class="WB_detail"]/div[2]/a[1]').text.split(' ')
    # print('第 %d 条原创微博， 发表时间为：%s' % (i, date))
    # print("第 %d 条原创微博: %s" % (i, element.text))
    if (len(date) < 2) or date[0] == '今天':
        text = element.find_element_by_xpath('//div[@class="WB_detail"]/div[3]').text.strip()
        if (text.find('抽') != -1) or (text.find('送') != -1) or (text.find('开') != -1):
            time.sleep(1)
            if text.find('赞') != -1:
                print(' ------需要点赞！！！', i)
                confirm(driver)
                zan = WebDriverWait(feed_handle, 10).until(lambda x: x.find_element_by_xpath('div/ul/li[4]/a'))
                ActionChains(driver).move_to_element(zan).perform()
                zan.click()
                print(' -----完成点赞！')
            if text.find('转') != -1:
                print(' ------需要转发！！！', i)
                confirm(driver)
                repost = WebDriverWait(feed_handle, 10).until(lambda x: x.find_element_by_xpath('div/ul/li[2]/a'))
                repost.click()
                path = '//*[@class="W_layer "]/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[1]/a'
                post = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(path))
                post.click()
                print(' -----完成转发！')
            if text.find('关注') != -1:
                print(' ------需要关注！！！', i)
                confirm(driver)
                href = element.find_element_by_xpath('//div[@class="WB_detail"]/div[3]/a').get_attribute('href')
                follows.append(href)
                print("follows: ", follows)
                print(' -----完成关注保存！')
    else:
        continue
    time.sleep(3)

follow(follows)

print('执行结束')
# driver.quit()
