# DevOps Assessment Automation Flow

This document outlines the steps and locators discovered for the DevOps assessment, which features an embedded VS Code environment on AWS.

## 1. Test Navigation & Login
- **URL**: `configs/urls.txt` -> `devops`
- **Login**: Reuses `GenericAssessmentAutoAgent` login logic (Terms -> Selfie -> Start).

## 2. VM Loading Phase
- **Wait Duration**: 3–8 minutes.
- **Indicator**: The presence of the VS Code editor container.
- **Locator**: `div.monaco-editor` (Wait until visible).

## 3. VS Code Interaction
- **File Explorer**:
  - **Task**: Open `playbook.yml`.
  - **Locator**: `div.monaco-list-row[aria-label="playbook.yml"]`
- **Editor**:
  - **Task**: Clear content and paste YAML solution.
  - **Locator**: `div.monaco-editor`
- **Terminal**:
  - **Process**: Application Menu -> Terminal -> New Terminal.
  - **App Menu**: `div.menubar-menu-button[aria-label="Application Menu"]`
  - **Terminal Item**: `//span[text()='Terminal']`
  - **New Terminal Item**: `//span[text()='New Terminal']`
  - **Command**: `solveproblem` (Type + Enter).

## 4. Assessment Controls (External)
These buttons are located outside the IDE container.
- **Run Tests**: `//button[contains(text(), 'Run Tests')]`
- **Save My Work**: `//button[contains(text(), 'Save My Work')]`
- **End Test**: `//button[contains(text(), 'End Test')]`

## 5. Success Verification
- **Upload Sync**: `//*[contains(text(), 'Uploading files to the server...')]`
- **Save Confirmed**: `//*[contains(text(), 'Saved successfully.')]` (Must wait for this before clicking "End Test").
