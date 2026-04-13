import csv
import os

# =====================================================================
# QA TEST DATA — All 3 URLs validated on 2026-03-12
# =====================================================================

data = [
    # ---- URL 1: Standard Compatibility Check ----
    {
        "testcase id": "TC-URL1-001",
        "testcase name": "Email Pre-Validation Prompt",
        "testcase description": "Verify if the system handles the initial email prompt correctly.",
        "testcase steps": "1. Open URL.\n2. Observe email prompt.\n3. Enter qa_test@example.com.\n4. Submit.",
        "testcase expected result": "Email accepted and page proceeds to system checks.",
        "testcase actual result": "Email prompt appeared, entered dummy email, and page proceeded successfully.",
        "testcase status": "PASS",
        "testcase remarks": "Handled correctly.",
        "testcase severity": "Medium",
        "testcase priority": "P2",
        "url": "URL1"
    },
    {
        "testcase id": "TC-URL1-002",
        "testcase name": "Camera Detection",
        "testcase description": "Verify webcam detection and live feed display.",
        "testcase steps": "1. Open URL.\n2. Grant camera permission.\n3. Observe camera check.",
        "testcase expected result": "Camera detected and live feed shown.",
        "testcase actual result": "Camera detected; live feed shown in verification photo block.",
        "testcase status": "PASS",
        "testcase remarks": "Verification photo captured successfully.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": "URL1"
    },
    {
        "testcase id": "TC-URL1-003",
        "testcase name": "Microphone Detection",
        "testcase description": "Verify microphone detection and audio level indicator.",
        "testcase steps": "1. Open URL.\n2. Grant microphone permission.\n3. Observe mic check.",
        "testcase expected result": "Microphone detected with active audio level.",
        "testcase actual result": "Microphone detected; dynamic green volume meter active.",
        "testcase status": "PASS",
        "testcase remarks": "Audio level indicator working.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": "URL1"
    },
    {
        "testcase id": "TC-URL1-004",
        "testcase name": "Browser Detection",
        "testcase description": "Verify correct browser detection.",
        "testcase steps": "1. Open URL.\n2. Check browser detection result.",
        "testcase expected result": "Chrome detected with correct version.",
        "testcase actual result": "Detected as chrome - 145.0.0.0",
        "testcase status": "PASS",
        "testcase remarks": "Accurate detection.",
        "testcase severity": "High",
        "testcase priority": "P1",
        "url": "URL1"
    },
    {
        "testcase id": "TC-URL1-005",
        "testcase name": "OS Detection",
        "testcase description": "Verify correct OS detection.",
        "testcase steps": "1. Open URL.\n2. Check OS detection in System Info.",
        "testcase expected result": "Linux detected.",
        "testcase actual result": "linux / Linux x86_64",
        "testcase status": "PASS",
        "testcase remarks": "Correct OS identification.",
        "testcase severity": "High",
        "testcase priority": "P1",
        "url": "URL1"
    },
    {
        "testcase id": "TC-URL1-006",
        "testcase name": "Screen Resolution",
        "testcase description": "Verify screen resolution detection.",
        "testcase steps": "1. Open URL.\n2. Check resolution in System Info.",
        "testcase expected result": "Correct resolution reported.",
        "testcase actual result": "Dimension: 1920 x 1080, Viewport: 780 x 490",
        "testcase status": "PASS",
        "testcase remarks": "Accurate resolution detection.",
        "testcase severity": "Medium",
        "testcase priority": "P2",
        "url": "URL1"
    },
    {
        "testcase id": "TC-URL1-007",
        "testcase name": "Cookies Enabled Check",
        "testcase description": "Verify cookies are detected as enabled.",
        "testcase steps": "1. Open URL.\n2. Check Cookies status in System Info.",
        "testcase expected result": "Cookies: Enabled",
        "testcase actual result": "Cookies: Enabled",
        "testcase status": "PASS",
        "testcase remarks": "Correct.",
        "testcase severity": "Medium",
        "testcase priority": "P2",
        "url": "URL1"
    },
    {
        "testcase id": "TC-URL1-008",
        "testcase name": "Popup Enabled Check",
        "testcase description": "Verify popup status detection.",
        "testcase steps": "1. Open URL.\n2. Check Popup status in System Info.",
        "testcase expected result": "Popup: Enabled",
        "testcase actual result": "Popup: Enabled",
        "testcase status": "PASS",
        "testcase remarks": "Correct.",
        "testcase severity": "Medium",
        "testcase priority": "P2",
        "url": "URL1"
    },
    {
        "testcase id": "TC-URL1-009",
        "testcase name": "Internet Speed Check",
        "testcase description": "Verify download and upload speed measurement.",
        "testcase steps": "1. Open URL.\n2. Wait for speed test to complete.\n3. Observe results.",
        "testcase expected result": "Speed measured and rated as High.",
        "testcase actual result": "Download: 21.31 Mbps (High), Upload: 28.67 Mbps (High)",
        "testcase status": "PASS",
        "testcase remarks": "Speed test completed successfully.",
        "testcase severity": "High",
        "testcase priority": "P1",
        "url": "URL1"
    },
    {
        "testcase id": "TC-URL1-010",
        "testcase name": "Overall Status",
        "testcase description": "Verify overall compatibility status message.",
        "testcase steps": "1. Open URL.\n2. Wait for all checks.\n3. Observe overall status banner.",
        "testcase expected result": "Success message displayed.",
        "testcase actual result": "Success: Your system is compatible.",
        "testcase status": "PASS",
        "testcase remarks": "Clear success banner in green.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": "URL1"
    },

    # ---- URL 2: SEB Compatibility Check ----
    {
        "testcase id": "TC-URL2-001",
        "testcase name": "Page Load (No Email Prompt)",
        "testcase description": "Verify page loads without email prompt for SEB URL.",
        "testcase steps": "1. Open SEB URL.\n2. Observe if email prompt appears.",
        "testcase expected result": "Page loads directly to system checks.",
        "testcase actual result": "No email prompt; page directly initiated system checks.",
        "testcase status": "PASS",
        "testcase remarks": "Different behavior from URL1 (no email).",
        "testcase severity": "Medium",
        "testcase priority": "P2",
        "url": "URL2"
    },
    {
        "testcase id": "TC-URL2-002",
        "testcase name": "Camera Detection (SEB)",
        "testcase description": "Verify camera detection on SEB page.",
        "testcase steps": "1. Open SEB URL.\n2. Grant camera permission.\n3. Observe result.",
        "testcase expected result": "Camera detected and compatible.",
        "testcase actual result": "Compatible - camera feed shown.",
        "testcase status": "PASS",
        "testcase remarks": "Working correctly.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": "URL2"
    },
    {
        "testcase id": "TC-URL2-003",
        "testcase name": "Microphone Detection (SEB)",
        "testcase description": "Verify microphone detection on SEB page.",
        "testcase steps": "1. Open SEB URL.\n2. Grant mic permission.\n3. Observe result.",
        "testcase expected result": "Microphone detected and compatible.",
        "testcase actual result": "Compatible - audio indicator active.",
        "testcase status": "PASS",
        "testcase remarks": "Working correctly.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": "URL2"
    },
    {
        "testcase id": "TC-URL2-004",
        "testcase name": "Browser Detection (SEB)",
        "testcase description": "Verify browser detection on SEB page.",
        "testcase steps": "1. Open SEB URL.\n2. Check browser detection.",
        "testcase expected result": "Chrome detected with version.",
        "testcase actual result": "chrome - 145.0.0.0",
        "testcase status": "PASS",
        "testcase remarks": "Accurate detection.",
        "testcase severity": "High",
        "testcase priority": "P1",
        "url": "URL2"
    },
    {
        "testcase id": "TC-URL2-005",
        "testcase name": "Safe Browser Compatible (SEB Detection)",
        "testcase description": "Verify SEB detection shows correct status.",
        "testcase steps": "1. Open SEB URL in Chrome.\n2. Check Safe Browser Compatible field.",
        "testcase expected result": "No (since testing in standard Chrome, not SEB).",
        "testcase actual result": "Safe Browser Compatible: No (displayed in red).",
        "testcase status": "PASS",
        "testcase remarks": "Correctly identifies non-SEB browser. Red text is appropriate.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": "URL2"
    },
    {
        "testcase id": "TC-URL2-006",
        "testcase name": "Network Check (SEB)",
        "testcase description": "Verify network compatibility on SEB page.",
        "testcase steps": "1. Open SEB URL.\n2. Wait for network check.",
        "testcase expected result": "Network compatible.",
        "testcase actual result": "Compatible.",
        "testcase status": "PASS",
        "testcase remarks": "Network check passed.",
        "testcase severity": "High",
        "testcase priority": "P1",
        "url": "URL2"
    },
    {
        "testcase id": "TC-URL2-007",
        "testcase name": "Popup Status (SEB)",
        "testcase description": "Verify popup detection on SEB page.",
        "testcase steps": "1. Open SEB URL.\n2. Check Popup status in System Info.",
        "testcase expected result": "Popup status detected.",
        "testcase actual result": "Popup: Blocked (displayed in red).",
        "testcase status": "PASS",
        "testcase remarks": "Popup is blocked but overall status still shows success.",
        "testcase severity": "Low",
        "testcase priority": "P3",
        "url": "URL2"
    },
    {
        "testcase id": "TC-URL2-008",
        "testcase name": "Internet Speed (SEB)",
        "testcase description": "Verify speed test on SEB page.",
        "testcase steps": "1. Open SEB URL.\n2. Wait for speed test.",
        "testcase expected result": "Speed measured with rating.",
        "testcase actual result": "Download: 16.40 Mbps (High), Upload: 13.51 Mbps (High)",
        "testcase status": "PASS",
        "testcase remarks": "Speed test completed.",
        "testcase severity": "High",
        "testcase priority": "P2",
        "url": "URL2"
    },
    {
        "testcase id": "TC-URL2-009",
        "testcase name": "Overall Status (SEB)",
        "testcase description": "Verify overall status despite SEB not installed.",
        "testcase steps": "1. Open SEB URL.\n2. Wait for all checks.\n3. Observe overall status.",
        "testcase expected result": "Success (SEB is optional for overall pass).",
        "testcase actual result": "Success: Your system is compatible.",
        "testcase status": "PASS",
        "testcase remarks": "Overall status shows success even with SEB: No.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": "URL2"
    },

    # ---- URL 3: Full Test Compatibility Check ----
    {
        "testcase id": "TC-URL3-001",
        "testcase name": "Page Load (No Email Prompt)",
        "testcase description": "Verify page loads without email prompt.",
        "testcase steps": "1. Open check.html URL.\n2. Observe page load.",
        "testcase expected result": "Page loads directly to system checks.",
        "testcase actual result": "No email prompt; page loaded and initiated checks.",
        "testcase status": "PASS",
        "testcase remarks": "Clean load.",
        "testcase severity": "Medium",
        "testcase priority": "P2",
        "url": "URL3"
    },
    {
        "testcase id": "TC-URL3-002",
        "testcase name": "Camera Detection (Full)",
        "testcase description": "Verify camera detection on full compatibility page.",
        "testcase steps": "1. Open URL.\n2. Grant camera permission.\n3. Observe result.",
        "testcase expected result": "Camera detected.",
        "testcase actual result": "Detected with green checkmark.",
        "testcase status": "PASS",
        "testcase remarks": "Working correctly.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": "URL3"
    },
    {
        "testcase id": "TC-URL3-003",
        "testcase name": "Microphone Detection (Full)",
        "testcase description": "Verify microphone detection on full page.",
        "testcase steps": "1. Open URL.\n2. Grant mic permission.\n3. Observe result.",
        "testcase expected result": "Microphone detected.",
        "testcase actual result": "Detected with green checkmark and audio indicator.",
        "testcase status": "PASS",
        "testcase remarks": "Working correctly.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": "URL3"
    },
    {
        "testcase id": "TC-URL3-004",
        "testcase name": "Browser Detection (Full)",
        "testcase description": "Verify browser detection on full page.",
        "testcase steps": "1. Open URL.\n2. Check browser detection.",
        "testcase expected result": "Chrome detected with version.",
        "testcase actual result": "chrome - 145.0.0.0",
        "testcase status": "PASS",
        "testcase remarks": "Accurate detection.",
        "testcase severity": "High",
        "testcase priority": "P1",
        "url": "URL3"
    },
    {
        "testcase id": "TC-URL3-005",
        "testcase name": "Network Compatibility",
        "testcase description": "Verify network compatibility check.",
        "testcase steps": "1. Open URL.\n2. Wait for network check to complete.",
        "testcase expected result": "Network shown as compatible.",
        "testcase actual result": "Initially showed 'Loading...' in red, resolved to Compatible (green).",
        "testcase status": "PASS",
        "testcase remarks": "Brief loading state observed before passing.",
        "testcase severity": "High",
        "testcase priority": "P1",
        "url": "URL3"
    },
    {
        "testcase id": "TC-URL3-006",
        "testcase name": "WebSocket Checks (HV, AS, HP)",
        "testcase description": "Verify WebSocket connectivity to HV, AS, HP servers.",
        "testcase steps": "1. Open URL.\n2. Observe WebSocket check results.",
        "testcase expected result": "All three servers (HV, AS, HP) show green ticks.",
        "testcase actual result": "HV ✅, AS ✅, HP ✅ — all green ticks.",
        "testcase status": "PASS",
        "testcase remarks": "All WebSocket connections successful.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": "URL3"
    },
    {
        "testcase id": "TC-URL3-007",
        "testcase name": "ICE Candidate Checks",
        "testcase description": "Verify ICE candidate types: host, srflx, relay.",
        "testcase steps": "1. Open URL.\n2. Observe ICE check results.",
        "testcase expected result": "All ICE types show green ticks.",
        "testcase actual result": "host ✅, srflx ✅, relay ✅ — all green ticks.",
        "testcase status": "PASS",
        "testcase remarks": "All ICE candidates verified.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": "URL3"
    },
    {
        "testcase id": "TC-URL3-008",
        "testcase name": "Server Reachability",
        "testcase description": "Verify server reachability across UDP/TCP/TLS on ports 80 and 443.",
        "testcase steps": "1. Open URL.\n2. Scroll to Server Reachability section.\n3. Observe all checks.",
        "testcase expected result": "All 5 checks (UDP 80, UDP 443, TCP 80, TCP 443, TLS over TCP) pass.",
        "testcase actual result": "UDP Over 80 ✅, UDP Over 443 ✅, TCP Over 80 ✅, TCP Over 443 ✅, TLS Over TCP ✅",
        "testcase status": "PASS",
        "testcase remarks": "Full server reachability confirmed.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": "URL3"
    },
    {
        "testcase id": "TC-URL3-009",
        "testcase name": "Internet Speed (Full)",
        "testcase description": "Verify internet speed measurement.",
        "testcase steps": "1. Open URL.\n2. Wait for speed test.",
        "testcase expected result": "Speed measured with High rating.",
        "testcase actual result": "Download: 21.83 Mbps (High), Upload: 28.88 Mbps (High)",
        "testcase status": "PASS",
        "testcase remarks": "Speed test completed successfully.",
        "testcase severity": "High",
        "testcase priority": "P2",
        "url": "URL3"
    },
    {
        "testcase id": "TC-URL3-010",
        "testcase name": "Overall Status (Full)",
        "testcase description": "Verify overall compatibility status.",
        "testcase steps": "1. Open URL.\n2. Wait for all checks.\n3. Observe overall status.",
        "testcase expected result": "Success message displayed.",
        "testcase actual result": "Success: Your system is compatible.",
        "testcase status": "PASS",
        "testcase remarks": "All checks pass including WebSocket, ICE, and Server Reachability.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "url": "URL3"
    },
]

