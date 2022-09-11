#!/usr/bin/env python3

# SPDX-License-Identifier: MIT

import getpass
import logging
import os
import sys

from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ZendeskAuto:
    def __init__(self, driver_type, **args):
        self.driver = driver_type()
        self.e_mail = args["e_mail"]
        self.password = args["password"]
        self.ticket_url = args["ticket_url"]
        parsed_result = urlparse(self.ticket_url)
        self.base_url = parsed_result.scheme + "://" + parsed_result.netloc

    def login(self):
        self.driver.get(self.base_url + "/access/normal")
        timeout = 10
        try:
            element_present = EC.visibility_of_element_located((By.XPATH, "//iframe"))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            logging.error("Timed out waiting for login page to load")
            raise

        email_password_iframe = self.driver.find_element(By.XPATH, "//iframe")
        email_password_iframe.send_keys(self.e_mail)
        email_password_iframe.send_keys(Keys.TAB)
        email_password_iframe.send_keys(self.password)
        email_password_iframe.send_keys(Keys.RETURN)

        try:
            element_present = EC.title_is("Zendesk...")
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            logging.error("Timed out waiting for Zendesk dashboard page to load")
            raise

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
            logging.error("Timed out waiting for take-it button to appear")
            raise

        take_it_button = self.driver.find_element(
            By.XPATH, '//button[@data-test-id="assignee-field-take-it-button"]'
        )
        take_it_button.click()
        submit_button = self.driver.find_element(
            By.XPATH, '//button[@data-test-id="submit_button-button"]'
        )
        submit_button.click()


def find_driver():
    driver_map = {"geckodriver": webdriver.Firefox, "chromedriver": webdriver.Chrome}

    def find_driver_impl():
        for pe in os.environ["PATH"].split(os.pathsep):
            for binary_name, driver_type in driver_map.items():
                checkname = os.path.join(pe, binary_name)
                if os.access(checkname, os.X_OK) and not os.path.isdir(checkname):
                    return driver_type

    driver = find_driver_impl()
    if not driver:
        msg = (
            "Could not find any webdriver in your system PATH.\n"
            "Make sure you install one of those for your preferred browser:\n"
            "https://www.selenium.dev/documentation/"
            "webdriver/getting_started/install_drivers/"
        )
        raise RuntimeError(msg)
    return driver


if __name__ == "__main__":

    try:
        driver_type = find_driver()

        zd = ZendeskAuto(
            driver_type=driver_type,
            e_mail=input("E-Mail:\n> "),
            password=getpass.getpass("Password (will be hidden):\n> "),
            ticket_url=input("Ticket URL:\n> "),
        )
        zd.login()
        zd.navigate_to_ticket()
        zd.take_it_and_submit()
    except Exception as e:
        if hasattr(e, "message") and e.message:
            logging.error(e.message)
        else:
            logging.error(e)
        sys.exit(255)
