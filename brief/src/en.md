# Bitaid: emergency help, paid peer to peer on Bitcoin

November 2026 · [@fiatstandard](https://x.com/fiatstandard)

Bitaid lets a person in danger summon capable people nearby and pay them, with no dispatcher, no token and no company in the middle. Every payout the case can end in is signed before anyone has a reason to dispute, so whoever decides the outcome can pick one but never take the money. It now runs end to end on Bitcoin's public test network, over Tor, between a PC, a phone and a tablet.

## The problem

Violence is decided in the minutes between an attack and the response to it. Self-defence is always there, but one person against several is outmatched; what turns the outcome is a second and third capable person arriving within minutes.

Today insurance pays after the harm is done. Rescue in the moment is almost nowhere for sale, and nothing lets you pay whoever capable can get there first. Private security bills hours, not results, so it guards places for those who can afford idle time. The police are a monopoly: no prices, no rival, no customer who can leave, so they cannot learn what protection is worth or to whom. Bitaid pays for the problem solved, not for the hours spent waiting for one.

## The insurance lever

A Bitaid offer is escrowed in advance and costs nothing until it is used: the money waits as unspent bitcoin, paying no wages for idle hours. And because emergencies rarely strike the same people at once, an insurer can stand one stake behind many offers.

A thousand people paying two dollars a month can each summon help with an offer of $8,000: leverage of some three hundred to one. That leverage rests on emergencies being rare and spread out, and on the insurer holding reserves of its own for the bad years; the premium prices both. Underwriting it lets bitcoin capital earn bitcoin from real risk, without lending it out. Bounties that size draw the most capable responders, and fund the teams, drones and medics that compete to arrive first.

Then the insurer's own interest takes over. With enough capital committed, it pays to keep its own guards and patrols near its clients: they deter the emergencies its offers would otherwise pay for, and when one happens they are first on the scene, earning back the bounty it escrowed. Fewer claims mean lower premiums, which bring more clients, whose premiums fund more patrols. That flywheel turns insurers into security providers that compete on price and on how fast they arrive, paid for results rather than idle hours.

Bitaid does not declare a right to security or persuade anyone to pay for it; it raises the price paid for saving life and property, and lets the market answer.

## How a case runs

1. **Before any emergency**, the caller (or their insurer) escrows an offer in bitcoin. It sits in a script nobody can spend alone; if no emergency ever comes, it returns to its owner.
2. **The alert** goes to bonded responders in the surrounding area. Each one who accepts posts a bond of their own.
3. **Within about a minute**, the parties' devices sign every payout the case can end in: on the public test network, 39 possible payouts for three responders. Nothing new can be added later.
4. **Everyone records.** Whoever claims pay must prove what they did on their own footage, so every scene is filmed from several angles. Each recording is hashed and anchored to Bitcoin.
5. **The people who were there vote**, blind and item by item: who attended, who helped, what happened. If they agree, that settles it.
6. **If they disagree**, pseudonymous arbitrators drawn at random answer narrow factual questions about the footage. Each staked bond is at risk if the answer is wrong. A party can buy a larger panel, and a sample of verdicts is reviewed again by three fresh panels.
7. **An attestation picks one of the pre-signed payouts**, and it is broadcast. The money moves straight from the escrow to the people who earned it.

## Why cheating does not pay

- **Those who decide never hold the money.** They choose among payouts signed in advance, each paying only the parties. No outcome pays them. A wrong ruling can still pick the wrong payout, which is what the bonds, reviews and restitution are for.
- **Every role stakes a bond larger than what cheating could win.** An arbitrator who votes against the final ruling forfeits part of it.
- **Faking the scene is the hard part.** Footage hashed the moment it is taken cannot be edited afterwards, and a staged scene must hold up across several independent cameras and the people who were there.
- **Weight is earned, not bought.** A responder's vote counts by the paid work done in that area; an arbitrator's seat by the cases already judged. Both season over calendar time no one can buy.
- **Any case can be reopened.** Three fresh panels that overturn a verdict seize the whole case stake of those who voted for it, and repay the wronged.
- **Nothing to capture.** No token, no company, no administrator, no governance vote. Ordering and finality come from Bitcoin.

## What already runs

A working prototype in Rust runs every role: callers, responders, archivists, the threshold-signing oracle pool and arbitrators. Each check below is a script that passes or fails on a real chain, with the logs published.

| Date | Where | What ran | Result |
| --- | --- | --- | --- |
| Nov 8, 2026 | Liquid testnet | The escrows: funding, a pool-co-signed incident, pre-signed payouts, a wrong attestation refused by the network, a bond forfeiture, the timelocked fallback | [15 passed, 0 failed](https://github.com/FaithStandard/Bitaid-prototype/blob/main/results/m3_liquid_testnet_2026-11-08.txt) |
| Nov 7, 2026 | Bitcoin public signet, over Tor, PC + phone + tablet | The staged review: three fresh panels overturn a verdict; the wrong arbitrators lose their stakes, which repay the wronged responder and the dissenter who was right | [74 passed, 0 failed](https://github.com/FaithStandard/Bitaid-prototype/blob/main/results/m3_public_signet_review_2026-11-07.txt) |
| Nov 7, 2026 | Same run, plus a hostile stranger | Floods, garbage, oversized and replayed messages, fake block heights, connection storms aimed at the network while the case ran. The case finished, and every node refused the fake height | Undisturbed |
| Nov 6, 2026 | Bitcoin public signet, over Tor | A full disputed case: a split vote, two arbitration tiers, an appeal, missed deadlines replaced, penalties, all payouts on chain | [71 passed, 0 failed](https://github.com/FaithStandard/Bitaid-prototype/blob/main/results/m3_public_signet_2026-11-06.txt) |
| Oct 29, 2026 | Private signet, over Tor | The same case on a private test network | [84 passed, 0 failed](https://github.com/FaithStandard/Bitaid-prototype/blob/main/results/m3_signet_tor_2026-10-29.txt) |
| Oct 2026 | Economic simulations | Eight experiments, thousands of cases each: honest work profits; lazy, bought and staged verdicts lose under the adopted rules | [Reproducible with one command](https://github.com/FaithStandard/Bitaid-prototype/tree/main/sim) |

## What is not done yet

- **Every node so far is ours.** The cheaters in these tests cheat because a script tells them to. Independent operators, choosing their own strategies, are the next milestone.
- **The deadlines now count blocks**, as the specification requires, but so far only on a local test chain. The next public-signet run checks them on the real one.
- **No outside review yet** of the cryptography (FROST, MuSig2, the scripts) or of the incentives.
- **Test coins only.** The prototype must not hold real funds.

## How to help

- **Run a node** in the coming test pilot, and try to break it. Attacks that work are the most useful thing anyone can send.
- **Review the cryptography**: the threshold oracle (FROST with ROAST), the pre-signed payout sets (MuSig2) and the Taproot scripts.
- **Attack the incentives**: the simulations are open; change an assumption and see what breaks.
- **Pilot it**: insurers, security firms and communities where help arrives late or not at all.

Issues and pull requests are welcome on either repository.

## Read more

- [Whitepaper](https://bitaid-whitepaper.pages.dev/): the argument, in full
- [Specification](https://bitaid-whitepaper.pages.dev/bitaid_v6_specification.html): scripts, messages, parameters and the record of every test
- [Prototype](https://github.com/FaithStandard/Bitaid-prototype): the Rust code, the test logs and the simulations
