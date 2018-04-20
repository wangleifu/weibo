from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time

# 如果有操作太快的提示框，点击确定
def confirm(driver):
    try:
        confirm = WebDriverWait(driver, 3).until(lambda x: x.find_element_by_xpath('//*[@class="W_layer_btn S_bg1"]/a'))
        confirm.click()
        print(' ----处理提示框！')
        return True
    except:
        return False

def get_element(driver, xpath):
    flag = True
    while flag:
        try:
            tag = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(xpath))
            return tag
        except:
            time.sleep(2)
            print('当前标签获取失败，刷新重试！')
            driver.refresh()

def get_elements(driver, xpath):
    flag = True
    while flag:
        try:
            tags = WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_xpath(xpath))
            flag = False
            return tags
        except:
            time.sleep(2)
            print('当前标签集获取失败，刷新重试！')
            driver.refresh()

# 点赞操作
def praise(driver, element):
    ActionChains(driver).move_to_element(element).perform()
    praise = WebDriverWait(element, 10).until(lambda x: x.find_element_by_xpath('div[@class="WB_feed_handle"]/div/ul/li[4]/a'))
    if praise.get_attribute('title') == '赞':
        confirm(driver)
        praise.click()
        while confirm(driver):
            praise.click()
        print('  -----成功点赞！')
    else:
        print('  -----已赞！')
    time.sleep(2)

# 转发操作
def repost(driver, element):
	flag = True
	while flag:
		try:
			confirm(driver)
			ActionChains(driver).move_to_element(element).perform()
			repost = WebDriverWait(element, 10).until(lambda x: x.find_element_by_xpath('div[@class="WB_feed_handle"]/div/ul/li[2]/a'))
			confirm(driver)
			repost.click()
			while confirm(driver):
				repost.click()
			textarea_path = '//div[@class="p_input p_textarea"]/textarea'
			textarea = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(textarea_path))
			textarea.send_keys('抽我！抽我！！抽我！！！')
			time.sleep(1)
			checkbox_path = '//*[@id="forward_comment_opt_originLi"]'
			checkbox = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(checkbox_path))
			checkbox.click()
			time.sleep(1)
			path = '//div[@class="btn W_fr"]/a[@class="W_btn_a"]'
			post = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(path))
			post.click()
			print('  -----完成转发！')
			flag = False
			time.sleep(2)
		except:
			print('<----转发失败！---->')
			text = element.find_element_by_xpath('div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_text W_f14"]').strip().text
			print('   微博内容如下：')
			print('        ', text)
			return

def add(element, follows):
    try:
        a_tags = element.find_elements_by_xpath('a')
    except:
        a_tags = []

    if len(a_tags) == 1:
        href = a_tags[0].get_attribute('href')
        follows.append(href)
        print('  -----保存需要关注人的微博: ', a_tags[0].text)
    else:
        for a_tag in a_tags:
            if a_tag.text.startswith("@"):
                if not a_tag.text.startswith('@微博抽奖平台'):
                    href = a_tag.get_attribute('href')
                    follows.append(href)
                    print('  -----保存需要关注人的微博: ', a_tag.text)

# 关注新用户操作
def follow(driver, follows):
    print(' ----处理需要关注人列表！')
    if len(follows) == 0:
        print('  ----此次没有需要关注的人！')
        return
    for follow in follows:
        js='window.open("%s");' % follow
        print('   ----打开需要关注人主页: ', follow)
        driver.execute_script(js)
        handles = driver.window_handles
        driver.switch_to.window(handles[2])
        gz = get_element(driver, '//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[4]/div/div[1]/a[1]')
        # gz = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[4]/div/div[1]/a[1]'))
        if ((gz.text == '+关注') or (gz.text == '关注')):
            gz.click()
            print('    ----新关注一名用户!')
        else:
            print('    -----已关注博主，无需重复操作！')
        driver.close()
        driver.switch_to.window(handles[1])
    print('    -----完成对关注人列表的关注！')
    follows = []
    time.sleep(2)

