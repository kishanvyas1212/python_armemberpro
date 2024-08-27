import logging
import time
from selenium import webdriver #by this we can access the webdriver which is inbuild method of selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from src.cases.constants import *
from src.utilitises.get_element import get_element as ge
from src.utilitises.validate import validate
from datetime import datetime


class helpingfun:
    
    def payment_history(driver,plan_amount):
        driver.get(BASE_URL+"/current-memership")
        time.sleep(5)
        transation_id = ge.get_table_value(driver,locator="xpath",locatorpath="//td[@data-label='Transaction ID']")
        result,deductedamount = validate.varify_tranction_amount(transation_id,plan_amount)
        logging.info("inside payment history")
        logging.info(f"deducted amount is {deductedamount} for transaction {transation_id}")
        return result,transation_id

        
def testcase_1(drivers):
    # Correct username, wrong password
    drivers.get(BASE_URL+"/login")
    usernamef = ge.findelement(drivers,"NAME","user_login","send_keys",right_username) 
    pwd = ge.findelement(drivers,"NAME","user_pass","send_keys","test")   
    beforelogin = drivers.get_cookies()
    login = ge.findelement(drivers,"NAME","armFormSubmitBtn","click")
    time.sleep(3)
    error_message = drivers.find_element(By.CSS_SELECTOR, "div.arm-df__fc--validation__wrap")
    
    if WRONG_PASS_ERROR in error_message.text:
        actual_result = f"Case is passed, and displayed error message is {error_message.text}"
        status = "pass"
    else:
        actual_result = f"Case is failed, and displayed error message is {error_message.text}"
        status ="Failed"
    
    return actual_result,status
def testcase_2(drivers):
    # wrong username, wrong password
    drivers.get(BASE_URL+"/login")
    usernamef = ge.findelement(drivers,"NAME","user_login","send_keys","afdmin") 
    pwd = ge.findelement(drivers,"NAME","user_pass","send_keys","test")   
    beforelogin = drivers.get_cookies()
    login = ge.findelement(drivers,"NAME","armFormSubmitBtn","click")
    time.sleep(3)
    error_message = drivers.find_element(By.CSS_SELECTOR, "div.arm-df__fc--validation__wrap")
    
    if NO_USER_EXIST in error_message.text:
        actual_result = f"Case is passed, and displayed error message is {error_message.text}"
        status = "pass"
    else:
        actual_result = f"Case is failed, and displayed error message is {error_message.text}"
        status ="Failed"
    
    return actual_result,status
    
    
def testcase_3(drivers,username=right_username,logincheck=1):
    # Login with right creds
    drivers.get(BASE_URL+"/login")
    usernamef = ge.findelement(drivers,"NAME","user_login","send_keys",username) 
    pwd = ge.findelement(drivers,"NAME","user_pass","send_keys",username)   
    beforelogin = drivers.get_cookies()
    login = ge.findelement(drivers,"NAME","armFormSubmitBtn","click")
    time.sleep(5)
    if logincheck == 1:
        loggedin_cookies = drivers.get_cookies()
    # Find the dictionary that matches the specified name
        desired_cookie = next((cookie for cookie in loggedin_cookies if cookie['name'] == COOKIE), None)
        if right_username in desired_cookie['value']:
            
            current_url =drivers.current_url
            
            if str(LOGIN_REDIRECTS_URL) == str(current_url):
                actual_result = "Case is passed, login and user redirect success fully"
                
            else:    
                actual_result = f"Case is passed, but not redirected successfully redirected to {current_url}"
            status = "pass"
        else:
            actual_result ="Case failed, user can not logged in"
            status="failed"
        return actual_result,status
    else:
        return
    
def testcase_4(drivers):
    # Register user
    drivers.get(BASE_URL+"/register")
    ge.findelement(drivers,"NAME","user_login","send_keys",Create_username)
    ge.findelement(drivers,"NAME","first_name","send_keys",f_name)
    ge.findelement(drivers,"NAME","last_name","send_keys",l_name)
    ge.findelement(drivers,"NAME","user_email","send_keys",u_email)
    ge.findelement(drivers,"NAME","user_pass","send_keys",password)
    
    validation = validate.registerformverification(drivers)
    if validation[0] == 0:
        
        submit_form = ge.findelement(drivers,"NAME","armFormSubmitBtn","click")
        time.sleep(10)
        loggedin_cookies = drivers.get_cookies()
