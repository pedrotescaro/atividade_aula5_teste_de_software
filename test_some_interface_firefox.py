import os
import unittest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSomaInterfaceFirefox(unittest.TestCase):

    def setUp(self):
        firefox_options = FirefoxOptions()
        # firefox_options.add_argument("--headless") # Descomente para rodar sem abrir a janela
        
        service = FirefoxService(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=firefox_options)
        
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

if __name__ == "__main__":
    unittest.main()