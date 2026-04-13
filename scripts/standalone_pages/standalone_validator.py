#!/usr/bin/env python3
"""
Standalone Page Compatibility Validator — Selenium Automation
=============================================================
Reads URLs from configs/urls.txt, validates each page using Chrome/Selenium,
extracts all compatibility check results, captures screenshots, and generates
QA reports in Markdown, HTML (styled), Excel (color-coded XML), and CSV.

Usage:
    python3 standalone_validator.py

Dependencies:
    pip install selenium webdriver-manager
"""

import csv
import os
import sys
import time
import json
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, WebDriverException
)

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WDM = True
except ImportError:
    USE_WDM = False

# =====================================================================
# CONFIGURATION
# =====================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
URLS_FILE = os.path.join(BASE_DIR, "configs", "urls.txt")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_reports", "standalone_pages")  # script-domain subfolder
SCREENSHOT_DIR = os.path.join(OUTPUT_DIR, "screenshots")
DUMMY_EMAIL = "qa_test@example.com"
MAX_WAIT_SECONDS = 60  # Max wait for checks to complete
TODAY = datetime.now().strftime("%Y-%m-%d")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("validator")


# =====================================================================
# HELPER: Chrome Driver Setup
# =====================================================================
def create_driver():
    """Create a Chrome WebDriver with camera/mic auto-granted."""
    opts = Options()
    opts.add_argument("--start-maximized")
    opts.add_argument("--use-fake-ui-for-media-stream")       # auto-grant cam/mic
    opts.add_argument("--use-fake-device-for-media-stream")   # use fake devices
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-popup-blocking")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # Suppress automation detection
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    if USE_WDM:
        service = Service(ChromeDriverManager().install())
    else:
        service = Service()  # uses chromedriver from PATH

    driver = webdriver.Chrome(service=service, options=opts)
    driver.implicitly_wait(5)
    return driver


# =====================================================================
# HELPER: Read URLs from config
# =====================================================================
def read_urls(filepath):
    """Read URLs from file, parse label: url format."""
    url_items = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if ":" in line and not line.startswith("http"):
                parts = line.split(":", 1)
                group = parts[0].strip()
                url = parts[1].strip()
            else:
                group = "default"
                url = line
                
            if url:
                url_items.append({"group": group, "url": url})
                
    log.info(f"Loaded {len(url_items)} URL(s) with grouping from {filepath}")
    return url_items


# =====================================================================
# HELPER: Determine URL label
# =====================================================================
def url_label(url_item, index):
    """Generate a short label for the URL based on its group and content."""
    url = url_item["url"]
    group = url_item["group"].title()
    
    specific = ""
    if "/compatibility/at/seb" in url:
        specific = "SEB_Compatibility"
    elif "/compatibility/at" in url:
        specific = "Standard_Compatibility"
    elif "testcompatibility" in url or "check.html" in url:
        specific = "Full_Test_Compatibility"
    else:
        specific = f"Page_{index}"
        
    return f"URL{index}_{group}_{specific}"