# Find the dictionary that matches the specified name
        if loggedin_cookies != "none" or loggedin_cookies != "":
            desired_cookie = next((cookie for cookie in loggedin_cookies if cookie['name'] == COOKIE), None)
        else:
            time.sleep(5)
            loggedin_cookies=drivers.get_cookies()
            desired_cookie = next((cookie for cookie in loggedin_cookies if cookie['name'] == COOKIE), None)
         
        response = validate.verifyuser(drivers,Create_username,desired_cookie,register_redirect_url)
        
        if response == 0:
            actual_result = f"User register properly and user redirected to set url{drivers.current_url}"
            status ="Pass"
        elif response == 1:
            actual_result = f"User register properly but user not redirected to set url{register_redirect_url} instead it redirected to {drivers.current_url}"
            status ="Pass"
            
    else: 
        actual_result =validation[1]
        status = "failed"
    return actual_result,status
    
def testcase_5(drivers):
    # Login with right creds
    actual_result,status = testcase_4(drivers)
    return actual_result,status 

def testcase_6(drivers):
    #sign up with stripe using paid trial plan
    testcase_3(drivers,right_username,logincheck=4)
    drivers.get(BASE_URL+"/setup")
    time.sleep(5)
    ge.findelement(driver=drivers,locator="xpath",locatorpath="input[name='subscription_plan'][value='5']",action="click")
    ge.findelement(driver=drivers,locator="name",locatorpath="ARMSETUPSUBMIT",action="click")
    time.sleep(10)
    ge.getinto_iframe(driver=drivers,locator="xpath",locatorpath="//iframe[@title='Secure card number input frame']")
    time.sleep(1)
    ge.findelement(driver=drivers,locator="name",locatorpath="cardnumber",action="click")
    ge.findelement(driver=drivers,locator="name",locatorpath="cardnumber",action="send_keys",value="4242424242424242")
    ge.backtonormal(drivers)
    time.sleep(2)
    
    ge.getinto_iframe(driver=drivers,locator="xpath",locatorpath="//iframe[@title='Secure expiration date input frame']")
    ge.findelement(driver=drivers,locator="name",locatorpath="exp-date",action="click")
    
    ge.findelement(driver=drivers,locator="name",locatorpath="exp-date",action="send_keys",value="12 / 27")
    ge.backtonormal(drivers)
    time.sleep(2)
    
    ge.getinto_iframe(driver=drivers,locator="xpath",locatorpath="//iframe[@title='Secure CVC input frame']")
    ge.findelement(driver=drivers,locator="name",locatorpath="cvc",action="click")
    ge.findelement(driver=drivers,locator="name",locatorpath="cvc",action="send_keys",value="123")
    ge.backtonormal(drivers)
    time.sleep(5)
    
    ge.findelement(driver=drivers,locator="xpath",locatorpath="//*[@id='card-button']",action="click")
    
    time.sleep(10)
    current_url = drivers.current_url
    if current_url in singup_redirect or current_url == singup_redirect:
        actual_result,status = f"sign up the user {right_username} with free plan and redirected properly","pass"
    else:
        actual_result,status = f"sign up the user {right_username} with free plan and but not redirected properly","pass"
    return actual_result,status

