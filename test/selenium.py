import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import app, db

class SeleniumTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        with cls.app.app_context():
            db.create_all()
            cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_register_page(self):
        self.driver.get('http://127.0.0.1:5000')

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form.login-form"))
        )

        username = self.driver.find_element(By.NAME, 'username')
        email = self.driver.find_element(By.NAME, 'email')
        password = self.driver.find_element(By.NAME, 'password')
        password2 = self.driver.find_element(By.NAME, 'password2')

        username.send_keys('testuser')
        email.send_keys('test@example.com')
        password.send_keys('testpassword')
        password2.send_keys('testpassword')

        submit_button = self.driver.find_element(By.CSS_SELECTOR, "form.login-form input[type='submit']")
        submit_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.login-container"))
        )

        self.assertNotIn('error', self.driver.current_url.lower())

if __name__ == '__main__':
    unittest.main()