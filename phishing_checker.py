"""Check URL text for a small set of educational phishing warning signs."""

import re
from urllib.parse import urlparse


# These messages mean the input could not be checked or no warning was found.
INFO_MESSAGES = (
    "No URL entered.",
    "Could not identify a hostname.",
    "This text is not a valid URL format.",
    "No listed warning signs found.",
)


def inspect_url(raw_url: str) -> list[str]:
    """Inspect URL text and return the warning or information messages."""
    url = raw_url.strip()
    findings = []

    if not url:
        return ["No URL entered."]

    # Add a scheme only to help urlparse split an input that omits one.
    candidate = url if "://" in url else "http://" + url

    # urlparse raises ValueError for malformed bracketed IPv6-style input.
    try:
        parsed = urlparse(candidate)
        host = (parsed.hostname or "").lower()
    except ValueError:
        return ["This text is not a valid URL format."]

    if not host:
        return ["Could not identify a hostname."]

    # Check 1: an @ can make text before it look like the destination.
    if "@" in candidate:
        findings.append("Contains an @ symbol; inspect carefully.")

    # Check 2: the workbook flags URLs longer than 100 characters.
    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")

    # Check 3: match the four-part numeric hostname pattern from the workbook.
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append("Uses an IP address instead of a familiar domain.")

    # Check 4: five or more dot-separated hostname parts are a clue to review.
    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append("Contains many hostname segments/subdomains.")

    # Check 5: xn-- is the visible punycode marker described in the workbook.
    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")

    # Check 6: plain HTTP is not encrypted like HTTPS.
    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP. HTTPS alone does not prove trust.")

    if not findings:
        findings.append(
            "No listed warning signs found. This does NOT prove safety."
        )

    return findings


def has_warnings(findings: list[str]) -> bool:
    """Return True if the results contain a warning rather than information."""
    return any(
        not finding.startswith(INFO_MESSAGES)
        for finding in findings
    )


def main() -> None:
    """Ask for URLs repeatedly until the user enters a quit command."""
    print("EWB Phishing URL Awareness Checker")
    print("Text checks only - this program does not open URLs.")

    while True:
        try:
            raw_url = input("\nEnter a sample URL (or type q to quit): ")
        except EOFError:
            print("\nGoodbye! Stay alert online.")
            break

        if raw_url.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye! Stay alert online.")
            break

        findings = inspect_url(raw_url)

        print("\nResult:")
        for item in findings:
            print("- " + item)

        if has_warnings(findings):
            print(
                f"\nREVIEW CAREFULLY: {len(findings)} warning sign(s) found."
            )

        print("\nNever enter passwords from unexpected links.")


if __name__ == "__main__":
    main()
