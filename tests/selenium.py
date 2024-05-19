import multiprocessing
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from unittest import TestCase
from selenium.webdriver.support import expected_conditions as EC

from app import create_app, db
from app.config import TestConfig

class SeleniumTestCase(TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        # Run Flask app on a different port to avoid conflicts
        self.port = 5002
        self.server_process = multiprocessing.Process(target=self.testApp.run, kwargs={'port': self.port})
        self.server_process.start()
        time.sleep(5)
        try:
            # Setup Chrome WebDriver with options
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")  # Uncomment for headless mode
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        except Exception as e:
            raise

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        self.server_process.terminate()
        self.driver.quit()


    def test_login_error(self):
        self.driver.get('http://localhost:5002/login')
        time.sleep(5)
        user_email = "john@example.com"
        loginElement = self.driver.find_element(By.ID, "email")
        loginElement.send_keys(user_email)
        loginElement = self.driver.find_element(By.ID, "password")
        loginElement.send_keys("wrong-password")
        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()
        time.sleep(15)
        message = self.driver.find_element(By.ID, "error-message").text
        self.assertEqual(message, "Invalid username or password")

    def test_register_page(self):
        self.driver.get('http://localhost:5002/register')

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form.login-form"))
        )

        username = self.driver.find_element(By.ID, 'username')
        email = self.driver.find_element(By.ID, 'email')
        password = self.driver.find_element(By.ID, 'password')
        password2 = self.driver.find_element(By.ID, 'password2')

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

    def test_login_page(self):
        self.driver.get('http://localhost:5002/login')

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form.login-form"))
        )

        email = self.driver.find_element(By.ID, 'email')
        password = self.driver.find_element(By.ID, 'password')
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "form.login-form input[type='submit']")

        test_user_email = 'john@example.com'
        test_user_password = 'password1'
        email.send_keys(test_user_email)
        password.send_keys(test_user_password)

        submit_button.click()
        print("Loggedin")
        time.sleep(20)

        self.driver.quit()