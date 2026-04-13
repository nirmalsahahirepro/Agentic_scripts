import os

data = [
    {
        "testcase id": "TC-001",
        "testcase name": "Browser Detection Verification",
        "testcase description": "Verify if the system correctly detects the Chrome browser and its version.",
        "testcase steps": "1. Open URL in Chrome.\n2. Wait for auto-checks.\n3. Check Browser row.",
        "testcase expected result": "Correctly identify Chrome and version.",
        "testcase actual result": "Detected: chrome - 145.0.0.0",
        "testcase status": "PASS",
        "testcase remarks": "Accurate detection.",
        "testcase severity": "High",
        "testcase priority": "P1",
        "testcase reproducibility": "Always",
        "testcase console errors": "None",
        "testcase permission handling results": "N/A",
        "testcase ui/ux observations": "Clear row displaying info.",
        "testcase performance observations": "Instant.",
        "testcase security concerns": "None",
        "testcase final qa verdict": "Ready"
    },
    {
        "testcase id": "TC-002",
        "testcase name": "OS Detection Verification",
        "testcase description": "Verify if the system correctly detects the Linux OS.",
        "testcase steps": "1. Open URL in Chrome.\n2. Wait for auto-checks.\n3. Check OS row.",
        "testcase expected result": "Identify Linux OS.",
        "testcase actual result": "Detected: linux / Linux x86_64",
        "testcase status": "PASS",
        "testcase remarks": "Accurate detection.",
        "testcase severity": "High",
        "testcase priority": "P1",
        "testcase reproducibility": "Always",
        "testcase console errors": "None",
        "testcase permission handling results": "N/A",
        "testcase ui/ux observations": "Clear row displaying info.",
        "testcase performance observations": "Instant.",
        "testcase security concerns": "None",
        "testcase final qa verdict": "Ready"
    },
    {
        "testcase id": "TC-003",
        "testcase name": "Screen Resolution Check",
        "testcase description": "Verify if the system correctly detects screen resolution.",
        "testcase steps": "1. Open URL in Chrome.\n2. Wait for auto-checks.\n3. Check Screen Resolution row.",
        "testcase expected result": "Identify resolution correctly (e.g. 1920x1080).",
        "testcase actual result": "Detected: 1920x1080 (avail: 1920x961)",
        "testcase status": "PASS",
        "testcase remarks": "Handled correctly.",
        "testcase severity": "Medium",
        "testcase priority": "P2",
        "testcase reproducibility": "Always",
        "testcase console errors": "None",
        "testcase permission handling results": "N/A",
        "testcase ui/ux observations": "None",
        "testcase performance observations": "Instant.",
        "testcase security concerns": "None",
        "testcase final qa verdict": "Ready"
    },
    {
        "testcase id": "TC-004",
        "testcase name": "Webcam Permission and Detection",
        "testcase description": "Verify webcam permission request and preview.",
        "testcase steps": "1. Open URL.\n2. Click allow camera.\n3. Observe preview.",
        "testcase expected result": "Request access, show preview upon allow.",
        "testcase actual result": "Perm granted, live video preview shown, green check.",
        "testcase status": "PASS",
        "testcase remarks": "Functions perfectly.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "testcase reproducibility": "Always",
        "testcase console errors": "None",
        "testcase permission handling results": "Handled gracefully. Deny shows error, allow shows preview. Recovery button works.",
        "testcase ui/ux observations": "Clear video stream in center.",
        "testcase performance observations": "No lag.",
        "testcase security concerns": "Uses native secure WebRTC.",
        "testcase final qa verdict": "Ready"
    },
    {
        "testcase id": "TC-005",
        "testcase name": "Microphone Permission and Detection",
        "testcase description": "Verify microphone permission request and audio level detection.",
        "testcase steps": "1. Open URL.\n2. Click allow mic.\n3. Speak and observe bar.",
        "testcase expected result": "Request access, detect sound levels with visual bar.",
        "testcase actual result": "Perm granted, sound bar oscilates, green check.",
        "testcase status": "PASS",
        "testcase remarks": "Functions perfectly.",
        "testcase severity": "Critical",
        "testcase priority": "P1",
        "testcase reproducibility": "Always",
        "testcase console errors": "None",
        "testcase permission handling results": "Graceful. Deny msg: 'Please speak higher...'",
        "testcase ui/ux observations": "Oscillating green bar.",
        "testcase performance observations": "Real-time.",
        "testcase security concerns": "Native permissions.",
        "testcase final qa verdict": "Ready"
    },
    {
        "testcase id": "TC-006",
        "testcase name": "Network Speed Check",
        "testcase description": "Verify upload and download speed calculation.",
        "testcase steps": "1. Open URL.\n2. Check Bandwidth row.",
        "testcase expected result": "Validate download/upload speeds.",
        "testcase actual result": "Down: 36.66 Mbps, Up: 23.39 Mbps",
        "testcase status": "PASS",
        "testcase remarks": "Handled correctly.",
        "testcase severity": "High",
        "testcase priority": "P2",
        "testcase reproducibility": "Always",
        "testcase console errors": "None",
        "testcase permission handling results": "N/A",
        "testcase ui/ux observations": "None",
        "testcase performance observations": "Fast execution.",
        "testcase security concerns": "None",
        "testcase final qa verdict": "Ready"
    },
    {
        "testcase id": "TC-007",
        "testcase name": "Server Reachability - TCP",
        "testcase description": "Verify Server TCP Reachability.",
        "testcase steps": "1. Open URL.\n2. Check Server Reachability section.",
        "testcase expected result": "Verify UDP, TCP, TLS.",
        "testcase actual result": "UDP: PASS, TLS: PASS, TCP over 80/443: FAIL",
        "testcase status": "FAIL",
        "testcase remarks": "TCP failure doesn't block overall pass execution.",
        "testcase severity": "Low",
        "testcase priority": "P4",
        "testcase reproducibility": "Always",
        "testcase console errors": "None",
        "testcase permission handling results": "N/A",
        "testcase ui/ux observations": "Contradictory UI (Red X vs Overall Success).",
        "testcase performance observations": "N/A",
        "testcase security concerns": "None",
        "testcase final qa verdict": "Ready for production, but UX can be improved."
    },
    {
        "testcase id": "TC-008",
        "testcase name": "Accessibility - Keyboard Navigation",
        "testcase description": "Verify if interactive elements are focusable via keyboard.",
        "testcase steps": "1. Open URL.\n2. Press Tab repeatedly.",
        "testcase expected result": "Elements have a clear focus ring.",
        "testcase actual result": "Elements are focusable but lack a clear visual indicator.",
        "testcase status": "FAIL",
        "testcase remarks": "Missing visual focus ring for keyboard navigation.",
        "testcase severity": "Low",
        "testcase priority": "P4",
        "testcase reproducibility": "Always",
        "testcase console errors": "None",
        "testcase permission handling results": "N/A",
        "testcase ui/ux observations": "Missing focus rings.",
        "testcase performance observations": "N/A",
        "testcase security concerns": "None",
        "testcase final qa verdict": "Requires minor fix."
    }
]