def operation(driver, elements, last_time):
    i = 0
    m = len(elements)
    follows = []
    max_time = last_time
    for element in elements:
        i += 1
        ActionChains(driver).move_to_element(element).perform()
        flag = True
        while flag:
            try:
                date = WebDriverWait(element, 10).until(lambda x: x.find_element_by_xpath('div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[2]/a[1]'))
                flag = False
            except:
                print('<----找不到日期标签！---->')
                continue
        if (date.text.find('推荐') != -1):
        	continue
        date = date.get_attribute('date')

        date = int(int(date)/1000)
        if date > last_time:
            if date > max_time:
                max_time = date
                print('更新当前max_time：', max_time)
            text_div = element.find_element_by_xpath('div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_text W_f14"]')
            text = text_div.text.strip()
            if (text.find('抽') != -1) or (text.find('送') != -1) or (text.find('开') != -1):
                time.sleep(1)
                print('---抽奖微博, 执行操作！---')
                if text.find('赞') != -1:
                    print(' ------点赞！！！', i)
                    praise(driver, element)
                if (text.find('转') != -1) or (text.find('评论') != -1):
                    print(' ------转发+评论！！！', i)
                    repost(driver, element)
                if text.find('关注') != -1:
                    print(' ------保存关注！！！', i)
                    add(text_div, follows)
        else:
            print('---以前的微博，忽略！---')
            break
        time.sleep(3)
    if i == m:
    	print('<----抓取下一页---->')
    	try:
    		next_page = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//a[@class="page next S_txt1 S_line1"]'))
    		ActionChains(driver).move_to_element(next_page).perform()
    		next_page.click()
    		time.sleep(3)
    		loop(driver, last_time)
    	except:
    		print('找不到下一页标签！')

    follow(driver, follows)
    return max_time

# 执行操作的循环
def loop(driver, last_time):
    # 刷新出本页所有微博
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        print('-----下拉加载页面！')
        time.sleep(3)

    # 获取当前页的所有用户微博
    # elements = driver.find_elements_by_xpath('//*[@id="v6_pl_content_homefeed"]/div/div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div')
    elements = get_elements(driver, '//div[@id="v6_pl_content_homefeed"]/div[1]/div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div')
    elements = elements[:-2]
    print('---共获取到 %d 条原创微博---' % len(elements))

    # 爬取所有微博并对符合要求的微博（抽奖微博）进行相应的操作
    if len(elements) > 0:
        max_time = operation(driver, elements, last_time)
    else:
        print('无法获取微博内容！')
    return max_time



# 用Chrome浏览器打开登录页面
driver = webdriver.Chrome()
driver.maximize_window()
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
		time.sleep(2)
		print('<----我的新浪首页加载失败，刷新重试---->')
		driver.refresh()

# 切换窗口到微博首页
handles = driver.window_handles
wb = handles[1]
driver.switch_to.window(wb)

# 初次启动，只抓取24小时内的微博
try:
	with open('time.txt','r') as f:
		last_time = int(f.read())
except:
	last_time = int(time.time()) - 60*60*24



while True:

	# 点击原创
	flag = True
	while flag:
		try:
			original = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//ul[@class="tab W_fl clearfix"]/li[3]/a'))
			ActionChains(driver).move_to_element(original).perform()
			print('---进入原创页面---')
			original.click()
			flag = False
			time.sleep(2)
		except:
			time.sleep(2)
			print('<----我的微博首页，原创微博页面加载失败，刷新重试---->')
			driver.refresh()

	last_time = loop(driver, last_time)

	# 保存上次最新微博的时间，下次之对更新微博进行操作
	with open('time.txt','w') as f:
		f.write(str(last_time))
		print('更新last_time：', last_time)

	print('本次执行结束，休息30分钟后继续！')
	# 间隔半小时
	time.sleep(60*30)