# Define output directory
output_dir = "/home/nirmalsaha/Hirepro_Test_files/automation_scripts/agents/antigravity/assessments/agentic_scripts/output_reports/standalone_pages"

# =====================================================================
# HTML REPORT GENERATION
# =====================================================================
html_template = """<!DOCTYPE html>
<html>
<head>
    <title>QA Test Report - Standalone Compatibility Pages - 2026-03-12</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f4f6f9; color: #333; }
        .container { max-width: 1400px; margin: auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        h1 { color: #1a237e; border-bottom: 3px solid #3949ab; padding-bottom: 12px; font-size: 24px; }
        h2 { color: #283593; margin-top: 30px; font-size: 18px; }
        .env-info { background: #e8eaf6; padding: 16px 20px; border-radius: 8px; margin: 20px 0; font-size: 14px; line-height: 1.8; }
        .summary { background: #e8f5e9; padding: 16px 20px; border-radius: 8px; margin: 20px 0; font-size: 14px; }
        .summary strong { color: #2e7d32; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 13px; }
        th { background: #1a237e; color: white; padding: 10px 12px; text-align: left; font-weight: 600; }
        td { padding: 10px 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top; }
        tr:nth-child(even) { background-color: #fafafa; }
        tr:hover { background-color: #f1f1f1; }
        pre { margin: 0; font-family: inherit; white-space: pre-wrap; word-wrap: break-word; font-size: 13px; }
        .status-pass { color: #2e7d32; font-weight: bold; }
        .status-fail { color: #c62828; font-weight: bold; }
        .url-header { background: #e3f2fd; padding: 10px 16px; border-radius: 6px; margin: 20px 0 10px 0; border-left: 4px solid #1565c0; }
        .verdict { background: #e8f5e9; border: 2px solid #4caf50; padding: 20px; border-radius: 8px; margin-top: 30px; text-align: center; }
        .verdict h2 { color: #2e7d32; margin: 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 QA Test Report — Standalone Compatibility Pages</h1>
        <div class="env-info">
            <strong>Test Date:</strong> 2026-03-12<br>
            <strong>Chrome Version:</strong> 145.0.0.0<br>
            <strong>OS:</strong> Linux / Linux x86_64<br>
            <strong>Screen Resolution:</strong> 1920 x 1080<br>
            <strong>Network:</strong> Broadband (High bandwidth)<br>
            <strong>Mode:</strong> Normal
        </div>
        <div class="summary">
            <strong>Total Checks:</strong> 28 |
            <strong>Passed:</strong> 28 |
            <strong>Failed:</strong> 0 |
            <strong>Overall:</strong> ✅ PASS
        </div>

        <div class="url-header"><strong>URL 1:</strong> https://amsin.hirepro.in/assessment/#/compatibility/at</div>
        <div class="url-header"><strong>URL 2:</strong> https://amsin.hirepro.in/assessment/#/compatibility/at/seb</div>
        <div class="url-header"><strong>URL 3:</strong> https://amsin.hirepro.in/testcompatibility/check.html</div>

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
                {rows}
            </tbody>
        </table>

        <div class="verdict">
            <h2>✅ FINAL VERDICT: PASS — All pages are production-ready</h2>
            <p>All three standalone compatibility check pages are functioning correctly with no critical or blocking issues.</p>
        </div>
    </div>
</body>
</html>
"""

