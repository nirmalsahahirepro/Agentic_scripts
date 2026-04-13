import csv
import os

data = [
    {
        "testcase id": "TC-URL1-001",
        "testcase name": "Email Pre-Validation Prompt",
        "testcase description": "Verify if the system handles the initial email prompt correctly.",
        "testcase steps": "1. Open URL.\n2. Enter dummy email.\n3. Click Submit.",
        "testcase expected result": "Accepts email and proceeds to checks.",
        "testcase actual result": "Accepted qa_test@example.com",
        "testcase status": "PASS",
        "testcase remarks": "Handled cleanly.",
        "testcase severity": "Critical",
        "testcase priority": "P1"
    },
    {
        "testcase id": "TC-URL1-002",
        "testcase name": "Browser Detection Verification",
        "testcase description": "Verify if the system correctly detects the Chrome browser and its version.",
        "testcase steps": "1. Open URL in Chrome.\n2. Wait for auto-checks.\n3. Check Browser row.",
        "testcase expected result": "Correctly identify Chrome and version.",
        "testcase actual result": "Detected: chrome - 145.0.0.0",
        "testcase status": "PASS",
        "testcase remarks": "Accurate detection.",
        "testcase severity": "High",
        "testcase priority": "P1"
    },
    {
        "testcase id": "TC-URL1-003",
        "testcase name": "OS Detection Verification",
        "testcase description": "Verify if the system correctly detects the Linux OS.",
        "testcase steps": "1. Open URL in Chrome.\n2. Wait for auto-checks.\n3. Check OS row.",
        "testcase expected result": "Identify Linux OS.",
        "testcase actual result": "Detected: linux / Linux x86_64",
        "testcase status": "PASS",
        "testcase remarks": "Accurate detection.",
        "testcase severity": "High",
        "testcase priority": "P1"
    },
    {
        "testcase id": "TC-URL1-004",
        "testcase name": "Hardware (Camera/Mic) Detection",
        "testcase description": "Verify webcam and mic permission request and detection.",
        "testcase steps": "1. Open URL.\n2. Click allow camera/mic.\n3. Observe UI.",
        "testcase expected result": "Request access, show green check and active sound bar upon allow.",
        "testcase actual result": "Perm granted, marked as Compatible, sound bar active.",
        "testcase status": "PASS",
        "testcase remarks": "Functions perfectly.",
        "testcase severity": "Critical",
        "testcase priority": "P1"
    },
    {
        "testcase id": "TC-URL1-005",
        "testcase name": "Network Speed Check",
        "testcase description": "Verify bandwidth calculation.",
        "testcase steps": "1. Open URL.\n2. Wait for network check.",
        "testcase expected result": "Validate download/upload speeds.",
        "testcase actual result": "Down: 33.05 Mbps, Up: 25 Mbps",
        "testcase status": "PASS",
        "testcase remarks": "Handled correctly.",
        "testcase severity": "High",
        "testcase priority": "P2"
    }
]

# ----------------- HTML REPORT GENERATION -----------------
html_template = """<!DOCTYPE html>
<html>
<head>
    <title>QA Test Report - URL 1 Compatibility</title>
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
        <h1>QA Test Report - URL 1 System Compatibility Check</h1>
        <div class="env-info">
            <strong>Target URL:</strong> https://amsin.hirepro.in/assessment/#/compatibility/at<br>
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
html_path = "/home/nirmalsaha/Hirepro_Test_files/automation_scripts/agents/antigravity/assessments/agentic_scripts/output_reports/standalone_pages/qa_report_url1_styled_2026-03-09.html"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML styled report generated at: {html_path}")

# ----------------- EXCEL XML (Color Coded) GENERATION -----------------
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
 <Worksheet ss:Name="QA Report URL 1">
  <Table>
   <Column ss:Width="80"/>  <!-- ID -->
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
xml_path = "/home/nirmalsaha/Hirepro_Test_files/automation_scripts/agents/antigravity/assessments/agentic_scripts/output_reports/standalone_pages/qa_report_url1_colorcoded_2026-03-09.xls"

with open(xml_path, "w", encoding="utf-8") as f:
    f.write(xml_content)

print(f"Excel (Color-Coded) report generated at: {xml_path}")
