"""
_*_ coding: UTF-8 _*_
@Time      : 2021/5/6 17:13
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : public_selenium.py
@Software  : PyCharm
"""
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 60)


# name 定位
def path_name_click(path):
    """name 定位 点击"""
    driver.find_element_by_name(path).click()


# class 定位
def path_class_click(path):
    """class 定位 点击"""
    driver.find_element_by_class_name(path).click()


# tag 定位
def path_tag_click(path):
    """tag 定位 点击"""
    driver.find_element_by_tag_name(path).click()


# link 定位
def path_link_click(path):
    """link 定位 点击"""
    driver.find_element_by_link_text(path).click()


# partial_link 定位
def path_partial_link_click(path):
    """partial_link 定位 点击"""
    driver.find_element_by_partial_link_text(path).click()


# xpath 定位
def path_xpath_click(path):
    """xpath 定位 点击"""
    driver.find_element_by_xpath(path).click()


# CSS 定位
def path_css_click(path):
    """CSS 定位 点击"""
    driver.find_element_by_css_selector(path).click()


# id 定位
def path_id_click(path):
    """id 定位 点击"""
    driver.find_element_by_id(path).click()


# name 定位
def path_name_send(path, values):
    """name 定位 输入"""
    driver.find_element_by_name(path).send_keys(values)


# class 定位
def path_class_send(path, values):
    """class 定位 输入"""
    driver.find_element_by_class_name(path).send_keys(values)


# tag 定位
def path_tag_send(path, values):
    """tag 定位 输入"""
    driver.find_element_by_tag_name(path).send_keys(values)


# link 定位
def path_link_send(path, values):
    """link 定位 输入"""
    driver.find_element_by_link_text(path).send_keys(values)


# partial_link 定位
def path_partial_link_send(path, values):
    """partial_link 定位 输入"""
    driver.find_element_by_partial_link_text(path).send_keys(values)


# xpath 定位
def path_xpath_send(path, values):
    """xpath 定位 输入"""
    driver.find_element_by_xpath(path).send_keys(values)


# CSS 定位
def path_css_send(path, values):
    """CSS 定位 输入"""
    driver.find_element_by_css_selector(path).send_keys(values)


# id 定位
def path_id_send(path, values):
    """id 定位 输入"""
    driver.find_element_by_id(path).send_keys(values)


# 显示等待
def wait_ec_xpath(path):
    """显示等待wait_ec_xpath"""
    wait.until(ec.presence_of_element_located((By.XPATH, path)))


# 显示等待
def wait_ec_id(path):
    """显示等待 wait_ec_id"""
    wait.until(ec.presence_of_element_located((By.ID, path)))


# 显示等待
def wait_ec_name(path):
    """显示等待 wait_ec_name"""
    wait.until(ec.presence_of_element_located((By.NAME, path)))


# 显示等待
def wait_ec_css_selector(path):
    """显示等待 wait_ec_css_selector"""
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, path)))


# 显示等待
def wait_ec_link_text(path):
    """显示等待 wait_ec_link_text"""
    wait.until(ec.presence_of_element_located((By.LINK_TEXT, path)))


# 显示等待
def wait_ec_partial_link_text(path):
    """显示等待 wait_ec_partial_link_text"""
    wait.until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, path)))


# 显示等待
def wait_ec_class_name(path):
    """显示等待 wait_ec_class_name"""
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, path)))


# 显示等待
def wait_ec_tag_name(path):
    """显示等待 wait_ec_tag_name"""
    wait.until(ec.presence_of_element_located((By.TAG_NAME, path)))


# 强制等待
def wait_sleep():
    """强制等待3秒"""
    time.sleep(3)


# 切换进入iframe
def In_iframe(path_type):
    """定位方式加路径 切换进入iframe"""
    driver.switch_to.frame(path_type)


# 切换退出iframe
def Out_iframe():
    """切换退出iframe"""
    driver.switch_to_default_content()


# 鼠标悬停
def Hovering(move):
    """定位到悬停元素进行悬停"""
    # 对定位到的元素执行悬停操作
    ActionChains(driver).move_to_element(move).perform()