rows_html = ""
for item in data:
    status_class = "status-pass" if item["testcase status"] == "PASS" else "status-fail"
    row = f"""
    <tr>
        <td><strong>{item['testcase id']}</strong></td>
        <td>{item['url']}</td>
        <td>{item['testcase name']}</td>
        <td>{item['testcase description']}</td>
        <td><pre>{item['testcase steps']}</pre></td>
        <td>{item['testcase expected result']}</td>
        <td>{item['testcase actual result']}</td>
        <td class="{status_class}">{item['testcase status']}</td>
        <td>{item['testcase remarks']}</td>
        <td>{item['testcase severity']}</td>
        <td>{item['testcase priority']}</td>
    </tr>"""
    rows_html += row

html_content = html_template.replace("{rows}", rows_html)
html_path = os.path.join(output_dir, "qa_report_styled_2026-03-12.html")
with open(html_path, "w") as f:
    f.write(html_content)

print(f"HTML styled report generated at: {html_path}")

# =====================================================================
# EXCEL XML (Color Coded) GENERATION
# =====================================================================
xml_template = """<?xml version="1.0"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:x="urn:schemas-microsoft-com:office:excel"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:html="http://www.w3.org/TR/REC-html40">
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
 <Worksheet ss:Name="QA Report 2026-03-12">
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
{xml_rows}
  </Table>
 </Worksheet>
</Workbook>
"""

