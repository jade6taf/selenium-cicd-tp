"""
Configuration pytest pour les tests Selenium
"""
import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


def pytest_addoption(parser):
    """Ajouter des options de ligne de commande"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Navigateur à utiliser: chrome ou firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Exécuter les tests en mode headless"
    )


@pytest.fixture(scope="session")
def browser_name(request):
    """Récupérer le nom du navigateur depuis la ligne de commande"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def is_headless(request):
    """Vérifier si le mode headless est activé"""
    return request.config.getoption("--headless") or os.getenv("CI")


@pytest.fixture(scope="class")
def driver(browser_name, is_headless):
    """
    Fixture pour créer une instance du driver Selenium
    Supporte Chrome et Firefox avec mode headless
    """
    driver = None
    
    try:
        if browser_name.lower() == "chrome":
            options = ChromeOptions()
            if is_headless:
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
        elif browser_name.lower() == "firefox":
            options = FirefoxOptions()
            if is_headless:
                options.add_argument("--headless")
            
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            
        else:
            raise ValueError(f"Navigateur non supporté: {browser_name}")
        
        driver.implicitly_wait(10)
        driver.maximize_window()
        
        yield driver
        
    finally:
        if driver:
            driver.quit()


@pytest.fixture
def calculator_page(driver):
    """Fixture pour créer une instance de CalculatorPage"""
    from calculator_page import CalculatorPage
    return CalculatorPage(driver)


# Hooks pytest pour logging amélioré
def pytest_configure(config):
    """Configuration globale pytest"""
    config.addinivalue_line(
        "markers", "smoke: tests de fumée rapides"
    )
    config.addinivalue_line(
        "markers", "regression: tests de régression complets"
    )
    config.addinivalue_line(
        "markers", "slow: tests lents"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook pour capturer les échecs de tests et prendre des screenshots
    """
    outcome = yield
    report = outcome.get_result()
    
    # Capturer screenshot en cas d'échec
    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            try:
                screenshot_name = f"screenshot_{item.name}_{call.when}.png"
                driver.save_screenshot(screenshot_name)
                print(f"\n📸 Screenshot sauvegardé: {screenshot_name}")
            except Exception as e:
                print(f"\n⚠️  Erreur lors de la capture d'écran: {e}")


def pytest_html_report_title(report):
    """Personnaliser le titre du rapport HTML"""
    report.title = "Rapport de Tests Selenium - Calculatrice"


def pytest_html_results_summary(prefix, summary, postfix):
    """Ajouter des informations au résumé du rapport"""
    prefix.extend([
        "<h2>Informations de Test</h2>",
        f"<p>Environment: {os.getenv('CI', 'Local')}</p>",
    ])
