# Python Test Automation Tool

A small tool that automatically tests web/API endpoints and produces a pass/fail report.
Written in plain Python (no extra libraries needed).

## What it does
1. Reads test cases from `test_cases.json` (URL, expected status, expected text, max response time).
2. Sends a request for each test case and measures the response time.
3. Marks each test PASS or FAIL and explains why it failed.
4. Writes `report.csv` and `report.html`.
5. Exits with code 1 if any test fails, so CI tools (GitHub Actions) can detect failures.

## How to run
Open two terminals in this folder.

Terminal 1 (the sample system under test):
    python mock_server.py

Terminal 2:
    python run_tests.py

Open `report.html` in a browser to see the report.

## Try it yourself
- Change `"expected_text": "Sword"` to `"Axe"` in `test_cases.json` and run again: the test should FAIL and the report should say why.
- Stop the mock server and run the tests: every test fails with a connection error.
- Add a new test case for a new endpoint.

## CI/CD
`.github/workflows/tests.yml` runs the tests automatically on every push using GitHub Actions
(it starts the mock server, runs the tests and uploads the report).

## Files
- `run_tests.py` - the test runner
- `mock_server.py` - sample web server to test against
- `test_cases.json` - the test cases
- `.github/workflows/tests.yml` - GitHub Actions workflow