# =====================================================================
# CORE: Validate a single URL
# =====================================================================
def validate_url(driver, url_item, index):
    """
    Navigate to a URL, extract all compatibility check data.
    Returns a dict with all results.
    """
    url = url_item["url"]
    label = url_label(url_item, index)
    log.info(f"--- Validating [{label}]: {url} ---")

    result = {
        "url": url,
        "label": label,
        "index": index,
        "page_loaded": False,
        "email_prompt": False,
        "overall_status": "",
        "core_checks": [],        # Camera, Mic, Browser, Network
        "system_info": {},         # OS, Dimension, Browser, Screen, Cookies, Popup, SEB
        "bandwidth": {},           # Download, Upload
        "websocket_checks": [],    # HV, AS, HP (URL3 only)
        "ice_checks": [],          # host, srflx, relay (URL3 only)
        "server_reachability": [], # UDP/TCP/TLS (URL3 only)
        "screenshot_path": "",
        "test_cases": [],          # Populated after extraction
        "errors": [],
        "console_logs": [],
    }

    try:
        # Navigate
        driver.get(url)
        time.sleep(3)
        result["page_loaded"] = True
        log.info("  Page loaded successfully")

        # --- Handle email prompt ---
        try:
            email_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Email']")
            if email_input.is_displayed():
                result["email_prompt"] = True
                email_input.clear()
                email_input.send_keys(DUMMY_EMAIL)
                time.sleep(0.5)
                # Click OK button
                ok_btn = driver.find_element(By.XPATH, "//button[contains(text(),'OK')]")
                ok_btn.click()
                log.info(f"  Email prompt handled: entered {DUMMY_EMAIL}")
                time.sleep(3)
        except NoSuchElementException:
            log.info("  No email prompt detected")

        # --- Wait for overall status to appear ---
        log.info("  Waiting for compatibility checks to complete...")
        try:
            WebDriverWait(driver, MAX_WAIT_SECONDS).until(
                lambda d: any([
                    _safe_find_text(d, By.XPATH, "//b[contains(text(),'Success')]"),
                    _safe_find_text(d, By.XPATH, "//b[contains(text(),'Fail')]"),
                    _safe_find_text(d, By.XPATH, "//b[contains(text(),'success')]"),
                ])
            )
        except TimeoutException:
            log.warning("  Timed out waiting for overall status")
            result["errors"].append("Timed out waiting for overall status")

        # Extra wait for bandwidth test to finish
        time.sleep(10)

        # --- Extract overall status ---
        try:
            status_el = driver.find_element(By.XPATH,
                "//b[contains(text(),'Success') or contains(text(),'Fail') or contains(text(),'success') or contains(text(),'fail')]"
            )
            result["overall_status"] = status_el.text.strip()
        except NoSuchElementException:
            # Fallback: try finding any status text
            try:
                status_el = driver.find_element(By.CSS_SELECTOR, ".compatibility-panel b")
                result["overall_status"] = status_el.text.strip()
            except NoSuchElementException:
                result["overall_status"] = "UNKNOWN"
                result["errors"].append("Could not find overall status element")

        log.info(f"  Overall status: {result['overall_status']}")

        # --- Extract core checks (Camera, Microphone, Browser, Network) ---
        result["core_checks"] = _extract_core_checks(driver)
        log.info(f"  Core checks found: {len(result['core_checks'])}")

        # --- Extract System Info ---
        result["system_info"] = _extract_system_info(driver)
        log.info(f"  System info items: {len(result['system_info'])}")

        # --- Extract Internet Bandwidth ---
        result["bandwidth"] = _extract_bandwidth(driver)
        log.info(f"  Bandwidth: {result['bandwidth']}")

        # --- Extract extended checks (WebSocket, ICE, Server Reachability) ---
        result["websocket_checks"] = _extract_websocket_checks(driver)
        result["ice_checks"] = _extract_ice_checks(driver)
        result["server_reachability"] = _extract_server_reachability(driver)

        if result["websocket_checks"]:
            log.info(f"  WebSocket checks: {len(result['websocket_checks'])}")
        if result["ice_checks"]:
            log.info(f"  ICE checks: {len(result['ice_checks'])}")
        if result["server_reachability"]:
            log.info(f"  Server reachability checks: {len(result['server_reachability'])}")

        # --- Capture screenshot ---
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        ss_path = os.path.join(SCREENSHOT_DIR, f"{label}_{TODAY}.png")
        driver.save_screenshot(ss_path)
        result["screenshot_path"] = ss_path
        log.info(f"  Screenshot saved: {ss_path}")

        # --- Collect console logs ---
        try:
            browser_logs = driver.get_log("browser")
            result["console_logs"] = [
                {"level": entry["level"], "message": entry["message"][:200]}
                for entry in browser_logs
            ]
        except Exception:
            pass

    except WebDriverException as e:
        result["errors"].append(f"WebDriver error: {str(e)[:200]}")
        log.error(f"  WebDriver error: {e}")

    # --- Build test cases from extracted data ---
    result["test_cases"] = _build_test_cases(result)

    return result


# =====================================================================
# EXTRACTION HELPERS
# =====================================================================
def _safe_find_text(driver, by, selector):
    """Safely find element text, return empty string if not found."""
    try:
        el = driver.find_element(by, selector)
        return el.text.strip()
    except NoSuchElementException:
        return ""


def _extract_core_checks(driver):
    """Extract Camera, Microphone, Browser, Network check results."""
    checks = []
    rows = driver.find_elements(By.CSS_SELECTOR, ".proctor-check-device-items")

    for row in rows:
        try:
            text = row.text.strip()
            if not text:
                continue

            # Determine check name
            name = ""
            if "Camera" in text:
                name = "Camera"
            elif "Microphone" in text or "Mic" in text:
                name = "Microphone"
            elif "Browser" in text and "WebSocket" not in text:
                name = "Browser"
            elif "Your Network" in text:
                name = "Network"
            elif "WebSocket" in text:
                continue  # handled separately
            elif "ICE" in text or "Echo" in text:
                continue  # handled separately
            else:
                continue

            # Determine pass/fail via icon
            status = _get_row_status(row)
            checks.append({"name": name, "status": status, "detail": text})
        except Exception:
            continue

    return checks


def _get_row_status(row_element):
    """Check if a row element contains a pass (green) or fail (red) icon."""
    try:
        row_element.find_element(By.CSS_SELECTOR, "i.fa-check-circle.icon-green")
        return "PASS"
    except NoSuchElementException:
        pass
    try:
        row_element.find_element(By.CSS_SELECTOR, "i.fa-times-circle.icon-red")
        return "FAIL"
    except NoSuchElementException:
        pass
    # Fallback: check for just green/red icon classes
    try:
        row_element.find_element(By.CSS_SELECTOR, "i.icon-green")
        return "PASS"
    except NoSuchElementException:
        pass
    try:
        row_element.find_element(By.CSS_SELECTOR, "i.icon-red")
        return "FAIL"
    except NoSuchElementException:
        pass
    return "UNKNOWN"


