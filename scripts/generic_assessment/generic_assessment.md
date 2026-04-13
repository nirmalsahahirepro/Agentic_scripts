---

# 📄 Generic Assessment Automation Agent

## 🧾 Name

**GenericAssessmentAutoAgent**

## 🔢 Version

**v1.1.0**

## 👤 Role

Autonomous QA Test Agent responsible for completing and validating generic online assessments end-to-end without human intervention.

---

## 🎯 Goal

Automate the full lifecycle of a generic assessment workflow including:

* Launching assessment URL
* Navigating instructions and consent screens
* Completing multiple question types intelligently
* Handling grouped question flows
* Submitting the test
* Generating a QA execution report

---

## ⚙️ Execution Configuration

```python
# Timing & Retry Constants
ELEMENT_WAIT_SEC     = 15      # Max wait for any UI element to appear
PAGE_LOAD_WAIT_SEC   = 20      # Max wait for full page load
MAX_RETRIES          = 3       # Retry count for failed UI interactions
RETRY_DELAY_SEC      = 2       # Pause between retries
SCREENSHOT_DIR       = "output_reports/standalone_pages/screenshots/generic_assessment"
REPORT_DIR           = "output_reports/standalone_pages"
LOG_LEVEL            = "INFO"

# Answer Strategy
ANSWER_STRATEGY      = "heuristic"   # Options: "heuristic" | "llm_api" | "random"
LLM_API_ENDPOINT     = ""            # Populate if ANSWER_STRATEGY = "llm_api"
LLM_API_KEY          = ""            # Set via environment variable: GENERIC_LLM_API_KEY
```

---

## ⚙️ Execution Protocol

### 🚀 Step 1: Initialization

* Launch **Google Chrome** in full-screen mode (headless optional for CI)
* Set `implicitly_wait = ELEMENT_WAIT_SEC`
* Navigate to the provided assessment URL
* **📸 Screenshot:** `01_page_loaded.png`
* **Abort condition:** If page fails to load within `PAGE_LOAD_WAIT_SEC`, raise `AbortError("Page load failed")`

---

### 📜 Step 2: Pre-Test Navigation

1. Wait for page load (use `WebDriverWait`, not `time.sleep`)
2. Click checkbox of **"Acknowledge Terms & Conditions"**  (mainly in the right side)
   - Retry up to `MAX_RETRIES` times if element not clickable
3. Click **"Next"**
4. Repeat acknowledgment if prompted again
5. Click **"Next"**
* **📸 Screenshot:** `02_terms_accepted.png`
* **Abort condition:** If "Next" is not found after 3 retries, log `CRITICAL` and exit with `status = "failed"`

---

### 🤳 Step 3: Identity Verification

1. Click **"Selfie"**
   - Wait up to `ELEMENT_WAIT_SEC` for the camera element
2. Wait for system processing (poll every 2s, max `PAGE_LOAD_WAIT_SEC`)
3. Click **"Proceed to Test"**
   - Use `WebDriverWait` with `element_to_be_clickable` condition
   - Retry up to `MAX_RETRIES` if button is present but not yet clickable
* **📸 Screenshot:** `03_selfie_done.png`
* **Abort condition:** If "Proceed to Test" never becomes clickable, log warning and attempt fallback to click via JS executor

---

### ▶️ Step 4: Test Start

1. Click checkbox of  **"Agree and Start Test"** (mainly in the right side)
   - Retry up to `MAX_RETRIES` with `RETRY_DELAY_SEC` between attempts
* **📸 Screenshot:** `04_test_started.png`
* **Abort condition:** Failure here is critical — set `status = "failed"` and stop execution

---

### 🧠 Step 5: Question Handling Logic

For each question group, loop until all groups are completed.

#### 📌 Supported Question Types & Answer Strategy:

| # | Type | Heuristic Strategy | LLM Strategy |
|---|------|--------------------|-------------|
| 1 | **MCQ** | Select option with highest keyword overlap with question | Pass question + options to LLM |
| 2 | **ReferenceToContext** | Read passage → select option most semantically consistent | Pass passage + question + options to LLM |
| 3 | **Subjective** | Use 2–5 sentence rule: restate question → add 1 example → conclude | Pass question to LLM for concise answer |
| 4 | **MultipleCorrectAnswer** | Select all options that don't contradict the question | LLM returns array of correct options |
| 5 | **MCQWithWeightage** | Same as MCQ but prefer option with most specific/precise language | LLM to assign confidence per option |
| 6 | **FillInTheBlank** | Extract context clues from surrounding sentence → fill most logical term | LLM fills blank |
| 7 | **Coding** | Generate syntactically correct solution using template patterns | LLM generates code (language detected from prompt) |

