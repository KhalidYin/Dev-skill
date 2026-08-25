# Cross-section Checks

Run these checks after drafting. They are internal authoring checks, not an independent validation or compliance conclusion.

## Required checks

| Check ID | Relationship |
|----------|--------------|
| XCHK-001 | Protocol objective -> SAP objective -> endpoint hierarchy |
| XCHK-002 | Endpoint definition -> estimand variable -> primary response variable |
| XCHK-003 | Estimand population -> analysis population -> treatment assignment rule |
| XCHK-004 | ICE strategy -> post-ICE data use -> missing-data handling |
| XCHK-005 | Primary hypothesis -> effect measure -> model contrast -> confidence interval and alpha |
| XCHK-006 | Visit schedule -> analysis visits -> primary timepoint -> visit-window convention |
| XCHK-007 | Primary assumptions -> sensitivity analysis that varies those named assumptions |
| XCHK-008 | Multiplicity family -> endpoint hierarchy -> testing order and alpha allocation |
| XCHK-009 | Sample-size assumptions -> primary effect measure and variance/event assumptions |
| XCHK-010 | Source versions on title/purpose sections -> source inventory used throughout |

## Finding schema

```yaml
finding_id: XCHK-004-01
check_id: XCHK-004
status: pass | unresolved | conflict | not-applicable
sections: [SEC-07, SEC-12]
summary: ""
related_query_id: Q-EST-001
```

## Handling

- Add a query when a mismatch needs accountable resolution.
- Reuse an existing query if the same missing decision caused the mismatch.
- Do not rewrite a confirmed decision merely to make sections appear consistent.
- Do not treat absence of a finding as proof of regulatory compliance.