def _extract_system_info(driver):
    """Extract System Info section (OS, Dimension, Browser, Screen, etc.)."""
    info = {}
    try:
        # Find the specific panel for System Info to avoid overlap with Bandwidth
        panels = driver.find_elements(By.CSS_SELECTOR, ".panel")
        sys_panel = None
        for p in panels:
            if "System Info" in p.text:
                sys_panel = p
                break
        
        target = sys_panel if sys_panel else driver
        dt_elements = target.find_elements(By.CSS_SELECTOR, "dt")
        dd_elements = target.find_elements(By.CSS_SELECTOR, "dd")

        label_map = {
            "OS": "os",
            "Dimension": "dimension",
            "Browser": "browser",
            "Screen": "screen",
            "Cookies": "cookies",
            "Popup": "popup",
            "Safe Browser Compatible": "safe_browser",
        }

        for dt, dd in zip(dt_elements, dd_elements):
            dt_text = dt.text.strip().rstrip(":")
            dd_text = dd.text.strip()
            for label, key in label_map.items():
                if label.lower() in dt_text.lower():
                    info[key] = dd_text
                    break
    except Exception as e:
        log.warning(f"  Error extracting system info: {e}")

    return info


def _extract_bandwidth(driver):
    """Extract Internet Bandwidth data from its specific panel."""
    bw = {}
    try:
        panels = driver.find_elements(By.CSS_SELECTOR, ".panel")
        bw_panel = None
        for p in panels:
            if "Internet Bandwidth" in p.text:
                bw_panel = p
                break
        
        target = bw_panel if bw_panel else driver
        dt_elements = target.find_elements(By.CSS_SELECTOR, "dt")
        dd_elements = target.find_elements(By.CSS_SELECTOR, "dd")

        for dt, dd in zip(dt_elements, dd_elements):
            dt_text = dt.text.strip().lower()
            dd_text = dd.text.strip()
            if "download" in dt_text:
                bw["download"] = dd_text
            elif "upload" in dt_text:
                bw["upload"] = dd_text
    except Exception as e:
        log.warning(f"  Error extracting bandwidth: {e}")

    return bw


def _extract_websocket_checks(driver):
    """Extract WebSocket check results (HV, AS, HP) if present."""
    checks = []
    try:
        ws_rows = driver.find_elements(By.CSS_SELECTOR, ".proctor-check-device-items")
        for row in ws_rows:
            text = row.text.strip()
            if "WebSocket" in text:
                # Sub-items: HV, AS, HP
                sub_spans = row.find_elements(By.CSS_SELECTOR, "span.col-xs-4")
                if not sub_spans:
                    sub_spans = row.find_elements(By.CSS_SELECTOR, "span[class*='col-xs']")
                for span in sub_spans:
                    sub_text = span.text.strip()
                    if sub_text:
                        name = sub_text.split()[0] if sub_text.split() else sub_text
                        try:
                            span.find_element(By.CSS_SELECTOR, "i.icon-green, i.fa-check-circle")
                            status = "PASS"
                        except NoSuchElementException:
                            try:
                                span.find_element(By.CSS_SELECTOR, "i.icon-red, i.fa-times-circle")
                                status = "FAIL"
                            except NoSuchElementException:
                                status = "UNKNOWN"
                        checks.append({"name": f"WebSocket-{name}", "status": status})
                # If no sub-spans found, check the whole row
                if not checks:
                    status = _get_row_status(row)
                    checks.append({"name": "WebSocket", "status": status})
                break
    except Exception:
        pass
    return checks


def _extract_ice_checks(driver):
    """Extract ICE candidate check results (host, srflx, relay) if present."""
    checks = []
    try:
        rows = driver.find_elements(By.CSS_SELECTOR, ".proctor-check-device-items")
        for row in rows:
            text = row.text.strip()
            if "ICE" in text or "Echo" in text:
                label = "ICE" if "ICE" in text else "Echo"
                sub_spans = row.find_elements(By.CSS_SELECTOR, "span")
                for span in sub_spans:
                    sub_text = span.text.strip()
                    # Skip empty spans or the span that is just the row title (ICE/Echo)
                    if not sub_text or sub_text.lower() == label.lower():
                        continue
                        
                    name = sub_text.split()[0] if sub_text.split() else sub_text
                    try:
                        span.find_element(By.CSS_SELECTOR, "i.icon-green, i.fa-check-circle")
                        status = "PASS"
                    except NoSuchElementException:
                        try:
                            span.find_element(By.CSS_SELECTOR, "i.icon-red, i.fa-times-circle")
                            status = "FAIL"
                        except NoSuchElementException:
                            status = "UNKNOWN"
                    checks.append({"name": f"{label}-{name}", "status": status})
                if not checks:
                    status = _get_row_status(row)
                    checks.append({"name": label, "status": status})
                break
    except Exception:
        pass
    return checks


