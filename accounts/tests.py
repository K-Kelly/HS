"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from datetime import datetime
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from wuska.hockey.models import Player, Team, League, Arena

class AccountTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_cant_login_via_login_page(self):
        self.browser.get(self.live_server_url + '/accounts/login/')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        self.assertIn('',username_box.text)
        self.assertIn('',password_box.text)
        self.browser.find_element_by_id('submit').click()
        self.assertIn('/accounts/login', self.browser.current_url)
        
    def test_can_register_new_user(self):
        self.browser.get(self.live_server_url + '/accounts/register/')
        username_box = self.browser.find_element_by_id('id_username')
        email_box = self.browser.find_element_by_id('id_email')
        password1_box = self.browser.find_element_by_id('id_password1')
        password2_box = self.browser.find_element_by_id('id_password2')
        self.assertIn('',username_box.text)
        self.assertIn('',email_box.text)
        self.assertIn('',password1_box.text)
        self.assertIn('',password2_box.text)
        self.browser.find_element_by_id('submit').click()
        self.assertIn('/accounts/register', self.browser.current_url)

        self.browser.get(self.live_server_url + '/accounts/register/')
        username_box = self.browser.find_element_by_id('id_username').send_keys('Test')
        email_box = self.browser.find_element_by_id('id_email')
        email_box.send_keys('testuser@localhostadfsdfsf')
        self.browser.find_element_by_id('submit').click()
        self.assertIn('/accounts/register', self.browser.current_url)
        email_box = self.browser.find_element_by_id('id_email')
        email_box.send_keys('.com')
        password1_box = self.browser.find_element_by_id('id_password1')
        password1_box.send_keys('testing1')
        password2_box = self.browser.find_element_by_id('id_password2')
        password2_box.send_keys('ExFail')
        self.browser.find_element_by_id('submit').click()
        self.assertIn('/accounts/register', self.browser.current_url)
        
        

