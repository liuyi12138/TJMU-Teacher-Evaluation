import time
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://curriculum.hust.edu.cn/")

ACCOUNT = " " #学号
PASSWORD = " " #统一认证平台密码
TEACHER = 1 #要评价某一科目的第几个老师,最小值为 1 

def login(): 
    driver.find_element_by_class_name('login_box_landing_btn').click()
    account = driver.find_element_by_id("username_text")
    account.send_keys(ACCOUNT)
    password = driver.find_element_by_id("password_text")
    password.send_keys(PASSWORD)
    driver.find_element_by_class_name('login_box_landing_btn').click()
    driver.find_elements_by_class_name('buttonDivLeft')[2].click()
    print("\n 登陆成功!\n")


def evaluationAll(): #遍历page
    pageNum = 1
    nextBtn = driver.find_element_by_class_name('buttonRight')
    while(nextBtn.get_attribute('style') == "cursor: pointer;"):
        evaluationPage(pageNum)
        nextBtn.click()
        pageNum += 1
        nextBtn = driver.find_element_by_class_name('buttonRight')
    evaluationPage(pageNum)

def evaluationPage(pageNum): #获取page中课程列表
    try:
        time.sleep(0.3)
        items = driver.find_elements_by_xpath('//td[@class = "tableSM"]/div')

        for item in items:
            itemName = driver.find_elements_by_class_name('tableTitleDIV_green')[items.index(item)].text
            if(item.text == "评价" or item.text == "未评完"):
                print(itemName + "开始评教")
                itemId = item.get_attribute('onclick')[13:20]
                evaluation(itemId,pageNum)
                print(itemName + "评教已完成")
            else:
                print(itemName + "评教已完成")
        print("\n")
    except:
        evaluationPage(pageNum)
    else:
        return


def evaluation(itemId,page): #对某课程进行评教
    
    itemIdStr = "http://curriculum.hust.edu.cn/wspj/awspj.jsp?kcdm=" + str(itemId) + "&xnxq=20182&pjlc=2018201&num=" + str(TEACHER - 1) + "&pjlx=01"
    js='window.open( \"' + itemIdStr + '\")'

    driver.execute_script(js)
    driver.switch_to.window(driver.window_handles[-1])
    
    time.sleep(0.2)
    for i in range(10):
        tempStr = '//td[@id = \"pjxx' + str(i)  + '\"]/input'
        item = driver.find_elements_by_xpath(tempStr)
        if(len(item) != 0):
            item[0].click() #修改此处可以改变评教等级 默认为优秀
            time.sleep(0.1)
    driver.find_elements_by_class_name('buttonDivLeft')[1].click()
    driver.switch_to.alert.accept()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)


login()
evaluationAll()
