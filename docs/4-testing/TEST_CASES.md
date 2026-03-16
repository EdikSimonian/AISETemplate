# Test Cases

> Document the test cases for each acceptance criterion.
> Use this to ensure your tests actually verify the requirements from Day 1.

---

## How to use this document

For each user story in `docs/1-requirements/ACCEPTANCE_CRITERIA.md`, write the corresponding test cases here.
Then implement them in code. Check off each row when the test is written and passing.

---

## US-01 — [User Story Title]

| # | Test Case | Type | Expected Result | Status |
|---|-----------|------|-----------------|--------|
| 1.1 | Happy path: [describe input] | Unit | [expected output] | [ ] |
| 1.2 | Edge case: empty input | Unit | Returns validation error | [ ] |
| 1.3 | Edge case: maximum length input | Unit | Accepts and processes | [ ] |
| 1.4 | Error case: missing required field | Integration | Returns 400 with clear error | [ ] |
| 1.5 | Error case: unauthorized user | Integration | Returns 401 | [ ] |

---

## US-02 — [User Story Title]

| # | Test Case | Type | Expected Result | Status |
|---|-----------|------|-----------------|--------|
| 2.1 | | | | [ ] |
| 2.2 | | | | [ ] |
| 2.3 | | | | [ ] |

---

<!-- Add a section for each user story -->

---

## Cross-Cutting Test Cases

These apply across features and should be tested for all protected endpoints.

### Authentication
| # | Test Case | Expected Result | Status |
|---|-----------|-----------------|--------|
| A.1 | Request with no token | 401 Unauthorized | [ ] |
| A.2 | Request with expired token | 401 Unauthorized | [ ] |
| A.3 | Request with malformed token | 401 Unauthorized | [ ] |
| A.4 | Request with valid token | Proceeds normally | [ ] |

### Authorization
| # | Test Case | Expected Result | Status |
|---|-----------|-----------------|--------|
| Z.1 | User accesses their own resource | 200 OK | [ ] |
| Z.2 | User accesses another user's resource | 403 Forbidden | [ ] |
| Z.3 | User deletes another user's resource | 403 Forbidden | [ ] |

### Input Validation
| # | Test Case | Expected Result | Status |
|---|-----------|-----------------|--------|
| V.1 | SQL injection attempt in string field | 400 or sanitized safely | [ ] |
| V.2 | XSS payload in text field | Sanitized or rejected | [ ] |
| V.3 | Extremely large payload | 400 or 413 | [ ] |
| V.4 | Wrong data type (e.g. string where number expected) | 400 with clear message | [ ] |
