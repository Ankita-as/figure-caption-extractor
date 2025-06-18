### API Key Access
- All REST API endpoints are protected via a header: `x-api-key`.
- If key is missing or invalid, return `401 Unauthorized`.

### Tests
- ✅ Access with valid API key: should return 200.
- ❌ Access without API key: should return 401.
- ❌ Access with wrong API key: should return 401.
## Performance Testing Plan

### Metrics:
- Ingestion time per 10 papers
- API response time for large results
- Max paper ID list size (stress test)

### Tools:
- Custom Python timer for CLI
- Locust or curl-based tests for API

### Benchmarks:
- Ingest 100 PMC IDs in < 60 seconds
- API response time < 300ms for single queries
