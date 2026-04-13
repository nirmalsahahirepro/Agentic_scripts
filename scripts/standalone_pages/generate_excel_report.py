import csv
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

output_path = "/home/nirmalsaha/Hirepro_Test_files/automation_scripts/agents/antigravity/assessments/agentic_scripts/output_reports/standalone_pages/qa_report_2026-03-09.csv"

if data:
    keys = data[0].keys()
    with open(output_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print("Excel (CSV) report generated at:", output_path)

