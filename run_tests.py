"""Simple test automation tool.

Reads test cases from a JSON file, sends an HTTP GET request for each one,
checks the result against the expected values, then prints a summary and
writes report.csv and report.html.

Usage:  python run_tests.py [test_cases.json]
Exit code is 0 if all tests pass and 1 if any fail (so CI tools can use it).
"""
import csv
import html
import json
import sys
import time
import urllib.error
import urllib.request


def run_case(case):
    """Run one test case and return a result dictionary."""
    start = time.time()
    status, body, error = None, "", ""
    try:
        with urllib.request.urlopen(case["url"], timeout=10) as response:
            status = response.status
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:      # 4xx / 5xx still return a response
        status = e.code
        body = e.read().decode("utf-8", errors="replace")
    except Exception as e:                   # connection refused, timeout, etc.
        error = str(e)
    elapsed = round(time.time() - start, 3)

    problems = []
    if error:
        problems.append(f"request failed: {error}")
    else:
        if status != case["expected_status"]:
            problems.append(f"status {status}, expected {case['expected_status']}")
        if case.get("expected_text") and case["expected_text"] not in body:
            problems.append(f"text '{case['expected_text']}' not found in response")
        if elapsed > case.get("max_seconds", 5):
            problems.append(f"took {elapsed}s, limit {case['max_seconds']}s")

    return {
        "name": case["name"],
        "url": case["url"],
        "status": status,
        "seconds": elapsed,
        "result": "PASS" if not problems else "FAIL",
        "details": "; ".join(problems),
    }


def write_csv(results, path="report.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


def write_html(results, path="report.html"):
    rows = ""
    for r in results:
        colour = "#d4f5d4" if r["result"] == "PASS" else "#f9d4d4"
        rows += (
            f"<tr style='background:{colour}'><td>{html.escape(r['name'])}</td>"
            f"<td>{r['status']}</td><td>{r['seconds']}</td>"
            f"<td>{r['result']}</td><td>{html.escape(r['details'])}</td></tr>"
        )
    page = (
        "<html><body><h2>Test Report</h2>"
        "<table border='1' cellpadding='6' style='border-collapse:collapse'>"
        "<tr><th>Test</th><th>Status</th><th>Seconds</th><th>Result</th><th>Details</th></tr>"
        f"{rows}</table></body></html>"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "test_cases.json"
    with open(path, encoding="utf-8") as f:
        cases = json.load(f)

    results = [run_case(c) for c in cases]
    for r in results:
        print(f"[{r['result']}] {r['name']} ({r['seconds']}s) {r['details']}")

    passed = sum(1 for r in results if r["result"] == "PASS")
    print(f"\n{passed}/{len(results)} tests passed")
    write_csv(results)
    write_html(results)
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
