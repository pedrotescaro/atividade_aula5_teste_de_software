import os
import unittest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

class TestSomaInterfaceFirefox(unittest.TestCase):

    def setUp(self):
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")

        try:
            self.driver = webdriver.Firefox(options=firefox_options)
        except WebDriverException as error:
            raise unittest.SkipTest(
                f"Firefox indisponível no ambiente atual: {error.msg}"
            ) from error
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        html_file_path = os.path.abspath(os.path.join(base_dir, "soma.html"))
        self.driver.get(f"file:///{html_file_path}")

    def tearDown(self):
        self.driver.quit()

    def test_soma_interface(self):
        self.driver.find_element(By.ID, "num1").send_keys("5")
        self.driver.find_element(By.ID, "num2").send_keys("3")
        self.driver.find_element(By.ID, "somar").click()

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.ID, 'resultado'), '8'))
        self.assertEqual(self.driver.find_element(By.ID, "resultado").text, "8")

    def test_soma_interface_numeros_negativos(self):
        self.driver.find_element(By.ID, "num1").send_keys("-5")
        self.driver.find_element(By.ID, "num2").send_keys("3")
        self.driver.find_element(By.ID, "somar").click()

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.ID, 'resultado'), '-2'))
        self.assertEqual(self.driver.find_element(By.ID, "resultado").text, "-2")

if __name__ == "__main__":
    unittest.main()