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

def get_element(driver, element, xpath):
    flag = True
    while flag:
        try:
            tag = WebDriverWait(element, 10).until(lambda x: x.find_element_by_xpath(xpath))
            return tag
        except:
            driver.refresh()

# 点赞操作
def praise(driver, element):
    praise = WebDriverWait(element, 10).until(lambda x: x.find_element_by_xpath('div[@class="WB_feed_handle"]/div/ul/li[4]/a'))
    if praise.get_attribute('title') == '赞':
        confirm(driver)
        praise.click()
        while confirm(driver):
            praise.click()
        print('  -----成功点赞！')
    print('  ----已赞！')
    time.sleep(2)

# 转发操作
def repost(driver, element):
	flag = True
	while flag:
		try:
			ActionChains(driver).move_to_element(element).perform()
			repost = WebDriverWait(element, 10).until(lambda x: x.find_element_by_xpath('div[@class="WB_feed_handle"]/div/ul/li[2]/a'))
			confirm(driver)
			repost.click()
			while confirm(driver):
				repost.click()
			path = '//*[@class="W_layer "]/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[1]/a'
			post = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(path))
			post.click()
			print('  -----完成转发！')
			flag = False
			time.sleep(2)
		except:
			print('<----转发失败，刷新重试！---->')
			driver.refresh()

def add(element, follows):
	ActionChains(driver).move_to_element(element).perform()
	href = element.find_element_by_xpath('div[1]/div[@class="WB_detail"]/div[3]/a').get_attribute('href')
	follows.append(href)
	print('  -----完成保存需要关注的微博！')

# 关注新用户操作
def follow(driver, follows):
    print(' ----处理需要关注人列表！')
    if len(follows) == 0:
        print('  ----此次不需要关注操作！')
        return
    for follow in follows:
        js='window.open("%s");' % follow
        print('   ----打开需要关注人主页: ', follow)
        driver.execute_script(js)
        handles = driver.window_handles
        driver.switch_to.window(handles[2])
        gz = get_element(driver, element, '//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[4]/div/div[1]/a[1]')
        # gz = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[4]/div/div[1]/a[1]'))
        if ((gz.text == '已关注') or (gz.text == 'Y已关注')):
        	print('    ----已关注博主，无需重复操作！')
        else:
            gz.click()
            print('    -----新关注一名用户！')
        driver.close()
        driver.switch_to.window(handles[1])
    print('    -----关注操作完成，关闭当前窗口并切换至首页窗口！')
    time.sleep(2)

def operation(elements, last_time):
    i = 0
    follows = []
    max_time = last_time
    for element in elements:
        i += 1
        ActionChains(driver).move_to_element(element).perform()
        flag = True
        while flag:
            try:
                date = WebDriverWait(element, 10).until(lambda x: x.find_element_by_xpath('div[1]/div[@class="WB_detail"]/div[2]/a[1]').get_attribute('date')) #element.find_element_by_xpath('div[1]/div[@class="WB_detail"]/div[2]/a[1]').get_attribute('date')
                flag = False
            except:
                print('<----找不到日期标签！---->')
                driver.refresh()
        date = int(int(date)/1000)
        if date > last_time:
            if date > max_time:
                max_time = date
                print('更新当前max_time：', max_time)
            text = element.find_element_by_xpath('div[1]/div[@class="WB_detail"]/div[3]').text.strip()
            if (text.find('抽') != -1) or (text.find('送') != -1) or (text.find('开') != -1):
                time.sleep(1)
                print('---抽奖微博, 执行操作！---')
                if text.find('赞') != -1:
                    print(' ------需要点赞！！！', i)
                    praise(driver, element)
                if text.find('转') != -1:
                    print(' ------需要转发！！！', i)
                    repost(driver, element)
                if text.find('关注') != -1:
                    print(' ------需要关注！！！', i)
                    add(element, follows)
        else:
            print('---以前的微博，忽略！---')
        time.sleep(3)
    last_time = max_time
    print('更新last_time：', last_time)
    follow(driver, follows)

# 执行操作的循环
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
    if len(elements) > 0:
        operation(driver, elements, last_time)
        print('本次执行结束！')
    else:
        print('本次没有更新微博，不需要操作！')
    # 间隔1小时
    time.sleep(60*60)

# 用Chrome浏览器打开登录页面
driver = webdriver.Chrome()
# driver.maximize_window()
login_url = "https://login.sina.com.cn/signup/signin.php?entry=sso"
driver.get(login_url)

# 登录页面
WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('username')).send_keys('username')
WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('password')).send_keys('password')
WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('#vForm > div.main_cen > div > ul > li:nth-child(8) > div.btn_mod > input')).click()
print('---进入新浪个人中心---')

# 进入我的微首页
flag = True
while flag:
	try:
		weibo = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/ul/li[1]/a'))
		ActionChains(driver).move_to_element(weibo).perform() 
		weibo.click()
		print('---进入微博首页---')
		flag = False
	except:
		print('<----我的新浪首页加载失败，刷新重试---->')
		driver.refresh()

# 切换窗口到微博首页
handles = driver.window_handles
wb = handles[1]
driver.switch_to.window(wb)

# 点击原创
flag = True
while flag:
	try:
		original = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="v6_pl_content_homefeed"]/div/div[1]/div/ul/li[3]/a'))
		original.click()
		print('---进入原创页面---')
		flag = False
		time.sleep(2)
	except:
		print('<----我的微博首页加载失败，刷新重试---->')
		driver.refresh()

# 初次启动，只抓取24小时内的微博
last_time = int(time.time()) - 60*60*24
while True:
    loop(driver, last_time)