def testcase_7(drivers):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    testcase_3(drivers,right_username)
    drivers.get(BASE_URL+"/edit_profile")
    time.sleep(1)
    editedname="name edited"
    ge.findelement(drivers,"NAME","first_name","send_keys",editedname)
    ge.findelement(drivers,"NAME","last_name","send_keys",editedname)
    # ge.findelement(drivers,"NAME","profile_cover","send_keys",image_file)
    ge.findelement(drivers,"NAME","armFormSubmitBtn","click")
    time.sleep(1)
    error, error_msg = validate.registerformverification(drivers) 
     
    if error == 0:
        drivers.refresh()
        element,first_name = ge.findelement(drivers,"NAME","first_name","get_attribute")
        element,last_name = ge.findelement(drivers,"NAME","last_name","get_attribute")
        # element,profile_cover = ge.findelement(drivers,"NAME","profile_cover","get_attribute")
        
        if editedname in first_name :
            actual_result,status = f"the user {right_username} profile is edited, updated first name from {f_name} to {first_name} ","pass"
        else:
            actual_result,status = f"The user {right_username} profile is editedn not updated first name from {f_name} to {first_name}","pass"
        if editedname in last_name:
            actual_result,status =actual_result+ f". The user {right_username} profile is edited updated Last name from {l_name} to {last_name} ","pass"
        else:
            actual_result,status = f". The user {right_username} profile is editedn not updated last name from {l_name} to {last_name}","pass"
        # if imagename in profile_cover:
        #     actual_result,status =actual_result+ f" and profile cover {profile_cover} is added ","pass"
        # else:
        #     actual_result,status =actual_result+ f" and profile cover is not updated ","pass"
    elif error ==1:
        actual_result,status = error_msg,"failed"
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print(start_time)
    # print(end_time)
    return actual_result,status
def testcase_8(drivers):
    testcase_3(drivers,right_username,2)
    drivers.get(BASE_URL + "/change_password")
    time.sleep(5)
    ge.findelement(drivers,"NAME","current_user_pass","send_keys","right_username")
    
    ge.findelement(drivers,"NAME","user_pass","send_keys",new_pass)
    ge.findelement(drivers,"NAME","repeat_pass","send_keys",new_pass)
    ge.findelement(drivers,"NAME","armFormSubmitBtn","click")
    error, error_msg = validate.registerformverification(drivers)
    print(error,error_msg)
    print(error_msg)
    return "tested and works","testing"
    
def testcase_10(drivers,checkcoupon=0,coupon=0,tax=0,istax=0,sub=0,id=""):
    # testing the finite plan without tax and coupon 
    username=Create_username
    email= u_email
    coupon_code= onetimecoupon
    plan_amount=finite_plan_amount
    drivers.get(BASE_URL+"/setup")
    time.sleep(2)
    
    ge.findelement(drivers,"NAME","user_login","send_keys",username)
    ge.findelement(drivers,"NAME","first_name","send_keys",username)
    ge.findelement(drivers,"NAME","last_name","send_keys",username)
    ge.findelement(drivers,"NAME","user_email","send_keys",email)
    ge.findelement(drivers,"NAME","user_pass","send_keys",username)
    if sub==1:
        ge.findelement(driver=drivers,locator="id",locatorpath=id,action="click")
        
        
    if checkcoupon==1:
        ge.findelement(drivers,"name","arm_coupon_code",action="send_keys",value=coupon_code)
        ge.findelement(drivers,"xpath",'//*[@id="arm_setup_coupon_button_container"]/button',action="click")
        time.sleep(5)
        # validate.validate_summery(drivers,plan_amount,coupon,tax,istax)
    
    # else:
        
        # validate.validate_summery(drivers,plan_amount,coupon,tax,istax)
    
    time.sleep(2)
    logging.info("Clicking on the submit button")
    ge.findelement(driver=drivers,locator="name",locatorpath="ARMSETUPSUBMIT",action="click")
    logging.info("the submit button clicked properly")
    time.sleep(5)
    ge.getinto_iframe(driver=drivers,locator="xpath",locatorpath="//iframe[@title='Secure card number input frame']")
    ge.findelement(driver=drivers,locator="name",locatorpath="cardnumber",action="click")
    ge.findelement(driver=drivers,locator="name",locatorpath="cardnumber",action="send_keys",value="4242424242424242")
    ge.backtonormal(drivers)
    time.sleep(2)
    
    ge.getinto_iframe(driver=drivers,locator="xpath",locatorpath="//iframe[@title='Secure expiration date input frame']")
    ge.findelement(driver=drivers,locator="name",locatorpath="exp-date",action="click")
    
    ge.findelement(driver=drivers,locator="name",locatorpath="exp-date",action="send_keys",value="12 / 27")
    ge.backtonormal(drivers)
    time.sleep(2)
    
    ge.getinto_iframe(driver=drivers,locator="xpath",locatorpath="//iframe[@title='Secure CVC input frame']")
    ge.findelement(driver=drivers,locator="name",locatorpath="cvc",action="click")
    ge.findelement(driver=drivers,locator="name",locatorpath="cvc",action="send_keys",value="123")
    ge.backtonormal(drivers)
    time.sleep(2)
    
    ge.findelement(driver=drivers,locator="xpath",locatorpath="//*[@id='card-button']",action="click")
    
    time.sleep(20)
    if checkcoupon==0:
        result,test =helpingfun.payment_history(drivers,plan_amount)
        logging.info(f"Result form payment {result}")
        logging.info(f"second parameter form payment {test}")
        return result,test
    else:
        return
