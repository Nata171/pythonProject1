# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException


def logout(driver):
    driver.find_element_by_link_text("Logout").click()


class Login(unittest.TestCase):
    def setUp(self):
        self.wd = webdriver.Chrome(executable_path=r'')
        self.wd.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_login(self):
        driver = self.wd
        self.open_home_page(driver)
        self.login(username="admin", password="secret")
        self.open_groups(driver)
        self.create_group(driver, name="NaraTest", header="TEST header", footer="TEST header")
        self.return_group_page(driver)
        logout(driver)

    def return_group_page(self, wd):
        wd.find_element_by_link_text("group page").click()

    def create_group(self, wd, name, header, footer):
        wd.find_element_by_name("new").click()
        wd.find_element_by_name("group_name").click()
        wd.find_element_by_name("group_name").clear()
        wd.find_element_by_name("group_name").send_keys("%s" % name)
        wd.find_element_by_name("group_header").click()
        wd.find_element_by_name("group_header").clear()
        wd.find_element_by_name("group_header").send_keys("%s" % header)
        wd.find_element_by_name("group_footer").click()
        wd.find_element_by_name("group_footer").clear()
        wd.find_element_by_name("group_footer").send_keys("%s" % footer)
        wd.find_element_by_name("submit").click()

    def open_groups(self, wd):
        wd.find_element_by_link_text("groups").click()

    def login(self, wd, username, password):
        wd.find_element_by_name("user").click()
        wd.find_element_by_name("user").clear()
        wd.find_element_by_name("user").send_keys("%s" % username)
        wd.find_element_by_name("pass").clear()
        wd.find_element_by_name("pass").send_keys("%s" % password)
        wd.find_element_by_xpath("//input[@value='Login']").click()

    def open_home_page(self, wd):
        wd.get("http://localhost/addressbook/")

    def is_element_present(self, how, what):
        try:
            self.wd.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.wd.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.wd.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.wd.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
