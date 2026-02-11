import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected
conditions as EC
_
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver
_
manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
class TestCalculator:
@pytest.fixture(scope="class")
def driver(self):
"""Configuration du driver Chrome pour les tests"""
chrome
_
options = Options()
# Configuration pour environnement CI/CD
if os.getenv('CI'):
chrome
_
options.add
_
argument('
--headless')
chrome
_
options.add
_
argument('
--no-sandbox')
chrome
_
options.add
_
argument('
--disable-dev-shm-usage')
chrome
_
options.add
_
argument('
--disable-gpu')
chrome
_
options.add
_
argument('
--window-size=1920,1080')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome
_
driver.implicitly_
wait(10)
yield driver
driver.quit()
def test
_page
_
loads(self, driver):
"""Test 1: Vérifier que la page se charge correctement"""
file
_path = os.path.abspath("
../src/index.html")
driver.get(f"file://{file
_path}")
# Vérifier le titre
assert "Calculatrice Simple" in driver.title
# Vérifier la présence des éléments principaux
assert driver.find
_
element(By.ID,
"num1").is
_
displayed()
assert driver.find
_
element(By.ID,
"num2").is
_
displayed()
assert driver.find
_
element(By.ID,
"operation").is
_
displayed()
assert driver.find
_
element(By.ID,
"calculate").is
_
displayed()
def test
_
addition(self, driver):
"""Test 2: Tester l'addition"""
file
_path = os.path.abspath("
../src/index.html")
driver.get(f"file://{file
_path}")
# Saisir les valeurs
driver.find
_
element(By.ID,
driver.find
_
element(By.ID,
"num1").send
"num2").send
_
_
keys("10")
keys("5")
# Sélectionner l'addition
select = Select(driver.find
_
element(By.ID,
select.select
_
by_
value("add")
"operation"))
# Cliquer sur calculer
driver.find
_
element(By.ID,
"calculate").click()
# Vérifier le résultat
result = WebDriverWait(driver, 10).until(
EC.presence
of
element
_
_
_
located((By.ID,
"result"))
)
assert "Résultat: 15" in result.text
def test
division
_
_
by_
zero(self, driver):
"""Test 3: Tester la division par zéro"""
file
_path = os.path.abspath("
../src/index.html")
driver.get(f"file://{file
_path}")
options)
# Saisir les valeurs
driver.find
_
element(By.ID,
driver.find
_
element(By.ID,
driver.find
_
element(By.ID,
driver.find
_
element(By.ID,
"num1").clear()
"num1").send
_
"num2").clear()
"num2").send
_
keys("10")
keys("0")
# Sélectionner la division
select = Select(driver.find
_
element(By.ID,
select.select
_
by_
value("divide")
"operation"))
driver.find
_
element(By.ID,
"calculate").click()
# Vérifier le message d'erreur
result = WebDriverWait(driver, 10).until(
EC.presence
of
element
_
_
_
located((By.ID,
"result"))
)
assert "Erreur: Division par zéro" in result.text
def test
all
_
_
operations(self, driver):
"""Test 4: Tester toutes les opérations"""
file
_path = os.path.abspath("
../src/index.html")
driver.get(f"file://{file
_path}")
operations = [
("add"
"8"
"2"
,
,
,
"10"),
("subtract"
"8"
"2"
,
,
,
"6"),
("multiply"
"8"
"2"
,
,
,
"16"),
("divide"
"8"
"2"
,
,
,
"4")
]
for op, num1, num2, expected in operations:
# Nettoyer les champs
driver.find
_
element(By.ID,
driver.find
_
element(By.ID,
"num1").clear()
"num2").clear()
# Saisir les valeurs
driver.find
_
element(By.ID,
driver.find
_
element(By.ID,
"num1").send
"num2").send
_
_
keys(num1)
keys(num2)
# Sélectionner l'opération
select = Select(driver.find
_
select.select
_
by_
value(op)
element(By.ID,
"operation"))
# Calculer
driver.find
_
element(By.ID,
"calculate").click()
# Vérifier le résultat
result = WebDriverWait(driver, 10).until(
EC.presence
of
element
_
_
_
located((By.ID,
"result"))
)
assert f"Résultat: {expected}" in result.text
time.sleep(1)
if
name
== "
__
__
__
pytest.main(["
-v"
,
main
":
__
"
--html=report.html"
,
"
--self-contained-html"])
