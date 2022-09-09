#!/usr/bin/env python3

# SPDX-License-Identifier: MIT

import getpass
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


class ZendeskAuto:
    def __init__(self, **args):
        self.e_mail = args["e_mail"]
        self.password = args["password"]
        self.ticket_url = args["ticket_url"]
        parsed_result = urlparse(self.ticket_url)
        self.base_url = parsed_result.scheme + "://" + parsed_result.netloc
        self.driver = webdriver.Firefox()

    def login(self):
        self.driver.get(self.base_url + "/access/normal")
        timeout = 10
        try:
            element_present = EC.visibility_of_element_located((By.XPATH, "//iframe"))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for login page to load")

        email_password_iframe = self.driver.find_element(By.XPATH, "//iframe")
        email_password_iframe.send_keys(self.e_mail)
        email_password_iframe.send_keys(Keys.TAB)
        email_password_iframe.send_keys(self.password)
        email_password_iframe.send_keys(Keys.RETURN)

        try:
            element_present = EC.title_is("Zendesk...")
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for Zendesk dashboard page to load")

    def navigate_to_ticket(self):
        self.driver.get(self.ticket_url)

    def take_it_and_submit(self):
        try:
            timeout = 5
            element_present = EC.presence_of_element_located(
                (By.XPATH, '//button[@data-test-id="assignee-field-take-it-button"]')
            )
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for take-it button to appear")

        take_it_button = self.driver.find_element(
            By.XPATH, '//button[@data-test-id="assignee-field-take-it-button"]'
        )
        take_it_button.click()
        submit_button = self.driver.find_element(
            By.XPATH, '//button[@data-test-id="submit_button-button"]'
        )
        submit_button.click()


if __name__ == "__main__":

    zd = ZendeskAuto(
        e_mail=input("E-Mail:\n> "),
        password=getpass.getpass("Password (will be hidden):\n> "),
        ticket_url=input("Ticket URL:\n> "),
    )
    zd.login()
    zd.navigate_to_ticket()
    zd.take_it_and_submit()
