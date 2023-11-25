import argparse
import requests
import concurrent.futures
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.firefox.service import Service as GeckoService
from selenium.webdriver.ie.service import Service as IEService
import os
import subprocess
import colorama
from pygments import highlight, lexers, formatters

def install_required_modules():
    required_modules = ["webdriver_manager", "pipreqs"]
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.check_call(["pip", "install", module])

def generate_requirements():
    requirements = subprocess.check_output(["pip", "freeze"]).decode("utf-8")
    with open("requirements.txt", "w") as file:
        file.write(requirements)

def execute_test_with_selenium(test_path, browser_type):
    url = f"https://browserspy.dk/{test_path}"

    if browser_type == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=ChromiumService(), options=options)
    elif browser_type == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        driver = webdriver.Firefox(service=GeckoService(), options=options)
    elif browser_type == "ie":
        driver = webdriver.Ie(service=IEService())
    else:
        raise ValueError("Invalid browser type")

    try:
        driver.get(url)
        driver.implicitly_wait(5)
        html_content = driver.page_source
    finally:
        driver.quit()

    return html_content

def extract_test_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    test_name = soup.find('h1').text.strip() if soup.find('h1') else "Test Name Not Found"

    results_table = soup.find('table', class_='bspy')
    results = {}
    if results_table:
        rows = results_table.find_all('tr')
        results = {columns[0].text.strip(): columns[1].text.strip() for row in rows for columns in [row.find_all(['th', 'td'])] if len(columns) == 2}

    value_div = soup.find('div', class_='value')
    if value_div:
        results['Result'] = value_div.text.strip()

    return test_name, results

def execute_all_tests(output_format, output_location, browser_type):
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
        futures = {executor.submit(execute_test_with_selenium, test_path, browser_type): test_path for test_path in test_paths}

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(test_paths), desc="Running Tests"):
            html_content = future.result()
            test_name, test_info = extract_test_info(html_content)
            results[test_name] = test_info

    if output_format == "json":
        with open(output_location, "w") as output_file:
            json.dump(results, output_file, indent=2, ensure_ascii=False)
        print(f"{colorama.Fore.GREEN}JSON output saved to {output_location}{colorama.Style.RESET_ALL}")
    elif output_format == "xml":
        root = ET.Element("root")
        for test_name, test_info in results.items():
            test_element = ET.SubElement(root, test_name.replace(" ", ""))
            for prop, value in test_info.items():
                prop_element = ET.SubElement(test_element, prop.replace(" ", ""))
                prop_element.text = value
        tree = ET.ElementTree(root)
        tree.write(output_location)
        print(f"{colorama.Fore.GREEN}XML output saved to {output_location}{colorama.Style.RESET_ALL}")
    elif output_format == "text":
        print(f"\n{colorama.Fore.GREEN}Results:{colorama.Style.RESET_ALL}")
        for test_name, test_info in results.items():
            print(f"\n{colorama.Fore.CYAN}Test: {test_name}{colorama.Style.RESET_ALL}")
            for prop, value in test_info.items():
                print(f"{prop}: {value}")

    if output_format == "json" and output_location == "output.json":
        with open(output_location, "r") as output_file:
            json_data = output_file.read()
        colored_json_data = highlight(json_data, lexers.JsonLexer(), formatters.TerminalFormatter())
        with open(output_location, "w") as output_file:
            output_file.write(colored_json_data)
        print(f"{colorama.Fore.GREEN}Colored JSON output saved to {output_location}{colorama.Style.RESET_ALL}")

if __name__ == "__main__":
    install_required_modules()

    colorama.init()

    parser = argparse.ArgumentParser(
        description="A tiny tool to test your Browser OpSec.",
        epilog="""Examples:
    python3 BrowserSecTest.py - print out all the tests in json
    BrowserSecTest.py -f txt -o /path/desired/tests""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-f", "--format", choices=["text", "json", "xml"], default="json", help="Output format (default: json)")
    parser.add_argument("-o", "--output", default="output.json", help="Output file path (default: output.json)")
    parser.add_argument("-b", "--browser", choices=["chrome", "firefox", "ie"], default="chrome", help="Browser type (default: chrome)")
    args = parser.parse_args()

    if input("Do you want to install the required modules? (y/n): ").lower() in ["y", "yes"]:
        generate_requirements()
        subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
    else:
        print("The required modules are not installed. The script may not work properly.")

    execute_all_tests(args.format, args.output, args.browser)

############
# Rekt0x23 #
############
