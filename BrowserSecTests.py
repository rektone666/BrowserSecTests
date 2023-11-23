import argparse
import requests
import concurrent.futures
import json
import dicttoxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from tqdm import tqdm 
from pygments import highlight, lexers, formatters

#  Selenium test , options & chrome/chromium setup 
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

# Soup extractor for tests results 
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

# Selenium  going through each test   
def execute_single_test(test_path):
    html_content = execute_test_with_selenium(test_path)
    test_name, test_info = extract_test_info(html_content)
    return test_name, test_info

# all tests endpoints executed in parallel whit ThreadPoolExecutor
def execute_all_tests(output_format, output_location):
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

    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(execute_single_test, test_path): test_path for test_path in test_paths}

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(test_paths), desc="Running Tests"):
            test_name, test_info = future.result()
            results[test_name] = test_info
       
# Output , Formats & fancy colors * need some work here too
    if output_format == "json":
        json_output = json.dumps(results, indent=2, ensure_ascii=False)
        formatted_json = highlight(json_output, lexers.JsonLexer(), formatters.TerminalFormatter())
        with open(output_location, "w") as output_file:
            output_file.write(formatted_json)
        print(f"JSON output saved to {output_location}")
    elif output_format == "xml":
        xml_content = dicttoxml.dicttoxml(results)
        with open(output_location, "wb") as output_file:
            output_file.write(xml_content)
        print(f"XML output saved to {output_location}")
    elif output_format == "text":
        print(f"\nResults:")
        for test_name, test_info in results.items():
            print(f"\nTest: {test_name}")
            for prop, value in test_info.items():
                print(f"{prop}: {value}")

# Splitting lines in help , need works on that
class NewlineFormatter(argparse.RawTextHelpFormatter):
    def _split_lines(self, text, width):
        # Custom split lines method to preserve newlines
        if text.startswith('R|'):
            return text[2:].splitlines()  
        return super()._split_lines(text, width)

# Main  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A tiny tools for test your Browser OpSec.",
        epilog="""Examples:
  python3 BrowserSecTest.py - print out all the tests in json
  BrowserSecTest.py -f txt -o /path/desired/tests""",
        formatter_class=NewlineFormatter
    )
    parser.add_argument("-f", "--format", choices=["text", "json", "xml"], default="json", help="Output format (default: json)")
    parser.add_argument("-o", "--output", default="output.json", help="Output file path (default: output.json)")
    args = parser.parse_args()

    execute_all_tests(args.format, args.output)


    ###############
    #   Rekt023   #
    ###############
