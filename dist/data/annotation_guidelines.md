# Multilingual Customer Support Intent Annotation — guidelines

## Goal and provenance

Assign **one primary customer intent** and one **urgency** label to each short, fictional support message. The 48 messages and draft reference labels were prepared with AI assistance for an independent portfolio demonstration. No real customer records or employer data are included.

## Primary intent classes

| Label | Include | Exclude |
|---|---|---|
| `DELIVERY_ISSUE` | Tracking, delay, missing parcel, wrong delivery address | Product return or money-back request as the main action |
| `BILLING_ISSUE` | Charge, payment, invoice, failed transaction | Explicit request to get money back |
| `REFUND_REQUEST` | Explicit request for a refund, reversal, or money back | A charge merely described as incorrect, without asking for reimbursement |
| `ACCOUNT_ACCESS` | Login, reset, verification, suspicious sign-in | Bugs after a successful sign-in that do not concern access |
| `TECHNICAL_SUPPORT` | App, website, button, download, or error failure | Payment declined by bank without an interface failure |
| `OTHER` | Questions or suggestions outside the five classes | A message that clearly fits one of them |

## Decision order

1. Identify the action the customer wants, not just the topic mentioned.
2. An explicit money-back request takes `REFUND_REQUEST` over `BILLING_ISSUE`, even if a charge caused it.
3. If a message discusses a package's location or shipping status, use `DELIVERY_ISSUE`, unless the main request is a refund.
4. Use `ACCOUNT_ACCESS` for an expired reset link or failed sign-in; use `TECHNICAL_SUPPORT` for bugs in an otherwise accessible account.
5. Use `OTHER` only when no listed intent fits. Do not infer a refund request from frustration alone.

## Urgency

- `High`: explicit imminent deadline or possible account compromise/payment loss requiring prompt attention.
- `Medium`: active unresolved service, payment, or access issue without an imminent deadline.
- `Low`: informational question, minor inconvenience, or future-facing suggestion.

Urgency is a text-only triage exercise. It is not a safety or service-level decision. An annotator should record uncertainty when a message is too sparse to support a confident label.

## Ambiguous examples

| Message | Label | Reason |
|---|---|---|
| “Fui cobrado duas vezes pelo mesmo pedido.” | `BILLING_ISSUE` | Reports a charge, without explicitly asking for a refund. |
| “Por favor, estornem a cobrança duplicada no cartão.” | `REFUND_REQUEST` | Explicitly requests a reversal. |
| “The reset link keeps saying it has expired.” | `ACCOUNT_ACCESS` | The failure blocks access to the account. |
| “The item arrived damaged; I'd like my money back.” | `REFUND_REQUEST` | The requested action is reimbursement. |
| “Vocês vendem vale-presente para compras?” | `OTHER` | A product availability question outside the five specific intents. |

## Quality control plan

Before presenting this as personally verified annotation work, the portfolio owner should independently review all 48 items, especially the refund/billing boundary and urgency choices. For a consistency check, conceal the current labels and reannotate 10–12 selected items after a delay; document disagreements and revisions. No independent second-pass agreement is claimed in this release.
