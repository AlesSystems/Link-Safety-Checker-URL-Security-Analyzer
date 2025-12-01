Title: Define risk scoring rules

Description:
Create rule-based checks using:
- URL length
- Use of IP address instead of domain
- Suspicious keywords
- Unusual TLDs
- Presence of uncommon ports

Acceptance Criteria:
- Rules documented in docs/risk_rules.md
- Simple scoring algorithm implemented
- Unit tests added

Labels: backend, enhancement

---

Title: Combine API result with rule-based score

Description:
Build a function that merges:
- API risk result
- Internal rule-based score
into a final decision.

Acceptance Criteria:
- Response categories (safe / suspicious / dangerous)
- Tests covering multiple scenarios

Labels: backend

---

Title: Return final security verdict object

Description:
Create a structured return object with:
- URL
- Verdict
- API data
- Rule-based score
- Reason(s)

Acceptance Criteria:
- JSON-serializable dict
- Ready for CLI output
- Add tests

Labels: backend, enhancement
