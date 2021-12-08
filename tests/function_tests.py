import pytest
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from time import sleep

# User fixture
@pytest.fixture
def user1():
    return  {'username':'zachg', 'firstname':'Zach', 'lastname':'Griswold', 'email':'zachg@wsu.edu', 'phone':'5413906454', 'wsuid':'11111111', 'password':'strongpassword'}

# User fixture
@pytest.fixture
def user2():
    return  {'username':'blaket', 'firstname':'Blake', 'lastname':'Calvin', 'email':'blaket@wsu.edu', 'phone':'1234567890', 'wsuid':'12345678', 'password':'alsostrongpassword', 'faculty':True}

 # Post fixture
@pytest.fixture
def post1():
    return {'title': 'open position',
            'description': 'this position is for smart people only.' ,
            'startdate': '10-21-2021',
            'enddate': '10-31-2021',
            'timecommitment': '7',
            'qualifications': 'gotta be sooper smart'
            }

 # Post fixture
@pytest.fixture
def post2():
    return {'title': 'open position 2',
            'description': 'this position is also for smart people only.' ,
            'startdate': '10-22-2021',
            'enddate': '11-3-2021',
            'timecommitment': '5',
            'qualifications': 'gotta be sooper dooper smart'
            }

 # Post fixture
@pytest.fixture
def post3():
    return {'title': 'open position 3',
            'description':  """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc pretium est velit, ut rutrum nulla venenatis nec. Quisque blandit pharetra orci. Duis gravida nunc non mattis ornare. Cras tempus enim eget est gravida, et interdum neque sodales. Duis velit libero, rutrum ut posuere a, mattis ut enim. In hac habitasse platea dictumst. Proin at felis velit.
                            Vivamus elementum ipsum porta molestie malesuada. Nam a neque suscipit, venenatis mi nec, tempus turpis. Praesent laoreet ultrices purus, sagittis mattis odio varius placerat. Nam faucibus leo sed consectetur lacinia. In porta porttitor pulvinar. Integer non lorem nec odio sodales tempus eget ac urna. Morbi ac tellus nisl. Vivamus iaculis efficitur ultricies. Cras eleifend
                            uis ipsum et dictum. Donec a accumsan tellus, ac aliquet diam. Curabitur in rhoncus elit. Sed erat nulla, volutpat et dapibus vel, porttitor eget dolor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vestibulum eros sagittis accumsan iaculis. Fusce ac pretium enim, nec dapibus risus. Fusce malesuada vitae ligula vitae dictum.
                            Sed ornare mi pellentesque gravida mollis. Vivamus nec euismod nunc. Vestibulum imperdiet interdum efficitur. Morbi a sem quam. Cras commodo justo at iaculis blandit. Nunc magna ante, ultricies at finibus quis, bibendum non odio. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nulla euismod leo ut magna lobortis aliquam.
                            Nulla vitae elit posuere, lobortis magna a, volutpat nulla. Vivamus eget massa sollicitudin, condimentum sapien eget, ultrices lacus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Fusce mollis vitae ligula ut tempor. Integer sit amet massa et diam fringilla convallis. Mauris ac sapien libero.""" ,
            'startdate': '10-11-2021',
            'enddate': '10-18-2021',
            'timecommitment': '1',
            'qualifications': 'gotta be sooper dumb'
            }


# """
# Download the chrome driver and make sure you have chromedriver executable in your PATH variable.
# To download the ChromeDriver to your system navigate to its download page.
# https://sites.google.com/a/chromium.org/chromedriver/home
# """
@pytest.fixture
def browser():
    CHROME_PATH = "C:\Program Files (x86)\Google\Chrome\Application"
    print(CHROME_PATH)
    opts = Options()
    opts.headless = False
    driver = webdriver.Chrome(options=opts, executable_path = CHROME_PATH + '\chromedriver.exe')
    driver.implicitly_wait(10)

    yield driver

    # For cleanup, quit the driver
    driver.quit()