# ----------------- HTML REPORT GENERATION -----------------
html_template = """<!DOCTYPE html>
<html>
<head>
    <title>QA Test Report - HirePro Compatibility</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f9f9f9; color: #333;}
        .container { background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width: 1200px; margin: auto; }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .env-info { background: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-size: 14px;}
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #e0e0e0; padding: 12px 15px; text-align: left; vertical-align: top; }
        th { background-color: #34495e; color: #fff; position: sticky; top: 0; font-weight: 500; }
        .status-pass { background-color: #d4edda; color: #155724; font-weight: bold; border-radius: 4px; padding: 4px 8px; display: inline-block;}
        .status-fail { background-color: #f8d7da; color: #721c24; font-weight: bold; border-radius: 4px; padding: 4px 8px; display: inline-block;}
        tr:nth-child(even) { background-color: #fafafa; }
        tr:hover { background-color: #f1f1f1; }
        pre { margin: 0; font-family: inherit; white-space: pre-wrap; word-wrap: break-word; font-size: 13px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>QA Test Report - System Compatibility Check</h1>
        <div class="env-info">
            <strong>Environment Details:</strong><br>
            • Chrome 145.0.0.0 &nbsp;&nbsp;|&nbsp;&nbsp; • Linux x86_64 &nbsp;&nbsp;|&nbsp;&nbsp; • 1920x1080 &nbsp;&nbsp;|&nbsp;&nbsp; • Normal Mode
        </div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Steps to Reproduce</th>
                    <th>Expected Result</th>
                    <th>Actual Result</th>
                    <th>Status</th>
                    <th>Remarks</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
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
        <td>{item['testcase name']}</td>
        <td>{item['testcase description']}</td>
        <td><pre>{item['testcase steps']}</pre></td>
        <td>{item['testcase expected result']}</td>
        <td>{item['testcase actual result']}</td>
        <td><span class="{status_class}">{item['testcase status']}</span></td>
        <td>{item['testcase remarks']}</td>
    </tr>
    """
    rows_html += row

