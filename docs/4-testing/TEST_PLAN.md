# Test Plan

> Complete this on Day 4 before writing tests. Align the team on what to test and how.

---

## Testing Strategy

We use a three-layer test strategy:

```
         /\
        /  \   E2E Tests (few, slow, high confidence)
       /----\
      /      \ Integration Tests (some, moderate speed)
     /--------\
    /          \ Unit Tests (many, fast, isolated)
   /____________\
```

| Layer | What it tests | Speed | When to run |
|-------|--------------|-------|-------------|
| Unit | Individual functions and classes in isolation | Fast (~ms) | Every save / every commit |
| Integration | Functions that touch the database or external services | Medium (~100ms) | Every commit |
| E2E | Full user flows through a running server | Slow (~seconds) | Before merge / deploy |

---

## Scope

### In scope for testing
- [ ] All business logic in service layer
- [ ] All API endpoints (happy path + error cases)
- [ ] All data validation
- [ ] Authentication and authorization
- [ ] [Add your must-test features here]

### Out of scope
- Third-party library internals
- Framework boilerplate
- [other explicit exclusions]

---

## Test Framework

| Layer | Framework | Notes |
|-------|-----------|-------|
| Unit | [e.g., Jest / pytest / JUnit] | |
| Integration | [e.g., Jest + real DB / pytest + SQLAlchemy] | Use a test database, not dev |
| E2E | [e.g., Supertest / httpx / RestAssured] | Spin up server, run requests |

---

## Test Database Strategy

- Use a dedicated test database (e.g., `DATABASE_URL_TEST`)
- Reset database state before each test (use transactions or truncation)
- Run migrations before the test suite
- Seed with only the data each test needs — no shared global state

---

## Coverage Goals

| Area | Target | Rationale |
|------|--------|-----------|
| Service layer (business logic) | 90%+ | Core of the application |
| Repository layer (DB queries) | 80%+ | Data integrity matters |
| Route handlers | 70%+ | Integration tests cover the rest |
| Utilities / helpers | 95%+ | Pure functions are easy to test |

> Coverage % is a guide, not a goal in itself. 100% coverage with weak assertions is worse than 70% with strong ones.

---

## CI Integration

- Tests run automatically on every push and PR
- PRs cannot merge if tests fail
- Test reports are stored as CI artifacts
- Failing tests block deployment

---

## Responsibilities

| Task | Owner |
|------|-------|
| Write unit tests | Feature developer |
| Write integration tests | Feature developer |
| Review test quality | Reviewer in PR |
| Maintain test DB setup | [assign] |
