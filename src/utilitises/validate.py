import logging
from src.cases.constants import *
from src.utilitises.get_element import get_element as ge
 

class validate:
    def verifyuser(drivers,username,desired_cookie,URL):
        if username in desired_cookie['value']:
        
            current_url =drivers.current_url
        
            if str(URL) == str(current_url):
                return 0

            else:    
                return 1
        else:
            return -1
    def registerformverification(drivers):
       
        # in this we can check only two field validation, username and user email, so need to check this two only
        # below code to check the error message
        try: 
            error_msg =  ge.wait_for_element_display(drivers,"arm-df__fc--validation__wrap")
            # print(type(error_msg))
            # print(error_msg)
        
        except: 
            
            print("no error is displayed it works properly")
            return 0, "no error is found"
        else: 
            return 1,error_msg
    def redirection_validation(drivers,expected_url):
        redirected_url = drivers.current_url
        if redirected_url == expected_url:
            print("it redirects properly, the redirection works properly")
            return 1, redirected_url
        else:
            print("redirection is not working properly")
            return 0, redirected_url
        
    def varify_tranction_amount(tr_id,plan_amount):
        if tr_id!=None:
            from src.utilitises.stripe_get import get_transaction_details
            amount = get_transaction_details(tr_id)
            if float(amount):
                if plan_amount==round(float(amount),1):
                    return "Case Pass, the deducted amount is as per the calculation",plan_amount
                else:
                    return f"Case failed, it deducted wrong amount, amount is not as per the calculation amount {plan_amount}",float(amount)
            else:
                return "Sorry either transaction id is wrong or not get details",plan_amount
        else:
            return "Transaction is not proper or null"
    
    def varify_subscription_amount(tr_id,subscription_amount):
        if tr_id!=None:
            from src.utilitises.stripe_get import get_subscription_amount
            subscriptionAmount = round(float(get_subscription_amount(tr_id)),1)
            if float(subscriptionAmount):
                if subscription_amount==subscriptionAmount:
                    return f"Case passed, the subscription is created with expected amount {subscription_amount}",subscription_amount
                else:
                    return f"Case failed, the subscription is not created with expected amount {subscription_amount}, but actully create with {subscriptionAmount}",subscriptionAmount
            else:
                return "Sorry either transaction id is wrong or not get details",subscription_amount
        else:
            return "Transaction is not proper or null"
                        
    def calculation(plan_amount,coupon=0,tax=0,istax=0):
        plan_amount = round(float(plan_amount),1)
        coupon=round(float(coupon),1)
        tax=round(float(tax),1)
        if coupon>0:
            print("inside coupon")
            couponamount=round((plan_amount - (plan_amount*coupon)/100),1)
            if tax>0:
                
                withouttax= round(plan_amount - couponamount,1)
                if istax==1:  # istax=1 means included tax
                    print("inside coupon and include tax")
                    acount_plan = withouttax * 100/(100+ tax)
                    taxamount = round(acount_plan*tax/100,1)
                    print(f"tax amount {taxamount}")
                    
                    payableamount = round(withouttax,1)
                    return payableamount,couponamount,taxamount
                elif istax==2: # istax=2 means exluded tax
                    taxamount = round(withouttax * tax/100,1)
                    payableamount =round(plan_amount - couponamount + taxamount,1)
                    return payableamount,couponamount,taxamount
            elif not(tax>0):
                payableamount= plan_amount -couponamount
                taxamount = round(0,1)
                return payableamount,couponamount,taxamount
        
        elif not(coupon > 0):
            couponamount=round(0,1)
            print("inside not coupon")
            logging.info("inside not coupon")
            if tax>0 and istax==2:
                taxamount = round(plan_amount * tax/100,1)
                payableamount = round(plan_amount + taxamount,1)
                return payableamount, couponamount,taxamount
            elif tax>0 and istax==1:
                print("inside include tax with no coupon")
                originalplanamount=  plan_amount * 100/(100+ tax)
                taxamount =round( originalplanamount * tax/100,1)
                print(taxamount)
                return plan_amount, couponamount,taxamount
            elif not(tax>0):
                return plan_amount, couponamount,0.0
                               
    def validate_summery(driver,plan_amount,coupon=0,tax=0,istax=0):
        payable,discount_amount,tax_amount = validate.calculation(plan_amount,coupon,tax,istax)

        taxamount=round(float(ge.get_table_value(driver,"xpath","//span[@class='arm_tax_amount_text']")),1)
        couponamount=round(float(ge.get_table_value(driver,"xpath","//span[@class='arm_discount_amount_text']")),1)
        payableamount = round(float(ge.get_table_value(driver,"xpath","//span[@class='arm_payable_amount_text']")),1)
        
        
        if payable==payableamount and taxamount==tax_amount and discount_amount==couponamount:
            
            return "summery works properly",{"paybale amount":payable,"discount amount":discount_amount,"tax amount":tax_amount}
        else:
            return "summery is not working",{"paybale amount":payable,"discount amount":discount_amount,"tax amount":tax_amount}
        