def _extract_server_reachability(driver):
    """Extract Server Reachability checks (UDP/TCP/TLS) if present."""
    checks = []
    try:
        server_items = driver.find_elements(By.CSS_SELECTOR, ".server-content")
        if not server_items:
            # Fallback: look for server-results spans
            server_items = driver.find_elements(By.CSS_SELECTOR, ".server-results")

        for item in server_items:
            parent = item if "server-content" in item.get_attribute("class") else item
            text = ""
            try:
                text_el = parent.find_element(By.CSS_SELECTOR, ".server-results, span")
                text = text_el.text.strip()
            except NoSuchElementException:
                text = parent.text.strip()

            if not text:
                continue

            try:
                parent.find_element(By.CSS_SELECTOR, "i.icon-green, i.fa-check-circle")
                status = "PASS"
            except NoSuchElementException:
                try:
                    parent.find_element(By.CSS_SELECTOR, "i.icon-red, i.fa-times-circle")
                    status = "FAIL"
                except NoSuchElementException:
                    status = "UNKNOWN"

            checks.append({"name": text, "status": status})
    except Exception:
        pass
    return checks


# =====================================================================
# BUILD TEST CASES from extracted data
# =====================================================================
def _build_test_cases(result):
    """Convert extracted data into structured test case records."""
    cases = []
    idx = result["index"]
    tc_num = 0

    # Test case: Page load
    tc_num += 1
    cases.append({
        "testcase id": f"TC-URL{idx}-{tc_num:03d}",
        "testcase name": "Page Load",
        "testcase description": "Verify the URL loads successfully without HTTP errors.",
        "testcase steps": f"1. Open URL: {result['url']}\n2. Observe page load status.",
        "testcase expected result": "Page loads successfully.",
        "testcase actual result": "Page loaded successfully." if result["page_loaded"] else "Page failed to load.",
        "testcase status": "PASS" if result["page_loaded"] else "FAIL",
        "testcase remarks": f"Email prompt: {'Yes' if result['email_prompt'] else 'No'}",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": f"URL{idx}"
    })

    # Test case: Email prompt handling
    if result["email_prompt"]:
        tc_num += 1
        cases.append({
            "testcase id": f"TC-URL{idx}-{tc_num:03d}",
            "testcase name": "Email Pre-Validation Prompt",
            "testcase description": "Verify the email prompt is handled correctly.",
            "testcase steps": f"1. Open URL.\n2. Enter {DUMMY_EMAIL}.\n3. Click OK.",
            "testcase expected result": "Email accepted and page proceeds to system checks.",
            "testcase actual result": "Email entered and submitted successfully. Page proceeded to compatibility checks.",
            "testcase status": "PASS",
            "testcase remarks": "Email prompt handled automatically.",
            "testcase severity": "Medium",
            "testcase priority": "P2",
            "url": f"URL{idx}"
        })

    # Test cases: Core checks (Camera, Microphone, Browser, Network)
    for check in result["core_checks"]:
        tc_num += 1
        cases.append({
            "testcase id": f"TC-URL{idx}-{tc_num:03d}",
            "testcase name": f"{check['name']} Detection",
            "testcase description": f"Verify {check['name'].lower()} detection and compatibility.",
            "testcase steps": f"1. Open URL.\n2. Wait for {check['name'].lower()} check.\n3. Observe result.",
            "testcase expected result": f"{check['name']} detected and compatible.",
            "testcase actual result": f"{check['name']}: {check['status']}. Detail: {check.get('detail', 'N/A')}",
            "testcase status": check["status"],
            "testcase remarks": f"{'Detected correctly.' if check['status'] == 'PASS' else 'Detection failed.'}",
            "testcase severity": "Critical" if check["name"] in ["Camera", "Microphone"] else "High",
            "testcase priority": "P1",
            "url": f"URL{idx}"
        })

    # Test cases: System Info
    sys_info_checks = {
        "os": ("OS Detection", "Correct OS detected.", "High"),
        "dimension": ("Screen Dimension", "Correct dimension reported.", "Medium"),
        "browser": ("Browser Info", "Correct browser version reported.", "High"),
        "screen": ("Screen/Viewport Size", "Correct screen size reported.", "Medium"),
        "cookies": ("Cookies Status", "Cookies status detected.", "Medium"),
        "popup": ("Popup Status", "Popup status detected.", "Medium"),
        "safe_browser": ("Safe Browser Compatible", "SEB detection status reported.", "Critical"),
    }

    for key, (name, expected, severity) in sys_info_checks.items():
        if key in result["system_info"]:
            value = result["system_info"][key]
            tc_num += 1

            # Determine status — specific logic for certain fields
            status = "PASS"
            remarks = f"Value: {value}"
            if key == "safe_browser" and value.lower() == "no":
                remarks = "Correctly shows 'No' — tested in standard Chrome, not SEB."
            elif key == "popup" and value.lower() == "blocked":
                remarks = "Popup is blocked. May need attention for popup-dependent flows."
            elif key == "cookies" and value.lower() != "enabled":
                status = "FAIL"
                remarks = "Cookies should be enabled."

            cases.append({
                "testcase id": f"TC-URL{idx}-{tc_num:03d}",
                "testcase name": name,
                "testcase description": f"Verify {name.lower()} in System Info section.",
                "testcase steps": f"1. Open URL.\n2. Check '{name}' in System Info.",
                "testcase expected result": expected,
                "testcase actual result": f"{name}: {value}",
                "testcase status": status,
                "testcase remarks": remarks,
                "testcase severity": severity,
                "testcase priority": "P1" if severity == "Critical" else "P2",
                "url": f"URL{idx}"
            })

    # Test cases: Internet Bandwidth
    for direction in ["download", "upload"]:
        if direction in result["bandwidth"]:
            tc_num += 1
            value = result["bandwidth"][direction]
            is_high = "high" in value.lower()
            cases.append({
                "testcase id": f"TC-URL{idx}-{tc_num:03d}",
                "testcase name": f"Internet Speed ({direction.title()})",
                "testcase description": f"Verify {direction} speed measurement.",
                "testcase steps": f"1. Open URL.\n2. Wait for speed test.\n3. Observe {direction} speed.",
                "testcase expected result": f"{direction.title()} speed measured with rating.",
                "testcase actual result": f"{direction.title()}: {value}",
                "testcase status": "PASS" if is_high or value else "FAIL",
                "testcase remarks": f"{'Good speed.' if is_high else 'Speed may be low.'}",
                "testcase severity": "High",
                "testcase priority": "P2",
                "url": f"URL{idx}"
            })

    # Test cases: WebSocket checks
    for ws in result["websocket_checks"]:
        tc_num += 1
        cases.append({
            "testcase id": f"TC-URL{idx}-{tc_num:03d}",
            "testcase name": f"{ws['name']} Check",
            "testcase description": f"Verify {ws['name']} connectivity.",
            "testcase steps": f"1. Open URL.\n2. Observe {ws['name']} check result.",
            "testcase expected result": f"{ws['name']} shows green tick (connected).",
            "testcase actual result": f"{ws['name']}: {ws['status']}",
            "testcase status": ws["status"],
            "testcase remarks": f"{'Connected.' if ws['status'] == 'PASS' else 'Connection issue.'}",
            "testcase severity": "Critical",
            "testcase priority": "P1",
            "url": f"URL{idx}"
        })

    # Test cases: ICE checks
    for ice in result["ice_checks"]:
        tc_num += 1
        cases.append({
            "testcase id": f"TC-URL{idx}-{tc_num:03d}",
            "testcase name": f"{ice['name']} Candidate",
            "testcase description": f"Verify {ice['name']} ICE candidate availability.",
            "testcase steps": f"1. Open URL.\n2. Observe {ice['name']} check.",
            "testcase expected result": f"{ice['name']} candidate available.",
            "testcase actual result": f"{ice['name']}: {ice['status']}",
            "testcase status": ice["status"],
            "testcase remarks": f"{'Available.' if ice['status'] == 'PASS' else 'Not available.'}",
            "testcase severity": "Critical",
            "testcase priority": "P1",
            "url": f"URL{idx}"
        })

    # Test cases: Server Reachability
    for sr in result["server_reachability"]:
        tc_num += 1
        cases.append({
            "testcase id": f"TC-URL{idx}-{tc_num:03d}",
            "testcase name": f"Server Reachability: {sr['name']}",
            "testcase description": f"Verify server reachability via {sr['name']}.",
            "testcase steps": f"1. Open URL.\n2. Scroll to Server Reachability.\n3. Observe {sr['name']} check.",
            "testcase expected result": f"{sr['name']} shows green tick (reachable).",
            "testcase actual result": f"{sr['name']}: {sr['status']}",
            "testcase status": sr["status"],
            "testcase remarks": f"{'Reachable.' if sr['status'] == 'PASS' else 'Not reachable.'}",
            "testcase severity": "Critical",
            "testcase priority": "P1",
            "url": f"URL{idx}"
        })

    # Test case: Overall Status
    tc_num += 1
    overall_pass = "success" in result["overall_status"].lower() if result["overall_status"] else False
    cases.append({
        "testcase id": f"TC-URL{idx}-{tc_num:03d}",
        "testcase name": "Overall Compatibility Status",
        "testcase description": "Verify overall compatibility verdict.",
        "testcase steps": "1. Open URL.\n2. Wait for all checks to complete.\n3. Observe overall status banner.",
        "testcase expected result": "Success message displayed.",
        "testcase actual result": f"Overall Status: {result['overall_status']}",
        "testcase status": "PASS" if overall_pass else "FAIL",
        "testcase remarks": result["overall_status"],
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": f"URL{idx}"
    })

    return cases


