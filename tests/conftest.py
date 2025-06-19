# filepath:tests/conftest.py
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    print("\nTest Results by File:")
    # Collect all test reports
    reports = terminalreporter.stats
    passed = reports.get('passed', [])
    failed = reports.get('failed', [])

    # Helper to extract file name from nodeid
    def get_file(report):
        return report.nodeid.split("::")[0]

    # Count passed/failed per file
    from collections import Counter
    passed_files = Counter(get_file(rep) for rep in passed)
    failed_files = Counter(get_file(rep) for rep in failed)

    # Print summary per file
    all_files = set(passed_files) | set(failed_files)
    for file in sorted(all_files):
        print(f"  {file}: {passed_files.get(file, 0)} passed, {failed_files.get(file, 0)} failed")

    # Print total summary
    print(f"\nFinal Summary: {len(passed)} Tests Passed, {len(failed)} Tests Failed\n")




