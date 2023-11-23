import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from tqdm import tqdm 


def execute_test_with_selenium(test_path):
    url = f"https://browserspy.dk/{test_path}"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # no GUI popping out 

    # ChromeDriver 
    chrome_driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()

    driver = webdriver.Chrome(service=ChromiumService(chrome_driver_path), options=chrome_options)

    try:
        driver.get(url)
        driver.implicitly_wait(5)
        html_content = driver.page_source
    finally:
        driver.quit()

    return html_content

### BeautifulSoup need some checks  ####

def extract_test_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check if h1 tag is present
    h1_tag = soup.find('h1')
    if h1_tag:
        test_name = h1_tag.text.strip()
    else:
        test_name = "Test Name Not Found"

    results = {}

    # Check if there is a results table
    results_table = soup.find('table', class_='bspy')
    if results_table:
        rows = results_table.find_all('tr')
        for row in rows:
            columns = row.find_all(['th', 'td'])
            if len(columns) == 2:
                property_name = columns[0].text.strip()
                property_value = columns[1].text.strip()
                results[property_name] = property_value

    # Check if there is a div with class 'value'
    value_div = soup.find('div', class_='value')
    if value_div:
        results['Result'] = value_div.text.strip()

    return test_name, results

def execute_all_tests():
    test_paths = [
        "accept.php",
        "activex.php",
        "adobereader.php",
        "ajax.php",
        "bandwidth.php",
        "browser.php",
        "capabilities.php",
        "colors.php",
        "components.php",
        "connections.php",
        "cookie.php",
        "cpu.php",
        "css.php",
        "css-exploit.php",
        "cursors.php",
        "date.php",
        "directx.php",
        "document.php",
        "donottrack.php",
        "dotnet.php",
        "emailcheck.php",
        "flash.php",
        "fonts-flash.php",
        "fonts-java.php",
        "gears.php",
        "gecko.php",
        "geolocation.php",
        "googlechrome.php",
        "googleapps.php",
        "gzip.php",
        "headers.php",
        "http.php",
        "images.php",
        "ip.php",
        "java.php",
        "javascript.php",
        "language.php",
        "math.php",
        "mathml.php",
        "mimetypes.php",
        "mobile.php",
        "network.php",
        "object.php",
        "showprop.php",
        "offline.php",
        "opendns.php",
        "openoffice.php",
        "opera.php",
        "os.php",
        "pagerank.php",
        "ping.php",
        "plugins.php",
        "plugs.php",
        "prefetch.php",
        "proxy.php",
        "psm.php",
        "quicktime.php",
        "realplayer.php",
        "resolution.php",
        "screen.php",
        "security.php",
        "shockwave.php",
        "silverlight.php",
        "soundcard.php",
        "svg.php",
        "textformat.php",
        "upload.php",
        "useragent.php",
        "vbscript.php",
        "wap.php",
        "webkit.php",
        "webserver.php",
        "window.php",
        "windowsmediaplayer.php",
    ]

    # timing bar  
    results = {}
    for test_path in tqdm(test_paths, desc="Running Tests"):
        html_content = execute_test_with_selenium(test_path)
        test_name, test_info = extract_test_info(html_content)
        results[test_name] = test_info


    # results = {}
    # for test_path in test_paths:
    #     print(f"\nExecuting test: {test_path}")
        
        # Execute the test using Selenium
        html_content = execute_test_with_selenium(test_path)

        #Process the HTML content with BeautifulSoup
        test_name, test_info = extract_test_info(html_content)
        results[test_name] = test_info

    print("\nResults:")
    for test_name, test_info in results.items():
        print(f"\nTest: {test_name}")
        for prop, value in test_info.items():
            print(f"{prop}: {value}")

if __name__ == "__main__":
    execute_all_tests()


    ##########
    #   Rekt023   #
    ##########