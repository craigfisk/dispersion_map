from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://127.0.0.1:8000/")
signin_elem = driver.find_element_by_link_text("sign-in")
# signin_element.tag_name --> u'a'
# signin_element.text --> u'sign-in'
signin_elem.click()   # goes to the sign-in page
# where username and password are the names of the form fields to fill in:
elem_username = driver.find_element_by_name('username')
elem_password = driver.find_element_by_name('password')
# send the text to the form:
elem_username.send_keys('lindamagee')
elem_password.send_keys('Sp8rky=4242')
elem_password.submit()          # bubbles up to the form and submits it

# go to Forum
driver.find_element_by_link_text('Forum').click()
# go to a forum
driver.find_element_by_link_text('Fruitcake tradition').click()
# go to a thread
driver.find_element_by_link_text('Holiday baking for pet birds').click()
# Reply to create another post in the thread
driver.find_element_by_link_text('Reply').click()
# Get elem for "body" of the post, fill in some text, post it:
##elem_reply_body = driver.find_element_by_id('subject')
##elem_reply_body.send_keys("Birds and holiday baked goods.")
elem_reply_body = driver.find_element_by_id('body')
elem_reply_body.send_keys("Birds are big fans of holiday baked goods.")
elem_reply_body.submit()

# Return to page with choice between existing and new thread:
driver.back()
driver.back()
driver.back()
# Click on "start new discussion"
driver.find_element_by_id("new_topic").click()
# fill in the new discussion form:
elem_new_subject = driver.find_element_by_name("subject")
elem_new_body = driver.find_element_by_id("body")
elem_new_subject.send_keys("This is a test")
elem_new_body.send_keys("This is the body of a test")
elem_new_body.submit()
# end
#driver.close()  # closes the window
driver.quit()   # exits the driver and closes window

