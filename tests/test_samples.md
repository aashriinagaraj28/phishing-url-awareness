# Test Results

Python version used: 3.13.9  
Operating system: Windows  
Testing date: 2026-10-31

## Required sample tests

| Test | Input | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|
| 1 | `https://www.example.com/login` | No warnings; not a safety guarantee. | No listed warnings; not proof of safety. | PASS |
| 2 | `http://192.0.2.10/account` | IP-address hostname + HTTP. | IP-address hostname; HTTP. | PASS |
| 3 | `http://example.com@sample.invalid/login` | @ symbol + HTTP. | @ symbol; HTTP. | PASS |
| 4 | `https://a.b.c.d.e.example.invalid/path` | Many hostname segments. | Many hostname segments/subdomains. | PASS |
| 5 | `https://xn--example.invalid/` | Punycode-style hostname. | Punycode-style hostname. | PASS |

## Additional input handling checks

These two inputs are the workbook's optional checks for empty and malformed input. The loop check used two of the five exact sample URLs above, then the `q` quit command.

| Check | Input | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|
| Empty input | (press Enter without typing a URL) | `No URL entered.` and continue running. | `No URL entered.`; the program stayed open for the next input. | PASS |
| Malformed input | `http://[bad` | A clear message without a crash. | `This text is not a valid URL format.`; the program stayed open for the next input. | PASS |
| Repeat and quit | Tests 1 and 2 above, then `q` | Inspect both URLs and exit. | Both results appeared in one run; `Goodbye! Stay alert online.` appeared after `q`. | PASS |

## Notes

I learned that `urlparse()` separates a URL into parts so the checker can examine its hostname.  
One input can show more than one warning, while no warning signs still cannot prove that a URL is safe.  
The five required sample URLs do not exercise the over-100-character check; that rule is implemented with the Section 06 threshold, but I did not add an unprovided sample URL.
