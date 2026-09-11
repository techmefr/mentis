# Licensing

mentis is **dual-licensed**. Two tracks, and you pick the one that fits what you
are doing.

| | 🟢 AGPL-3.0-or-later | 💼 Commercial licence |
|---|---|---|
| **Cost** | Free | Negotiated |
| **Use it internally** | ✅ | ✅ |
| **Modify it** | ✅ | ✅ |
| **Redistribute it** | ✅ | ✅ |
| **Offer it as a hosted or networked service** | ✅ | ✅ |
| **Keep your modifications private** | ❌ — you must release the complete corresponding source, under AGPL, to everyone you serve | ✅ |
| **Ship it inside a proprietary product** | ❌ | ✅ |
| **Resell it, or a derivative, under your own terms** | ❌ | ✅ |

## The free track: AGPL-3.0-or-later

The full text is in [`LICENSE`](./LICENSE). What it means here, in plain terms:

- **Use it, for anything, including at work and including commercially.** There is
  no non-commercial clause. Running mentis inside a company that makes money is
  fine and always will be.
- **Modify it freely.** Adapt a block, retune a reader's calibration, add your own
  agents.
- **But if you hand your modified version to anyone — by distributing it *or* by
  operating it as a service they use over a network — you owe them the complete
  corresponding source of your version, under this same licence.** That is
  AGPL §13, and it is the clause that makes the difference: the ordinary GPL
  loophole of "we never distribute it, we only run it for customers" is closed.
- **You cannot relicense it**, sublicense it, or fold it into something
  proprietary.

> [!NOTE]
> **Why AGPL for a corpus of markdown.** mentis is not a compiled library; it is a
> body of prose that is read into an agent's context. The AGPL's copyleft attaches
> to the work itself, so a modified corpus stays a modified corpus and stays open.
> Whether an *output produced by* an agent reading these files is a derivative work
> is not something a licence choice settles, and this project makes no claim over
> your code. **The copyleft covers the blocks, not what you build with them.**

## The commercial track

The copyright holder retains full ownership and offers mentis under separate,
negotiated terms for anyone who wants what the AGPL does not allow:

- Embedding mentis, or a derivative, in a **closed-source product**.
- Operating a **hosted service** built on a modified mentis without publishing
  those modifications.
- **Reselling** mentis, a rebranded fork, or an integration, under your own terms.
- A **warranty, indemnity or support commitment**, none of which the AGPL provides
  (it disclaims all of them).

Open a GitHub issue titled `Commercial licence` to start that conversation.

> The copyright holder is also free to sell, advertise, package and monetise mentis
> in any way, on any track. That right comes from owning the copyright, not from
> the licence, and the [contribution terms](./CONTRIBUTING.md) exist to keep it
> intact as contributions come in.

## Why the contribution terms matter to this

Dual licensing only works if **one party holds the rights to the whole work**. If a
contribution landed under AGPL alone, the copyright holder could no longer offer
the resulting file commercially — a single unlicensed patch would silently kill the
commercial track for that file.

That is the entire reason [`CONTRIBUTING.md`](./CONTRIBUTING.md) asks every
contributor to grant a relicensing right along with their patch. It is not a
formality and it is not a rights grab: contributors keep the copyright on what they
wrote, and their work stays available to everyone under AGPL, forever.