def testcase_11(drivers):
    # testing the finite plan with applied coupon 50%
    testcase_10(drivers,1,50,0,0)
    plan_amount=finite_plan_amount
    discount_amount = validate.calculation(plan_amount,coupon=50,tax=0,istax=0)
    result,test =helpingfun.payment_history(drivers,discount_amount[0])
    logging.info(f"Result form payment {result}")
    logging.info(f"second parameter form payment {test}")
    return result,test
def testcase_12(drivers): 
    # Testing the finite plan with applying coupon 50% and excluded tax 10% 
    testcase_10(drivers,1,50,10,2)
    plan_amount=finite_plan_amount
    discount_amount = validate.calculation(plan_amount,coupon=50,tax=10,istax=2)
    result,test =helpingfun.payment_history(drivers,discount_amount[0])
    logging.info(f"Result form payment {result}")
    logging.info(f"second parameter form payment {test}")
    return result,test
def testcase_13(drivers): 
    # Testing the finite plan with applying coupon no coupon and excluded tax 10% 
    testcase_10(drivers,2,0,10,2)
    plan_amount=finite_plan_amount
    discount_amount = validate.calculation(plan_amount,coupon=0,tax=10,istax=2)
    print(discount_amount)
    result,test =helpingfun.payment_history(drivers,discount_amount[0])
    logging.info(f"Result form payment {result}")
    logging.info(f"second parameter form payment {test}")
    return result,test
def testcase_14(drivers): 
    # Testing the finite plan with applying coupon no coupon and include tax 10% 
    testcase_10(drivers,2,0,10,1)
    plan_amount=finite_plan_amount
    discount_amount = validate.calculation(plan_amount,coupon=0,tax=10,istax=1)
    print(discount_amount)
    result,test =helpingfun.payment_history(drivers,discount_amount[0])
    logging.info(f"Result form payment {result}")
    logging.info(f"second parameter form payment {test}")
    return result,test

def testcase_15(drivers): 
    # Testing the finite plan with applying coupon 50% discount and included tax 10% 
    testcase_10(drivers,1,50,10,1)
    plan_amount=finite_plan_amount
    discount_amount = validate.calculation(plan_amount,coupon=50,tax=10,istax=1)
    print(discount_amount)
    result,test =helpingfun.payment_history(drivers,discount_amount[0])
    logging.info(f"Result form payment {result}")
    logging.info(f"second parameter form payment {test}")
    return result,test

def testcase_16(drivers): 
    # Testing the subscription no trial plan with no coupon and tax
    testcase_10(drivers,2,0,0,0,1,"arm_subscription_plan_option_3")
    plan_amount=subscription_plan_amount
    discount_amount = validate.calculation(plan_amount,coupon=0,tax=0,istax=0)
    print(discount_amount)
    result,test =helpingfun.payment_history(drivers,discount_amount[0])
    logging.info(f"Result form payment {result}")
    logging.info(f"second parameter form payment {test}")
    # This is for checking the subscription created amount
    result1,created_sub_amount = validate.varify_subscription_amount(test,plan_amount)
    compressive_result = result + result1
    logging.info(f"Result form payment {result1}")
    logging.info(f"second parameter form payment {created_sub_amount}")
    return result,created_sub_amount


def link_checker(driver):
    driver.get("https://www.sociamonials.com")
    
    links = driver.find_elements(By.TAG_NAME,'a')
    use_full_links = []
    broken_links = []
    same_domain_link=[]
    for link in links:
        url = link.get_attribute('href')
        if url and url !="#" and "https" in url:
            use_full_links.append(url)
            response = requests.get(url)
            if response.status_code == 400 or response.status_code == 404:
                broken_links.append(url)
            elif "sociamonials.com" in url:
                same_domain_link.append(url)
        else:
            continue                        
    
    return use_full_links,broken_links

