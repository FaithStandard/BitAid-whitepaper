# Bitaid — Whitepaper

**Read it online: [bitaid-whitepaper.pages.dev](https://bitaid-whitepaper.pages.dev/)**

Bitaid is a peer-to-peer emergency response protocol built on Bitcoin. A person in danger summons nearby, capable strangers and pays them without asking anyone's permission; the strangers are paid without trusting the person who called them.

The offer is escrowed before any emergency. The moment a responder accepts, the parties' devices sign every payout the case can end in, before anyone has a reason to dispute. Payment then needs only an attestation choosing one outcome from that fixed set: whoever attests can choose among the outcomes but cannot add one, so the intermediaries who decide never hold the funds and cannot pay themselves any of it. The people who were there settle the outcome by blind itemised ballots; where they disagree, a closed pool of pseudonymous arbitrators answers narrow factual questions and loses money when it departs from the canon of reference cases.

This repository holds the documents and serves them as the site above.

## The documents

| | Online | What it is |
|---|---|---|
| **Whitepaper** | [Read](https://bitaid-whitepaper.pages.dev/) | The argument: why the protocol works and why it matters. Start here. |
| **Specification** | [Read](https://bitaid-whitepaper.pages.dev/bitaid_v6_specification.html) | Precisely how it works, for implementers and auditors: scripts, messages, parameters, and the record of what has been tested. |
| **Foundations** | [Read](https://bitaid-whitepaper.pages.dev/bitaid_v6_foundations.html) | The case at full length — the market, judgment without authority, bootstrapping, resilience, evolution without governance — with the theoretical foundations and the objections answered. |
| **A Palatable Guide** | [Read](https://bitaid-whitepaper.pages.dev/BitaidGuide/) | The protocol problem by problem, for a general reader. |

All three main documents are version 6.0.

## Files

| File | Served at |
|---|---|
| `index.html` | the Whitepaper (the site's home page) |
| `bitaid_v6_specification.html` | the Specification |
| `bitaid_v6_foundations.html` | the Foundations |
| `BitaidGuide/index.html` | the Guide |
| `bitaid_v5_24.md` | the earlier single-document version 5.24, as plain text prepared for review by AI models; kept for reference |

Each page is self-contained: one HTML file with its figures inline. The site is served as-is, with no build step.

## The prototype

A working prototype of the protocol in Rust lives at **[FaithStandard/Bitaid-prototype](https://github.com/FaithStandard/Bitaid-prototype)**. It runs the whole network — callers, responders, archivists, the oracle pool and arbitrators — over Tor between a PC, a phone and a tablet, on regtest and on signet. Its test results are recorded in Specification Appendix B.9.

The prototype is for testing and review. It must not hold real funds.
