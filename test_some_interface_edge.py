import os
import unittest
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

class TestSomaInterfaceEdge(unittest.TestCase):

    def setUp(self):
        edge_options = EdgeOptions()
        edge_options.add_argument("--headless=new")

        try:
            self.driver = webdriver.Edge(options=edge_options)
        except WebDriverException as error:
            raise unittest.SkipTest(
                f"Edge indisponível no ambiente atual: {error.msg}"
            ) from error

        base_dir = os.path.dirname(os.path.abspath(__file__))
        html_file_path = os.path.abspath(os.path.join(base_dir, "soma.html"))
        self.driver.get(f"file:///{html_file_path}")

    def tearDown(self):
        # Fecha o navegador após o teste
        if hasattr(self, 'driver'):
            self.driver.quit()

    def test_soma_interface(self):
        # Localiza os elementos
        input1 = self.driver.find_element(By.ID, "num1")
        input2 = self.driver.find_element(By.ID, "num2")
        botao_soma = self.driver.find_element(By.ID, "somar")

        # Realiza a ação
        input1.send_keys("10")
        input2.send_keys("5")
        botao_soma.click()

        # Aguarda o resultado aparecer na tela
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.ID, 'resultado'), '15'))
        
        # Validação final
        resultado_texto = self.driver.find_element(By.ID, "resultado").text
        self.assertEqual(resultado_texto, "15")

    def test_soma_interface_numeros_negativos(self):
        # Localiza os elementos
        input1 = self.driver.find_element(By.ID, "num1")
        input2 = self.driver.find_element(By.ID, "num2")
        botao_soma = self.driver.find_element(By.ID, "somar")

        # Testa com números negativos (-5 + 3 = -2)
        input1.send_keys("-5")
        input2.send_keys("3")
        botao_soma.click()

        # Aguarda o resultado ser -2
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.ID, 'resultado'), '-2'))
        
        resultado_texto = self.driver.find_element(By.ID, "resultado").text
        self.assertEqual(resultado_texto, "-2")

if __name__ == "__main__":
    unittest.main()