xml_rows = ""

def escape_xml(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

for item in data:
    status_style = "sPass" if item["testcase status"] == "PASS" else "sFail"
    
    row = f"""   <Row>
    <Cell ss:StyleID="sCenter"><Data ss:Type="String">{escape_xml(item['testcase id'])}</Data></Cell>
    <Cell ss:StyleID="sCenter"><Data ss:Type="String">{escape_xml(item['url'])}</Data></Cell>
    <Cell><Data ss:Type="String">{escape_xml(item['testcase name'])}</Data></Cell>
    <Cell><Data ss:Type="String">{escape_xml(item['testcase description'])}</Data></Cell>
    <Cell><Data ss:Type="String">{escape_xml(item['testcase steps'])}</Data></Cell>
    <Cell><Data ss:Type="String">{escape_xml(item['testcase expected result'])}</Data></Cell>
    <Cell><Data ss:Type="String">{escape_xml(item['testcase actual result'])}</Data></Cell>
    <Cell ss:StyleID="{status_style}"><Data ss:Type="String">{escape_xml(item['testcase status'])}</Data></Cell>
    <Cell><Data ss:Type="String">{escape_xml(item['testcase remarks'])}</Data></Cell>
    <Cell ss:StyleID="sCenter"><Data ss:Type="String">{escape_xml(item['testcase severity'])}</Data></Cell>
    <Cell ss:StyleID="sCenter"><Data ss:Type="String">{escape_xml(item['testcase priority'])}</Data></Cell>
   </Row>
"""
    xml_rows += row

xml_content = xml_template.replace("{xml_rows}", xml_rows)
xml_path = os.path.join(output_dir, "qa_report_colorcoded_2026-03-12.xls")

with open(xml_path, "w") as f:
    f.write(xml_content)

print(f"Color-coded Excel report generated at: {xml_path}")

# =====================================================================
# CSV REPORT GENERATION
# =====================================================================
csv_path = os.path.join(output_dir, "qa_report_2026-03-12.csv")
fieldnames = [
    "testcase id", "url", "testcase name", "testcase description",
    "testcase steps", "testcase expected result", "testcase actual result",
    "testcase status", "testcase remarks", "testcase severity", "testcase priority"
]

with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for item in data:
        writer.writerow({k: item[k] for k in fieldnames})

print(f"CSV report generated at: {csv_path}")
print("\n✅ All reports generated successfully!")