html_content = html_template.replace("{rows}", rows_html)
html_path = "/home/nirmalsaha/Hirepro_Test_files/automation_scripts/agents/antigravity/assessments/agentic_scripts/output_reports/standalone_pages/qa_report_styled_2026-03-09.html"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML styled report generated at: {html_path}")

# ----------------- EXCEL XML (Color Coded) GENERATION -----------------
# XML Spreadsheet 2003 format allows native Excel styling without 3rd party libraries
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
    <Border ss:Position="Left" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#D4D4D4"/>
    <Border ss:Position="Right" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#D4D4D4"/>
    <Border ss:Position="Top" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#D4D4D4"/>
   </Borders>
   <Font ss:FontName="Calibri" x:Family="Swiss" ss:Size="11" ss:Color="#000000"/>
  </Style>
  <Style ss:ID="sHeader">
   <Alignment ss:Horizontal="Center" ss:Vertical="Top" ss:WrapText="1"/>
   <Font ss:FontName="Calibri" x:Family="Swiss" ss:Size="12" ss:Color="#FFFFFF" ss:Bold="1"/>
   <Interior ss:Color="#2F5597" ss:Pattern="Solid"/>
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
 <Worksheet ss:Name="QA Report">
  <Table>
   <Column ss:Width="65"/>  <!-- ID -->
   <Column ss:Width="160"/> <!-- Name -->
   <Column ss:Width="200"/> <!-- Desc -->
   <Column ss:Width="150"/> <!-- Steps -->
   <Column ss:Width="180"/> <!-- Expected -->
   <Column ss:Width="180"/> <!-- Actual -->
   <Column ss:Width="80"/>  <!-- Status -->
   <Column ss:Width="180"/> <!-- Remarks -->
   <Column ss:Width="80"/>  <!-- Severity -->
   <Column ss:Width="80"/>  <!-- Priority -->
   
   <Row ss:Height="25">
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">ID</Data></Cell>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">Test Case Name</Data></Cell>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">Description</Data></Cell>
    <Cell ss:StyleID="sHeader"><Data ss:Type="String">Steps to Reproduce</Data></Cell>
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
    if not text: return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

for item in data:
    status_style = "sPass" if item["testcase status"] == "PASS" else "sFail"
    
    row = f"""   <Row>
    <Cell ss:StyleID="sCenter"><Data ss:Type="String">{escape_xml(item['testcase id'])}</Data></Cell>
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
# We save with .xls extension but it's actually XML Spreadsheet format so Excel reads styles
xml_path = "/home/nirmalsaha/Hirepro_Test_files/automation_scripts/agents/antigravity/assessments/agentic_scripts/output_reports/standalone_pages/qa_report_colorcoded_2026-03-09.xls"

with open(xml_path, "w", encoding="utf-8") as f:
    f.write(xml_content)

print(f"Excel (Color-Coded) report generated at: {xml_path}")