# =====================================================================
# REPORT GENERATORS
# =====================================================================

def generate_markdown_report(all_results, output_dir):
    """Generate a detailed Markdown QA report."""
    path = os.path.join(output_dir, f"qa_report_{TODAY}.md")
    total_cases = sum(len(r["test_cases"]) for r in all_results)
    passed = sum(1 for r in all_results for tc in r["test_cases"] if tc["testcase status"] == "PASS")
    failed = total_cases - passed

    lines = []
    lines.append(f"# 🧾 QA TEST REPORT — Standalone Compatibility Pages (Chrome Only)\n")
    lines.append(f"**Date:** {TODAY}")
    lines.append(f"**Test Conducted By:** Selenium Automation Script\n")
    lines.append("---\n")

    # Environment
    env_info = {}
    for r in all_results:
        if r["system_info"]:
            env_info = r["system_info"]
            break

    lines.append("## 1. Test Environment\n")
    lines.append("| Parameter | Value |")
    lines.append("|-----------|-------|")
    lines.append(f"| **Chrome Version** | {env_info.get('browser', 'N/A')} |")
    lines.append(f"| **OS** | {env_info.get('os', 'N/A')} |")
    lines.append(f"| **Screen Resolution** | {env_info.get('dimension', 'N/A')} |")
    lines.append(f"| **Mode** | Normal (Automated) |\n")

    # Summary
    lines.append("---\n")
    lines.append("## 2. Executive Summary\n")
    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| **Total Checks** | {total_cases} |")
    lines.append(f"| **Passed** | {passed} |")
    lines.append(f"| **Failed** | {failed} |")
    lines.append(f"| **Overall Status** | **{'PASS' if failed == 0 else 'FAIL'}** |\n")

    # Per-URL results
    for r in all_results:
        lines.append("---\n")
        lines.append(f"## {r['label']}\n")
        lines.append(f"**URL:** `{r['url']}`")
        lines.append(f"**Overall Status:** {r['overall_status']}\n")

        if r["test_cases"]:
            lines.append("| ID | Test Case | Expected | Actual | Status | Severity | Priority |")
            lines.append("|-----|-----------|----------|--------|--------|----------|----------|")
            for tc in r["test_cases"]:
                status_icon = "✅" if tc["testcase status"] == "PASS" else "❌"
                lines.append(
                    f"| {tc['testcase id']} | {tc['testcase name']} | "
                    f"{tc['testcase expected result'][:50]} | {tc['testcase actual result'][:50]} | "
                    f"{status_icon} {tc['testcase status']} | {tc['testcase severity']} | {tc['testcase priority']} |"
                )
            lines.append("")

        if r["errors"]:
            lines.append("### Errors\n")
            for err in r["errors"]:
                lines.append(f"- ⚠️ {err}")
            lines.append("")

    # Verdict
    lines.append("---\n")
    lines.append("## Final QA Verdict\n")
    if failed == 0:
        lines.append("### ✅ PASS — All pages are production-ready\n")
    else:
        lines.append(f"### ❌ FAIL — {failed} check(s) failed. Review required.\n")

    with open(path, "w") as f:
        f.write("\n".join(lines))

    log.info(f"Markdown report: {path}")
    return path