def test_register_form(browser,user2):
    # test_user_1 = {'username':'ay1', 'email':'arslanay@wsu.edu', 'password':'strongpassword'}

    browser.get('http://localhost:5000/register')
    # Enable this to maximize the window
    # browser.maximize_window()
    browser.find_element_by_name("username").send_keys(user2['username'])
    sleep(2)
    browser.find_element_by_name("firstname").send_keys(user2['firstname'])
    sleep(2)
    browser.find_element_by_name("lastname").send_keys(user2['lastname'])
    sleep(2)
    browser.find_element_by_name("email").send_keys(user2['email'])
    sleep(2)
    browser.find_element_by_name("phone").send_keys(user2['phone'])
    sleep(2)
    browser.find_element_by_name("wsuid").send_keys(user2['wsuid'])
    sleep(2)
    browser.find_element_by_name("password").send_keys(user2['password'])
    sleep(2)
    browser.find_element_by_name("password2").send_keys(user2['password'])
    sleep(2)
    browser.find_element_by_name("submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    # print(content)
    assert 'Congratulations, you are now a registered user!' in content

def test_register_error(browser,user2):
    browser.get('http://localhost:5000/register')
    browser.find_element_by_name("username").send_keys(user2['username'])
    sleep(2)
    browser.find_element_by_name("firstname").send_keys(user2['firstname'])
    sleep(2)
    browser.find_element_by_name("lastname").send_keys(user2['lastname'])
    sleep(2)
    browser.find_element_by_name("email").send_keys(user2['email'])
    sleep(2)
    browser.find_element_by_name("phone").send_keys(user2['phone'])
    sleep(2)
    browser.find_element_by_name("wsuid").send_keys(user2['wsuid'])
    sleep(2)
    browser.find_element_by_name("password").send_keys(user2['password'])
    sleep(2)
    browser.find_element_by_name("password2").send_keys(user2['password'])
    sleep(2)
    browser.find_element_by_name("submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    assert 'Register' in content
    assert '[Please use a different username.]' in content

def test_login_form(browser,user2):
    browser.get('http://localhost:5000/login')
    browser.find_element_by_name("username").send_keys(user2['username'])
    sleep(2)
    browser.find_element_by_name("password").send_keys(user2['password'])
    sleep(2)
    browser.find_element_by_name("remember_me").click()
    sleep(2)
    button = browser.find_element_by_name("submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    assert 'Welcome to Undergrad Research Portal!' in content
    assert user2['username'] in content

def test_invalidlogin(browser,user2):
    browser.get('http://localhost:5000/login')
    browser.find_element_by_name("username").send_keys(user2['username'])
    sleep(2)
    browser.find_element_by_name("password").send_keys('wrongpassword')
    sleep(2)
    browser.find_element_by_name("remember_me").click()
    sleep(2)
    browser.find_element_by_name("submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    assert 'Invalid username or password' in content
    assert 'Sign In' in content

def test_post(browser,user2,post1):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element_by_name("username").send_keys(user2['username'])
    browser.find_element_by_name("password").send_keys(user2['password'])
    browser.find_element_by_name("remember_me").click()
    browser.find_element_by_name("submit").click()

    browser.get('http://localhost:5000/post')
    browser.find_element_by_name("title").send_keys(post1['title'])
    sleep(2)
    browser.find_element_by_name("description").send_keys(post1['description'])
    sleep(2)
    browser.find_element_by_name("startdate").send_keys(post1['startdate'])
    sleep(2)
    browser.find_element_by_name("enddate").send_keys(post1['enddate'])
    sleep(2)
    browser.find_element_by_name("timecommitment").send_keys(post1['timecommitment'])
    sleep(2)
    ResearchFields = browser.find_element_by_name("ResearchFields").click()
    sleep(2)
    browser.find_element_by_name("qualifications").send_keys(post1['qualifications'])
    sleep(2)
    browser.find_element_by_name("submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    assert post1['title'] in content
    assert post1['body'] in content

def post_2(browser,user2,post2):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element_by_name("username").send_keys(user2['username'])
    browser.find_element_by_name("password").send_keys(user2['password'])
    browser.find_element_by_name("remember_me").click()
    browser.find_element_by_name("submit").click()

    browser.get('http://localhost:5000/post')
    browser.find_element_by_name("title").send_keys(post2['title'])
    sleep(2)
    browser.find_element_by_name("description").send_keys(post2['description'])
    sleep(2)
    browser.find_element_by_name("startdate").send_keys(post2['startdate'])
    sleep(2)
    browser.find_element_by_name("enddate").send_keys(post2['enddate'])
    sleep(2)
    browser.find_element_by_name("timecommitment").send_keys(post2['timecommitment'])
    sleep(2)
    ResearchFields = browser.find_element_by_name("ResearchFields").click()
    sleep(2)
    browser.find_element_by_name("qualifications").send_keys(post2['qualifications'])
    sleep(2)
    browser.find_element_by_name("submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    assert post2['title'] in content
    assert post2['body'] in content

def test_post_error(browser,user2,post3):
    #first login
    browser.get('http://localhost:5000/login')
    browser.find_element_by_name("username").send_keys(user2['username'])
    browser.find_element_by_name("password").send_keys(user2['password'])
    browser.find_element_by_name("remember_me").click()
    browser.find_element_by_name("submit").click()

    browser.get('http://localhost:5000/post')
    browser.find_element_by_name("title").send_keys(post3['title'])
    sleep(2)
    browser.find_element_by_name("description").send_keys(post3['description'])
    sleep(2)
    browser.find_element_by_name("startdate").send_keys(post3['startdate'])
    sleep(2)
    browser.find_element_by_name("enddate").send_keys(post3['enddate'])
    sleep(2)
    browser.find_element_by_name("timecommitment").send_keys(post3['timecommitment'])
    sleep(2)
    ResearchFields = browser.find_element_by_name("ResearchFields").click()
    sleep(2)
    browser.find_element_by_name("qualifications").send_keys(post3['qualifications'])
    sleep(2)
    browser.find_element_by_name("submit").click()
    sleep(5)
    #verification
    content = browser.page_source
    assert "[Field must be between 1 and 1500 characters long.]" in content


if __name__ == "__main__":
    retcode = pytest.main()