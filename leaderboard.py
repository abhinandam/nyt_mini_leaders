# -*- coding: utf-8 -*-

from selenium import webdriver
from time import sleep
from secrets import NY_TIMES_CREDENTIALS

POST_LOGIN_URL = 'https://myaccount.nytimes.com/auth/login/'
LEADERBOARD_URL = 'https://www.nytimes.com/puzzles/leaderboards'

LEADERBOARD_ROW_DELIMITER = '\n'


class NYTLeaderboard(object):

    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get(POST_LOGIN_URL)
        sleep(2)

        google_auth_button = self.driver.find_element_by_xpath('// *[ @ id = "js-google-oauth-login"]')
        google_auth_button.click()
        sleep(2)

        # switch to login popup
        base_window = self.driver.window_handles[0]
        self.driver.switch_to.window(self.driver.window_handles[1])

        email_in = self.driver.find_element_by_xpath('//*[@id="identifierId"]')
        email_in.send_keys(NY_TIMES_CREDENTIALS['username'])

        next_button = self.driver.find_element_by_xpath('//*[@id="identifierNext"]')
        next_button.click()
        sleep(2)

        pw_in = self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        pw_in.send_keys(NY_TIMES_CREDENTIALS['password'])

        next_button = self.driver.find_element_by_xpath('//*[@id="passwordNext"]')
        next_button.click()

        self.driver.switch_to.window(base_window)

    def fetch_leaderboard(self):
        self.driver.get(LEADERBOARD_URL)
        leaderboard_text = self.driver.find_element_by_xpath('//*[@id="lbd-root"]/div/div[2]').text
        leaderboard_details = self.parse_leaderboard_text(leaderboard_text)
        for solver in leaderboard_details:
            print(solver.name, solver.time)

    def parse_leaderboard_text(self, leaderboard_text):
        rows = leaderboard_text.split(LEADERBOARD_ROW_DELIMITER)
        solvers = self.chunks(rows, 3)
        leaderboard_details = []
        for solver in solvers:
            leaderboard_details.append(SolverStats(solver[0], solver[1], solver[2]))
        return leaderboard_details

    @staticmethod
    def chunks(l, n):
        n = max(1, n)
        return (l[i:i + n] for i in range(0, len(l), n))


class SolverStats(object):

    def __init__(self, rank, name, time):
        self.rank = rank
        self.name = name
        self.time = time