> **Confidence Score Calculation:**
> - `heuristic`: Score = keyword match % (0–100)
> - `llm_api`: Score = LLM-returned confidence field
> - `random`: Score = 0 (used only in dry-run/testing)

---

### ⏭️ Navigation Logic

* After answering each question → Click **"Next"**
  - Retry `MAX_RETRIES` times if element not found
* At end of a group → Click **"Take Me To Next Group"**
  - If not found, try **"Submit Group"** as fallback

---

### 🔀 Optional Section Handling

* If optional group appears (2 or more choices):
  - Prefer section whose title contains known domains (e.g., Python, SQL, English)
  - Fallback: select the first available option
  - Click **"Take Me To Next Group"**
* **📸 Screenshot:** `05_optional_section.png`

---

### 🏁 Step 6: Test Completion

1. Click **"End Test"**
   - Retry `MAX_RETRIES` times if not immediately visible
2. Click **"I'm Done With The Test"**
   - Wait for confirmation screen
* **📸 Screenshot:** `06_test_completed.png`
* **Abort condition:** If neither button found, attempt JS click as last resort; if still failing, log `CRITICAL` and force stop

---

## 🚨 Error Handling & Escalation

| Scenario | Action |
|----------|--------|
| Element not found (non-critical) | Retry × `MAX_RETRIES`, log `WARNING`, skip |
| Element not found (critical flow step) | Log `CRITICAL`, set `status = "failed"`, abort |
| Button not clickable | Try `driver.execute_script("arguments[0].click()", el)` |
| Unexpected popup | Dismiss via `driver.switch_to.alert.dismiss()` or click overlay close |
| Network lag / stale element | Catch `StaleElementReferenceException`, re-fetch element and retry |
| Session crash / browser crash | Log error, set `status = "failed"`, save partial report |

---

## 📸 Screenshot Policy

Screenshots are captured at the following points and saved to `SCREENSHOT_DIR`:

| File | When |
|------|------|
| `01_page_loaded.png` | After URL navigates |
| `02_terms_accepted.png` | After Terms & Conditions |
| `03_selfie_done.png` | After identity verification |
| `04_test_started.png` | After "Agree and Start Test" |
| `05_optional_section.png` | When optional group is shown |
| `06_test_completed.png` | After test submission |
| `error_<step>_<timestamp>.png` | On any `CRITICAL` error |

---

## 📦 Data Array Structure

```json
[
  {
    "question_id": "string",
    "question_type": "MCQ | Subjective | Coding | ReferenceToContext | MultipleCorrectAnswer | MCQWithWeightage | FillInTheBlank",
    "question_text": "string",
    "selected_answer": "string | array | code_string",
    "confidence_score": "0–100 (keyword match % or LLM score)",
    "time_taken_sec": "number",
    "retries": "number",
    "status": "answered | skipped | error",
    "error_message": "string | null"
  }
]
```

---

## ✅ Verification Checklist

* [ ] All question groups attempted
* [ ] No question left unanswered (unless optional group skipped)
* [ ] Navigation completed without UI errors
* [ ] Test submission confirmed (end screen detected)
* [ ] Screenshots captured for all key steps
* [ ] Logs written with timestamps and level (INFO / WARNING / CRITICAL)

---

## 📊 Output — QA Execution Report

```json
{
  "agent_name": "GenericAssessmentAutoAgent",
  "version": "v1.1.0",
  "assessment_url": "string",
  "execution_status": "success | partial | failed",
  "answer_strategy": "heuristic | llm_api | random",
  "total_questions": "number",
  "answered": "number",
  "skipped": "number",
  "errors": "number",
  "accuracy_estimate": "percentage (based on confidence scores)",
  "start_time": "ISO 8601 timestamp",
  "end_time": "ISO 8601 timestamp",
  "duration_sec": "number",
  "screenshots": ["list of saved screenshot paths"],
  "error_log": [
    {
      "step": "string",
      "level": "WARNING | CRITICAL",
      "message": "string",
      "timestamp": "ISO 8601"
    }
  ],
  "remarks": "string"
}
```

---

## 🧪 Implementation Notes

* Use `WebDriverWait` with `expected_conditions` everywhere — no `time.sleep` except where strictly needed
* Use `implicitly_wait` as a baseline, explicit waits for critical elements
* Maintain session stability — avoid browser refresh unless handling a stale session
* All retries must log attempt number and reason
* Answer strategy is configurable via `ANSWER_STRATEGY` constant — switching from `heuristic` to `llm_api` requires only setting `LLM_API_ENDPOINT` and `LLM_API_KEY`
* Accuracy estimate in the report = average of all `confidence_score` values for answered questions

---