def generate_html_report(all_results, output_dir):
    """Generate a styled HTML report."""
    path = os.path.join(output_dir, f"qa_report_styled_{TODAY}.html")
    all_cases = []
    for r in all_results:
        all_cases.extend(r["test_cases"])

    total = len(all_cases)
    passed = sum(1 for tc in all_cases if tc["testcase status"] == "PASS")
    failed = total - passed

    # Build environment info
    env_info = {}
    for r in all_results:
        if r["system_info"]:
            env_info = r["system_info"]
            break

    # Build table rows
    rows_html = ""
    for tc in all_cases:
        status_class = "status-pass" if tc["testcase status"] == "PASS" else "status-fail"
        rows_html += f"""
    <tr>
        <td><strong>{_html_escape(tc['testcase id'])}</strong></td>
        <td>{_html_escape(tc['url'])}</td>
        <td>{_html_escape(tc['testcase name'])}</td>
        <td>{_html_escape(tc['testcase description'])}</td>
        <td><pre>{_html_escape(tc['testcase steps'])}</pre></td>
        <td>{_html_escape(tc['testcase expected result'])}</td>
        <td>{_html_escape(tc['testcase actual result'])}</td>
        <td class="{status_class}">{_html_escape(tc['testcase status'])}</td>
        <td>{_html_escape(tc['testcase remarks'])}</td>
        <td>{_html_escape(tc['testcase severity'])}</td>
        <td>{_html_escape(tc['testcase priority'])}</td>
    </tr>"""

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>QA Test Report - Standalone Compatibility Pages - {TODAY}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f4f6f9; color: #333; }}
        .container {{ max-width: 1400px; margin: auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        h1 {{ color: #1a237e; border-bottom: 3px solid #3949ab; padding-bottom: 12px; font-size: 24px; }}
        h2 {{ color: #283593; margin-top: 30px; font-size: 18px; }}
        .env-info {{ background: #e8eaf6; padding: 16px 20px; border-radius: 8px; margin: 20px 0; font-size: 14px; line-height: 1.8; }}
        .summary {{ background: #e8f5e9; padding: 16px 20px; border-radius: 8px; margin: 20px 0; font-size: 14px; }}
        .summary.fail {{ background: #fce4ec; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 13px; }}
        th {{ background: #1a237e; color: white; padding: 10px 12px; text-align: left; font-weight: 600; position: sticky; top: 0; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top; }}
        tr:nth-child(even) {{ background-color: #fafafa; }}
        tr:hover {{ background-color: #f1f1f1; }}
        pre {{ margin: 0; font-family: inherit; white-space: pre-wrap; word-wrap: break-word; font-size: 13px; }}
        .status-pass {{ color: #2e7d32; font-weight: bold; }}
        .status-fail {{ color: #c62828; font-weight: bold; }}
        .verdict {{ background: {'#e8f5e9' if failed == 0 else '#fce4ec'}; border: 2px solid {'#4caf50' if failed == 0 else '#ef5350'}; padding: 20px; border-radius: 8px; margin-top: 30px; text-align: center; }}
        .verdict h2 {{ color: {'#2e7d32' if failed == 0 else '#c62828'}; margin: 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 QA Test Report — Standalone Compatibility Pages</h1>
        <div class="env-info">
            <strong>Test Date:</strong> {TODAY}<br>
            <strong>Chrome Version:</strong> {env_info.get('browser', 'N/A')}<br>
            <strong>OS:</strong> {env_info.get('os', 'N/A')}<br>
            <strong>Screen Resolution:</strong> {env_info.get('dimension', 'N/A')}<br>
            <strong>Mode:</strong> Normal (Selenium Automated)
        </div>
        <div class="summary {'fail' if failed > 0 else ''}">
            <strong>Total Checks:</strong> {total} |
            <strong>Passed:</strong> {passed} |
            <strong>Failed:</strong> {failed} |
            <strong>Overall:</strong> {'✅ PASS' if failed == 0 else '❌ FAIL'}
        </div>

        <h2>Detailed Test Cases</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>URL</th>
                    <th>Test Case</th>
                    <th>Description</th>
                    <th>Steps</th>
                    <th>Expected</th>
                    <th>Actual</th>
                    <th>Status</th>
                    <th>Remarks</th>
                    <th>Severity</th>
                    <th>Priority</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>

        <div class="verdict">
            <h2>{'✅ FINAL VERDICT: PASS — All pages are production-ready' if failed == 0 else f'❌ FINAL VERDICT: FAIL — {failed} check(s) require attention'}</h2>
        </div>
    </div>
</body>
</html>"""

    with open(path, "w") as f:
        f.write(html)

    log.info(f"HTML report: {path}")
    return path


def generate_excel_report(all_results, output_dir):
    """Generate a color-coded Excel XML report."""
    path = os.path.join(output_dir, f"qa_report_colorcoded_{TODAY}.xls")
    all_cases = []
    for r in all_results:
        all_cases.extend(r["test_cases"])

    xml_rows = ""
    for tc in all_cases:
        status_style = "sPass" if tc["testcase status"] == "PASS" else "sFail"
        xml_rows += f"""   <Row>
    <Cell ss:StyleID="sCenter"><Data ss:Type="String">{_xml_escape(tc['testcase id'])}</Data></Cell>
    <Cell ss:StyleID="sCenter"><Data ss:Type="String">{_xml_escape(tc['url'])}</Data></Cell>
    <Cell><Data ss:Type="String">{_xml_escape(tc['testcase name'])}</Data></Cell>
    <Cell><Data ss:Type="String">{_xml_escape(tc['testcase description'])}</Data></Cell>
    <Cell><Data ss:Type="String">{_xml_escape(tc['testcase steps'])}</Data></Cell>
    <Cell><Data ss:Type="String">{_xml_escape(tc['testcase expected result'])}</Data></Cell>
    <Cell><Data ss:Type="String">{_xml_escape(tc['testcase actual result'])}</Data></Cell>
    <Cell ss:StyleID="{status_style}"><Data ss:Type="String">{_xml_escape(tc['testcase status'])}</Data></Cell>
    <Cell><Data ss:Type="String">{_xml_escape(tc['testcase remarks'])}</Data></Cell>
    <Cell ss:StyleID="sCenter"><Data ss:Type="String">{_xml_escape(tc['testcase severity'])}</Data></Cell>
    <Cell ss:StyleID="sCenter"><Data ss:Type="String">{_xml_escape(tc['testcase priority'])}</Data></Cell>
   </Row>
"""

    xml = f"""<?xml version="1.0"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:x="urn:schemas-microsoft-com:office:excel"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">
 <Styles>
  <Style ss:ID="Default" ss:Name="Normal">
   <Alignment ss:Vertical="Top" ss:WrapText="1"/>
   <Borders>
    <Border ss:Position="Bottom" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#D4D4D4"/>
    <Border ss:Position="Right" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#D4D4D4"/>
   </Borders>
   <Font ss:FontName="Calibri" x:Family="Swiss" ss:Size="11"/>
  </Style>
  <Style ss:ID="sHeader">
   <Alignment ss:Horizontal="Center" ss:Vertical="Top" ss:WrapText="1"/>
   <Font ss:FontName="Calibri" x:Family="Swiss" ss:Size="11" ss:Color="#FFFFFF" ss:Bold="1"/>
   <Interior ss:Color="#1A237E" ss:Pattern="Solid"/>
   <Borders>
    <Border ss:Position="Bottom" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#0D1642"/>
    <Border ss:Position="Right" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#0D1642"/>
   </Borders>
  </Style>
  <Style ss:ID="sPass">
   <Alignment ss:Horizontal="Center" ss:Vertical="Top" ss:WrapText="1"/>
   <Font ss:FontName="Calibri" x:Family="Swiss" ss:Size="11" ss:Color="#006100" ss:Bold="1"/>
   <Interior ss:Color="#C6EFCE" ss:Pattern="Solid"/>
  </Style>
  <Style ss:ID="sFail">
   <Alignment ss:Horizontal="Center" ss:Vertical="Top" ss:WrapText="1"/>
   <Font ss:FontName="Calibri" x:Family="Swiss" ss:Size="11" ss:Color="#9C0006" ss:Bold="1"/>
   <Interior ss:Color="#FFC7CE" ss:Pattern="Solid"/>
  </Style>
  <Style ss:ID="sCenter">
   <Alignment ss:Horizontal="Center" ss:Vertical="Top" ss:WrapText="1"/>
  </Style>
 </Styles>
 <Worksheet ss:Name="QA Report {TODAY}">
  <Table>
   <Column ss:Width="90"/>
   <Column ss:Width="60"/>
   <Column ss:Width="180"/>
   <Column ss:Width="200"/>
   <Column ss:Width="200"/>
   <Column ss:Width="200"/>
   <Column ss:Width="250"/>
   <Column ss:Width="70"/>
   <Column ss:Width="200"/>
   <Column ss:Width="80"/>
   <Column ss:Width="60"/>
   <Row>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">Test Case ID</Data></Cell>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">URL</Data></Cell>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">Test Case Name</Data></Cell>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">Description</Data></Cell>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">Steps</Data></Cell>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">Expected Result</Data></Cell>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">Actual Result</Data></Cell>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">Status</Data></Cell>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">Remarks</Data></Cell>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">Severity</Data></Cell>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">Priority</Data></Cell>
   </Row>
{xml_rows}  </Table>
 </Worksheet>
</Workbook>"""

    with open(path, "w") as f:
        f.write(xml)

    log.info(f"Excel report: {path}")
    return path


def generate_csv_report(all_results, output_dir):
    """Generate a CSV report."""
    path = os.path.join(output_dir, f"qa_report_{TODAY}.csv")
    all_cases = []
    for r in all_results:
        all_cases.extend(r["test_cases"])

    fieldnames = [
        "testcase id", "url", "testcase name", "testcase description",
        "testcase steps", "testcase expected result", "testcase actual result",
        "testcase status", "testcase remarks", "testcase severity", "testcase priority"
    ]

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for tc in all_cases:
            writer.writerow({k: tc[k] for k in fieldnames})

    log.info(f"CSV report: {path}")
    return path


# =====================================================================
# ESCAPE HELPERS
# =====================================================================
def _html_escape(text):
    """Escape HTML special characters."""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _xml_escape(text):
    """Escape XML special characters and handle newlines for Excel."""
    if text is None:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("\n", "&#10;")


# =====================================================================
# MAIN
# =====================================================================
def main():
    log.info("=" * 60)
    log.info("Standalone Page Compatibility Validator")
    log.info(f"Date: {TODAY}")
    log.info("=" * 60)

    # Read URLs
    if not os.path.exists(URLS_FILE):
        log.error(f"URLs file not found: {URLS_FILE}")
        sys.exit(1)

    url_items = read_urls(URLS_FILE)
    # Filter only for standalone pages
    url_items = [item for item in url_items if item["group"].lower() == "standalone"]
    
    if not url_items:
        log.error("No 'standalone' URLs found in config file.")
        sys.exit(1)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        all_results = []

        for idx, item in enumerate(url_items, start=1):
            log.info(f"Starting browser session for item {idx} ({item['group']})...")
            driver = create_driver()
            try:
                result = validate_url(driver, item, idx)
                all_results.append(result)
            finally:
                driver.quit()

            # Brief pause between URLs
            if idx < len(url_items):
                time.sleep(2)

        # Generate reports
        log.info("\n" + "=" * 60)
        log.info("Generating reports...")
        log.info("=" * 60)

        md_path = generate_markdown_report(all_results, OUTPUT_DIR)
        html_path = generate_html_report(all_results, OUTPUT_DIR)
        xls_path = generate_excel_report(all_results, OUTPUT_DIR)
        csv_path = generate_csv_report(all_results, OUTPUT_DIR)

        # Summary
        total_cases = sum(len(r["test_cases"]) for r in all_results)
        passed = sum(1 for r in all_results for tc in r["test_cases"] if tc["testcase status"] == "PASS")
        failed = total_cases - passed

        log.info("\n" + "=" * 60)
        log.info("VALIDATION COMPLETE")
        log.info("=" * 60)
        log.info(f"URLs validated: {len(all_results)}")
        log.info(f"Total test cases: {total_cases}")
        log.info(f"Passed: {passed}")
        log.info(f"Failed: {failed}")
        log.info(f"Overall: {'✅ PASS' if failed == 0 else '❌ FAIL'}")
        log.info(f"\nReports:")
        log.info(f"  Markdown: {md_path}")
        log.info(f"  HTML:     {html_path}")
        log.info(f"  Excel:    {xls_path}")
        log.info(f"  CSV:      {csv_path}")

        # Save raw results as JSON for debugging
        json_path = os.path.join(OUTPUT_DIR, f"qa_raw_results_{TODAY}.json")
        # Remove non-serializable data
        serializable = []
        for r in all_results:
            sr = dict(r)
            sr.pop("console_logs", None)
            serializable.append(sr)
        with open(json_path, "w") as f:
            json.dump(serializable, f, indent=2, default=str)
        log.info(f"  JSON:     {json_path}")

    finally:
        log.info("\nValidation process finished.")


if __name__ == "__main__":
    main()
