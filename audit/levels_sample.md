# VolDesk level audit: sample questions

10 questions per sub-section per level. Seeds are deterministic, so re-running gives the same file.

# Section 1: Interview Prep (Options)

## 1A Greek drills (quickfire)

### Level 1: directional intuition, no calculations

**Q1** (`compare`, topic `greeks:gamma`, seed 1007495)

EURJPY, same notional. Which option has more **gamma** (in size)?

- A: 1W ATM call
- B: 1W 10-delta OTM call

- *Which has more?*: **A: 1W ATM call**
- *Written*: Why?

<details><summary>Model answer</summary>

**Answer: A: 1W ATM call.**

1. Intuition: ATM gamma ~ e^(-rf T) n(d1) / (S vol sqrt(T)): the shorter the expiry the more concentrated (and larger) gamma is near the strike. For OTM strikes this reverses close to expiry, because the strike becomes many standard deviations away.
2. Engine numbers (EUR/base 10m each): A = +3.16m EUR, B = +1.45m EUR; |A|/|B| = 2.18.


</details>

**Q2** (`matrix_L1`, topic `greeks:theta`, seed 1007526)

You are **short a 1-month GBPUSD 15-delta OTM put** (notional GBP 10m, strike 1.28940, spot 1.32000, spot delta unadjusted).

**Change:** compare it with the same strike at a 2-month expiry instead of 1M (longer time to expiry, spot and vol unchanged).

What happens to the **size** of your theta exposure?

- *Sign of your theta now*: **Positive (long)**
- *Change in your theta*: **Shrinks in size**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your theta shrinks in size** (positive to start).

1. Sign: you are short the option, so your theta has the opposite sign to a long put's.
2. Intuition: (Here the option has MORE time to expiry, so read this in reverse.) Near the strike, decay accelerates into expiry (~1/sqrt T); far from the strike there is little time value left, so decay fades. Deep ITM options can even have positive theta from carry.
3. Engine: theta goes from 1,156 to 1,040 (P&L per day). A shock one third the size gives 1,130, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ITM 75-delta put with the same tenor and shock, the engine says theta shrinks in size too.


</details>

**Q3** (`matrix_L1`, topic `greeks:delta`, seed 1007557)

You are **long a 6-month NZDUSD 15-delta OTM call** (notional NZD 10m, strike 0.62869, spot 0.58000, spot delta unadjusted).

**Change:** implied vol rises 2.0 vol points (from 10.1%), all strikes.

What happens to the **size** of your delta exposure?

- *Sign of your delta now*: **Positive (long)**
- *Change in your delta*: **Grows in size**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your delta grows in size** (positive to start).

1. Sign: you are long the option, so your delta has the same sign as a long call's.
2. Intuition: Higher vol makes every strike look closer to the money, so deltas are pulled towards 50: OTM deltas grow and ITM deltas shrink (that is vanna). Lower vol pushes them apart.
3. Engine: delta goes from 1,500,000 to 1,969,059 (base-ccy notional). A shock one third the size gives 1,665,695, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ITM 75-delta call with the same tenor and shock, the engine says delta shrinks in size, the opposite way. Where the strike sits matters.


</details>

**Q4** (`matrix_L1`, topic `greeks:theta`, seed 1007588)

You are **short a 1-year AUDUSD 15-delta OTM put** (notional AUD 10m, strike 0.59342, spot 0.66000, spot delta unadjusted).

**Change:** spot rallies 1.0% (sticky strike).

What happens to the **size** of your theta exposure?

- *Sign of your theta now*: **Positive (long)**
- *Change in your theta*: **Shrinks in size**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your theta shrinks in size** (positive to start).

1. Sign: you are short the option, so your theta has the opposite sign to a long put's.
2. Intuition: Theta mirrors gamma (theta ~ -0.5 gamma S^2 vol^2 plus rate terms): it is largest near the strike.
3. Engine: theta goes from 224 to 207 (P&L per day). A shock one third the size gives 218, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ITM 75-delta put with the same tenor and shock, the engine says theta grows in size, the opposite way. Where the strike sits matters.


</details>

**Q5** (`compare`, topic `greeks:vega`, seed 1007619)

EURUSD, same notional. Which option has more **vega** (in size)?

- A: 1M 25-delta OTM call
- B: 1Y 25-delta OTM call

- *Which has more?*: **B: 1Y 25-delta OTM call**
- *Written*: Why?

<details><summary>Model answer</summary>

**Answer: B: 1Y 25-delta OTM call.**

1. Intuition: Vega ~ S e^(-rf T) n(d1) sqrt(T): longer expiries carry more vega because there is more time for vol to matter. At a given expiry ATM has the most vega; OTM has less (n(d1) is smaller).
2. Engine numbers (EUR/base 10m each): A = +10.6k USD, B = +36.5k USD; |A|/|B| = 0.29.


</details>

**Q6** (`matrix_L1`, topic `greeks:vega`, seed 1007650)

You are **short a 6-month EURUSD 25-delta OTM put** (notional EUR 10m, strike 1.13011, spot 1.16000, spot delta unadjusted).

**Change:** compare it with the same strike at a 12-month expiry instead of 6M (longer time to expiry, spot and vol unchanged).

What happens to the **size** of your vega exposure?

- *Sign of your vega now*: **Negative (short)**
- *Change in your vega*: **Grows in size**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your vega grows in size** (negative to start).

1. Sign: you are short the option, so your vega has the opposite sign to a long put's.
2. Intuition: (Here the option has MORE time to expiry, so read this in reverse.) Vega scales with sqrt(T) near the money: less time, less vega; wing vega falls faster still.
3. Engine: vega goes from -25,943 to -38,238 (P&L per vol point). A shock one third the size gives -30,688, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ITM 75-delta put with the same tenor and shock, the engine says vega grows in size too.


</details>

**Q7** (`matrix_L1`, topic `greeks:delta`, seed 1007681)

You are **long a 6-month GBPUSD ITM 75-delta put** (notional GBP 10m, strike 1.37100, spot 1.32000, spot delta unadjusted).

**Change:** spot sells off 1.0% (sticky strike).

What happens to the **size** of your delta exposure?

- *Sign of your delta now*: **Negative (short)**
- *Change in your delta*: **Grows in size**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your delta grows in size** (negative to start).

1. Sign: you are long the option, so your delta has the same sign as a long put's.
2. Intuition: Delta changes by about gamma x dS, and long-option gamma is positive: a rally raises a call's delta towards 1 and moves a put's delta towards 0; a selloff does the opposite.
3. Engine: delta goes from -7,321,610 to -7,860,013 (base-ccy notional). A shock one third the size gives -7,508,602, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ATM put with the same tenor and shock, the engine says delta grows in size too.


</details>

**Q8** (`matrix_L1`, topic `greeks:rho`, seed 1007712)

You are **short a 1-week GBPUSD ATM put** (notional GBP 10m, strike 1.32006, spot 1.32000, spot delta unadjusted).

**Change:** spot rallies 1.0% (sticky strike).

What happens to the **size** of your rho exposure?

- *Sign of your rho now*: **Positive (long)**
- *Change in your rho*: **Shrinks in size**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your rho shrinks in size** (positive to start).

1. Sign: you are short the option, so your rho has the opposite sign to a long put's.
2. Intuition: Rho to the quote-ccy rate is K T e^(-rd T) N(d2) for a call and -K T e^(-rd T) N(-d2) for a put: it grows as the option moves into the money (the strike payment becomes likely).
3. Engine: rho goes from 13 to 4 (P&L per +1bp in the quote-ccy rate). A shock one third the size gives 9, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ITM 75-delta put with the same tenor and shock, the engine says rho shrinks in size too.


</details>

**Q9** (`matrix_L1`, topic `greeks:rho`, seed 1007743)

You are **short a 1-week GBPUSD 15-delta OTM call** (notional GBP 10m, strike 1.33385, spot 1.32000, spot delta unadjusted).

**Change:** compare it with the same strike at a 14-day expiry instead of 1W (longer time to expiry).

What happens to the **size** of your rho exposure?

- *Sign of your rho now*: **Negative (short)**
- *Change in your rho*: **Grows in size**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your rho grows in size** (negative to start).

1. Sign: you are short the option, so your rho has the opposite sign to a long call's.
2. Intuition: (Here the option has MORE time to expiry, so read this in reverse.) Rho is proportional to T (the strike is discounted over T), so it shrinks as time passes; ITM rho also depends on how likely exercise stays.
3. Engine: rho goes from -4 to -12 (P&L per +1bp in the quote-ccy rate). A shock one third the size gives -6, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ITM 75-delta call with the same tenor and shock, the engine says rho grows in size too.


</details>

**Q10** (`matrix_L1`, topic `greeks:gamma`, seed 1007774)

You are **short a 1-month AUDUSD ATM put** (notional AUD 10m, strike 0.66038, spot 0.66000, spot delta unadjusted).

**Change:** spot sells off 1.5% (sticky strike).

What happens to the **size** of your gamma exposure?

- *Sign of your gamma now*: **Negative (short)**
- *Change in your gamma*: **Shrinks in size**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your gamma shrinks in size** (negative to start).

1. Sign: you are short the option, so your gamma has the opposite sign to a long put's.
2. Intuition: Gamma peaks near the strike: spot moving towards the strike raises it, moving away lowers it.
3. Engine: gamma goes from -1,481,854 to -1,264,697 (change in delta per 1% spot). A shock one third the size gives -1,456,249, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ITM 75-delta put with the same tenor and shock, the engine says gamma shrinks in size too.


</details>

### Level 2: combinations, light calculations with every input given

**Q1** (`via_second_order`, topic `greeks:vanna`, seed 1112224)

You are **short a 1-month NZDUSD deep ITM 85-delta put** (notional NZD 10m). **Change:** spot rallies 0.5% (sticky strike).

Using **vanna**, does your **vega** exposure rise or fall? What is the sign of your vanna?

- *Sign of your vanna*: **Negative**
- *Your vega exposure*: **Falls (more negative)**
- *Written*: Explain using the second-order Greek.

<details><summary>Model answer</summary>

**Your vanna is negative, so your vega falls.**

1. Vanna is both d(delta)/d(vol) and d(vega)/d(spot).
2. Vanna = -e^(-rf T) n(d1) d2 / vol: positive for strikes above the forward, negative below, near zero around the money, largest in size near the 25-delta points. Moving spot moves where the strike sits on that S-shaped curve.
3. Change in vega ~ vanna x change in spot: sign(vanna) = -, change in spot = +.
4. Engine: vanna = -256,057 (change in delta per vol point); vega goes from -3,901 to -4,642 (P&L per vol point).

</details>

**Q2** (`matrix_L2`, topic `greeks:vanna`, seed 1112255)

You are **short a 3-month NZDUSD ATM call** (notional NZD 10m, strike 0.58231, spot 0.58000, spot delta unadjusted).

**Change:** compare it with the same strike at a 6-month expiry instead of 3M (longer time to expiry, spot and vol unchanged).

What happens to your **vanna** exposure (signed)?

- *Sign of your vanna now*: **Roughly zero**
- *Change in your vanna*: **Rises (more positive)**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your vanna rises** (roughly to start).

1. Sign: you are short the option, so your vanna has the opposite sign to a long call's.
2. Intuition: (Here the option has MORE time to expiry, so read this in reverse.) As expiry approaches the vanna profile gets narrower and taller; far strikes lose vanna, nearer ones can gain.
3. Engine: vanna goes from -19,823 to -5,657 (change in delta per vol point). A shock one third the size gives -13,524, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ITM 75-delta call with the same tenor and shock, the engine says vanna falls, the opposite way. Where the strike sits matters.


</details>

**Q3** (`matrix_L2`, topic `greeks:vanna`, seed 1112286)

You are **short a 6-month AUDUSD ATM put** (notional AUD 10m, strike 0.66238, spot 0.66000, spot delta unadjusted).

**Change:** spot rallies 1.0% (sticky strike).

What happens to your **vanna** exposure (signed)?

- *Sign of your vanna now*: **Negative (short)**
- *Change in your vanna*: **Rises (more positive)**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your vanna rises** (negative to start).

1. Sign: you are short the option, so your vanna has the opposite sign to a long put's.
2. Intuition: Vanna = -e^(-rf T) n(d1) d2 / vol: positive for strikes above the forward, negative below, near zero around the money, largest in size near the 25-delta points. Moving spot moves where the strike sits on that S-shaped curve.
3. Engine: vanna goes from -27,741 to 30,609 (change in delta per vol point). A shock one third the size gives -8,108, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ITM 75-delta put with the same tenor and shock, the engine says vanna rises too.


</details>

**Q4** (`matrix_L2`, topic `greeks:vanna`, seed 1112317)

You are **short a 6-month EURUSD ATM put** (notional EUR 10m, strike 1.17096, spot 1.16000, spot delta unadjusted).

**Change:** spot sells off 1.0% (sticky strike).

What happens to your **vanna** exposure (signed)?

- *Sign of your vanna now*: **Roughly zero**
- *Change in your vanna*: **Falls (more negative)**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your vanna falls** (roughly to start).

1. Sign: you are short the option, so your vanna has the opposite sign to a long put's.
2. Intuition: Vanna = -e^(-rf T) n(d1) d2 / vol: positive for strikes above the forward, negative below, near zero around the money, largest in size near the 25-delta points. Moving spot moves where the strike sits on that S-shaped curve.
3. Engine: vanna goes from -27,929 to -125,458 (change in delta per vol point). A shock one third the size gives -60,964, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ITM 75-delta put with the same tenor and shock, the engine says vanna falls too.


</details>

**Q5** (`via_second_order`, topic `greeks:charm`, seed 1112348)

You are **short a 1-month AUDUSD 15-delta OTM put** (notional AUD 10m). **Change:** 3 days pass (spot and vol unchanged).

Using **charm**, does your **delta** exposure rise or fall? What is the sign of your charm?

- *Sign of your charm*: **Negative**
- *Your delta exposure*: **Falls (more negative)**
- *Written*: Explain using the second-order Greek.

<details><summary>Model answer</summary>

**Your charm is negative, so your delta falls.**

1. Charm is d(delta)/d(time): how delta drifts as time passes.
2. Charm (delta decay per day) is biggest for options near the 25-delta points and changes sign across the money.
3. Change in delta ~ charm x change in time: sign(charm) = -, change in time = + (time passing).
4. Engine: charm = -37,814 (change in delta per day); delta goes from 1,500,000 to 1,381,897 (base-ccy notional).

</details>

**Q6** (`via_second_order`, topic `greeks:veta`, seed 1112379)

You are **long a 6-month GBPUSD 15-delta OTM put** (notional GBP 10m). **Change:** 18 days pass (spot and vol unchanged).

Using **veta**, does your **vega** exposure rise or fall? What is the sign of your veta?

- *Sign of your veta*: **Negative**
- *Your vega exposure*: **Falls (more negative)**
- *Written*: Explain using the second-order Greek.

<details><summary>Model answer</summary>

**Your veta is negative, so your vega falls.**

1. Veta is d(vega)/d(time): how fast vega bleeds.
2. Veta = d(vega)/dt. Vega bleeds fastest near the strike, so veta is most negative there.
3. Change in vega ~ veta x change in time: sign(veta) = -, change in time = + (time passing).
4. Engine: veta = -114 (change in vega per day); vega goes from 21,632 to 19,503 (P&L per vol point).

</details>

**Q7** (`matrix_L2`, topic `greeks:charm`, seed 1112410)

You are **short a 6-month AUDUSD 15-delta OTM put** (notional AUD 10m, strike 0.61206, spot 0.66000, spot delta unadjusted).

**Change:** 91 days pass (spot and vol unchanged).

What happens to your **charm** exposure (signed)?

- *Sign of your charm now*: **Negative (short)**
- *Change in your charm*: **Falls (more negative)**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your charm falls** (negative to start).

1. Sign: you are short the option, so your charm has the opposite sign to a long put's.
2. Intuition: Charm grows sharply into expiry: deltas snap towards 0 or 1 in the last days.
3. Engine: charm goes from -5,679 to -10,783 (change in delta per day). A shock one third the size gives -6,932, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ITM 75-delta put with the same tenor and shock, the engine says charm rises, the opposite way. Where the strike sits matters.


</details>

**Q8** (`via_second_order`, topic `greeks:volga`, seed 1112441)

You are **long a 1-month AUDUSD deep ITM 85-delta put** (notional AUD 10m). **Change:** implied vol rises 1.0 vol points (from 9.3%), all strikes.

Using **volga**, does your **vega** exposure rise or fall? What is the sign of your volga?

- *Sign of your volga*: **Positive**
- *Your vega exposure*: **Rises (more positive)**
- *Written*: Explain using the second-order Greek.

<details><summary>Model answer</summary>

**Your volga is positive, so your vega rises.**

1. Volga is d(vega)/d(vol): how vega itself responds to vol.
2. Volga = vega x d1 d2 / vol: ~0 at the money and positive in the wings (it peaks around the 10-15 delta points). Moving spot changes how far into the wings the strike sits.
3. Change in vega ~ volga x change in vol: sign(volga) = +, change in vol = +.
4. Engine: volga = 527 (change in vega per vol point); vega goes from 4,438 to 4,914 (P&L per vol point).

</details>

**Q9** (`matrix_L2`, topic `greeks:veta`, seed 1112472)

You are **long a 1-week EURUSD deep ITM 85-delta call** (notional EUR 10m, strike 1.14883, spot 1.16000, spot delta unadjusted).

**Change:** implied vol falls 2.0 vol points (from 6.8%), all strikes.

What happens to your **veta** exposure (signed)?

- *Sign of your veta now*: **Negative (short)**
- *Change in your veta*: **Rises (more positive)**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your veta rises** (negative to start).

1. Sign: you are long the option, so your veta has the same sign as a long call's.
2. Intuition: Higher vol changes how fast vega bleeds: wing vega bleeds differently once the strike is closer in standard deviations.
3. Engine: veta goes from -540 to -458 (change in vega per day). A shock one third the size gives -528, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ATM call with the same tenor and shock, the engine says veta stays roughly unchanged, the opposite way. Where the strike sits matters.


</details>

**Q10** (`matrix_L2`, topic `greeks:vanna`, seed 1112503)

You are **long a 6-month EURUSD ATM call** (notional EUR 10m, strike 1.17096, spot 1.16000, spot delta unadjusted).

**Change:** implied vol rises 3.0 vol points (from 7.5%), all strikes.

What happens to your **vanna** exposure (signed)?

- *Sign of your vanna now*: **Roughly zero**
- *Change in your vanna*: **Falls (more negative)**
- *Written*: Why? (one or two sentences)

<details><summary>Model answer</summary>

**Answer: your vanna falls** (roughly to start).

1. Sign: you are long the option, so your vanna has the same sign as a long call's.
2. Intuition: Higher vol stretches the vanna profile out: the strike looks closer to the money in standard deviations, which moves its vanna along the S-shaped curve.
3. Engine: vanna goes from 27,929 to 21,086 (change in delta per vol point). A shock one third the size gives 24,836, the same direction, so the answer does not depend on the shock size.
4. Contrast: for an ITM 75-delta call with the same tenor and shock, the engine says vanna rises, the opposite way. Where the strike sits matters.


</details>

### Level 3: calculations plus subtler concepts

**Q1** (`breakeven`, topic `concepts:gamma_theta`, seed 1216953)

You buy a 3M ATM EURGBP straddle (EUR 10m per leg) at 5.20% vol and delta-hedge it. How big a daily move (in %) do you need to break even on theta? If spot then moves 0.16% a day on average, do you make or lose money?

Givens:

| Given | Value |
|---|---|
| Spot | 0.87879 |
| Theta (GBP per day) | -984 |
| Gamma (EUR delta change per 1% spot move) | 3,051,420 |

- *Breakeven daily move (%)*: **0.2709 %**
- *With 0.16% daily moves*: **Lose money**
- *Written*: Explain the gamma/theta trade-off.

<details><summary>Model answer</summary>

**About 0.27% a day; with 0.16% moves you lose money.**

1. Each day you earn 0.5 x Gamma x dS^2 and pay |theta|. Break even when they are equal: dS = sqrt(2|theta| / Gamma).
2. Gamma = 3,051,420 / (1% x 0.87879) = 347,229,714; dS = 0.0023807, i.e. 0.27%.
3. Check: theta ~ -0.5 Gamma S^2 vol^2 / 365, so the breakeven is about vol / sqrt(365) = 5.20% / 19.1 = 0.27%. Realised above implied wins.

</details>

**Q2** (`time_scaling`, topic `greeks:gamma`, seed 1216984)

You are long a 1Y ATM USDJPY straddle (vol 10.3%, USD 10m per leg). 3 months pass with spot and implied vol unchanged. Which way does your gamma move, and roughly what is it now?

Givens:

| Given | Value |
|---|---|
| Greek | gamma |
| Time to expiry now (years) | 1 |
| Time to expiry later (years) | 0.75 |
| Your gamma now (USD delta per 1% spot) | 741,936 |

- *Direction of gamma (size)*: **Increases**
- *New gamma (USD delta per 1% spot)*: **856,714**
- *Written*: Explain the scaling.

<details><summary>Model answer</summary>

**Gamma rises to about 856,714 USD delta per 1% spot.**

1. Intuition: spot and vol are unchanged, so the straddle stays at the money and only time matters. ATM vega ~ S n(d1) sqrt(T); ATM gamma ~ n(d1) / (S vol sqrt(T)); ATM theta ~ -S n(d1) vol / (2 sqrt(T)).
2. Formula: gamma_later = gamma_now x sqrt(T0/T1) = 741,936 x 1.155 = 856,714.
3. Engine (full revaluation): 854,487. The gap (-0.3%) comes from rates and the strike drifting slightly off the new ATM (d1 is not exactly 0).

</details>

**Q3** (`rv_iv`, topic `concepts:implied_vs_realised`, seed 1217015)

You are long a delta-hedged 1M ATM EURUSD straddle. Over the next 5 days spot realises 10.1% vol while implied stays at 7.1%. Do you make or lose money, and roughly how much (in USD, holding gamma constant)?

Givens:

| Given | Value |
|---|---|
| Spot | 1.16 |
| Gamma (EUR delta change per 1% spot move) | 3,886,409 |
| Implied vol paid (%) | 7.1 |
| Realised vol (%) | 10.1 |
| Days held (calendar) | 5 |

- *Sign of P&L*: **Profit**
- *P&L (USD)*: **15,933**
- *Written*: Explain where the P&L comes from and why the estimate is approximate.

<details><summary>Model answer</summary>

**Profit of about 15,933 USD.**

1. Intuition: a delta-hedged option earns 0.5 Gamma dS^2 on each move and pays theta, which is priced at the implied vol. Net, you earn the gap between realised and implied variance.
2. Gamma in d2V/dS2 terms = gamma_1pct / (1% x S) = 3,886,409 / 0.0116 = 335,035,259.
3. P&L ~ 0.5 x Gamma x S^2 x (realised^2 - implied^2) x days/365 = 15,933.
4. Approximate because gamma changes as spot moves and time passes, and the P&L depends on when the moves happen (path dependence).

</details>

**Q4** (`vega_buckets`, topic `greeks:vega_buckets`, seed 1217046)

Your USDJPY book's vega is in two buckets (see Givens). 1M vol moves +2.4 and 1Y moves +0.8. What is your vega P&L in thousands? Is it bigger or smaller than total vega x the 1M move (240k)?

Givens:

| Given | Value |
|---|---|
| 1M vega (JPY per vol pt) | 50,000 |
| 1Y vega (JPY per vol pt) | 50,000 |
| 1M vol move (pts) | 2.4 |
| 1Y vol move (pts) | 0.8 |

- *Vega P&L (k JPY)*: **160.00**
- *Compared with the naive number*: **Smaller**
- *Written*: Why must vega be bucketed by tenor?

<details><summary>Model answer</summary>

**About 160k, vs 240k naive.**

1. Vol term structures rarely move in parallel: front vols move several times more than back vols, so vega is bucketed by tenor.
2. P&L ~ 50,000 x 2.4 + 50,000 x 0.8 = 160,000.
3. Engine full revaluation: 159,999 (gap from volga, the change in vega as vol moves).

</details>

**Q5** (`breakeven`, topic `concepts:gamma_theta`, seed 1217077)

You buy a 1M ATM EURUSD straddle (EUR 10m per leg) at 7.10% vol and delta-hedge it. How big a daily move (in %) do you need to break even on theta? If spot then moves 0.22% a day on average, do you make or lose money?

Givens:

| Given | Value |
|---|---|
| Spot | 1.16 |
| Theta (USD per day) | -3,094 |
| Gamma (EUR delta change per 1% spot move) | 3,887,182 |

- *Breakeven daily move (%)*: **0.3704 %**
- *With 0.22% daily moves*: **Lose money**
- *Written*: Explain the gamma/theta trade-off.

<details><summary>Model answer</summary>

**About 0.37% a day; with 0.22% moves you lose money.**

1. Each day you earn 0.5 x Gamma x dS^2 and pay |theta|. Break even when they are equal: dS = sqrt(2|theta| / Gamma).
2. Gamma = 3,887,182 / (1% x 1.16) = 335,101,897; dS = 0.0042972, i.e. 0.37%.
3. Check: theta ~ -0.5 Gamma S^2 vol^2 / 365, so the breakeven is about vol / sqrt(365) = 7.10% / 19.1 = 0.37%. Realised above implied wins.

</details>

**Q6** (`time_scaling`, topic `greeks:vega`, seed 1217108)

You are long a 1Y ATM USDCHF straddle (vol 8.0%, USD 10m per leg). 9 months pass with spot and implied vol unchanged. Which way does your vega move, and roughly what is it now?

Givens:

| Given | Value |
|---|---|
| Greek | vega |
| Time to expiry now (years) | 1 |
| Time to expiry later (years) | 0.25 |
| Your vega now (CHF per vol pt) | 61,379 |

- *Direction of vega (size)*: **Decreases**
- *New vega (CHF per vol pt)*: **30,690**
- *Written*: Explain the scaling.

<details><summary>Model answer</summary>

**Vega falls to about 30,690 CHF per vol pt.**

1. Intuition: spot and vol are unchanged, so the straddle stays at the money and only time matters. ATM vega ~ S n(d1) sqrt(T); ATM gamma ~ n(d1) / (S vol sqrt(T)); ATM theta ~ -S n(d1) vol / (2 sqrt(T)).
2. Formula: vega_later = vega_now x sqrt(T1/T0) = 61,379 x 0.500 = 30,690.
3. Engine (full revaluation): 23,383. The gap (-23.8%) comes from rates and the strike drifting slightly off the new ATM (d1 is not exactly 0).

</details>

**Q7** (`time_scaling`, topic `greeks:theta`, seed 1217139)

You are long a 1Y ATM USDJPY straddle (vol 10.3%, USD 10m per leg). 9 months pass with spot and implied vol unchanged. Which way does your theta move, and roughly what is it now?

Givens:

| Given | Value |
|---|---|
| Greek | theta |
| Time to expiry now (years) | 1 |
| Time to expiry later (years) | 0.25 |
| Your theta now (JPY per day) | -152,605 |

- *Direction of theta (size)*: **Increases**
- *New theta (JPY per day)*: **-305,210**
- *Written*: Explain the scaling.

<details><summary>Model answer</summary>

**Theta rises to about -305,210 JPY per day.**

1. Intuition: spot and vol are unchanged, so the straddle stays at the money and only time matters. ATM vega ~ S n(d1) sqrt(T); ATM gamma ~ n(d1) / (S vol sqrt(T)); ATM theta ~ -S n(d1) vol / (2 sqrt(T)).
2. Formula: theta_later = theta_now x sqrt(T0/T1) = -152,605 x 2.000 = -305,210.
3. Engine (full revaluation): -243,162. The gap (-20.3%) comes from rates and the strike drifting slightly off the new ATM (d1 is not exactly 0).

</details>

**Q8** (`vega_buckets`, topic `greeks:vega_buckets`, seed 1217170)

Your EURUSD book's vega is in two buckets (see Givens). 1M vol moves +2.4 and 1Y moves -0.5. What is your vega P&L in thousands? Is it bigger or smaller than total vega x the 1M move (-58k)?

Givens:

| Given | Value |
|---|---|
| 1M vega (USD per vol pt) | 60,000 |
| 1Y vega (USD per vol pt) | -84,000 |
| 1M vol move (pts) | 2.4 |
| 1Y vol move (pts) | -0.5 |

- *Vega P&L (k USD)*: **186.00**
- *Compared with the naive number*: **Bigger**
- *Written*: Why must vega be bucketed by tenor?

<details><summary>Model answer</summary>

**About 186k, vs -58k naive.**

1. Vol term structures rarely move in parallel: front vols move several times more than back vols, so vega is bucketed by tenor.
2. P&L ~ 60,000 x 2.4 + -84,000 x -0.5 = 186,000.
3. Engine full revaluation: 185,999 (gap from volga, the change in vega as vol moves).

</details>

**Q9** (`time_scaling`, topic `greeks:vega`, seed 1217201)

You are long a 1Y ATM USDJPY straddle (vol 10.3%, USD 10m per leg). 6 months pass with spot and implied vol unchanged. Which way does your vega move, and roughly what is it now?

Givens:

| Given | Value |
|---|---|
| Greek | vega |
| Time to expiry now (years) | 1 |
| Time to expiry later (years) | 0.5 |
| Your vega now (JPY per vol pt) | 11,636,890 |

- *Direction of vega (size)*: **Decreases**
- *New vega (JPY per vol pt)*: **8,228,524**
- *Written*: Explain the scaling.

<details><summary>Model answer</summary>

**Vega falls to about 8,228,524 JPY per vol pt.**

1. Intuition: spot and vol are unchanged, so the straddle stays at the money and only time matters. ATM vega ~ S n(d1) sqrt(T); ATM gamma ~ n(d1) / (S vol sqrt(T)); ATM theta ~ -S n(d1) vol / (2 sqrt(T)).
2. Formula: vega_later = vega_now x sqrt(T1/T0) = 11,636,890 x 0.707 = 8,228,524.
3. Engine (full revaluation): 8,040,531. The gap (-2.3%) comes from rates and the strike drifting slightly off the new ATM (d1 is not exactly 0).

</details>

**Q10** (`vega_buckets`, topic `greeks:vega_buckets`, seed 1217232)

Your NZDUSD book's vega is in two buckets (see Givens). 1M vol moves +1.7 and 1Y moves +0.8. What is your vega P&L in thousands? Is it bigger or smaller than total vega x the 1M move (170k)?

Givens:

| Given | Value |
|---|---|
| 1M vega (USD per vol pt) | 70,000 |
| 1Y vega (USD per vol pt) | 30,000 |
| 1M vol move (pts) | 1.7 |
| 1Y vol move (pts) | 0.8 |

- *Vega P&L (k USD)*: **143.00**
- *Compared with the naive number*: **Smaller**
- *Written*: Why must vega be bucketed by tenor?

<details><summary>Model answer</summary>

**About 143k, vs 170k naive.**

1. Vol term structures rarely move in parallel: front vols move several times more than back vols, so vega is bucketed by tenor.
2. P&L ~ 70,000 x 1.7 + 30,000 x 0.8 = 143,000.
3. Engine full revaluation: 142,999 (gap from volga, the change in vega as vol moves).

</details>

## 1B Write your Greek exposures

### Level 1: directional intuition, no calculations

**Q1** (`exposures_L1`, topic `exposures:put`, seed 1015414)

You are **long a 3M EURUSD 25-delta put**, notional 50.00m EUR per leg.

Spot 1.16000. Legs: put K=1.13713. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: -, Gamma: +, Theta: -, Vega: +**
- *Written*: How do your exposures change if time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **-** (-12.50m EUR, base notional)
- Gamma: **+** (+4.32m EUR, delta change per 1% spot)
- Theta: **-** (-3.0k USD, P&L per day)
- Vega: **+** (+91.9k USD, P&L per vol pt)

**Intuition for the structure:** A vanilla is long gamma, long vega and pays theta when bought; delta is negative for a put.

**After the shock (time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged):**
- short delta: -12.50m EUR to -52.4k EUR (less short). Charm: OTM deltas decay towards 0 and ITM deltas grow towards 100 as time passes.
- long gamma: +4.32m EUR to +270.2k EUR (less long). As expiry approaches, gamma at strikes near spot grows (~1/sqrt(T)) while gamma at strikes away from spot (ITM or OTM) collapses.
- short theta: -3.0k USD to -329 USD (less short). Theta at strikes near spot grows as expiry approaches; theta of options far from the strike (ITM or OTM) fades, and deep ITM options can even earn carry.
- long vega: +91.9k USD to +151 USD (less long). Vega falls with sqrt(T): less time left means less exposure to vol.

**P&L from the shock:** -323.5k USD by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol 0, theta -323.5k. The biggest driver is **theta**.

**Where the risk sits now:** the position is close to flat on the main Greeks.

</details>

**Q2** (`exposures_L1`, topic `exposures:put`, seed 1015445)

You are **long a 3M SPX 10-delta put**, notional $1.0k units per leg.

Spot 6,000. Legs: put K=5324. Convention: Black-Scholes, ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot rallies 6.0% (vol surface sticky by strike)**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: -/0, Gamma: +, Theta: -, Vega: +**
- *Written*: How do your exposures change if spot rallies 6.0% (vol surface sticky by strike)? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **-** (-100 units, base notional)
- Gamma: **+** (+17 units, delta change per 1% spot)
- Theta: **-** (-547 USD, P&L per day)
- Vega: **+** (+5.3k USD, P&L per vol pt)

**Intuition for the structure:** A vanilla is long gamma, long vega and pays theta when bought; delta is negative for a put.

**After the shock (spot rallies 6.0% (vol surface sticky by strike)):**
- short delta: -100 units to -32 units (less short). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite.
- long gamma: +17 units to +7 units (less long). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk.
- short theta: -547 USD to -241 USD (less short). Theta mirrors gamma: it is largest near the strikes.
- long vega: +5.3k USD to +2.3k USD (less long). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes.

**P&L from the shock:** -21.8k USD by full revaluation. Breakdown (spot, then vol, then time): delta -36.0k, gamma and higher-order spot +14.2k, vega/vol 0, theta 0. The biggest driver is **delta**.

**Where the risk sits now:** long vega (~0.2x a single ATM option).

</details>

**Q3** (`exposures_L1`, topic `exposures:put`, seed 1015476)

You are **long a 1M EURUSD 25-delta put**, notional 25.00m EUR per leg.

Spot 1.16000. Legs: put K=1.14578. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **implied vol is crushed 1.4 vol points across the surface**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: -, Gamma: +, Theta: -, Vega: +**
- *Written*: How do your exposures change if implied vol is crushed 1.4 vol points across the surface? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **-** (-6.25m EUR, base notional)
- Gamma: **+** (+3.85m EUR, delta change per 1% spot)
- Theta: **-** (-2.8k USD, P&L per day)
- Vega: **+** (+26.6k USD, P&L per vol pt)

**Intuition for the structure:** A vanilla is long gamma, long vega and pays theta when bought; delta is negative for a put.

**After the shock (implied vol is crushed 1.4 vol points across the surface):**
- short delta: -6.25m EUR to -5.05m EUR (less short). Vol down pushes deltas away from 50: OTM deltas shrink, ITM deltas grow.
- long gamma: +3.85m EUR to +4.25m EUR (more long). Lower vol concentrates gamma near the strikes: ATM gamma rises, far-strike gamma falls.
- short theta: -2.8k USD to -2.0k USD (less short). Theta scales with vol, so time decay shrinks.
- long vega: +26.6k USD to +23.6k USD (less long). ATM vega barely changes; wing vega falls (positive volga in the wings).

**P&L from the shock:** -35.3k USD by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol -35.3k, theta 0. The biggest driver is **vega**.

**Where the risk sits now:** long gamma (~0.9x a single ATM option); long vega (~0.7x a single ATM option); short delta (20% of notional).

</details>

**Q4** (`exposures_L1`, topic `exposures:put`, seed 1015507)

You are **short a 3M USDJPY ATM put**, notional 50.00m USD per leg.

Spot 152.000. Legs: put K=150.732. Convention: Spot delta, premium-adjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **implied vol spikes 3.4 vol points across the surface**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: +, Gamma: -, Theta: +, Vega: -**
- *Written*: How do your exposures change if implied vol spikes 3.4 vol points across the surface? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **+** (+24.75m USD, base notional, premium-adjusted)
- Gamma: **-** (-3.95m USD, delta change per 1% spot)
- Theta: **+** (+1.10m JPY, P&L per day)
- Vega: **-** (-15.01m JPY, P&L per vol pt)

**Intuition for the structure:** A vanilla is long gamma, long vega and pays theta when bought; delta is negative for a put. You are SHORT the structure, so flip every sign.

**After the shock (implied vol spikes 3.4 vol points across the surface):**
- long delta: +24.75m USD to +25.04m USD (roughly unchanged). Vol up pulls every strike's delta towards 50 (vanna): OTM deltas grow, ITM deltas shrink.
- short gamma: -3.95m USD to -2.95m USD (less short). Higher vol spreads gamma over a wider range of spot: gamma near the strikes falls (ATM gamma ~ 1/vol) and gamma at far strikes rises.
- long theta: +1.10m JPY to +1.38m JPY (more long). ATM theta scales roughly with vol, so the daily decay (paid or received) grows.
- short vega: -15.01m JPY to -15.00m JPY (roughly unchanged). ATM vega barely moves with the vol level (volga ~ 0 ATM); wing vega rises (positive volga). Long-wing structures gain vega.

**P&L from the shock:** -51.02m JPY by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol -51.02m, theta 0. The biggest driver is **vega**.

**Where the risk sits now:** short gamma (~0.7x a single ATM option); short vega (~1.0x a single ATM option); long delta (~0.5x a single ATM option).

</details>

**Q5** (`exposures_L1`, topic `exposures:put`, seed 1015538)

You are **short a 3M EURGBP ATM put**, notional 10.00m EUR per leg.

Spot 0.87879. Legs: put K=0.88201. Convention: Spot delta, premium-adjusted (premium in EUR); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: +, Gamma: -, Theta: +, Vega: -**
- *Written*: How do your exposures change if time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **+** (+4.97m EUR, base notional, premium-adjusted)
- Gamma: **-** (-1.53m EUR, delta change per 1% spot)
- Theta: **+** (+300 GBP, P&L per day)
- Vega: **-** (-17.4k GBP, P&L per vol pt)

**Intuition for the structure:** A vanilla is long gamma, long vega and pays theta when bought; delta is negative for a put. You are SHORT the structure, so flip every sign.

**After the shock (time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged):**
- long delta: +4.97m EUR to +8.41m EUR (more long). Charm: OTM deltas decay towards 0 and ITM deltas grow towards 100 as time passes.
- short gamma: -1.53m EUR to -6.78m EUR (more short). As expiry approaches, gamma at strikes near spot grows (~1/sqrt(T)) while gamma at strikes away from spot (ITM or OTM) collapses.
- long theta: +300 GBP to +1.6k GBP (more long). Theta at strikes near spot grows as expiry approaches; theta of options far from the strike (ITM or OTM) fades, and deep ITM options can even earn carry.
- short vega: -17.4k GBP to -1.6k GBP (less short). Vega falls with sqrt(T): less time left means less exposure to vol.

**P&L from the shock:** +55.0k GBP by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol 0, theta +55.0k. The biggest driver is **theta**.

**Where the risk sits now:** short gamma (~4.4x a single ATM option); long delta (~0.8x a single ATM option).

</details>

**Q6** (`exposures_L1`, topic `exposures:call`, seed 1015569)

You are **short a 3M EURCHF ATM call**, notional 50.00m EUR per leg.

Spot 0.92800. Legs: call K=0.92302. Convention: Spot delta, premium-adjusted (premium in EUR); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **implied vol spikes 2.9 vol points across the surface**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: -, Gamma: -, Theta: +, Vega: -**
- *Written*: How do your exposures change if implied vol spikes 2.9 vol points across the surface? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **-** (-24.87m EUR, base notional, premium-adjusted)
- Gamma: **-** (-7.21m EUR, delta change per 1% spot)
- Theta: **+** (+1.5k CHF, P&L per day)
- Vega: **-** (-92.1k CHF, P&L per vol pt)

**Intuition for the structure:** A vanilla is long gamma, long vega and pays theta when bought; delta is positive for a call. You are SHORT the structure, so flip every sign.

**After the shock (implied vol spikes 2.9 vol points across the surface):**
- short delta: -24.87m EUR to -24.63m EUR (roughly unchanged). Vol up pulls every strike's delta towards 50 (vanna): OTM deltas grow, ITM deltas shrink.
- short gamma: -7.21m EUR to -4.72m EUR (less short). Higher vol spreads gamma over a wider range of spot: gamma near the strikes falls (ATM gamma ~ 1/vol) and gamma at far strikes rises.
- long theta: +1.5k CHF to +2.9k CHF (more long). ATM theta scales roughly with vol, so the daily decay (paid or received) grows.
- short vega: -92.1k CHF to -92.1k CHF (roughly unchanged). ATM vega barely moves with the vol level (volga ~ 0 ATM); wing vega rises (positive volga). Long-wing structures gain vega.

**P&L from the shock:** -267.0k CHF by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol -267.0k, theta 0. The biggest driver is **vega**.

**Where the risk sits now:** short gamma (~0.7x a single ATM option); short vega (~1.0x a single ATM option); short delta (~0.5x a single ATM option).

</details>

**Q7** (`exposures_L1`, topic `exposures:call`, seed 1015600)

You are **long a 3M AUDUSD 75-delta call**, notional 25.00m AUD per leg.

Spot 0.66000. Legs: call K=0.63935. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot sells off 5.4% (vol surface sticky by strike)**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: +, Gamma: +, Theta: -, Vega: +**
- *Written*: How do your exposures change if spot sells off 5.4% (vol surface sticky by strike)? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **+** (+18.54m AUD, base notional)
- Gamma: **+** (+1.57m AUD, delta change per 1% spot)
- Theta: **-** (-1.5k USD, P&L per day)
- Vega: **+** (+26.1k USD, P&L per vol pt)

**Intuition for the structure:** A vanilla is long gamma, long vega and pays theta when bought; delta is positive for a call.

**After the shock (spot sells off 5.4% (vol surface sticky by strike)):**
- long delta: +18.54m AUD to +8.24m AUD (less long). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite.
- long gamma: +1.57m AUD to +1.79m AUD (more long). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk.
- short theta: -1.5k USD to -1.6k USD (more short). Theta mirrors gamma: it is largest near the strikes.
- long vega: +26.1k USD to +28.1k USD (more long). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes.

**P&L from the shock:** -482.8k USD by full revaluation. Breakdown (spot, then vol, then time): delta -660.8k, gamma and higher-order spot +178.0k, vega/vol 0, theta 0. The biggest driver is **delta**.

**Where the risk sits now:** long gamma (~0.9x a single ATM option); long vega (~0.9x a single ATM option); long delta (33% of notional).

</details>

**Q8** (`exposures_L1`, topic `exposures:put`, seed 1015631)

You are **short a 3M USDJPY 75-delta put**, notional 25.00m USD per leg.

Spot 152.000. Legs: put K=155.807. Convention: Spot delta, premium-adjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **46 days pass with spot and vols unchanged**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: +, Gamma: -, Theta: +, Vega: -**
- *Written*: How do your exposures change if 46 days pass with spot and vols unchanged? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **+** (+19.33m USD, base notional, premium-adjusted)
- Gamma: **-** (-1.68m USD, delta change per 1% spot)
- Theta: **+** (+533.4k JPY, P&L per day)
- Vega: **-** (-6.10m JPY, P&L per vol pt)

**Intuition for the structure:** A vanilla is long gamma, long vega and pays theta when bought; delta is negative for a put. You are SHORT the structure, so flip every sign.

**After the shock (46 days pass with spot and vols unchanged):**
- long delta: +19.33m USD to +20.66m USD (more long). Charm: OTM deltas decay towards 0 and ITM deltas grow towards 100 as time passes.
- short gamma: -1.68m USD to -2.11m USD (more short). As expiry approaches, gamma at strikes near spot grows (~1/sqrt(T)) while gamma at strikes away from spot (ITM or OTM) collapses.
- long theta: +533.4k JPY to +625.2k JPY (more long). Theta at strikes near spot grows as expiry approaches; theta of options far from the strike (ITM or OTM) fades, and deep ITM options can even earn carry.
- short vega: -6.10m JPY to -3.76m JPY (less short). Vega falls with sqrt(T): less time left means less exposure to vol.

**P&L from the shock:** +26.88m JPY by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol 0, theta +26.88m. The biggest driver is **theta**.

**Where the risk sits now:** short gamma (~1.1x a single ATM option); short vega (~0.5x a single ATM option); long delta (~0.8x a single ATM option).

</details>

**Q9** (`exposures_L1`, topic `exposures:call`, seed 1015662)

You are **short a 1M GBPUSD ATM call**, notional 25.00m GBP per leg.

Spot 1.32000. Legs: call K=1.32030. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: -, Gamma: -, Theta: +, Vega: -**
- *Written*: How do your exposures change if time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **-** (-12.46m GBP, base notional)
- Gamma: **-** (-4.65m GBP, delta change per 1% spot)
- Theta: **+** (+4.6k USD, P&L per day)
- Vega: **-** (-37.9k USD, P&L per vol pt)

**Intuition for the structure:** A vanilla is long gamma, long vega and pays theta when bought; delta is positive for a call. You are SHORT the structure, so flip every sign.

**After the shock (time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged):**
- short delta: -12.46m GBP to -12.09m GBP (less short). Charm: OTM deltas decay towards 0 and ITM deltas grow towards 100 as time passes.
- short gamma: -4.65m GBP to -19.19m GBP (more short). As expiry approaches, gamma at strikes near spot grows (~1/sqrt(T)) while gamma at strikes away from spot (ITM or OTM) collapses.
- long theta: +4.6k USD to +17.1k USD (more long). Theta at strikes near spot grows as expiry approaches; theta of options far from the strike (ITM or OTM) fades, and deep ITM options can even earn carry.
- short vega: -37.9k USD to -9.7k USD (less short). Vega falls with sqrt(T): less time left means less exposure to vol.

**P&L from the shock:** +212.0k USD by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol 0, theta +212.0k. The biggest driver is **theta**.

**Where the risk sits now:** short gamma (~4.1x a single ATM option); short vega (~0.3x a single ATM option); short delta (48% of notional).

</details>

**Q10** (`exposures_L1`, topic `exposures:put`, seed 1015693)

You are **long a 3M GBPUSD ATM put**, notional 25.00m GBP per leg.

Spot 1.32000. Legs: put K=1.32095. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: -, Gamma: +, Theta: -, Vega: +**
- *Written*: How do your exposures change if time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **-** (-12.39m GBP, base notional)
- Gamma: **+** (+2.60m GBP, delta change per 1% spot)
- Theta: **-** (-2.7k USD, P&L per day)
- Vega: **+** (+65.2k USD, P&L per vol pt)

**Intuition for the structure:** A vanilla is long gamma, long vega and pays theta when bought; delta is negative for a put.

**After the shock (time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged):**
- short delta: -12.39m GBP to -13.86m GBP (more short). Charm: OTM deltas decay towards 0 and ITM deltas grow towards 100 as time passes.
- long gamma: +2.60m GBP to +19.04m GBP (more long). As expiry approaches, gamma at strikes near spot grows (~1/sqrt(T)) while gamma at strikes away from spot (ITM or OTM) collapses.
- short theta: -2.7k USD to -16.9k USD (more short). Theta at strikes near spot grows as expiry approaches; theta of options far from the strike (ITM or OTM) fades, and deep ITM options can even earn carry.
- long vega: +65.2k USD to +9.7k USD (less long). Vega falls with sqrt(T): less time left means less exposure to vol.

**P&L from the shock:** -427.0k USD by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol 0, theta -427.0k. The biggest driver is **theta**.

**Where the risk sits now:** long gamma (~7.3x a single ATM option); short delta (55% of notional).

</details>

### Level 2: combinations, light calculations with every input given

**Q1** (`exposures_L2`, topic `exposures:calendar`, seed 1120143)

You are **long a 1W EURUSD ATM call calendar (short near, long 3M)**, notional 10.00m EUR per leg.

Spot 1.16000. Legs: short near call K=1.16041, long far call K=1.16041. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **the skew steepens: 25d risk reversals move 1.4 vols further towards puts**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: 0, Gamma: -, Theta: +, Vega: +**
- *Written*: How do your exposures change if the skew steepens: 25d risk reversals move 1.4 vols further towards puts? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **0** (+446.0k EUR, base notional)
- Gamma: **-** (-3.15m EUR, delta change per 1% spot)
- Theta: **+** (+2.2k USD, P&L per day)
- Vega: **+** (+16.5k USD, P&L per vol pt)

**Intuition for the structure:** Short the near expiry, long the far expiry at the same strike: short gamma (the near leg dominates gamma), long vega (the far leg dominates vega), and you earn theta.

**After the shock (the skew steepens: 25d risk reversals move 1.4 vols further towards puts):**
- long delta: +446.0k EUR to +441.5k EUR (roughly unchanged). Each leg's delta moves via vanna and its own vol change: puts' deltas grow in size as their vols rise.
- short gamma: -3.15m EUR to -3.17m EUR (roughly unchanged). A skew move changes each strike's vol differently: low-strike vols rise, high-strike vols fall, so each leg's gamma moves the opposite way to its vol.
- long theta: +2.2k USD to +2.2k USD (roughly unchanged). Legs whose vol rose decay faster, legs whose vol fell decay slower.
- long vega: +16.5k USD to +16.5k USD (roughly unchanged). Each leg's vega responds to its own vol change via volga; wing legs are affected most.

**P&L from the shock:** +2.4k USD by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol +2.4k, theta 0. The biggest driver is **vega**.

**Where the risk sits now:** short gamma (~0.7x a single ATM option); long vega (~2.6x a single ATM option).

</details>

**Q2** (`exposures_L2`, topic `exposures:risk_reversal`, seed 1120174)

You are **long a 6M AUDUSD 25-delta risk reversal (call over put), delta-hedged**, notional 10.00m AUD per leg.

Spot 0.66000. Legs: long call K=0.69235, short put K=0.63120. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: 0, Gamma: 0, Theta: 0, Vega: 0**
- *Written*: How do your exposures change if time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **0** (0 AUD, base notional)
- Gamma: **0** (+40.9k AUD, delta change per 1% spot)
- Theta: **0** (+13 USD, P&L per day)
- Vega: **0** (-1.74e-09 USD, P&L per vol pt)

**Intuition for the structure:** Long OTM call, short OTM put: a directional, skew trade. Delta is long, gamma and vega roughly cancel, and vanna is strongly positive (you are long the call wing's vol versus the put wing's). The spot hedge sets delta to zero but leaves every other Greek unchanged.

**After the shock (time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged):**
- delta flips from flat (0 AUD) to short (-5.00m AUD). Charm: OTM deltas decay towards 0 and ITM deltas grow towards 100 as time passes.
- gamma flips from long (+40.9k AUD) to short (-1.2k AUD). As expiry approaches, gamma at strikes near spot grows (~1/sqrt(T)) while gamma at strikes away from spot (ITM or OTM) collapses.
- long theta: +13 USD to +3 USD (less long). Theta at strikes near spot grows as expiry approaches; theta of options far from the strike (ITM or OTM) fades, and deep ITM options can even earn carry.
- short vega: -1.74e-09 USD to -0.66 USD (more short). Vega falls with sqrt(T): less time left means less exposure to vol.

**P&L from the shock:** +11.3k USD by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol 0, theta +11.3k. The biggest driver is **theta**.

**Where the risk sits now:** short delta (50% of notional).

</details>

**Q3** (`exposures_L2`, topic `exposures:butterfly`, seed 1120205)

You are **short a 1W USDCAD 25-delta call butterfly (1x2x1), delta-hedged**, notional 25.00m USD per leg.

Spot 1.39000. Legs: low wing K=1.38314, body x2 K=1.38961, high wing K=1.39636. Convention: Spot delta, premium-adjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot rallies 0.8% (vol surface sticky by strike)**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: 0, Gamma: +, Theta: -, Vega: +**
- *Written*: How do your exposures change if spot rallies 0.8% (vol surface sticky by strike)? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **0** (+30.8k USD, base notional, premium-adjusted)
- Gamma: **+** (+6.26m USD, delta change per 1% spot)
- Theta: **-** (-2.6k CAD, P&L per day)
- Vega: **+** (+7.8k CAD, P&L per vol pt)

**Intuition for the structure:** Long the wings, short 2x the body: you are short gamma and vega near the body strike and collect theta; you want spot to pin near the body. You are SHORT the structure, so flip every sign. The spot hedge sets delta to zero but leaves every other Greek unchanged.

**After the shock (spot rallies 0.8% (vol surface sticky by strike)):**
- long delta: +30.8k USD to +2.83m USD (more long). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite.
- gamma flips from long (+6.26m USD) to short (-620.3k USD). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk.
- theta flips from short (-2.6k CAD) to long (+865 CAD). Theta mirrors gamma: it is largest near the strikes.
- vega flips from long (+7.8k CAD) to short (-1.4k CAD). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes.

**P&L from the shock:** +21.2k CAD by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot +21.2k, vega/vol 0, theta 0. The biggest driver is **gamma**.

**Where the risk sits now:** the position is close to flat on the main Greeks.

</details>

**Q4** (`exposures_L2`, topic `exposures:ratio_spread`, seed 1120236)

You are **short a 1W EURUSD 1x2 call ratio spread (long ATM, short 2x 25d)**, notional 10.00m EUR per leg.

Spot 1.16000. Legs: long 1x ATM call K=1.16041, short 2x OTM call K=1.16798. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **implied vol is crushed 2.1 vol points across the surface**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: 0, Gamma: +, Theta: -, Vega: +**
- *Written*: How do your exposures change if implied vol is crushed 2.1 vol points across the surface? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **0** (+1.9k EUR, base notional)
- Gamma: **+** (+2.36m EUR, delta change per 1% spot)
- Theta: **-** (-2.0k USD, P&L per day)
- Vega: **+** (+3.8k USD, P&L per vol pt)

**Intuition for the structure:** Long 1 ATM call, short 2 OTM calls: near the ATM strike you are long gamma, but the extra short OTM calls make you short vega and short gamma as spot rallies towards them. You are SHORT the structure, so flip every sign.

**After the shock (implied vol is crushed 2.1 vol points across the surface):**
- delta flips from long (+1.9k EUR) to short (-1.66m EUR). Vol down pushes deltas away from 50: OTM deltas shrink, ITM deltas grow.
- long gamma: +2.36m EUR to +1.28m EUR (less long). Lower vol concentrates gamma near the strikes: ATM gamma rises, far-strike gamma falls.
- short theta: -2.0k USD to -548 USD (less short). Theta scales with vol, so time decay shrinks.
- long vega: +3.8k USD to +1.6k USD (less long). ATM vega barely changes; wing vega falls (positive volga in the wings).

**P&L from the shock:** -6.0k USD by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol -6.0k, theta 0. The biggest driver is **vega**.

**Where the risk sits now:** long gamma (~0.3x a single ATM option); long vega (~0.3x a single ATM option); short delta (17% of notional).

</details>

**Q5** (`exposures_L2`, topic `exposures:straddle`, seed 1120267)

You are **long a 6M USDJPY ATM straddle**, notional 10.00m USD per leg.

Spot 152.000. Legs: ATM call K=149.460, ATM put K=149.460. Convention: Spot delta, premium-adjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot rallies 6.0% (vol surface sticky by strike)**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: 0, Gamma: +, Theta: -, Vega: +**
- *Written*: How do your exposures change if spot rallies 6.0% (vol surface sticky by strike)? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **0** (-2.03e-05 USD, base notional, premium-adjusted)
- Gamma: **+** (+1.08m USD, delta change per 1% spot)
- Theta: **-** (-226.3k JPY, P&L per day)
- Vega: **+** (+8.40m JPY, P&L per vol pt)

**Intuition for the structure:** ATM call + ATM put: delta-neutral at the DNS strike, maximum gamma and vega for the premium, and the biggest theta bill.

**After the shock (spot rallies 6.0% (vol surface sticky by strike)):**
- delta flips from short (-2.03e-05 USD) to long (+5.37m USD). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite.
- long gamma: +1.08m USD to +737.7k USD (less long). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk.
- short theta: -226.3k JPY to -90.2k JPY (less short). Theta mirrors gamma: it is largest near the strikes.
- long vega: +8.40m JPY to +6.06m JPY (less long). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes.

**P&L from the shock:** +32.22m JPY by full revaluation. Breakdown (spot, then vol, then time): delta +5.15m, gamma and higher-order spot +27.07m, vega/vol 0, theta 0. The biggest driver is **gamma**.

**Where the risk sits now:** long gamma (~1.4x a single ATM option); long vega (~1.4x a single ATM option); long delta (~0.5x a single ATM option).

</details>

**Q6** (`exposures_L2`, topic `exposures:straddle`, seed 1120298)

You are **long a 3M EURUSD ATM straddle**, notional 10.00m EUR per leg.

Spot 1.16000. Legs: ATM call K=1.16543, ATM put K=1.16543. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **the term structure inverts: front-end vols rise ~2.6 pts, 1Y falls ~1.3 pts**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: 0, Gamma: +, Theta: -, Vega: +**
- *Written*: How do your exposures change if the term structure inverts: front-end vols rise ~2.6 pts, 1Y falls ~1.3 pts? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **0** (+0.000161 EUR, base notional)
- Gamma: **+** (+2.18m EUR, delta change per 1% spot)
- Theta: **-** (-1.8k USD, P&L per day)
- Vega: **+** (+46.0k USD, P&L per vol pt)

**Intuition for the structure:** ATM call + ATM put: delta-neutral at the DNS strike, maximum gamma and vega for the premium, and the biggest theta bill.

**After the shock (the term structure inverts: front-end vols rise ~2.6 pts, 1Y falls ~1.3 pts):**
- delta flips from long (+0.000161 EUR) to short (-15.7k EUR). Deltas shift via vanna, in different directions for the front and back legs.
- long gamma: +2.18m EUR to +2.30m EUR (more long). Front-end vols up and back-end down: short-dated gamma falls, longer-dated gamma rises slightly.
- short theta: -1.8k USD to -1.7k USD (less short). Front-end theta grows with the higher front vol; back-end theta shrinks.
- long vega: +46.0k USD to +46.0k USD (roughly unchanged). Vega per tenor bucket now matters: the front-end legs gained vol, the back-end legs lost vol.

**P&L from the shock:** -17.7k USD by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol -17.7k, theta 0. The biggest driver is **vega**.

**Where the risk sits now:** long gamma (~2.1x a single ATM option); long vega (~2.0x a single ATM option).

</details>

**Q7** (`exposures_L2`, topic `exposures:risk_reversal`, seed 1120329)

You are **short a 1M NZDUSD 25-delta risk reversal (call over put)**, notional 50.00m NZD per leg.

Spot 0.58000. Legs: long call K=0.59167, short put K=0.56943. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **15 days pass with spot and vols unchanged**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: -, Gamma: 0, Theta: 0, Vega: 0**
- *Written*: How do your exposures change if 15 days pass with spot and vols unchanged? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **-** (-25.00m NZD, base notional)
- Gamma: **0** (-325.7k NZD, delta change per 1% spot)
- Theta: **0** (+186 USD, P&L per day)
- Vega: **0** (+5.46e-09 USD, P&L per vol pt)

**Intuition for the structure:** Long OTM call, short OTM put: a directional, skew trade. Delta is long, gamma and vega roughly cancel, and vanna is strongly positive (you are long the call wing's vol versus the put wing's). You are SHORT the structure, so flip every sign.

**After the shock (15 days pass with spot and vols unchanged):**
- short delta: -25.00m NZD to -17.12m NZD (less short). Charm: OTM deltas decay towards 0 and ITM deltas grow towards 100 as time passes.
- gamma flips from short (-325.7k NZD) to long (+14.0k NZD). As expiry approaches, gamma at strikes near spot grows (~1/sqrt(T)) while gamma at strikes away from spot (ITM or OTM) collapses.
- theta flips from long (+186 USD) to short (-345 USD). Theta at strikes near spot grows as expiry approaches; theta of options far from the strike (ITM or OTM) fades, and deep ITM options can even earn carry.
- long vega: +5.46e-09 USD to +1.0k USD (more long). Vega falls with sqrt(T): less time left means less exposure to vol.

**P&L from the shock:** +981 USD by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol 0, theta +981. The biggest driver is **theta**.

**Where the risk sits now:** short delta (34% of notional).

</details>

**Q8** (`exposures_L2`, topic `exposures:straddle`, seed 1120360)

You are **long a 1Y EURUSD ATM straddle**, notional 25.00m EUR per leg.

Spot 1.16000. Legs: ATM call K=1.18221, ATM put K=1.18221. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **182 days pass with spot and vols unchanged**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: 0, Gamma: +, Theta: -, Vega: +**
- *Written*: How do your exposures change if 182 days pass with spot and vols unchanged? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **0** (+4.11e-05 EUR, base notional)
- Gamma: **+** (+2.54m EUR, delta change per 1% spot)
- Theta: **-** (-2.2k USD, P&L per day)
- Vega: **+** (+226.8k USD, P&L per vol pt)

**Intuition for the structure:** ATM call + ATM put: delta-neutral at the DNS strike, maximum gamma and vega for the premium, and the biggest theta bill.

**After the shock (182 days pass with spot and vols unchanged):**
- delta flips from long (+4.11e-05 EUR) to short (-3.49m EUR). Charm: OTM deltas decay towards 0 and ITM deltas grow towards 100 as time passes.
- long gamma: +2.54m EUR to +3.63m EUR (more long). As expiry approaches, gamma at strikes near spot grows (~1/sqrt(T)) while gamma at strikes away from spot (ITM or OTM) collapses.
- short theta: -2.2k USD to -3.0k USD (more short). Theta at strikes near spot grows as expiry approaches; theta of options far from the strike (ITM or OTM) fades, and deep ITM options can even earn carry.
- long vega: +226.8k USD to +159.7k USD (less long). Vega falls with sqrt(T): less time left means less exposure to vol.

**P&L from the shock:** -491.6k USD by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol 0, theta -491.6k. The biggest driver is **theta**.

**Where the risk sits now:** long gamma (~2.9x a single ATM option); long vega (~1.4x a single ATM option).

</details>

**Q9** (`exposures_L2`, topic `exposures:ratio_spread`, seed 1120391)

You are **short a 1M SPX 1x2 call ratio spread (long ATM, short 2x 25d), delta-hedged**, notional $1.0k units per leg.

Spot 6,000. Legs: long 1x ATM call K=6018, short 2x OTM call K=6195. Convention: Black-Scholes, ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **the term structure inverts: front-end vols rise ~3.5 pts, 1Y falls ~1.8 pts**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: 0, Gamma: +, Theta: -, Vega: +**
- *Written*: How do your exposures change if the term structure inverts: front-end vols rise ~3.5 pts, 1Y falls ~1.8 pts? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **0** (0 units, base notional)
- Gamma: **+** (+61 units, delta change per 1% spot)
- Theta: **-** (-896 USD, P&L per day)
- Vega: **+** (+4.1k USD, P&L per vol pt)

**Intuition for the structure:** Long 1 ATM call, short 2 OTM calls: near the ATM strike you are long gamma, but the extra short OTM calls make you short vega and short gamma as spot rallies towards them. You are SHORT the structure, so flip every sign. The spot hedge sets delta to zero but leaves every other Greek unchanged.

**After the shock (the term structure inverts: front-end vols rise ~3.5 pts, 1Y falls ~1.8 pts):**
- delta flips from flat (0 units) to long (+13 units). Deltas shift via vanna, in different directions for the front and back legs.
- long gamma: +61 units to +61 units (roughly unchanged). Front-end vols up and back-end down: short-dated gamma falls, longer-dated gamma rises slightly.
- short theta: -896 USD to -972 USD (more short). Front-end theta grows with the higher front vol; back-end theta shrinks.
- long vega: +4.1k USD to +4.3k USD (more long). Vega per tenor bucket now matters: the front-end legs gained vol, the back-end legs lost vol.

**P&L from the shock:** +1.9k USD by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol +1.9k, theta 0. The biggest driver is **vega**.

**Where the risk sits now:** long gamma (~0.7x a single ATM option); long vega (~0.6x a single ATM option).

</details>

**Q10** (`exposures_L2`, topic `exposures:calendar`, seed 1120422)

You are **short a 1W USDJPY ATM call calendar (short near, long 3M)**, notional 25.00m USD per leg.

Spot 152.000. Legs: short near call K=151.904, long far call K=151.904. Convention: Spot delta, premium-adjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot rallies 1.3% (vol surface sticky by strike)**, and what it does to your P&L.

- *Exposure signs before the shock*: **Delta: 0, Gamma: +, Theta: -, Vega: -**
- *Written*: How do your exposures change if spot rallies 1.3% (vol surface sticky by strike)? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **0** (+1.57m USD, base notional, premium-adjusted)
- Gamma: **+** (+5.74m USD, delta change per 1% spot)
- Theta: **-** (-976.3k JPY, P&L per day)
- Vega: **-** (-5.37m JPY, P&L per vol pt)

**Intuition for the structure:** Short the near expiry, long the far expiry at the same strike: short gamma (the near leg dominates gamma), long vega (the far leg dominates vega), and you earn theta. You are SHORT the structure, so flip every sign.

**After the shock (spot rallies 1.3% (vol surface sticky by strike)):**
- long delta: +1.57m USD to +7.42m USD (more long). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite.
- long gamma: +5.74m USD to +2.64m USD (less long). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk.
- short theta: -976.3k JPY to -351.4k JPY (less short). Theta mirrors gamma: it is largest near the strikes.
- short vega: -5.37m JPY to -6.25m JPY (more short). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes.

**P&L from the shock:** +9.09m JPY by full revaluation. Breakdown (spot, then vol, then time): delta +2.55m, gamma and higher-order spot +6.54m, vega/vol 0, theta 0. The biggest driver is **gamma**.

**Where the risk sits now:** long gamma (~0.3x a single ATM option); short vega (~3.0x a single ATM option); long delta (~0.3x a single ATM option).

</details>

### Level 3: calculations plus subtler concepts

**Q1** (`exposures_L3`, topic `exposures:collar`, seed 1224872)

You are **short a 1M EURJPY collar (long spot, long 25d put, short 25d call)**, notional 25.00m EUR per leg.

Spot 176.320. Legs: long put K=172.607, short call K=179.311. Convention: Spot delta, premium-adjusted (premium in EUR); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot rallies 1.7% (vol surface sticky by strike), and implied vol spikes 6.4 vol points across the surface**, and what it does to your P&L.

3. Using only the Greeks in the Givens box, estimate the instant P&L if spot moves **-1.0%** and vols move **-2.0 pts** in parallel.

Givens:

| Given | Value |
|---|---|
| Spot | 176.32 |
| Delta (EUR, unadjusted spot delta) | -12,511,756 |
| Gamma (EUR delta change per 1% spot) | 409,388 |
| Vega (JPY per vol pt) | 72,390 |
| Spot move (%) | -1 |
| Vol move (pts, parallel) | -2 |

- *Exposure signs before the shock*: **Delta: -, Gamma: +/0, Theta: +, Vega: 0, Vanna: +, Volga: +/0, Charm: -**
- *Estimated instant P&L (JPY) for spot -1.0% and vol -2.0 pts*: **22,276,865**
- *Written*: How do your exposures change if spot rallies 1.7% (vol surface sticky by strike), and implied vol spikes 6.4 vol points across the surface? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **-** (-12.50m EUR, base notional, premium-adjusted)
- Gamma: **+** (+409.4k EUR, delta change per 1% spot)
- Theta: **+** (+146.7k JPY, P&L per day)
- Vega: **0** (+72.4k JPY, P&L per vol pt)
- Vanna: **+** (+1.09m EUR, delta change per vol pt)
- Volga: **+** (+28.2k JPY, vega change per vol pt)
- Charm: **-** (-173.3k EUR, delta change per day)

**Intuition for the structure:** Long spot, long put, short call: a hedged long position. Delta stays positive (spot leg minus option deltas), gamma and vega are modest and depend on which strike spot is nearer. You are SHORT the structure, so flip every sign.

**After the shock (spot rallies 1.7% (vol surface sticky by strike), and implied vol spikes 6.4 vol points across the surface):**
- short delta: -12.50m EUR to -7.43m EUR (less short). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite. Vol up pulls every strike's delta towards 50 (vanna): OTM deltas grow, ITM deltas shrink.
- long gamma: +409.4k EUR to +711.3k EUR (more long). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk. Higher vol spreads gamma over a wider range of spot: gamma near the strikes falls (ATM gamma ~ 1/vol) and gamma at far strikes rises.
- theta flips from long (+146.7k JPY) to short (-163.8k JPY). Theta mirrors gamma: it is largest near the strikes. ATM theta scales roughly with vol, so the daily decay (paid or received) grows.
- long vega: +72.4k JPY to +1.38m JPY (more long). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes. ATM vega barely moves with the vol level (volga ~ 0 ATM); wing vega rises (positive volga). Long-wing structures gain vega.
- long vanna: +1.09m EUR to +349.3k EUR (less long)
- volga flips from long (+28.2k JPY) to short (-130.8k JPY)
- short charm: -173.3k EUR to -92.6k EUR (less short)

**P&L from the shock:** -22.10m JPY by full revaluation. Breakdown (spot, then vol, then time): delta -37.50m, gamma and higher-order spot +2.82m, vega/vol +12.59m, theta 0. The biggest driver is **delta**.

**Where the risk sits now:** long gamma (~0.2x a single ATM option); long vega (~0.3x a single ATM option); short delta (~0.3x a single ATM option).

**P&L estimate (part 3): +22.28m JPY.**
- Delta: -12,511,756 x dS (-1.7632) = 22,060,728
- Gamma: 0.5 x 409,388 x -1.0 x dS = 360,916
- Vega: 72,390 x -2.0 = -144,780
- Engine full revaluation: +26.29m JPY. The gap (+4.01m) is vanna (spot and vol moving together), volga, and gamma changing over the move (speed), which is large for short-dated options near their strikes.

</details>

**Q2** (`exposures_L3`, topic `exposures:collar`, seed 1224903)

You are **short a 1W EURUSD collar (long spot, long 25d put, short 25d call)**, notional 10.00m EUR per leg.

Spot 1.16000. Legs: long put K=1.15300, short call K=1.16798. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot rallies 0.9% (vol surface sticky by strike), and the term structure inverts: front-end vols rise ~2.6 pts, 1Y falls ~1.3 pts**, and what it does to your P&L.

3. Using only the Greeks in the Givens box, estimate the instant P&L if spot moves **+1.0%** and vols move **+1.0 pts** in parallel.

Givens:

| Given | Value |
|---|---|
| Spot | 1.16 |
| Delta (EUR, unadjusted spot delta) | -5,000,000 |
| Gamma (EUR delta change per 1% spot) | -46,233 |
| Vega (USD per vol pt) | 0 |
| Spot move (%) | 1 |
| Vol move (pts, parallel) | 1 |

- *Exposure signs before the shock*: **Delta: -, Gamma: 0, Theta: 0, Vega: 0, Vanna: +, Volga: 0, Charm: -**
- *Estimated instant P&L (USD) for spot +1.0% and vol +1.0 pts*: **-58,268**
- *Written*: How do your exposures change if spot rallies 0.9% (vol surface sticky by strike), and the term structure inverts: front-end vols rise ~2.6 pts, 1Y falls ~1.3 pts? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **-** (-5.00m EUR, base notional)
- Gamma: **0** (-46.2k EUR, delta change per 1% spot)
- Theta: **0** (-289 USD, P&L per day)
- Vega: **0** (+1.73e-09 USD, P&L per vol pt)
- Vanna: **+** (+619.8k EUR, delta change per vol pt)
- Volga: **0** (+5 USD, vega change per vol pt)
- Charm: **-** (-305.6k EUR, delta change per day)

**Intuition for the structure:** Long spot, long put, short call: a hedged long position. Delta stays positive (spot leg minus option deltas), gamma and vega are modest and depend on which strike spot is nearer. You are SHORT the structure, so flip every sign.

**After the shock (spot rallies 0.9% (vol surface sticky by strike), and the term structure inverts: front-end vols rise ~2.6 pts, 1Y falls ~1.3 pts):**
- short delta: -5.00m EUR to -3.27m EUR (less short). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite. Deltas shift via vanna, in different directions for the front and back legs.
- gamma flips from short (-46.2k EUR) to long (+2.00m EUR). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk. Front-end vols up and back-end down: short-dated gamma falls, longer-dated gamma rises slightly.
- short theta: -289 USD to -2.6k USD (more short). Theta mirrors gamma: it is largest near the strikes. Front-end theta grows with the higher front vol; back-end theta shrinks.
- long vega: +1.73e-09 USD to +3.7k USD (more long). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes. Vega per tenor bucket now matters: the front-end legs gained vol, the back-end legs lost vol.
- long vanna: +619.8k EUR to +164.5k EUR (less long)
- volga flips from long (+5 USD) to short (-541 USD)
- short charm: -305.6k EUR to -103.8k EUR (less short)

**P&L from the shock:** -41.1k USD by full revaluation. Breakdown (spot, then vol, then time): delta -52.2k, gamma and higher-order spot +5.7k, vega/vol +5.4k, theta 0. The biggest driver is **delta**.

**Where the risk sits now:** long gamma (~0.5x a single ATM option); long vega (~0.6x a single ATM option); short delta (33% of notional).

**P&L estimate (part 3): -58.3k USD.**
- Delta: -5,000,000 x dS (+0.0116) = -58,000
- Gamma: 0.5 x -46,233 x 1.0 x dS = -268
- Vega: 0 x 1.0 = 0
- Engine full revaluation: -46.0k USD. The gap (+12.2k) is vanna (spot and vol moving together), volga, and gamma changing over the move (speed), which is large for short-dated options near their strikes.

</details>

**Q3** (`exposures_L3`, topic `exposures:risk_reversal`, seed 1224934)

You are **short a 6M EURUSD 25-delta risk reversal (call over put)**, notional 10.00m EUR per leg.

Spot 1.16000. Legs: long call K=1.21537, short put K=1.13011. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **91 days pass with spot and vols unchanged, and implied vol is crushed 1.1 vol points across the surface**, and what it does to your P&L.

3. Using only the Greeks in the Givens box, estimate the instant P&L if spot moves **-0.5%** and vols move **+2.0 pts** in parallel.

Givens:

| Given | Value |
|---|---|
| Spot | 1.16 |
| Delta (EUR, unadjusted spot delta) | -5,000,000 |
| Gamma (EUR delta change per 1% spot) | 24,917 |
| Vega (USD per vol pt) | 0 |
| Spot move (%) | -0.5 |
| Vol move (pts, parallel) | 2 |

- *Exposure signs before the shock*: **Delta: -, Gamma: 0, Theta: +, Vega: 0, Vanna: -, Volga: -/0, Charm: +**
- *Estimated instant P&L (USD) for spot -0.5% and vol +2.0 pts*: **29,036**
- *Written*: How do your exposures change if 91 days pass with spot and vols unchanged, and implied vol is crushed 1.1 vol points across the surface? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **-** (-5.00m EUR, base notional)
- Gamma: **0** (+24.9k EUR, delta change per 1% spot)
- Theta: **+** (+278 USD, P&L per day)
- Vega: **0** (-1.69e-09 USD, P&L per vol pt)
- Vanna: **-** (-547.8k EUR, delta change per vol pt)
- Volga: **-** (-180 USD, vega change per vol pt)
- Charm: **+** (+11.2k EUR, delta change per day)

**Intuition for the structure:** Long OTM call, short OTM put: a directional, skew trade. Delta is long, gamma and vega roughly cancel, and vanna is strongly positive (you are long the call wing's vol versus the put wing's). You are SHORT the structure, so flip every sign.

**After the shock (91 days pass with spot and vols unchanged, and implied vol is crushed 1.1 vol points across the surface):**
- short delta: -5.00m EUR to -2.75m EUR (less short). Charm: OTM deltas decay towards 0 and ITM deltas grow towards 100 as time passes. Vol down pushes deltas away from 50: OTM deltas shrink, ITM deltas grow.
- long gamma: +24.9k EUR to +239.0k EUR (more long). As expiry approaches, gamma at strikes near spot grows (~1/sqrt(T)) while gamma at strikes away from spot (ITM or OTM) collapses. Lower vol concentrates gamma near the strikes: ATM gamma rises, far-strike gamma falls.
- long theta: +278 USD to +56 USD (less long). Theta at strikes near spot grows as expiry approaches; theta of options far from the strike (ITM or OTM) fades, and deep ITM options can even earn carry. Theta scales with vol, so time decay shrinks.
- vega flips from short (-1.69e-09 USD) to long (+3.5k USD). Vega falls with sqrt(T): less time left means less exposure to vol. ATM vega barely changes; wing vega falls (positive volga in the wings).
- short vanna: -547.8k EUR to -714.0k EUR (more short)
- short volga: -180 USD to -359 USD (more short)
- long charm: +11.2k EUR to +24.4k EUR (more long)

**P&L from the shock:** +10.4k USD by full revaluation. Breakdown (spot, then vol, then time): delta 0, gamma and higher-order spot 0, vega/vol -114, theta +10.5k. The biggest driver is **theta**.

**Where the risk sits now:** long gamma (~0.3x a single ATM option); short delta (27% of notional).

**P&L estimate (part 3): +29.0k USD.**
- Delta: -5,000,000 x dS (-0.0058) = 29,000
- Gamma: 0.5 x 24,917 x -0.5 x dS = 36
- Vega: -0 x 2.0 = -0
- Engine full revaluation: +34.0k USD. The gap (+4.9k) is vanna (spot and vol moving together), volga, and gamma changing over the move (speed), which is large for short-dated options near their strikes.

</details>

**Q4** (`exposures_L3`, topic `exposures:collar`, seed 1224965)

You are **short a 1W NZDUSD collar (long spot, long 25d put, short 25d call)**, notional 10.00m NZD per leg.

Spot 0.58000. Legs: long put K=0.57491, short call K=0.58525. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot rallies 1.1% (vol surface sticky by strike), and implied vol spikes 2.7 vol points across the surface**, and what it does to your P&L.

3. Using only the Greeks in the Givens box, estimate the instant P&L if spot moves **-1.0%** and vols move **+1.0 pts** in parallel.

Givens:

| Given | Value |
|---|---|
| Spot | 0.58 |
| Delta (NZD, unadjusted spot delta) | -5,000,000 |
| Gamma (NZD delta change per 1% spot) | 109,279 |
| Vega (USD per vol pt) | 0 |
| Spot move (%) | -1 |
| Vol move (pts, parallel) | 1 |

- *Exposure signs before the shock*: **Delta: -, Gamma: 0, Theta: 0, Vega: 0, Vanna: +, Volga: 0, Charm: -**
- *Estimated instant P&L (USD) for spot -1.0% and vol +1.0 pts*: **29,317**
- *Written*: How do your exposures change if spot rallies 1.1% (vol surface sticky by strike), and implied vol spikes 2.7 vol points across the surface? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **-** (-5.00m NZD, base notional)
- Gamma: **0** (+109.3k NZD, delta change per 1% spot)
- Theta: **0** (-8 USD, P&L per day)
- Vega: **0** (-1.92e-09 USD, P&L per vol pt)
- Vanna: **+** (+448.8k NZD, delta change per vol pt)
- Volga: **0** (+10 USD, vega change per vol pt)
- Charm: **-** (-305.8k NZD, delta change per day)

**Intuition for the structure:** Long spot, long put, short call: a hedged long position. Delta stays positive (spot leg minus option deltas), gamma and vega are modest and depend on which strike spot is nearer. You are SHORT the structure, so flip every sign.

**After the shock (spot rallies 1.1% (vol surface sticky by strike), and implied vol spikes 2.7 vol points across the surface):**
- short delta: -5.00m NZD to -3.24m NZD (less short). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite. Vol up pulls every strike's delta towards 50 (vanna): OTM deltas grow, ITM deltas shrink.
- long gamma: +109.3k NZD to +1.20m NZD (more long). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk. Higher vol spreads gamma over a wider range of spot: gamma near the strikes falls (ATM gamma ~ 1/vol) and gamma at far strikes rises.
- short theta: -8 USD to -1.4k USD (more short). Theta mirrors gamma: it is largest near the strikes. ATM theta scales roughly with vol, so the daily decay (paid or received) grows.
- vega flips from short (-1.92e-09 USD) to long (+1.6k USD). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes. ATM vega barely moves with the vol level (volga ~ 0 ATM); wing vega rises (positive volga). Long-wing structures gain vega.
- long vanna: +448.8k NZD to +146.7k NZD (less long)
- volga flips from long (+10 USD) to short (-172 USD)
- short charm: -305.8k NZD to -135.0k NZD (less short)

**P&L from the shock:** -23.8k USD by full revaluation. Breakdown (spot, then vol, then time): delta -31.9k, gamma and higher-order spot +3.2k, vega/vol +4.9k, theta 0. The biggest driver is **delta**.

**Where the risk sits now:** long gamma (~0.4x a single ATM option); long vega (~0.5x a single ATM option); short delta (32% of notional).

**P&L estimate (part 3): +29.3k USD.**
- Delta: -5,000,000 x dS (-0.0058) = 29,000
- Gamma: 0.5 x 109,279 x -1.0 x dS = 317
- Vega: -0 x 1.0 = -0
- Engine full revaluation: +25.1k USD. The gap (-4.2k) is vanna (spot and vol moving together), volga, and gamma changing over the move (speed), which is large for short-dated options near their strikes.

</details>

**Q5** (`exposures_L3`, topic `exposures:collar`, seed 1224996)

You are **short a 1M USDCHF collar (long spot, long 25d put, short 25d call)**, notional 25.00m USD per leg.

Spot 0.80000. Legs: long put K=0.78557, short call K=0.80894. Convention: Spot delta, premium-adjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot rallies 1.7% (vol surface sticky by strike), and implied vol spikes 2.5 vol points across the surface**, and what it does to your P&L.

3. Using only the Greeks in the Givens box, estimate the instant P&L if spot moves **-1.0%** and vols move **+2.0 pts** in parallel.

Givens:

| Given | Value |
|---|---|
| Spot | 0.8 |
| Delta (USD, unadjusted spot delta) | -12,505,210 |
| Gamma (USD delta change per 1% spot) | 328,916 |
| Vega (CHF per vol pt) | 253 |
| Spot move (%) | -1 |
| Vol move (pts, parallel) | 2 |

- *Exposure signs before the shock*: **Delta: -, Gamma: 0, Theta: +, Vega: 0, Vanna: +, Volga: 0, Charm: -**
- *Estimated instant P&L (CHF) for spot -1.0% and vol +2.0 pts*: **101,863**
- *Written*: How do your exposures change if spot rallies 1.7% (vol surface sticky by strike), and implied vol spikes 2.5 vol points across the surface? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **-** (-12.50m USD, base notional, premium-adjusted)
- Gamma: **0** (+328.9k USD, delta change per 1% spot)
- Theta: **+** (+1.1k CHF, P&L per day)
- Vega: **0** (+253 CHF, P&L per vol pt)
- Vanna: **+** (+1.41m USD, delta change per vol pt)
- Volga: **0** (+103 CHF, vega change per vol pt)
- Charm: **-** (-170.7k USD, delta change per day)

**Intuition for the structure:** Long spot, long put, short call: a hedged long position. Delta stays positive (spot leg minus option deltas), gamma and vega are modest and depend on which strike spot is nearer. You are SHORT the structure, so flip every sign.

**After the shock (spot rallies 1.7% (vol surface sticky by strike), and implied vol spikes 2.5 vol points across the surface):**
- short delta: -12.50m USD to -8.25m USD (less short). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite. Vol up pulls every strike's delta towards 50 (vanna): OTM deltas grow, ITM deltas shrink.
- long gamma: +328.9k USD to +1.66m USD (more long). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk. Higher vol spreads gamma over a wider range of spot: gamma near the strikes falls (ATM gamma ~ 1/vol) and gamma at far strikes rises.
- theta flips from long (+1.1k CHF) to short (-165 CHF). Theta mirrors gamma: it is largest near the strikes. ATM theta scales roughly with vol, so the daily decay (paid or received) grows.
- long vega: +253 CHF to +10.3k CHF (more long). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes. ATM vega barely moves with the vol level (volga ~ 0 ATM); wing vega rises (positive volga). Long-wing structures gain vega.
- long vanna: +1.41m USD to +478.4k USD (less long)
- volga flips from long (+103 CHF) to short (-1.4k CHF)
- short charm: -170.7k USD to -64.1k USD (less short)

**P&L from the shock:** -122.2k CHF by full revaluation. Breakdown (spot, then vol, then time): delta -170.1k, gamma and higher-order spot +17.0k, vega/vol +30.9k, theta 0. The biggest driver is **delta**.

**Where the risk sits now:** long gamma (~0.4x a single ATM option); long vega (~0.4x a single ATM option); short delta (~0.3x a single ATM option).

**P&L estimate (part 3): +101.9k CHF.**
- Delta: -12,505,210 x dS (-0.008) = 100,042
- Gamma: 0.5 x 328,916 x -1.0 x dS = 1,316
- Vega: 253 x 2.0 = 506
- Engine full revaluation: +81.4k CHF. The gap (-20.5k) is vanna (spot and vol moving together), volga, and gamma changing over the move (speed), which is large for short-dated options near their strikes.

</details>

**Q6** (`exposures_L3`, topic `exposures:call`, seed 1225027)

You are **long a 1W USDJPY ATM call**, notional 10.00m USD per leg.

Spot 152.000. Legs: call K=151.904. Convention: Spot delta, premium-adjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot sells off 0.8% (vol surface sticky by strike), and the skew steepens: 25d risk reversals move 1.5 vols further towards puts**, and what it does to your P&L.

3. Using only the Greeks in the Givens box, estimate the instant P&L if spot moves **+1.5%** and vols move **-2.0 pts** in parallel.

Givens:

| Given | Value |
|---|---|
| Spot | 152 |
| Delta (USD, unadjusted spot delta) | 5,047,892 |
| Gamma (USD delta change per 1% spot) | 3,095,200 |
| Vega (JPY per vol pt) | 839,113 |
| Spot move (%) | 1.5 |
| Vol move (pts, parallel) | -2 |

- *Exposure signs before the shock*: **Delta: +, Gamma: +, Theta: -, Vega: +, Vanna: 0, Volga: 0, Charm: +/0**
- *Estimated instant P&L (JPY) for spot +1.5% and vol -2.0 pts*: **15,123,760**
- *Written*: How do your exposures change if spot sells off 0.8% (vol surface sticky by strike), and the skew steepens: 25d risk reversals move 1.5 vols further towards puts? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **+** (+5.00m USD, base notional, premium-adjusted)
- Gamma: **+** (+3.10m USD, delta change per 1% spot)
- Theta: **-** (-497.3k JPY, P&L per day)
- Vega: **+** (+839.1k JPY, P&L per vol pt)
- Vanna: **0** (+1.94e-06 USD, delta change per vol pt)
- Volga: **0** (-5.27e-09 JPY, vega change per vol pt)
- Charm: **+** (+24.7k USD, delta change per day)

**Intuition for the structure:** A vanilla is long gamma, long vega and pays theta when bought; delta is positive for a call.

**After the shock (spot sells off 0.8% (vol surface sticky by strike), and the skew steepens: 25d risk reversals move 1.5 vols further towards puts):**
- long delta: +5.00m USD to +2.52m USD (less long). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite. Each leg's delta moves via vanna and its own vol change: puts' deltas grow in size as their vols rise.
- long gamma: +3.10m USD to +2.69m USD (less long). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk. A skew move changes each strike's vol differently: low-strike vols rise, high-strike vols fall, so each leg's gamma moves the opposite way to its vol.
- short theta: -497.3k JPY to -381.8k JPY (less short). Theta mirrors gamma: it is largest near the strikes. Legs whose vol rose decay faster, legs whose vol fell decay slower.
- long vega: +839.1k JPY to +669.3k JPY (less long). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes. Each leg's vega responds to its own vol change via volga; wing legs are affected most.
- long vanna: +1.94e-06 USD to +250.2k USD (more long)
- volga flips from short (-5.27e-09 JPY) to long (+34.5k JPY)
- charm flips from long (+24.7k USD) to short (-132.7k USD)

**P&L from the shock:** -5.14m JPY by full revaluation. Breakdown (spot, then vol, then time): delta -6.14m, gamma and higher-order spot +1.47m, vega/vol -467.3k, theta 0. The biggest driver is **delta**.

**Where the risk sits now:** long gamma (~0.9x a single ATM option); long vega (~0.8x a single ATM option); long delta (~0.3x a single ATM option).

**P&L estimate (part 3): +15.12m JPY.**
- Delta: 5,047,892 x dS (+2.28) = 11,509,194
- Gamma: 0.5 x 3,095,200 x 1.5 x dS = 5,292,792
- Vega: 839,113 x -2.0 = -1,678,226
- Engine full revaluation: +15.52m JPY. The gap (+392.7k) is vanna (spot and vol moving together), volga, and gamma changing over the move (speed), which is large for short-dated options near their strikes.

</details>

**Q7** (`exposures_L3`, topic `exposures:ratio_spread`, seed 1225058)

You are **short a 1M AUDUSD 1x2 call ratio spread (long ATM, short 2x 25d)**, notional 25.00m AUD per leg.

Spot 0.66000. Legs: long 1x ATM call K=0.66038, short 2x OTM call K=0.67224. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot rallies 2.3% (vol surface sticky by strike), and the term structure inverts: front-end vols rise ~2.0 pts, 1Y falls ~1.0 pts**, and what it does to your P&L.

3. Using only the Greeks in the Givens box, estimate the instant P&L if spot moves **-0.5%** and vols move **+1.0 pts** in parallel.

Givens:

| Given | Value |
|---|---|
| Spot | 0.66 |
| Delta (AUD, unadjusted spot delta) | 34,847 |
| Gamma (AUD delta change per 1% spot) | 2,283,853 |
| Vega (USD per vol pt) | 11,283 |
| Spot move (%) | -0.5 |
| Vol move (pts, parallel) | 1 |

- *Exposure signs before the shock*: **Delta: 0, Gamma: +, Theta: -, Vega: +, Vanna: +, Volga: +, Charm: -**
- *Estimated instant P&L (USD) for spot -0.5% and vol +1.0 pts*: **13,052**
- *Written*: How do your exposures change if spot rallies 2.3% (vol surface sticky by strike), and the term structure inverts: front-end vols rise ~2.0 pts, 1Y falls ~1.0 pts? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **0** (+34.8k AUD, base notional)
- Gamma: **+** (+2.28m AUD, delta change per 1% spot)
- Theta: **-** (-1.7k USD, P&L per day)
- Vega: **+** (+11.3k USD, P&L per vol pt)
- Vanna: **+** (+1.18m AUD, delta change per vol pt)
- Volga: **+** (+1.5k USD, vega change per vol pt)
- Charm: **-** (-179.4k AUD, delta change per day)

**Intuition for the structure:** Long 1 ATM call, short 2 OTM calls: near the ATM strike you are long gamma, but the extra short OTM calls make you short vega and short gamma as spot rallies towards them. You are SHORT the structure, so flip every sign.

**After the shock (spot rallies 2.3% (vol surface sticky by strike), and the term structure inverts: front-end vols rise ~2.0 pts, 1Y falls ~1.0 pts):**
- long delta: +34.8k AUD to +8.70m AUD (more long). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite. Deltas shift via vanna, in different directions for the front and back legs.
- long gamma: +2.28m AUD to +4.61m AUD (more long). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk. Front-end vols up and back-end down: short-dated gamma falls, longer-dated gamma rises slightly.
- short theta: -1.7k USD to -3.8k USD (more short). Theta mirrors gamma: it is largest near the strikes. Front-end theta grows with the higher front vol; back-end theta shrinks.
- long vega: +11.3k USD to +24.3k USD (more long). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes. Vega per tenor bucket now matters: the front-end legs gained vol, the back-end legs lost vol.
- long vanna: +1.18m AUD to +270.4k AUD (less long)
- volga flips from long (+1.5k USD) to short (-835 USD)
- short charm: -179.4k AUD to -45.5k AUD (less short)

**P&L from the shock:** +65.0k USD by full revaluation. Breakdown (spot, then vol, then time): delta +529, gamma and higher-order spot +58.0k, vega/vol +6.4k, theta 0. The biggest driver is **gamma**.

**Where the risk sits now:** long gamma (~1.2x a single ATM option); long vega (~1.3x a single ATM option); long delta (35% of notional).

**P&L estimate (part 3): +13.1k USD.**
- Delta: 34,847 x dS (-0.0033) = -115
- Gamma: 0.5 x 2,283,853 x -0.5 x dS = 1,884
- Vega: 11,283 x 1.0 = 11,283
- Engine full revaluation: +10.0k USD. The gap (-3.0k) is vanna (spot and vol moving together), volga, and gamma changing over the move (speed), which is large for short-dated options near their strikes.

</details>

**Q8** (`exposures_L3`, topic `exposures:call_spread`, seed 1225089)

You are **short a 3M EURCHF ATM/25-delta call spread**, notional 10.00m EUR per leg.

Spot 0.92800. Legs: long ATM call K=0.92302, short OTM call K=0.93976. Convention: Spot delta, premium-adjusted (premium in EUR); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot sells off 2.9% (vol surface sticky by strike), and implied vol spikes 3.0 vol points across the surface**, and what it does to your P&L.

3. Using only the Greeks in the Givens box, estimate the instant P&L if spot moves **+1.0%** and vols move **+3.0 pts** in parallel.

Givens:

| Given | Value |
|---|---|
| Spot | 0.928 |
| Delta (EUR, unadjusted spot delta) | -2,544,764 |
| Gamma (EUR delta change per 1% spot) | -223,142 |
| Vega (CHF per vol pt) | -3,580 |
| Spot move (%) | 1 |
| Vol move (pts, parallel) | 3 |

- *Exposure signs before the shock*: **Delta: -, Gamma: -/0, Theta: 0, Vega: -/0, Vanna: +, Volga: +, Charm: -**
- *Estimated instant P&L (CHF) for spot +1.0% and vol +3.0 pts*: **-35,391**
- *Written*: How do your exposures change if spot sells off 2.9% (vol surface sticky by strike), and implied vol spikes 3.0 vol points across the surface? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **-** (-2.47m EUR, base notional, premium-adjusted)
- Gamma: **-** (-223.1k EUR, delta change per 1% spot)
- Theta: **0** (-0.476 CHF, P&L per day)
- Vega: **-** (-3.6k CHF, P&L per vol pt)
- Vanna: **+** (+417.4k EUR, delta change per vol pt)
- Volga: **+** (+1.3k CHF, vega change per vol pt)
- Charm: **-** (-13.3k EUR, delta change per day)

**Intuition for the structure:** Long ATM call, short OTM call: long delta with capped upside. Net long gamma/vega near the lower strike, flipping to short near the upper strike. You are SHORT the structure, so flip every sign.

**After the shock (spot sells off 2.9% (vol surface sticky by strike), and implied vol spikes 3.0 vol points across the surface):**
- short delta: -2.47m EUR to -1.18m EUR (less short). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite. Vol up pulls every strike's delta towards 50 (vanna): OTM deltas grow, ITM deltas shrink.
- short gamma: -223.1k EUR to -235.8k EUR (more short). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk. Higher vol spreads gamma over a wider range of spot: gamma near the strikes falls (ATM gamma ~ 1/vol) and gamma at far strikes rises.
- theta flips from short (-0.476 CHF) to long (+178 CHF). Theta mirrors gamma: it is largest near the strikes. ATM theta scales roughly with vol, so the daily decay (paid or received) grows.
- short vega: -3.6k CHF to -4.8k CHF (more short). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes. ATM vega barely moves with the vol level (volga ~ 0 ATM); wing vega rises (positive volga). Long-wing structures gain vega.
- long vanna: +417.4k EUR to +34.4k EUR (less long)
- long volga: +1.3k CHF to +719 CHF (less long)
- short charm: -13.3k EUR to -2.5k EUR (less short)

**P&L from the shock:** +33.5k CHF by full revaluation. Breakdown (spot, then vol, then time): delta +68.5k, gamma and higher-order spot -17.3k, vega/vol -17.7k, theta 0. The biggest driver is **delta**.

**Where the risk sits now:** short gamma (~0.2x a single ATM option); short vega (~0.3x a single ATM option).

**P&L estimate (part 3): -35.4k CHF.**
- Delta: -2,544,764 x dS (+0.00928) = -23,615
- Gamma: 0.5 x -223,142 x 1.0 x dS = -1,035
- Vega: -3,580 x 3.0 = -10,740
- Engine full revaluation: -22.6k CHF. The gap (+12.7k) is vanna (spot and vol moving together), volga, and gamma changing over the move (speed), which is large for short-dated options near their strikes.

</details>

**Q9** (`exposures_L3`, topic `exposures:straddle`, seed 1225120)

You are **long a 1Y USDCAD ATM straddle**, notional 50.00m USD per leg.

Spot 1.39000. Legs: ATM call K=1.36898, ATM put K=1.36898. Convention: Spot delta, premium-adjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot sells off 5.6% (vol surface sticky by strike), and the skew steepens: 25d risk reversals move 1.1 vols further towards puts**, and what it does to your P&L.

3. Using only the Greeks in the Givens box, estimate the instant P&L if spot moves **+1.5%** and vols move **+1.0 pts** in parallel.

Givens:

| Given | Value |
|---|---|
| Spot | 1.39 |
| Delta (USD, unadjusted spot delta) | 2,269,215 |
| Gamma (USD delta change per 1% spot) | 6,511,298 |
| Vega (CAD per vol pt) | 533,992 |
| Spot move (%) | 1.5 |
| Vol move (pts, parallel) | 1 |

- *Exposure signs before the shock*: **Delta: 0, Gamma: +, Theta: -, Vega: +, Vanna: 0, Volga: 0, Charm: +**
- *Estimated instant P&L (CAD) for spot +1.5% and vol +1.0 pts*: **683,126**
- *Written*: How do your exposures change if spot sells off 5.6% (vol surface sticky by strike), and the skew steepens: 25d risk reversals move 1.1 vols further towards puts? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **0** (-0.000135 USD, base notional, premium-adjusted)
- Gamma: **+** (+6.51m USD, delta change per 1% spot)
- Theta: **-** (-4.0k CAD, P&L per day)
- Vega: **+** (+534.0k CAD, P&L per vol pt)
- Vanna: **0** (+2.28e-05 USD, delta change per vol pt)
- Volga: **0** (-1.87e-08 CAD, vega change per vol pt)
- Charm: **+** (+24.3k USD, delta change per day)

**Intuition for the structure:** ATM call + ATM put: delta-neutral at the DNS strike, maximum gamma and vega for the premium, and the biggest theta bill.

**After the shock (spot sells off 5.6% (vol surface sticky by strike), and the skew steepens: 25d risk reversals move 1.1 vols further towards puts):**
- short delta: -0.000135 USD to -37.51m USD (more short). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite. Each leg's delta moves via vanna and its own vol change: puts' deltas grow in size as their vols rise.
- long gamma: +6.51m USD to +4.26m USD (less long). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk. A skew move changes each strike's vol differently: low-strike vols rise, high-strike vols fall, so each leg's gamma moves the opposite way to its vol.
- short theta: -4.0k CAD to -3.4k CAD (less short). Theta mirrors gamma: it is largest near the strikes. Legs whose vol rose decay faster, legs whose vol fell decay slower.
- long vega: +534.0k CAD to +286.6k CAD (less long). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes. Each leg's vega responds to its own vol change via volga; wing legs are affected most.
- long vanna: +2.28e-05 USD to +4.75m USD (more long)
- volga flips from short (-1.87e-08 CAD) to long (+66.4k CAD)
- charm flips from long (+24.3k USD) to short (-21.0k USD)

**P&L from the shock:** +950.5k CAD by full revaluation. Breakdown (spot, then vol, then time): delta -176.6k, gamma and higher-order spot +1.37m, vega/vol -239.6k, theta 0. The biggest driver is **gamma**.

**Where the risk sits now:** long gamma (~1.3x a single ATM option); long vega (~1.1x a single ATM option); short delta (~0.8x a single ATM option).

**P&L estimate (part 3): +683.1k CAD.**
- Delta: 2,269,215 x dS (+0.02085) = 47,313
- Gamma: 0.5 x 6,511,298 x 1.5 x dS = 101,820
- Vega: 533,992 x 1.0 = 533,992
- Engine full revaluation: +667.8k CAD. The gap (-15.3k) is vanna (spot and vol moving together), volga, and gamma changing over the move (speed), which is large for short-dated options near their strikes.

</details>

**Q10** (`exposures_L3`, topic `exposures:call_spread`, seed 1225151)

You are **long a 1W AUDUSD ATM/25-delta call spread**, notional 10.00m AUD per leg.

Spot 0.66000. Legs: long ATM call K=0.66008, short OTM call K=0.66554. Convention: Spot delta, unadjusted (premium in USD); ATM = DNS.

1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).
2. Then describe how your exposures change if **spot rallies 1.0% (vol surface sticky by strike), and implied vol spikes 2.3 vol points across the surface**, and what it does to your P&L.

3. Using only the Greeks in the Givens box, estimate the instant P&L if spot moves **+1.5%** and vols move **+1.0 pts** in parallel.

Givens:

| Given | Value |
|---|---|
| Spot | 0.66 |
| Delta (AUD, unadjusted spot delta) | 2,496,789 |
| Gamma (AUD delta change per 1% spot) | 634,802 |
| Vega (USD per vol pt) | 740 |
| Spot move (%) | 1.5 |
| Vol move (pts, parallel) | 1 |

- *Exposure signs before the shock*: **Delta: +, Gamma: +/0, Theta: -, Vega: +, Vanna: -, Volga: -, Charm: +**
- *Estimated instant P&L (USD) for spot +1.5% and vol +1.0 pts*: **30,172**
- *Written*: How do your exposures change if spot rallies 1.0% (vol surface sticky by strike), and implied vol spikes 2.3 vol points across the surface? What happens to your P&L, and why?

<details><summary>Model answer</summary>

**Exposures before the shock** (engine):
- Delta: **+** (+2.50m AUD, base notional)
- Gamma: **+** (+634.8k AUD, delta change per 1% spot)
- Theta: **-** (-496 USD, P&L per day)
- Vega: **+** (+740 USD, P&L per vol pt)
- Vanna: **-** (-241.5k AUD, delta change per vol pt)
- Volga: **-** (-152 USD, vega change per vol pt)
- Charm: **+** (+152.0k AUD, delta change per day)

**Intuition for the structure:** Long ATM call, short OTM call: long delta with capped upside. Net long gamma/vega near the lower strike, flipping to short near the upper strike.

**After the shock (spot rallies 1.0% (vol surface sticky by strike), and implied vol spikes 2.3 vol points across the surface):**
- long delta: +2.50m AUD to +1.95m AUD (less long). Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite. Vol up pulls every strike's delta towards 50 (vanna): OTM deltas grow, ITM deltas shrink.
- gamma flips from long (+634.8k AUD) to short (-482.8k AUD). Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk. Higher vol spreads gamma over a wider range of spot: gamma near the strikes falls (ATM gamma ~ 1/vol) and gamma at far strikes rises.
- theta flips from short (-496 USD) to long (+507 USD). Theta mirrors gamma: it is largest near the strikes. ATM theta scales roughly with vol, so the daily decay (paid or received) grows.
- vega flips from long (+740 USD) to short (-666 USD). Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes. ATM vega barely moves with the vol level (volga ~ 0 ATM); wing vega rises (positive volga). Long-wing structures gain vega.
- short vanna: -241.5k AUD to -146.7k AUD (less short)
- volga flips from short (-152 USD) to long (+104 USD)
- long charm: +152.0k AUD to +118.1k AUD (less long)

**P&L from the shock:** +15.0k USD by full revaluation. Breakdown (spot, then vol, then time): delta +16.5k, gamma and higher-order spot +356, vega/vol -1.9k, theta 0. The biggest driver is **delta**.

**Where the risk sits now:** short vega (~0.2x a single ATM option); long delta (19% of notional).

**P&L estimate (part 3): +30.2k USD.**
- Delta: 2,496,789 x dS (+0.0099) = 24,718
- Gamma: 0.5 x 634,802 x 1.5 x dS = 4,713
- Vega: 740 x 1.0 = 740
- Engine full revaluation: +22.4k USD. The gap (-7.8k) is vanna (spot and vol moving together), volga, and gamma changing over the move (speed), which is large for short-dated options near their strikes.

</details>

## 1C Concepts and trade expression

### Level 1: directional intuition, no calculations

**Q1** (`view_match`, topic `concepts:trade_expression`, seed 1023333)

**USDJPY.** You think front-end vol will rise relative to back-end vol (term structure inverts). Which structure expresses the view best?

- *Structure*: **Long the near expiry, short the far expiry (short calendar), vega-weighted**
- *Written*: Why this structure, and what is its main risk?

<details><summary>Model answer</summary>

**Long the near expiry, short the far expiry (short calendar), vega-weighted.**

Being long short-dated vega and short long-dated vega profits from the front rising more. Weight by vega (or vega x sqrt(T) scaling) so a parallel move is roughly neutral.

</details>

**Q2** (`arb_butterfly`, topic `concepts:arbitrage`, seed 1023364)

0.25y calls on an index at 100 trade at: 90 strike **10.26**, 100 strike **5.63**, 110 strike **0.38**. Assume zero interest rates and no dividends. Is there an arbitrage? What is the trade?

- *Trade*: **Buy the 90/100/110 butterfly (buy 90, sell 2x100, buy 110): you get paid to own a non-negative payoff**
- *Written*: Explain the arbitrage and the bound being violated.

<details><summary>Model answer</summary>

**Buy the butterfly for a credit.** 1) A 1x2x1 call fly pays max(0, ...) >= 0 everywhere, so it must cost >= 0. Equivalently call prices must be convex in strike. 2) Price = C90 - 2C100 + C110 = -0.62 < 0, so you receive 0.62 to own a payoff that is never negative. 3) In vol terms: the 100 strike is too expensive relative to the wings, i.e. the implied density goes negative.

</details>

**Q3** (`skew`, topic `concepts:skew`, seed 1023395)

The 1M 25-delta risk reversal in **USDCAD** is **+0.25 vols**. Which explanation fits best?

- *Explanation*: **CAD is a commodity and risk currency. In risk-off USD rallies against CAD, so USDCAD topside (USD calls) is bid and the RR is positive.**
- *Written*: Explain in your own words, including the spot-vol correlation.

<details><summary>Model answer</summary>

**CAD is a commodity and risk currency. In risk-off USD rallies against CAD, so USDCAD topside (USD calls) is bid and the RR is positive.**

1. 1M 25d RR in USDCAD is +0.25 vols (RR = call vol - put vol on USD).
2. Skew prices the direction in which the market expects big moves and rising vol. Spot-vol correlation is the key: if spot falls when vol rises, puts are worth more than Black-Scholes says and the RR goes negative.
3. Compare: equity index skew is strongly negative (crash risk, leverage effect, structural put buying). USDJPY looks like equities with the sign set by yen strength in stress.

</details>

**Q4** (`trade_overpriced`, topic `concepts:trade_expression`, seed 1023426)

**AUDUSD**: the RBA meeting is in **5 days**. You think the market is overpricing the event: you expect a small move and a vol crush after. What trade do you put on, and which expiry?

- *Structure*: **Short strangle (or short straddle), delta-hedged**
- *Expiry*: **1W**
- *Written*: Justify the structure and expiry, and say what could go wrong.

<details><summary>Model answer</summary>

**Short strangle (or short straddle), delta-hedged; expiry 1W.**

1. Sell the event: short vega and gamma, collecting the event premium. Strangles give room for a moderate move; know your tail risk and size for it.
2. Expiry: the RBA meeting is in 5 days. Choose the shortest expiry that covers it (1W). The event day's variance is a bigger share of a short option's total variance, so short-dated options give the most exposure to the event per premium (and you are not paying for many dull days after it).
3. Engine context: the 1W ATM straddle costs 65 pips (0.98% of spot); spot needs to move about that much by expiry to break even unhedged.
4. Risk: after the event implied vol usually drops (crush), so a long holder should plan the exit; a short seller is exposed to a gap move.

</details>

**Q5** (`view_match`, topic `concepts:trade_expression`, seed 1023457)

**GBPUSD.** You expect a large move but straddles look expensive; you accept needing a bigger move. Which structure expresses the view best?

- *Structure*: **Long 25-delta strangle**
- *Written*: Why this structure, and what is its main risk?

<details><summary>Model answer</summary>

**Long 25-delta strangle.**

Cheaper than a straddle because both strikes are out of the money, but spot must travel further before it pays.

</details>

**Q6** (`trade_vol_up`, topic `concepts:trade_expression`, seed 1023488)

**AUDUSD**: the RBA meeting is in **12 days**. You expect vol to rise into the event but have no view on direction. What trade do you put on, and which expiry?

- *Structure*: **Long straddle (ATM, delta-hedged)**
- *Expiry*: **2W**
- *Written*: Justify the structure and expiry, and say what could go wrong.

<details><summary>Model answer</summary>

**Long straddle (ATM, delta-hedged); expiry 2W.**

1. Buy the event: own gamma and vega through the event day. ATM straddle maximises gamma and vega per premium and starts delta-neutral.
2. Expiry: the RBA meeting is in 12 days. Choose the shortest expiry that covers it (2W). The event day's variance is a bigger share of a short option's total variance, so short-dated options give the most exposure to the event per premium (and you are not paying for many dull days after it).
3. Engine context: the 2W ATM straddle costs 93 pips (1.40% of spot); spot needs to move about that much by expiry to break even unhedged.
4. Risk: after the event implied vol usually drops (crush), so a long holder should plan the exit; a short seller is exposed to a gap move.

</details>

**Q7** (`arb_call_spread`, topic `concepts:arbitrage`, seed 1023519)

A 1y 100/105 call spread (long the 100, short the 105) trades at **5.50**. Assume zero interest rates and no dividends. What do you do?

- *Trade*: **Sell the spread: its payoff can never exceed the strike width, so you lock in the excess**
- *Written*: Explain the arbitrage and the bound being violated.

<details><summary>Model answer</summary>

**Sell the spread.** 1) Intuition: a call spread pays between 0 and the strike width (5). Paying more than 5 today (more than PV of 5 with rates) guarantees a loss for the buyer. 2) Sell it at 5.50, worst case you pay 5 at expiry: locked-in profit at least 0.50. 3) Bounds: 0 <= spread <= (K2 - K1) e^(-rT).

</details>

**Q8** (`trade_vol_up`, topic `concepts:trade_expression`, seed 1023550)

**EURJPY**: the US CPI release is in **9 days**. You expect vol to rise into the event but have no view on direction. What trade do you put on, and which expiry?

- *Structure*: **Long straddle (ATM, delta-hedged)**
- *Expiry*: **2W**
- *Written*: Justify the structure and expiry, and say what could go wrong.

<details><summary>Model answer</summary>

**Long straddle (ATM, delta-hedged); expiry 2W.**

1. Buy the event: own gamma and vega through the event day. ATM straddle maximises gamma and vega per premium and starts delta-neutral.
2. Expiry: the US CPI release is in 9 days. Choose the shortest expiry that covers it (2W). The event day's variance is a bigger share of a short option's total variance, so short-dated options give the most exposure to the event per premium (and you are not paying for many dull days after it).
3. Engine context: the 2W ATM straddle costs 256 pips (1.45% of spot); spot needs to move about that much by expiry to break even unhedged.
4. Risk: after the event implied vol usually drops (crush), so a long holder should plan the exit; a short seller is exposed to a gap move.

</details>

**Q9** (`view_match`, topic `concepts:trade_expression`, seed 1023581)

**GBPUSD.** You think puts will get more expensive relative to calls (skew steepens towards puts). Which structure expresses the view best?

- *Structure*: **Long put / short call risk reversal, delta- and vega-hedged**
- *Written*: Why this structure, and what is its main risk?

<details><summary>Model answer</summary>

**Long put / short call risk reversal, delta- and vega-hedged.**

Owning the put wing and selling the call wing isolates the skew. Hedge delta and residual vega so the P&L comes from the RR moving.

</details>

**Q10** (`view_match`, topic `concepts:trade_expression`, seed 1023612)

**USDJPY.** You think puts will get more expensive relative to calls (skew steepens towards puts). Which structure expresses the view best?

- *Structure*: **Long put / short call risk reversal, delta- and vega-hedged**
- *Written*: Why this structure, and what is its main risk?

<details><summary>Model answer</summary>

**Long put / short call risk reversal, delta- and vega-hedged.**

Owning the put wing and selling the call wing isolates the skew. Hedge delta and residual vega so the P&L comes from the RR moving.

</details>

### Level 2: combinations, light calculations with every input given

**Q1** (`puzzle_call_rally_lost`, topic `concepts:pnl_explain`, seed 1128062)

**EURUSD**: you are long a 1M call (25-delta). Spot rallied 0.6% the day after an event, yet your long call lost money. Why?

- *Main reason*: **Event vol was crushed: the vega loss beat the delta gain**
- *Written*: Explain using the Greeks.

<details><summary>Model answer</summary>

**Event vol was crushed: the vega loss beat the delta gain.**

1. Engine P&L: -4.6k USD. Breakdown (spot, then vol, then time): delta +17.4k, gamma (and higher-order spot) +3.3k, vega/vol -24.1k, theta -1.2k. Biggest driver: vega/vol.
2. Lesson: an option position is a bet on realised AND implied vol, and on time; one leg of the Greek P&L can swamp the one you were focused on.

</details>

**Q2** (`puzzle_short_strangle_inside_lost`, topic `concepts:pnl_explain`, seed 1128093)

**EURUSD**: you are short a 1M strangle. Spot stayed well inside both strikes, yet the short strangle lost money. Why?

- *Main reason*: **Implied vol rose: you are short vega, and the vol move cost more than the theta earned**
- *Written*: Explain using the Greeks.

<details><summary>Model answer</summary>

**Implied vol rose: you are short vega, and the vol move cost more than the theta earned.**

1. Engine P&L: -19.4k USD. Breakdown (spot, then vol, then time): delta -6.09e-10, gamma (and higher-order spot) -704, vega/vol -21.8k, theta +3.1k. Biggest driver: vega/vol.
2. Lesson: an option position is a bet on realised AND implied vol, and on time; one leg of the Greek P&L can swamp the one you were focused on.

</details>

**Q3** (`puzzle_straddle_moved_lost`, topic `concepts:pnl_explain`, seed 1128124)

**USDJPY**: you are long a 1M straddle. A day later spot has moved 0.8%, yet you lost money. Why?

- *Main reason*: **Implied vol fell: the vega loss (plus theta) beat the gamma gain**
- *Written*: Explain using the Greeks.

<details><summary>Model answer</summary>

**Implied vol fell: the vega loss (plus theta) beat the gamma gain.**

1. Engine P&L: -3.80m JPY. Breakdown (spot, then vol, then time): delta +273.6k, gamma (and higher-order spot) +1.35m, vega/vol -4.99m, theta -437.2k. Biggest driver: vega/vol.
2. Lesson: an option position is a bet on realised AND implied vol, and on time; one leg of the Greek P&L can swamp the one you were focused on.

</details>

**Q4** (`puzzle_call_rally_lost`, topic `concepts:pnl_explain`, seed 1128155)

**AUDUSD**: you are long a 1M call (25-delta). Spot rallied 0.6% the day after an event, yet your long call lost money. Why?

- *Main reason*: **Event vol was crushed: the vega loss beat the delta gain**
- *Written*: Explain using the Greeks.

<details><summary>Model answer</summary>

**Event vol was crushed: the vega loss beat the delta gain.**

1. Engine P&L: -2.8k USD. Breakdown (spot, then vol, then time): delta +9.9k, gamma (and higher-order spot) +1.5k, vega/vol -13.4k, theta -812. Biggest driver: vega/vol.
2. Lesson: an option position is a bet on realised AND implied vol, and on time; one leg of the Greek P&L can swamp the one you were focused on.

</details>

**Q5** (`puzzle_straddle_moved_lost`, topic `concepts:pnl_explain`, seed 1128186)

**EURGBP**: you are long a 1M straddle. A day later spot has moved 0.8%, yet you lost money. Why?

- *Main reason*: **Implied vol fell: the vega loss (plus theta) beat the gamma gain**
- *Written*: Explain using the Greeks.

<details><summary>Model answer</summary>

**Implied vol fell: the vega loss (plus theta) beat the gamma gain.**

1. Engine P&L: -9.6k GBP. Breakdown (spot, then vol, then time): delta +808, gamma (and higher-order spot) +15.1k, vega/vol -24.4k, theta -1.1k. Biggest driver: vega/vol.
2. Lesson: an option position is a bet on realised AND implied vol, and on time; one leg of the Greek P&L can swamp the one you were focused on.

</details>

**Q6** (`puzzle_straddle_moved_lost`, topic `concepts:pnl_explain`, seed 1128217)

**GBPUSD**: you are long a 1M straddle. A day later spot has moved 0.8%, yet you lost money. Why?

- *Main reason*: **Implied vol fell: the vega loss (plus theta) beat the gamma gain**
- *Written*: Explain using the Greeks.

<details><summary>Model answer</summary>

**Implied vol fell: the vega loss (plus theta) beat the gamma gain.**

1. Engine P&L: -29.4k USD. Breakdown (spot, then vol, then time): delta -1.23e-07, gamma (and higher-order spot) +15.5k, vega/vol -42.0k, theta -2.8k. Biggest driver: vega/vol.
2. Lesson: an option position is a bet on realised AND implied vol, and on time; one leg of the Greek P&L can swamp the one you were focused on.

</details>

**Q7** (`puzzle_straddle_moved_lost`, topic `concepts:pnl_explain`, seed 1128248)

**GBPUSD**: you are long a 1M straddle. A day later spot has moved 0.8%, yet you lost money. Why?

- *Main reason*: **Implied vol fell: the vega loss (plus theta) beat the gamma gain**
- *Written*: Explain using the Greeks.

<details><summary>Model answer</summary>

**Implied vol fell: the vega loss (plus theta) beat the gamma gain.**

1. Engine P&L: -29.4k USD. Breakdown (spot, then vol, then time): delta -1.23e-07, gamma (and higher-order spot) +15.5k, vega/vol -42.0k, theta -2.8k. Biggest driver: vega/vol.
2. Lesson: an option position is a bet on realised AND implied vol, and on time; one leg of the Greek P&L can swamp the one you were focused on.

</details>

**Q8** (`puzzle_fly_pinned_lost`, topic `concepts:pnl_explain`, seed 1128279)

**USDCAD**: you are long a 1M butterfly. Spot sat right on the body strike for a day, yet the long butterfly lost money. Why?

- *Main reason*: **Implied vol rose: a long fly is short vega near the body, which outweighed a day of theta**
- *Written*: Explain using the Greeks.

<details><summary>Model answer</summary>

**Implied vol rose: a long fly is short vega near the body, which outweighed a day of theta.**

1. Engine P&L: -5.0k CAD. Breakdown (spot, then vol, then time): delta 0, gamma (and higher-order spot) 0, vega/vol -5.5k, theta +569. Biggest driver: vega/vol.
2. Lesson: an option position is a bet on realised AND implied vol, and on time; one leg of the Greek P&L can swamp the one you were focused on.

</details>

**Q9** (`puzzle_call_rally_lost`, topic `concepts:pnl_explain`, seed 1128310)

**USDJPY**: you are long a 1M call (25-delta). Spot rallied 0.6% the day after an event, yet your long call lost money. Why?

- *Main reason*: **Event vol was crushed: the vega loss beat the delta gain**
- *Written*: Explain using the Greeks.

<details><summary>Model answer</summary>

**Event vol was crushed: the vega loss beat the delta gain.**

1. Engine P&L: -607.8k JPY. Breakdown (spot, then vol, then time): delta +2.32m, gamma (and higher-order spot) +335.8k, vega/vol -3.10m, theta -159.1k. Biggest driver: vega/vol.
2. Lesson: an option position is a bet on realised AND implied vol, and on time; one leg of the Greek P&L can swamp the one you were focused on.

</details>

**Q10** (`puzzle_fly_pinned_lost`, topic `concepts:pnl_explain`, seed 1128341)

**EURCHF**: you are long a 1M butterfly. Spot sat right on the body strike for a day, yet the long butterfly lost money. Why?

- *Main reason*: **Implied vol rose: a long fly is short vega near the body, which outweighed a day of theta**
- *Written*: Explain using the Greeks.

<details><summary>Model answer</summary>

**Implied vol rose: a long fly is short vega near the body, which outweighed a day of theta.**

1. Engine P&L: -3.3k CHF. Breakdown (spot, then vol, then time): delta 0, gamma (and higher-order spot) 0, vega/vol -3.7k, theta +366. Biggest driver: vega/vol.
2. Lesson: an option position is a bet on realised AND implied vol, and on time; one leg of the Greek P&L can swamp the one you were focused on.

</details>

### Level 3: calculations plus subtler concepts

**Q1** (`breakeven`, topic `concepts:gamma_theta`, seed 1232791)

You buy a 1M ATM EURUSD straddle (EUR 10m per leg) at 7.10% vol and delta-hedge it. How big a daily move (in %) do you need to break even on theta? If spot then moves 0.45% a day on average, do you make or lose money?

Givens:

| Given | Value |
|---|---|
| Spot | 1.16 |
| Theta (USD per day) | -3,094 |
| Gamma (EUR delta change per 1% spot move) | 3,887,182 |

- *Breakeven daily move (%)*: **0.3704 %**
- *With 0.45% daily moves*: **Make money**
- *Written*: Explain the gamma/theta trade-off.

<details><summary>Model answer</summary>

**About 0.37% a day; with 0.45% moves you make money.**

1. Each day you earn 0.5 x Gamma x dS^2 and pay |theta|. Break even when they are equal: dS = sqrt(2|theta| / Gamma).
2. Gamma = 3,887,182 / (1% x 1.16) = 335,101,897; dS = 0.0042972, i.e. 0.37%.
3. Check: theta ~ -0.5 Gamma S^2 vol^2 / 365, so the breakeven is about vol / sqrt(365) = 7.10% / 19.1 = 0.37%. Realised above implied wins.

</details>

**Q2** (`sticky_calc`, topic `concepts:sticky`, seed 1232822)

EURUSD 1M smile in the Givens. Spot moves +1.3% and the ATM strike moves with it. Under **sticky strike**, estimate the change in 1M ATM vol (vol pts) by linear interpolation between the pillars. What happens under **sticky delta**?

Givens:

| Given | Value |
|---|---|
| ATM strike now | 1.1618 |
| ATM vol (%) | 7.1 |
| 25d call strike | 1.1785 |
| 25d call vol (%) | 7.35 |
| 25d put strike | 1.1458 |
| 25d put vol (%) | 7.15 |
| Spot move (%) | 1.3 |

- *Change in ATM vol, sticky strike (vol pts)*: **0.2257**
- *ATM vol under sticky delta*: **Unchanged**
- *Written*: Explain the difference and when traders assume each.

<details><summary>Model answer</summary>

**Sticky strike: about +0.23 vol pts. Sticky delta: unchanged.**

1. Sticky strike: each strike keeps its vol, so the new ATM strike (1.17689) reads the old smile on the call side.
2. Linear interpolation between ATM and the 25d call pillar gives +0.226.
3. Engine (SABR smile, exact ATM strike): +0.203; the gap is the smile's curvature.
4. Sticky delta: the smile moves with spot, so ATM vol is unchanged. Traders lean sticky strike in calm, range-bound markets and sticky delta (or worse, 'sticky moneyness with skew') in trending or stressed markets; the choice changes your smile-adjusted delta.

</details>

**Q3** (`skew_pnl`, topic `concepts:skew`, seed 1232853)

**USDCHF** risk-off: 1M ATM vol rises 0.5 and the 25d RR moves -0.6 (towards puts). You are short a 1M 25d risk reversal (call over put). Assume the 25d fly is unchanged. Estimate your vol P&L. Does the skew move help or hurt you?

Givens:

| Given | Value |
|---|---|
| Vega of your 25d call leg (CHF/vol pt, signed) | -18,442 |
| Vega of your 25d put leg (CHF/vol pt, signed) | 18,190 |
| Change in 1M ATM vol (pts) | 0.5 |
| Change in 1M 25d RR (vols) | -0.6 |

- *Vol P&L (CHF)*: **10,864**
- *The skew move alone*: **Helps you**
- *Written*: Explain the skew dynamics (why RRs move this way when spot falls).

<details><summary>Model answer</summary>

**About +10.9k CHF; the skew move helps you (+11.0k).**

1. With the fly fixed, 25d call vol moves dATM + dRR/2 = +0.20 and 25d put vol moves dATM - dRR/2 = +0.80.
2. P&L = vega_call x dvol_call + vega_put x dvol_put = 10,864.
3. Why skews move: in USDCHF the base currency falls in risk-off and vol rises with it, so downside (puts) reprices most: RRs move towards puts as spot falls (negative spot-vol correlation).

</details>

**Q4** (`arb_calc_parity`, topic `concepts:arbitrage`, seed 1232884)

EURUSD 3M options in the Givens. Does put-call parity hold? What is the trade, and the mispricing in pips?

Givens:

| Given | Value |
|---|---|
| EURUSD spot | 1.16 |
| Strike | 1.1646 |
| USD rate (cont.) | 0.036 |
| EUR rate (cont.) | 0.02 |
| Expiry (years) | 0.25 |
| Call price (USD pips) | 192.20 |
| Put price (USD pips) | 167.70 |

- *Trade*: **Sell the call, buy the put, buy EUR forward**
- *Locked-in profit (per unit / pips)*: **24.01**
- *Written*: Explain the bound being violated.

<details><summary>Model answer</summary>

**Sell the call, buy the put, buy EUR forward; profit 24.011.**

1. FX parity: C - P = S e^(-rf T) - K e^(-rd T).
2. Plugging in the Givens gives 24.0115.

</details>

**Q5** (`skew_pnl`, topic `concepts:skew`, seed 1232915)

**USDCHF** risk-off: 1M ATM vol rises 1.6 and the 25d RR moves -0.8 (towards puts). You are long a 1M 25d risk reversal (call over put). Assume the 25d fly is unchanged. Estimate your vol P&L. Does the skew move help or hurt you?

Givens:

| Given | Value |
|---|---|
| Vega of your 25d call leg (CHF/vol pt, signed) | 18,442 |
| Vega of your 25d put leg (CHF/vol pt, signed) | -18,190 |
| Change in 1M ATM vol (pts) | 1.6 |
| Change in 1M 25d RR (vols) | -0.8 |

- *Vol P&L (CHF)*: **-14,250**
- *The skew move alone*: **Hurts you**
- *Written*: Explain the skew dynamics (why RRs move this way when spot falls).

<details><summary>Model answer</summary>

**About -14.2k CHF; the skew move hurts you (-14.7k).**

1. With the fly fixed, 25d call vol moves dATM + dRR/2 = +1.20 and 25d put vol moves dATM - dRR/2 = +2.00.
2. P&L = vega_call x dvol_call + vega_put x dvol_put = -14,250.
3. Why skews move: in USDCHF the base currency falls in risk-off and vol rises with it, so downside (puts) reprices most: RRs move towards puts as spot falls (negative spot-vol correlation).

</details>

**Q6** (`breakeven`, topic `concepts:gamma_theta`, seed 1232946)

You buy a 3M ATM EURCHF straddle (EUR 10m per leg) at 5.49% vol and delta-hedge it. How big a daily move (in %) do you need to break even on theta? If spot then moves 0.23% a day on average, do you make or lose money?

Givens:

| Given | Value |
|---|---|
| Spot | 0.928 |
| Theta (CHF per day) | -1,097 |
| Gamma (EUR delta change per 1% spot move) | 2,890,432 |

- *Breakeven daily move (%)*: **0.286 %**
- *With 0.23% daily moves*: **Lose money**
- *Written*: Explain the gamma/theta trade-off.

<details><summary>Model answer</summary>

**About 0.29% a day; with 0.23% moves you lose money.**

1. Each day you earn 0.5 x Gamma x dS^2 and pay |theta|. Break even when they are equal: dS = sqrt(2|theta| / Gamma).
2. Gamma = 2,890,432 / (1% x 0.928) = 311,468,966; dS = 0.0026541, i.e. 0.29%.
3. Check: theta ~ -0.5 Gamma S^2 vol^2 / 365, so the breakeven is about vol / sqrt(365) = 5.49% / 19.1 = 0.29%. Realised above implied wins.

</details>

**Q7** (`sticky_calc`, topic `concepts:sticky`, seed 1232977)

EURUSD 1M smile in the Givens. Spot moves -1.5% and the ATM strike moves with it. Under **sticky strike**, estimate the change in 1M ATM vol (vol pts) by linear interpolation between the pillars. What happens under **sticky delta**?

Givens:

| Given | Value |
|---|---|
| ATM strike now | 1.1618 |
| ATM vol (%) | 7.1 |
| 25d call strike | 1.1785 |
| 25d call vol (%) | 7.35 |
| 25d put strike | 1.1458 |
| 25d put vol (%) | 7.15 |
| Spot move (%) | -1.5 |

- *Change in ATM vol, sticky strike (vol pts)*: **0.05436**
- *ATM vol under sticky delta*: **Unchanged**
- *Written*: Explain the difference and when traders assume each.

<details><summary>Model answer</summary>

**Sticky strike: about +0.05 vol pts. Sticky delta: unchanged.**

1. Sticky strike: each strike keeps its vol, so the new ATM strike (1.14436) reads the old smile on the put side.
2. Linear interpolation between ATM and the 25d put pillar gives +0.054.
3. Engine (SABR smile, exact ATM strike): +0.061; the gap is the smile's curvature.
4. Sticky delta: the smile moves with spot, so ATM vol is unchanged. Traders lean sticky strike in calm, range-bound markets and sticky delta (or worse, 'sticky moneyness with skew') in trending or stressed markets; the choice changes your smile-adjusted delta.

</details>

**Q8** (`arb_calc_calendar`, topic `concepts:arbitrage`, seed 1233008)

Zero rates, no dividends. Prices in the Givens. Is there an arbitrage? What credit do you lock in?

Givens:

| Given | Value |
|---|---|
| 3M 100-strike call (spot 100) | 6.26 |
| 6M 100-strike call | 5.64 |

- *Trade*: **Sell the 3M, buy the 6M (calendar for a credit)**
- *Locked-in profit (per unit / pips)*: **0.62**
- *Written*: Explain the bound being violated.

<details><summary>Model answer</summary>

**Sell the 3M, buy the 6M (calendar for a credit); profit 0.620.**

1. With zero rates and no dividends a longer-dated call is worth at least the shorter one at the same strike.
2. Plugging in the Givens gives 0.6200.

</details>

**Q9** (`sticky_calc`, topic `concepts:sticky`, seed 1233039)

USDCAD 1M smile in the Givens. Spot moves +2.3% and the ATM strike moves with it. Under **sticky strike**, estimate the change in 1M ATM vol (vol pts) by linear interpolation between the pillars. What happens under **sticky delta**?

Givens:

| Given | Value |
|---|---|
| ATM strike now | 1.3883 |
| ATM vol (%) | 5.3 |
| 25d call strike | 1.4035 |
| 25d call vol (%) | 5.545 |
| 25d put strike | 1.3743 |
| 25d put vol (%) | 5.295 |
| Spot move (%) | 2.3 |

- *Change in ATM vol, sticky strike (vol pts)*: **0.5147**
- *ATM vol under sticky delta*: **Unchanged**
- *Written*: Explain the difference and when traders assume each.

<details><summary>Model answer</summary>

**Sticky strike: about +0.51 vol pts. Sticky delta: unchanged.**

1. Sticky strike: each strike keeps its vol, so the new ATM strike (1.42020) reads the old smile on the call side.
2. Linear interpolation between ATM and the 25d call pillar gives +0.515.
3. Engine (SABR smile, exact ATM strike): +0.669; the gap is the smile's curvature.
4. Sticky delta: the smile moves with spot, so ATM vol is unchanged. Traders lean sticky strike in calm, range-bound markets and sticky delta (or worse, 'sticky moneyness with skew') in trending or stressed markets; the choice changes your smile-adjusted delta.

</details>

**Q10** (`rv_iv`, topic `concepts:implied_vs_realised`, seed 1233070)

You are long a delta-hedged 1M ATM AUDUSD straddle. Over the next 10 days spot realises 13.3% vol while implied stays at 9.3%. Do you make or lose money, and roughly how much (in USD, holding gamma constant)?

Givens:

| Given | Value |
|---|---|
| Spot | 0.66 |
| Gamma (AUD delta change per 1% spot move) | 2,963,707 |
| Implied vol paid (%) | 9.3 |
| Realised vol (%) | 13.3 |
| Days held (calendar) | 10 |

- *Sign of P&L*: **Profit**
- *P&L (USD)*: **24,223**
- *Written*: Explain where the P&L comes from and why the estimate is approximate.

<details><summary>Model answer</summary>

**Profit of about 24,223 USD.**

1. Intuition: a delta-hedged option earns 0.5 Gamma dS^2 on each move and pays theta, which is priced at the implied vol. Net, you earn the gap between realised and implied variance.
2. Gamma in d2V/dS2 terms = gamma_1pct / (1% x S) = 2,963,707 / 0.0066 = 449,046,515.
3. P&L ~ 0.5 x Gamma x S^2 x (realised^2 - implied^2) x days/365 = 24,223.
4. Approximate because gamma changes as spot moves and time passes, and the P&L depends on when the moves happen (path dependence).

</details>

# Section 2: Interview Prep (Rates)

## 2A-1 Stage 1: Government bonds

### Level 1: directional intuition, no calculations

**Q1** (`s1_l1_asymmetry`, topic `convexity:bond_basics`, seed 1759800)

You are short GBP 100m of a 4% 10Y gilt. Compare your P&L if yields fall 75bp vs rise 75bp. Which is larger in size, and why?

- *Larger in size*: **The P&L from yields falling**
- *Written*: Explain why.

<details><summary>Model answer</summary>

**The rally P&L is larger in size.**

1. Positive convexity: as yields fall duration lengthens, so price gains accelerate; as yields rise duration shortens, so losses slow down.
2. Short the bond (short convexity): you lose more in the rally than you gain in the selloff.
3. Illustration (engine): yields -75bp -GBP 6.36m, +75bp +GBP 5.92m.

</details>

**Q2** (`s1_l1_asymmetry`, topic `convexity:bond_basics`, seed 1759831)

You are short GBP 100m of a 4% 10Y gilt. Compare your P&L if yields fall 75bp vs rise 75bp. Which is larger in size, and why?

- *Larger in size*: **The P&L from yields falling**
- *Written*: Explain why.

<details><summary>Model answer</summary>

**The rally P&L is larger in size.**

1. Positive convexity: as yields fall duration lengthens, so price gains accelerate; as yields rise duration shortens, so losses slow down.
2. Short the bond (short convexity): you lose more in the rally than you gain in the selloff.
3. Illustration (engine): yields -75bp -GBP 6.36m, +75bp +GBP 5.92m.

</details>

**Q3** (`s1_l1_compare`, topic `convexity:drivers`, seed 1759862)

Which has more **convexity**? A: a **4% 30Y** bond. B: a **4% 5Y** bond (same 4% yield).

- *More convexity*: **A**
- *Written*: Why?

<details><summary>Model answer</summary>

**A.**

1. Convexity grows roughly with maturity squared: the long bond's duration changes much more as yields move.
2. Illustration (engine): A convexity 420.81, B 23.50.
3. Rules: duration rises with maturity, falls with coupon and yield; a zero's Macaulay duration equals its maturity; convexity ~ maturity squared.

</details>

**Q4** (`s1_l1_asymmetry`, topic `convexity:bond_basics`, seed 1759893)

You are short GBP 100m of a 4% 30Y gilt. Compare your P&L if yields fall 150bp vs rise 150bp. Which is larger in size, and why?

- *Larger in size*: **The P&L from yields falling**
- *Written*: Explain why.

<details><summary>Model answer</summary>

**The rally P&L is larger in size.**

1. Positive convexity: as yields fall duration lengthens, so price gains accelerate; as yields rise duration shortens, so losses slow down.
2. Short the bond (short convexity): you lose more in the rally than you gain in the selloff.
3. Illustration (engine): yields -150bp -GBP 31.53m, +150bp +GBP 21.92m.

</details>

**Q5** (`s1_l1_asymmetry`, topic `convexity:bond_basics`, seed 1759924)

You are short GBP 100m of a 4% 30Y gilt. Compare your P&L if yields fall 100bp vs rise 100bp. Which is larger in size, and why?

- *Larger in size*: **The P&L from yields falling**
- *Written*: Explain why.

<details><summary>Model answer</summary>

**The rally P&L is larger in size.**

1. Positive convexity: as yields fall duration lengthens, so price gains accelerate; as yields rise duration shortens, so losses slow down.
2. Short the bond (short convexity): you lose more in the rally than you gain in the selloff.
3. Illustration (engine): yields -100bp -GBP 19.69m, +100bp +GBP 15.45m.

</details>

**Q6** (`s1_l1_position`, topic `duration:bond_basics`, seed 1759955)

You are **short GBP 100m face of a zero-coupon 10Y gilt**. Are you long or short duration? Long or short convexity? Do you gain or lose if yields rise 25bp?

- *Duration*: **Short**
- *Convexity*: **Short**
- *Yields rise 25bp*: **Gain**
- *Written*: Explain each answer.

<details><summary>Model answer</summary>

**Short duration, short convexity; you gain if yields rise 25bp.**

1. A bond pays fixed cash flows; higher yields discount them more, so its price falls. Owning it = long duration (you gain when yields fall). Being short flips it.
2. A vanilla bond's price/yield curve bends upward (positive convexity): long the bond = long convexity, short the bond = SHORT convexity, so big moves either way hurt a short more than the duration term says.
3. Illustration (engine, full repricing): +GBP 1.63m for GBP 100m face.

</details>

**Q7** (`s1_l1_asymmetry`, topic `convexity:bond_basics`, seed 1759986)

You are short GBP 100m of a 4% 30Y gilt. Compare your P&L if yields fall 150bp vs rise 150bp. Which is larger in size, and why?

- *Larger in size*: **The P&L from yields falling**
- *Written*: Explain why.

<details><summary>Model answer</summary>

**The rally P&L is larger in size.**

1. Positive convexity: as yields fall duration lengthens, so price gains accelerate; as yields rise duration shortens, so losses slow down.
2. Short the bond (short convexity): you lose more in the rally than you gain in the selloff.
3. Illustration (engine): yields -150bp -GBP 31.53m, +150bp +GBP 21.92m.

</details>

**Q8** (`s1_l1_position`, topic `duration:bond_basics`, seed 1760017)

You are **short GBP 100m face of a 4.00% 5Y gilt**. Are you long or short duration? Long or short convexity? Do you gain or lose if yields rise 100bp?

- *Duration*: **Short**
- *Convexity*: **Short**
- *Yields rise 100bp*: **Gain**
- *Written*: Explain each answer.

<details><summary>Model answer</summary>

**Short duration, short convexity; you gain if yields rise 100bp.**

1. A bond pays fixed cash flows; higher yields discount them more, so its price falls. Owning it = long duration (you gain when yields fall). Being short flips it.
2. A vanilla bond's price/yield curve bends upward (positive convexity): long the bond = long convexity, short the bond = SHORT convexity, so big moves either way hurt a short more than the duration term says.
3. Illustration (engine, full repricing): +GBP 4.38m for GBP 100m face.

</details>

**Q9** (`s1_l1_compare`, topic `convexity:drivers`, seed 1760048)

Which has more **convexity**? A: a **4% 5Y** bond. B: a **4% 30Y** bond (same 4% yield).

- *More convexity*: **B**
- *Written*: Why?

<details><summary>Model answer</summary>

**B.**

1. Convexity grows roughly with maturity squared: the long bond's duration changes much more as yields move.
2. Illustration (engine): A convexity 23.50, B 420.81.
3. Rules: duration rises with maturity, falls with coupon and yield; a zero's Macaulay duration equals its maturity; convexity ~ maturity squared.

</details>

**Q10** (`s1_l1_compare`, topic `duration:drivers`, seed 1760079)

Which has more **duration**? A: a **5% 30Y** bond. B: a **zero-coupon 30Y** bond (same 4% yield).

- *More duration*: **B**
- *Written*: Why?

<details><summary>Model answer</summary>

**B.**

1. A zero pays everything at maturity; a coupon bond returns cash earlier, so its weighted-average time is shorter.
2. Illustration (engine): A duration 16.60, B 29.41.
3. Rules: duration rises with maturity, falls with coupon and yield; a zero's Macaulay duration equals its maturity; convexity ~ maturity squared.

</details>

### Level 2: combinations, light calculations with every input given

**Q1** (`s1_l2_sized`, topic `duration:sized_pnl`, seed 1864529)

You are short GBP 100m face of a zero-coupon 5Y gilt. Using the Givens, estimate your P&L if yields move +100bp. Are you long or short duration?

Givens:

| Given | Value |
|---|---|
| Face (GBP, + long / - short) | -100,000,000 |
| Price (per 100) | 82.0348 |
| Modified duration (years) | 4.902 |
| Convexity (years^2) | 26.432 |
| Yield move (bp, parallel) | 100 |

- *P&L (GBP thousands)*: **3,913 k**
- *Duration*: **Short**
- *Written*: Show the duration and convexity terms.

<details><summary>Model answer</summary>

**About +GBP 3.91m.**

(a) Approximation: duration term +GBP 4.02m + convexity term -GBP 108.4k = **+GBP 3.91m**.
(b) Exact full repricing (engine): **+GBP 3.91m**.
Gap: +GBP 2.1k (+0.05% of the move), from the higher-order terms the two-term Taylor expansion leaves out. It grows with the size of the move and with maturity.

</details>

**Q2** (`s1_l2_sized`, topic `duration:sized_pnl`, seed 1864560)

You are long GBP 100m face of a 4.50% 5Y gilt. Using the Givens, estimate your P&L if yields move +100bp. Are you long or short duration?

Givens:

| Given | Value |
|---|---|
| Face (GBP, + long / - short) | 100,000,000 |
| Price (per 100) | 100 |
| Modified duration (years) | 4.4331 |
| Convexity (years^2) | 23.05 |
| Yield move (bp, parallel) | 100 |

- *P&L (GBP thousands)*: **-4,318 k**
- *Duration*: **Long**
- *Written*: Show the duration and convexity terms.

<details><summary>Model answer</summary>

**About -GBP 4.32m.**

(a) Approximation: duration term -GBP 4.43m + convexity term +GBP 115.2k = **-GBP 4.32m**.
(b) Exact full repricing (engine): **-GBP 4.32m**.
Gap: -GBP 2.2k (-0.05% of the move), from the higher-order terms the two-term Taylor expansion leaves out. It grows with the size of the move and with maturity.

</details>

**Q3** (`s1_l2_asym_sized`, topic `convexity:sized`, seed 1864591)

You own GBP 100m of a 4% 30Y gilt. By how much does your gain if yields fall 100bp exceed your loss if they rise 100bp? Use the Givens.

Givens:

| Given | Value |
|---|---|
| Face (GBP) | 100,000,000 |
| Price (per 100) | 100 |
| Convexity (years^2) | 420.81 |
| Size of the move (bp) | 100 |

- *Gain minus |loss| (GBP thousands)*: **4,208 k**
- *Written*: Explain where the difference comes from.

<details><summary>Model answer</summary>

**About +GBP 4.21m.**

1. The duration terms are equal and opposite, so they cancel; the two convexity terms add: 2 x 0.5 C P dy^2 = C P dy^2 = +GBP 4.21m.
2. Exact (engine): +GBP 4.24m; gap +GBP 27.7k from higher-order terms.

</details>

**Q4** (`s1_l2_sized`, topic `duration:sized_pnl`, seed 1864622)

You are short GBP 100m face of a 4.25% 10Y gilt. Using the Givens, estimate your P&L if yields move +50bp. Are you long or short duration?

Givens:

| Given | Value |
|---|---|
| Face (GBP, + long / - short) | -100,000,000 |
| Price (per 100) | 106.28 |
| Modified duration (years) | 8.1696 |
| Convexity (years^2) | 78.891 |
| Yield move (bp, parallel) | 50 |

- *P&L (GBP thousands)*: **4,237 k**
- *Duration*: **Short**
- *Written*: Show the duration and convexity terms.

<details><summary>Model answer</summary>

**About +GBP 4.24m.**

(a) Approximation: duration term +GBP 4.34m + convexity term -GBP 104.8k = **+GBP 4.24m**.
(b) Exact full repricing (engine): **+GBP 4.24m**.
Gap: +GBP 1.8k (+0.04% of the move), from the higher-order terms the two-term Taylor expansion leaves out. It grows with the size of the move and with maturity.

</details>

**Q5** (`s1_l2_asym_sized`, topic `convexity:sized`, seed 1864653)

You own GBP 100m of a 4% 30Y gilt. By how much does your gain if yields fall 75bp exceed your loss if they rise 75bp? Use the Givens.

Givens:

| Given | Value |
|---|---|
| Face (GBP) | 100,000,000 |
| Price (per 100) | 100 |
| Convexity (years^2) | 420.81 |
| Size of the move (bp) | 75 |

- *Gain minus |loss| (GBP thousands)*: **2,367 k**
- *Written*: Explain where the difference comes from.

<details><summary>Model answer</summary>

**About +GBP 2.37m.**

1. The duration terms are equal and opposite, so they cancel; the two convexity terms add: 2 x 0.5 C P dy^2 = C P dy^2 = +GBP 2.37m.
2. Exact (engine): +GBP 2.38m; gap +GBP 8.7k from higher-order terms.

</details>

**Q6** (`s1_l2_sized`, topic `duration:sized_pnl`, seed 1864684)

You are long GBP 100m face of a 4.50% 5Y gilt. Using the Givens, estimate your P&L if yields move +25bp. Are you long or short duration?

Givens:

| Given | Value |
|---|---|
| Face (GBP, + long / - short) | 100,000,000 |
| Price (per 100) | 104.55 |
| Modified duration (years) | 4.4671 |
| Convexity (years^2) | 23.36 |
| Yield move (bp, parallel) | 25 |

- *P&L (GBP thousands)*: **-1,160 k**
- *Duration*: **Long**
- *Written*: Show the duration and convexity terms.

<details><summary>Model answer</summary>

**About -GBP 1.16m.**

(a) Approximation: duration term -GBP 1.17m + convexity term +GBP 7.6k = **-GBP 1.16m**.
(b) Exact full repricing (engine): **-GBP 1.16m**.
Gap: -GBP 42 (-0.00% of the move), from the higher-order terms the two-term Taylor expansion leaves out. It grows with the size of the move and with maturity.

</details>

**Q7** (`s1_l2_sized`, topic `duration:sized_pnl`, seed 1864715)

You are long GBP 100m face of a zero-coupon 10Y gilt. Using the Givens, estimate your P&L if yields move +100bp. Are you long or short duration?

Givens:

| Given | Value |
|---|---|
| Face (GBP, + long / - short) | 100,000,000 |
| Price (per 100) | 64.0816 |
| Modified duration (years) | 9.78 |
| Convexity (years^2) | 100.43 |
| Yield move (bp, parallel) | 100 |

- *P&L (GBP thousands)*: **-5,945 k**
- *Duration*: **Long**
- *Written*: Show the duration and convexity terms.

<details><summary>Model answer</summary>

**About -GBP 5.95m.**

(a) Approximation: duration term -GBP 6.27m + convexity term +GBP 321.8k = **-GBP 5.95m**.
(b) Exact full repricing (engine): **-GBP 5.96m**.
Gap: -GBP 11.2k (-0.19% of the move), from the higher-order terms the two-term Taylor expansion leaves out. It grows with the size of the move and with maturity.

</details>

**Q8** (`s1_l2_sized`, topic `duration:sized_pnl`, seed 1864746)

You are long GBP 100m face of a 4.25% 10Y gilt. Using the Givens, estimate your P&L if yields move -50bp. Are you long or short duration?

Givens:

| Given | Value |
|---|---|
| Face (GBP, + long / - short) | 100,000,000 |
| Price (per 100) | 102.04 |
| Modified duration (years) | 8.1086 |
| Convexity (years^2) | 77.99 |
| Yield move (bp, parallel) | -50 |

- *P&L (GBP thousands)*: **4,237 k**
- *Duration*: **Long**
- *Written*: Show the duration and convexity terms.

<details><summary>Model answer</summary>

**About +GBP 4.24m.**

(a) Approximation: duration term +GBP 4.14m + convexity term +GBP 99.5k = **+GBP 4.24m**.
(b) Exact full repricing (engine): **+GBP 4.24m**.
Gap: +GBP 1.8k (+0.04% of the move), from the higher-order terms the two-term Taylor expansion leaves out. It grows with the size of the move and with maturity.

</details>

**Q9** (`s1_l2_asym_sized`, topic `convexity:sized`, seed 1864777)

You own GBP 100m of a 4% 30Y gilt. By how much does your gain if yields fall 100bp exceed your loss if they rise 100bp? Use the Givens.

Givens:

| Given | Value |
|---|---|
| Face (GBP) | 100,000,000 |
| Price (per 100) | 100 |
| Convexity (years^2) | 420.81 |
| Size of the move (bp) | 100 |

- *Gain minus |loss| (GBP thousands)*: **4,208 k**
- *Written*: Explain where the difference comes from.

<details><summary>Model answer</summary>

**About +GBP 4.21m.**

1. The duration terms are equal and opposite, so they cancel; the two convexity terms add: 2 x 0.5 C P dy^2 = C P dy^2 = +GBP 4.21m.
2. Exact (engine): +GBP 4.24m; gap +GBP 27.7k from higher-order terms.

</details>

**Q10** (`s1_l2_asym_sized`, topic `convexity:sized`, seed 1864808)

You own GBP 100m of a 4% 30Y gilt. By how much does your gain if yields fall 75bp exceed your loss if they rise 75bp? Use the Givens.

Givens:

| Given | Value |
|---|---|
| Face (GBP) | 100,000,000 |
| Price (per 100) | 100 |
| Convexity (years^2) | 420.81 |
| Size of the move (bp) | 75 |

- *Gain minus |loss| (GBP thousands)*: **2,367 k**
- *Written*: Explain where the difference comes from.

<details><summary>Model answer</summary>

**About +GBP 2.37m.**

1. The duration terms are equal and opposite, so they cancel; the two convexity terms add: 2 x 0.5 C P dy^2 = C P dy^2 = +GBP 2.37m.
2. Exact (engine): +GBP 2.38m; gap +GBP 8.7k from higher-order terms.

</details>

### Level 3: calculations plus subtler concepts

**Q1** (`s1_l3_big_move`, topic `convexity:approx_vs_exact`, seed 1969258)

You own GBP 100m of a 4% 20Y gilt and yields move +150bp. Give (a) the duration+convexity approximation and (b) the exact repriced P&L. Which is closer to the truth, and why do they differ?

Givens:

| Given | Value |
|---|---|
| Face (GBP) | 100,000,000 |
| Coupon (%) | 4 |
| Maturity (years) | 20 |
| Yield (%) | 4 |
| Coupons per year | 2 |
| Price (per 100) | 100 |
| Modified duration | 13.6777 |
| Convexity | 239.88 |
| Yield move (bp) | 150 |

- *(a) Approximation (GBP k)*: **-17,818 k**
- *(b) Exact (GBP k)*: **-18,059 k**
- *Written*: Explain the gap.

<details><summary>Model answer</summary>

**(a) -GBP 17.82m, (b) -GBP 18.06m.**

(a) Approximation: duration term -GBP 20.52m + convexity term +GBP 2.70m = **-GBP 17.82m**.
(b) Exact full repricing (engine): **-GBP 18.06m**.
Gap: -GBP 240.6k (-1.33% of the move), from the higher-order terms the two-term Taylor expansion leaves out. It grows with the size of the move and with maturity.

</details>

**Q2** (`s1_l3_big_move`, topic `convexity:approx_vs_exact`, seed 1969289)

You own GBP 100m of a 4% 20Y gilt and yields move -200bp. Give (a) the duration+convexity approximation and (b) the exact repriced P&L. Which is closer to the truth, and why do they differ?

Givens:

| Given | Value |
|---|---|
| Face (GBP) | 100,000,000 |
| Coupon (%) | 4 |
| Maturity (years) | 20 |
| Yield (%) | 4 |
| Coupons per year | 2 |
| Price (per 100) | 100 |
| Modified duration | 13.6777 |
| Convexity | 239.88 |
| Yield move (bp) | -200 |

- *(a) Approximation (GBP k)*: **32,153 k**
- *(b) Exact (GBP k)*: **32,835 k**
- *Written*: Explain the gap.

<details><summary>Model answer</summary>

**(a) +GBP 32.15m, (b) +GBP 32.83m.**

(a) Approximation: duration term +GBP 27.36m + convexity term +GBP 4.80m = **+GBP 32.15m**.
(b) Exact full repricing (engine): **+GBP 32.83m**.
Gap: +GBP 681.7k (+2.08% of the move), from the higher-order terms the two-term Taylor expansion leaves out. It grows with the size of the move and with maturity.

</details>

**Q3** (`s1_l3_compute`, topic `duration:compute`, seed 1969320)

Compute the bond's **modified duration** and the position's **DV01** from the bond details in the Givens.

Givens:

| Given | Value |
|---|---|
| Coupon (% a year) | 3 |
| Maturity (years) | 7 |
| Coupons per year | 1 |
| Yield (%, compounded at the coupon frequency) | 4 |
| Face (GBP) | 100,000,000 |

- *Modified duration (years)*: **6.15 y**
- *DV01 (GBP per bp)*: **57,802**
- *Written*: Show the steps.

<details><summary>Model answer</summary>

**D_mod 6.149, DV01 +GBP 57.8k per bp.**

1. Price = sum of CF_k / (1 + y/f)^k = 93.9979.
2. Macaulay = sum of t_k x PV_k / P = 6.3953 years.
3. D_mod = D_mac / (1 + y/f) = 6.3953 / 1.0400 = 6.1493.
4. DV01 = D_mod x P/100 x face x 0.0001 = +GBP 57.8k.

</details>

**Q4** (`s1_l3_big_move`, topic `convexity:approx_vs_exact`, seed 1969351)

You own GBP 100m of a 4% 20Y gilt and yields move +200bp. Give (a) the duration+convexity approximation and (b) the exact repriced P&L. Which is closer to the truth, and why do they differ?

Givens:

| Given | Value |
|---|---|
| Face (GBP) | 100,000,000 |
| Coupon (%) | 4 |
| Maturity (years) | 20 |
| Yield (%) | 4 |
| Coupons per year | 2 |
| Price (per 100) | 100 |
| Modified duration | 13.6777 |
| Convexity | 239.88 |
| Yield move (bp) | 200 |

- *(a) Approximation (GBP k)*: **-22,558 k**
- *(b) Exact (GBP k)*: **-23,115 k**
- *Written*: Explain the gap.

<details><summary>Model answer</summary>

**(a) -GBP 22.56m, (b) -GBP 23.11m.**

(a) Approximation: duration term -GBP 27.36m + convexity term +GBP 4.80m = **-GBP 22.56m**.
(b) Exact full repricing (engine): **-GBP 23.11m**.
Gap: -GBP 556.9k (-2.41% of the move), from the higher-order terms the two-term Taylor expansion leaves out. It grows with the size of the move and with maturity.

</details>

**Q5** (`s1_l3_big_move`, topic `convexity:approx_vs_exact`, seed 1969382)

You own GBP 100m of a 4% 20Y gilt and yields move +200bp. Give (a) the duration+convexity approximation and (b) the exact repriced P&L. Which is closer to the truth, and why do they differ?

Givens:

| Given | Value |
|---|---|
| Face (GBP) | 100,000,000 |
| Coupon (%) | 4 |
| Maturity (years) | 20 |
| Yield (%) | 4 |
| Coupons per year | 2 |
| Price (per 100) | 100 |
| Modified duration | 13.6777 |
| Convexity | 239.88 |
| Yield move (bp) | 200 |

- *(a) Approximation (GBP k)*: **-22,558 k**
- *(b) Exact (GBP k)*: **-23,115 k**
- *Written*: Explain the gap.

<details><summary>Model answer</summary>

**(a) -GBP 22.56m, (b) -GBP 23.11m.**

(a) Approximation: duration term -GBP 27.36m + convexity term +GBP 4.80m = **-GBP 22.56m**.
(b) Exact full repricing (engine): **-GBP 23.11m**.
Gap: -GBP 556.9k (-2.41% of the move), from the higher-order terms the two-term Taylor expansion leaves out. It grows with the size of the move and with maturity.

</details>

**Q6** (`s1_l3_compute`, topic `duration:compute`, seed 1969413)

Compute the bond's **modified duration** and the position's **DV01** from the bond details in the Givens.

Givens:

| Given | Value |
|---|---|
| Coupon (% a year) | 4 |
| Maturity (years) | 5 |
| Coupons per year | 2 |
| Yield (%, compounded at the coupon frequency) | 4.5 |
| Face (GBP) | 100,000,000 |

- *Modified duration (years)*: **4.47 y**
- *DV01 (GBP per bp)*: **43,755**
- *Written*: Show the steps.

<details><summary>Model answer</summary>

**D_mod 4.475, DV01 +GBP 43.8k per bp.**

1. Price = sum of CF_k / (1 + y/f)^k = 97.7834.
2. Macaulay = sum of t_k x PV_k / P = 4.5753 years.
3. D_mod = D_mac / (1 + y/f) = 4.5753 / 1.0225 = 4.4747.
4. DV01 = D_mod x P/100 x face x 0.0001 = +GBP 43.8k.

</details>

**Q7** (`s1_l3_compute`, topic `duration:compute`, seed 1969444)

Compute the bond's **modified duration** and the position's **DV01** from the bond details in the Givens.

Givens:

| Given | Value |
|---|---|
| Coupon (% a year) | 4 |
| Maturity (years) | 7 |
| Coupons per year | 2 |
| Yield (%, compounded at the coupon frequency) | 4.5 |
| Face (GBP) | 100,000,000 |

- *Modified duration (years)*: **6.02 y**
- *DV01 (GBP per bp)*: **58,441**
- *Written*: Show the steps.

<details><summary>Model answer</summary>

**D_mod 6.023, DV01 +GBP 58.4k per bp.**

1. Price = sum of CF_k / (1 + y/f)^k = 97.0260.
2. Macaulay = sum of t_k x PV_k / P = 6.1588 years.
3. D_mod = D_mac / (1 + y/f) = 6.1588 / 1.0225 = 6.0233.
4. DV01 = D_mod x P/100 x face x 0.0001 = +GBP 58.4k.

</details>

**Q8** (`s1_l3_compute`, topic `duration:compute`, seed 1969475)

Compute the bond's **modified duration** and the position's **DV01** from the bond details in the Givens.

Givens:

| Given | Value |
|---|---|
| Coupon (% a year) | 5 |
| Maturity (years) | 7 |
| Coupons per year | 2 |
| Yield (%, compounded at the coupon frequency) | 4.5 |
| Face (GBP) | 100,000,000 |

- *Modified duration (years)*: **5.88 y**
- *DV01 (GBP per bp)*: **60,518**
- *Written*: Show the steps.

<details><summary>Model answer</summary>

**D_mod 5.877, DV01 +GBP 60.5k per bp.**

1. Price = sum of CF_k / (1 + y/f)^k = 102.9740.
2. Macaulay = sum of t_k x PV_k / P = 6.0092 years.
3. D_mod = D_mac / (1 + y/f) = 6.0092 / 1.0225 = 5.8770.
4. DV01 = D_mod x P/100 x face x 0.0001 = +GBP 60.5k.

</details>

**Q9** (`s1_l3_big_move`, topic `convexity:approx_vs_exact`, seed 1969506)

You own GBP 100m of a 4% 30Y gilt and yields move -200bp. Give (a) the duration+convexity approximation and (b) the exact repriced P&L. Which is closer to the truth, and why do they differ?

Givens:

| Given | Value |
|---|---|
| Face (GBP) | 100,000,000 |
| Coupon (%) | 4 |
| Maturity (years) | 30 |
| Yield (%) | 4 |
| Coupons per year | 2 |
| Price (per 100) | 100 |
| Modified duration | 17.3804 |
| Convexity | 420.81 |
| Yield move (bp) | -200 |

- *(a) Approximation (GBP k)*: **43,177 k**
- *(b) Exact (GBP k)*: **44,955 k**
- *Written*: Explain the gap.

<details><summary>Model answer</summary>

**(a) +GBP 43.18m, (b) +GBP 44.96m.**

(a) Approximation: duration term +GBP 34.76m + convexity term +GBP 8.42m = **+GBP 43.18m**.
(b) Exact full repricing (engine): **+GBP 44.96m**.
Gap: +GBP 1.78m (+3.96% of the move), from the higher-order terms the two-term Taylor expansion leaves out. It grows with the size of the move and with maturity.

</details>

**Q10** (`s1_l3_big_move`, topic `convexity:approx_vs_exact`, seed 1969537)

You own GBP 100m of a 4% 20Y gilt and yields move -150bp. Give (a) the duration+convexity approximation and (b) the exact repriced P&L. Which is closer to the truth, and why do they differ?

Givens:

| Given | Value |
|---|---|
| Face (GBP) | 100,000,000 |
| Coupon (%) | 4 |
| Maturity (years) | 20 |
| Yield (%) | 4 |
| Coupons per year | 2 |
| Price (per 100) | 100 |
| Modified duration | 13.6777 |
| Convexity | 239.88 |
| Yield move (bp) | -150 |

- *(a) Approximation (GBP k)*: **23,215 k**
- *(b) Exact (GBP k)*: **23,495 k**
- *Written*: Explain the gap.

<details><summary>Model answer</summary>

**(a) +GBP 23.22m, (b) +GBP 23.50m.**

(a) Approximation: duration term +GBP 20.52m + convexity term +GBP 2.70m = **+GBP 23.22m**.
(b) Exact full repricing (engine): **+GBP 23.50m**.
Gap: +GBP 280.0k (+1.19% of the move), from the higher-order terms the two-term Taylor expansion leaves out. It grows with the size of the move and with maturity.

</details>

## 2A-2 Stage 2: Bond futures and repo

### Level 1: directional intuition, no calculations

**Q1** (`s2_l1_futures`, topic `duration:futures`, seed 1767719)

You are **long Long Gilt futures**. Long or short duration? Do you gain or lose if yields fall 10bp?

- *Duration*: **Long**
- *P&L*: **Gain**
- *Written*: Explain the link to the cheapest-to-deliver bond.

<details><summary>Model answer</summary>

**Long duration; you gain.**

1. A bond future tracks the cheapest-to-deliver bond (scaled by its conversion factor), so long futures behave like a long bond with no cash outlay: leveraged duration.
2. Its DV01 is about the CTD's DV01 divided by the CF.

</details>

**Q2** (`s2_l1_futures`, topic `duration:futures`, seed 1767750)

You are **long Long Gilt futures**. Long or short duration? Do you gain or lose if yields fall 10bp?

- *Duration*: **Long**
- *P&L*: **Gain**
- *Written*: Explain the link to the cheapest-to-deliver bond.

<details><summary>Model answer</summary>

**Long duration; you gain.**

1. A bond future tracks the cheapest-to-deliver bond (scaled by its conversion factor), so long futures behave like a long bond with no cash outlay: leveraged duration.
2. Its DV01 is about the CTD's DV01 divided by the CF.

</details>

**Q3** (`s2_l1_futures`, topic `duration:futures`, seed 1767781)

You are **long Long Gilt futures**. Long or short duration? Do you gain or lose if yields rise 10bp?

- *Duration*: **Long**
- *P&L*: **Lose**
- *Written*: Explain the link to the cheapest-to-deliver bond.

<details><summary>Model answer</summary>

**Long duration; you lose.**

1. A bond future tracks the cheapest-to-deliver bond (scaled by its conversion factor), so long futures behave like a long bond with no cash outlay: leveraged duration.
2. Its DV01 is about the CTD's DV01 divided by the CF.

</details>

**Q4** (`s2_l1_repo`, topic `duration:repo_carry`, seed 1767812)

You buy a gilt trading close to par with a 5.00% coupon and fund it in repo at 5.00%. Is your carry positive or negative? Are you still long duration?

- *Carry*: **Negative**
- *Duration*: **Long**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Negative carry; still long duration.**

1. Carry = coupon income minus the repo cost of the cash you borrowed. Near par, that is roughly coupon < repo rate.
2. Funding in repo changes the cash you put up, not the rate risk: you still own the bond's duration. Carry is to bonds what theta is to options.

</details>

**Q5** (`s2_l1_repo`, topic `duration:repo_carry`, seed 1767843)

You buy a gilt trading close to par with a 5.00% coupon and fund it in repo at 3.50%. Is your carry positive or negative? Are you still long duration?

- *Carry*: **Positive**
- *Duration*: **Long**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Positive carry; still long duration.**

1. Carry = coupon income minus the repo cost of the cash you borrowed. Near par, that is roughly coupon > repo rate.
2. Funding in repo changes the cash you put up, not the rate risk: you still own the bond's duration. Carry is to bonds what theta is to options.

</details>

**Q6** (`s2_l1_repo`, topic `duration:repo_carry`, seed 1767874)

You buy a gilt trading close to par with a 5.00% coupon and fund it in repo at 3.75%. Is your carry positive or negative? Are you still long duration?

- *Carry*: **Positive**
- *Duration*: **Long**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Positive carry; still long duration.**

1. Carry = coupon income minus the repo cost of the cash you borrowed. Near par, that is roughly coupon > repo rate.
2. Funding in repo changes the cash you put up, not the rate risk: you still own the bond's duration. Carry is to bonds what theta is to options.

</details>

**Q7** (`s2_l1_futures`, topic `duration:futures`, seed 1767905)

You are **long Long Gilt futures**. Long or short duration? Do you gain or lose if yields rise 10bp?

- *Duration*: **Long**
- *P&L*: **Lose**
- *Written*: Explain the link to the cheapest-to-deliver bond.

<details><summary>Model answer</summary>

**Long duration; you lose.**

1. A bond future tracks the cheapest-to-deliver bond (scaled by its conversion factor), so long futures behave like a long bond with no cash outlay: leveraged duration.
2. Its DV01 is about the CTD's DV01 divided by the CF.

</details>

**Q8** (`s2_l1_repo`, topic `duration:repo_carry`, seed 1767936)

You buy a gilt trading close to par with a 5.00% coupon and fund it in repo at 3.75%. Is your carry positive or negative? Are you still long duration?

- *Carry*: **Positive**
- *Duration*: **Long**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Positive carry; still long duration.**

1. Carry = coupon income minus the repo cost of the cash you borrowed. Near par, that is roughly coupon > repo rate.
2. Funding in repo changes the cash you put up, not the rate risk: you still own the bond's duration. Carry is to bonds what theta is to options.

</details>

**Q9** (`s2_l1_repo`, topic `duration:repo_carry`, seed 1767967)

You buy a gilt trading close to par with a 5.00% coupon and fund it in repo at 5.50%. Is your carry positive or negative? Are you still long duration?

- *Carry*: **Negative**
- *Duration*: **Long**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Negative carry; still long duration.**

1. Carry = coupon income minus the repo cost of the cash you borrowed. Near par, that is roughly coupon < repo rate.
2. Funding in repo changes the cash you put up, not the rate risk: you still own the bond's duration. Carry is to bonds what theta is to options.

</details>

**Q10** (`s2_l1_repo`, topic `duration:repo_carry`, seed 1767998)

You buy a gilt trading close to par with a 4.50% coupon and fund it in repo at 5.00%. Is your carry positive or negative? Are you still long duration?

- *Carry*: **Negative**
- *Duration*: **Long**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Negative carry; still long duration.**

1. Carry = coupon income minus the repo cost of the cash you borrowed. Near par, that is roughly coupon < repo rate.
2. Funding in repo changes the cash you put up, not the rate risk: you still own the bond's duration. Carry is to bonds what theta is to options.

</details>

### Level 2: combinations, light calculations with every input given

**Q1** (`s2_l2_fut_pnl`, topic `duration:futures`, seed 1872448)

You are short 1000 Long Gilt futures. Using the Givens, what is your P&L if yields move -20bp?

Givens:

| Given | Value |
|---|---|
| Contracts (+ long / - short) | -1,000 |
| DV01 per contract (GBP per bp) | 85 |
| Yield move (bp) | -20 |

- *P&L (GBP thousands)*: **-1,700 k**
- *Written*: Explain.

<details><summary>Model answer</summary>

**-GBP 1.70m.**

 P&L ~ -(contracts x DV01) x move = -(-1000 x 85.0) x -20. Long futures gain when yields fall.

</details>

**Q2** (`s2_l2_fut_pnl`, topic `duration:futures`, seed 1872479)

You are long 1000 Long Gilt futures. Using the Givens, what is your P&L if yields move +10bp?

Givens:

| Given | Value |
|---|---|
| Contracts (+ long / - short) | 1,000 |
| DV01 per contract (GBP per bp) | 85 |
| Yield move (bp) | 10 |

- *P&L (GBP thousands)*: **-850.00 k**
- *Written*: Explain.

<details><summary>Model answer</summary>

**-GBP 850.0k.**

 P&L ~ -(contracts x DV01) x move = -(1000 x 85.0) x +10. Long futures gain when yields fall.

</details>

**Q3** (`s2_l2_fut_pnl`, topic `duration:futures`, seed 1872510)

You are short 200 Long Gilt futures. Using the Givens, what is your P&L if yields move -10bp?

Givens:

| Given | Value |
|---|---|
| Contracts (+ long / - short) | -200 |
| DV01 per contract (GBP per bp) | 85 |
| Yield move (bp) | -10 |

- *P&L (GBP thousands)*: **-170.00 k**
- *Written*: Explain.

<details><summary>Model answer</summary>

**-GBP 170.0k.**

 P&L ~ -(contracts x DV01) x move = -(-200 x 85.0) x -10. Long futures gain when yields fall.

</details>

**Q4** (`s2_l2_carry`, topic `duration:repo_carry`, seed 1872541)

You buy GBP 100m of a 4.50% 10Y gilt and fund it in 3-month repo. Using the Givens, what is your carry over 3 months (ignore pull-to-par)? Are you still long duration?

Givens:

| Given | Value |
|---|---|
| Face (GBP) | 100,000,000 |
| Coupon (% a year) | 4.5 |
| Dirty price (per 100) | 103.97 |
| Repo rate (% a year) | 3.75 |
| Horizon (years) | 0.25 |

- *Carry (GBP thousands)*: **150.32 k**
- *Duration*: **Long**
- *Written*: Explain the carry and why duration is unchanged.

<details><summary>Model answer</summary>

**Carry +GBP 150.3k; still long duration.**

1. Coupon: 4.50% x 100m x 0.25 = +GBP 1.12m.
2. Repo: 3.75% x 103.966/100 x 100m x 0.25 = -GBP 974.7k.
3. Funding changes the cash outlay, not the rate risk.

</details>

**Q5** (`s2_l2_carry`, topic `duration:repo_carry`, seed 1872572)

You buy GBP 100m of a 4.75% 5Y gilt and fund it in 3-month repo. Using the Givens, what is your carry over 3 months (ignore pull-to-par)? Are you still long duration?

Givens:

| Given | Value |
|---|---|
| Face (GBP) | 100,000,000 |
| Coupon (% a year) | 4.75 |
| Dirty price (per 100) | 105.62 |
| Repo rate (% a year) | 3.75 |
| Horizon (years) | 0.25 |

- *Carry (GBP thousands)*: **197.34 k**
- *Duration*: **Long**
- *Written*: Explain the carry and why duration is unchanged.

<details><summary>Model answer</summary>

**Carry +GBP 197.3k; still long duration.**

1. Coupon: 4.75% x 100m x 0.25 = +GBP 1.19m.
2. Repo: 3.75% x 105.617/100 x 100m x 0.25 = -GBP 990.2k.
3. Funding changes the cash outlay, not the rate risk.

</details>

**Q6** (`s2_l2_fut_pnl`, topic `duration:futures`, seed 1872603)

You are short 200 Long Gilt futures. Using the Givens, what is your P&L if yields move -5bp?

Givens:

| Given | Value |
|---|---|
| Contracts (+ long / - short) | -200 |
| DV01 per contract (GBP per bp) | 101 |
| Yield move (bp) | -5 |

- *P&L (GBP thousands)*: **-101.00 k**
- *Written*: Explain.

<details><summary>Model answer</summary>

**-GBP 101.0k.**

 P&L ~ -(contracts x DV01) x move = -(-200 x 101.0) x -5. Long futures gain when yields fall.

</details>

**Q7** (`s2_l2_fut_pnl`, topic `duration:futures`, seed 1872634)

You are short 500 Long Gilt futures. Using the Givens, what is your P&L if yields move +10bp?

Givens:

| Given | Value |
|---|---|
| Contracts (+ long / - short) | -500 |
| DV01 per contract (GBP per bp) | 101 |
| Yield move (bp) | 10 |

- *P&L (GBP thousands)*: **505.00 k**
- *Written*: Explain.

<details><summary>Model answer</summary>

**+GBP 505.0k.**

 P&L ~ -(contracts x DV01) x move = -(-500 x 101.0) x +10. Long futures gain when yields fall.

</details>

**Q8** (`s2_l2_fut_pnl`, topic `duration:futures`, seed 1872665)

You are short 1000 Long Gilt futures. Using the Givens, what is your P&L if yields move -5bp?

Givens:

| Given | Value |
|---|---|
| Contracts (+ long / - short) | -1,000 |
| DV01 per contract (GBP per bp) | 101 |
| Yield move (bp) | -5 |

- *P&L (GBP thousands)*: **-505.00 k**
- *Written*: Explain.

<details><summary>Model answer</summary>

**-GBP 505.0k.**

 P&L ~ -(contracts x DV01) x move = -(-1000 x 101.0) x -5. Long futures gain when yields fall.

</details>

**Q9** (`s2_l2_fut_pnl`, topic `duration:futures`, seed 1872696)

You are short 1000 Long Gilt futures. Using the Givens, what is your P&L if yields move +10bp?

Givens:

| Given | Value |
|---|---|
| Contracts (+ long / - short) | -1,000 |
| DV01 per contract (GBP per bp) | 101 |
| Yield move (bp) | 10 |

- *P&L (GBP thousands)*: **1,010 k**
- *Written*: Explain.

<details><summary>Model answer</summary>

**+GBP 1.01m.**

 P&L ~ -(contracts x DV01) x move = -(-1000 x 101.0) x +10. Long futures gain when yields fall.

</details>

**Q10** (`s2_l2_fut_pnl`, topic `duration:futures`, seed 1872727)

You are short 500 Long Gilt futures. Using the Givens, what is your P&L if yields move -5bp?

Givens:

| Given | Value |
|---|---|
| Contracts (+ long / - short) | -500 |
| DV01 per contract (GBP per bp) | 92 |
| Yield move (bp) | -5 |

- *P&L (GBP thousands)*: **-230.00 k**
- *Written*: Explain.

<details><summary>Model answer</summary>

**-GBP 230.0k.**

 P&L ~ -(contracts x DV01) x move = -(-500 x 92.0) x -5. Long futures gain when yields fall.

</details>

### Level 3: calculations plus subtler concepts

**Q1** (`s2_l3_hedge`, topic `duration:futures_hedge`, seed 1977177)

You own GBP 100m of a 4.5% 8Y gilt and want to hedge its duration with Long Gilt futures. How many contracts do you sell? (Givens)

Givens:

| Given | Value |
|---|---|
| DV01 of your gilt position (GBP per bp) | 69,233 |
| CTD DV01 per GBP 100k face (GBP per bp) | 75.78 |
| CTD conversion factor | 1.0185 |

- *Contracts to sell*: **930.51**
- *Written*: Explain the DV01 per contract and what risks remain.

<details><summary>Model answer</summary>

**Sell about 931 contracts.**

1. A future behaves like CTD/CF, so DV01 per contract = 75.78 / 1.0185 = 74.40.
2. Contracts = 69,233 / 74.40 = 931.
3. Left over: curve risk (your bond is not the CTD), basis risk and the CTD switching.

</details>

**Q2** (`s2_l3_hedge`, topic `duration:futures_hedge`, seed 1977208)

You own GBP 50m of a 4.5% 10Y gilt and want to hedge its duration with Long Gilt futures. How many contracts do you sell? (Givens)

Givens:

| Given | Value |
|---|---|
| DV01 of your gilt position (GBP per bp) | 41,865 |
| CTD DV01 per GBP 100k face (GBP per bp) | 75.78 |
| CTD conversion factor | 1.0185 |

- *Contracts to sell*: **562.67**
- *Written*: Explain the DV01 per contract and what risks remain.

<details><summary>Model answer</summary>

**Sell about 563 contracts.**

1. A future behaves like CTD/CF, so DV01 per contract = 75.78 / 1.0185 = 74.40.
2. Contracts = 41,865 / 74.40 = 563.
3. Left over: curve risk (your bond is not the CTD), basis risk and the CTD switching.

</details>

**Q3** (`s2_l3_hedge`, topic `duration:futures_hedge`, seed 1977239)

You own GBP 100m of a 4.5% 12Y gilt and want to hedge its duration with Long Gilt futures. How many contracts do you sell? (Givens)

Givens:

| Given | Value |
|---|---|
| DV01 of your gilt position (GBP per bp) | 97,248 |
| CTD DV01 per GBP 100k face (GBP per bp) | 75.78 |
| CTD conversion factor | 1.0185 |

- *Contracts to sell*: **1,307**
- *Written*: Explain the DV01 per contract and what risks remain.

<details><summary>Model answer</summary>

**Sell about 1,307 contracts.**

1. A future behaves like CTD/CF, so DV01 per contract = 75.78 / 1.0185 = 74.40.
2. Contracts = 97,248 / 74.40 = 1,307.
3. Left over: curve risk (your bond is not the CTD), basis risk and the CTD switching.

</details>

**Q4** (`s2_l3_hedge`, topic `duration:futures_hedge`, seed 1977270)

You own GBP 50m of a 4.5% 10Y gilt and want to hedge its duration with Long Gilt futures. How many contracts do you sell? (Givens)

Givens:

| Given | Value |
|---|---|
| DV01 of your gilt position (GBP per bp) | 41,865 |
| CTD DV01 per GBP 100k face (GBP per bp) | 75.78 |
| CTD conversion factor | 1.0185 |

- *Contracts to sell*: **562.67**
- *Written*: Explain the DV01 per contract and what risks remain.

<details><summary>Model answer</summary>

**Sell about 563 contracts.**

1. A future behaves like CTD/CF, so DV01 per contract = 75.78 / 1.0185 = 74.40.
2. Contracts = 41,865 / 74.40 = 563.
3. Left over: curve risk (your bond is not the CTD), basis risk and the CTD switching.

</details>

**Q5** (`s2_l3_hedge`, topic `duration:futures_hedge`, seed 1977301)

You own GBP 200m of a 4.5% 12Y gilt and want to hedge its duration with Long Gilt futures. How many contracts do you sell? (Givens)

Givens:

| Given | Value |
|---|---|
| DV01 of your gilt position (GBP per bp) | 194,496 |
| CTD DV01 per GBP 100k face (GBP per bp) | 75.78 |
| CTD conversion factor | 1.0185 |

- *Contracts to sell*: **2,614**
- *Written*: Explain the DV01 per contract and what risks remain.

<details><summary>Model answer</summary>

**Sell about 2,614 contracts.**

1. A future behaves like CTD/CF, so DV01 per contract = 75.78 / 1.0185 = 74.40.
2. Contracts = 194,496 / 74.40 = 2,614.
3. Left over: curve risk (your bond is not the CTD), basis risk and the CTD switching.

</details>

**Q6** (`s2_l3_hedge`, topic `duration:futures_hedge`, seed 1977332)

You own GBP 200m of a 4.5% 8Y gilt and want to hedge its duration with Long Gilt futures. How many contracts do you sell? (Givens)

Givens:

| Given | Value |
|---|---|
| DV01 of your gilt position (GBP per bp) | 138,466 |
| CTD DV01 per GBP 100k face (GBP per bp) | 75.78 |
| CTD conversion factor | 1.0185 |

- *Contracts to sell*: **1,861**
- *Written*: Explain the DV01 per contract and what risks remain.

<details><summary>Model answer</summary>

**Sell about 1,861 contracts.**

1. A future behaves like CTD/CF, so DV01 per contract = 75.78 / 1.0185 = 74.40.
2. Contracts = 138,466 / 74.40 = 1,861.
3. Left over: curve risk (your bond is not the CTD), basis risk and the CTD switching.

</details>

**Q7** (`s2_l3_hedge`, topic `duration:futures_hedge`, seed 1977363)

You own GBP 200m of a 4.5% 12Y gilt and want to hedge its duration with Long Gilt futures. How many contracts do you sell? (Givens)

Givens:

| Given | Value |
|---|---|
| DV01 of your gilt position (GBP per bp) | 194,496 |
| CTD DV01 per GBP 100k face (GBP per bp) | 75.78 |
| CTD conversion factor | 1.0185 |

- *Contracts to sell*: **2,614**
- *Written*: Explain the DV01 per contract and what risks remain.

<details><summary>Model answer</summary>

**Sell about 2,614 contracts.**

1. A future behaves like CTD/CF, so DV01 per contract = 75.78 / 1.0185 = 74.40.
2. Contracts = 194,496 / 74.40 = 2,614.
3. Left over: curve risk (your bond is not the CTD), basis risk and the CTD switching.

</details>

**Q8** (`s2_l3_hedge`, topic `duration:futures_hedge`, seed 1977394)

You own GBP 200m of a 4.5% 10Y gilt and want to hedge its duration with Long Gilt futures. How many contracts do you sell? (Givens)

Givens:

| Given | Value |
|---|---|
| DV01 of your gilt position (GBP per bp) | 167,459 |
| CTD DV01 per GBP 100k face (GBP per bp) | 75.78 |
| CTD conversion factor | 1.0185 |

- *Contracts to sell*: **2,251**
- *Written*: Explain the DV01 per contract and what risks remain.

<details><summary>Model answer</summary>

**Sell about 2,251 contracts.**

1. A future behaves like CTD/CF, so DV01 per contract = 75.78 / 1.0185 = 74.40.
2. Contracts = 167,459 / 74.40 = 2,251.
3. Left over: curve risk (your bond is not the CTD), basis risk and the CTD switching.

</details>

**Q9** (`s2_l3_hedge`, topic `duration:futures_hedge`, seed 1977425)

You own GBP 100m of a 4.5% 12Y gilt and want to hedge its duration with Long Gilt futures. How many contracts do you sell? (Givens)

Givens:

| Given | Value |
|---|---|
| DV01 of your gilt position (GBP per bp) | 97,248 |
| CTD DV01 per GBP 100k face (GBP per bp) | 75.78 |
| CTD conversion factor | 1.0185 |

- *Contracts to sell*: **1,307**
- *Written*: Explain the DV01 per contract and what risks remain.

<details><summary>Model answer</summary>

**Sell about 1,307 contracts.**

1. A future behaves like CTD/CF, so DV01 per contract = 75.78 / 1.0185 = 74.40.
2. Contracts = 97,248 / 74.40 = 1,307.
3. Left over: curve risk (your bond is not the CTD), basis risk and the CTD switching.

</details>

**Q10** (`s2_l3_hedge`, topic `duration:futures_hedge`, seed 1977456)

You own GBP 200m of a 4.5% 10Y gilt and want to hedge its duration with Long Gilt futures. How many contracts do you sell? (Givens)

Givens:

| Given | Value |
|---|---|
| DV01 of your gilt position (GBP per bp) | 167,459 |
| CTD DV01 per GBP 100k face (GBP per bp) | 75.78 |
| CTD conversion factor | 1.0185 |

- *Contracts to sell*: **2,251**
- *Written*: Explain the DV01 per contract and what risks remain.

<details><summary>Model answer</summary>

**Sell about 2,251 contracts.**

1. A future behaves like CTD/CF, so DV01 per contract = 75.78 / 1.0185 = 74.40.
2. Contracts = 167,459 / 74.40 = 2,251.
3. Left over: curve risk (your bond is not the CTD), basis risk and the CTD switching.

</details>

## 2A-3 Stage 3: Swaps

### Level 1: directional intuition, no calculations

**Q1** (`s3_l1_forward`, topic `duration:forward_swaps`, seed 1775638)

You receive fixed on a **2Y3Y forward-starting swap**. Where along the curve is your duration?

- *Exposure*: **Long duration around 5Y, short around 2Y**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Long duration around 5Y, short around 2Y.** A 2Y3Y receiver = receive 5Y and pay 2Y: the near cash flows cancel, leaving a bet on the 2Y3Y forward rate (long the 5Y point, short the 2Y point).

</details>

**Q2** (`s3_l1_forward`, topic `duration:forward_swaps`, seed 1775669)

You receive fixed on a **5Y5Y forward-starting swap**. Where along the curve is your duration?

- *Exposure*: **Long duration around 10Y, short around 5Y**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Long duration around 10Y, short around 5Y.** A 5Y5Y receiver = receive 10Y and pay 5Y: the near cash flows cancel, leaving a bet on the 5Y5Y forward rate (long the 10Y point, short the 5Y point).

</details>

**Q3** (`s3_l1_floater`, topic `duration:floaters`, seed 1775700)

GBP 100m of a 10Y SONIA floating-rate note (resets quarterly) vs GBP 100m of a 10Y fixed bond. Which one has almost no duration?

- *Answer*: **The floating-rate note: it has almost no duration**
- *Written*: Why?

<details><summary>Model answer</summary>

**The floater.** Its coupon resets to market each period, so after a reset it is worth about par whatever rates did; its only rate risk is until the next reset. Illustration: DV01 +GBP 2.5k vs +GBP 83.9k.

</details>

**Q4** (`s3_l1_floater`, topic `duration:floaters`, seed 1775731)

GBP 100m of a 10Y SONIA floating-rate note (resets quarterly) vs GBP 100m of a 10Y fixed bond. Which one has almost no duration?

- *Answer*: **The floating-rate note: it has almost no duration**
- *Written*: Why?

<details><summary>Model answer</summary>

**The floater.** Its coupon resets to market each period, so after a reset it is worth about par whatever rates did; its only rate risk is until the next reset. Illustration: DV01 +GBP 2.5k vs +GBP 83.9k.

</details>

**Q5** (`s3_l1_forward`, topic `duration:forward_swaps`, seed 1775762)

You receive fixed on a **2Y3Y forward-starting swap**. Where along the curve is your duration?

- *Exposure*: **Long duration around 5Y, short around 2Y**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Long duration around 5Y, short around 2Y.** A 2Y3Y receiver = receive 5Y and pay 2Y: the near cash flows cancel, leaving a bet on the 2Y3Y forward rate (long the 5Y point, short the 2Y point).

</details>

**Q6** (`s3_l1_forward`, topic `duration:forward_swaps`, seed 1775793)

You receive fixed on a **5Y5Y forward-starting swap**. Where along the curve is your duration?

- *Exposure*: **Long duration around 10Y, short around 5Y**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Long duration around 10Y, short around 5Y.** A 5Y5Y receiver = receive 10Y and pay 5Y: the near cash flows cancel, leaving a bet on the 5Y5Y forward rate (long the 10Y point, short the 5Y point).

</details>

**Q7** (`s3_l1_floater`, topic `duration:floaters`, seed 1775824)

GBP 100m of a 5Y SONIA floating-rate note (resets quarterly) vs GBP 100m of a 5Y fixed bond. Which one has almost no duration?

- *Answer*: **The floating-rate note: it has almost no duration**
- *Written*: Why?

<details><summary>Model answer</summary>

**The floater.** Its coupon resets to market each period, so after a reset it is worth about par whatever rates did; its only rate risk is until the next reset. Illustration: DV01 +GBP 2.5k vs +GBP 46.7k.

</details>

**Q8** (`s3_l1_floater`, topic `duration:floaters`, seed 1775855)

GBP 100m of a 5Y SONIA floating-rate note (resets quarterly) vs GBP 100m of a 5Y fixed bond. Which one has almost no duration?

- *Answer*: **The floating-rate note: it has almost no duration**
- *Written*: Why?

<details><summary>Model answer</summary>

**The floater.** Its coupon resets to market each period, so after a reset it is worth about par whatever rates did; its only rate risk is until the next reset. Illustration: DV01 +GBP 2.5k vs +GBP 46.7k.

</details>

**Q9** (`s3_l1_swap`, topic `duration:swaps`, seed 1775886)

You **pay fixed** on a 30Y SONIA swap. Long or short duration? Do you gain or lose if rates fall 10bp?

- *Duration*: **Short**
- *P&L*: **Lose**
- *Written*: Explain with the bond analogy.

<details><summary>Model answer</summary>

**Short duration; you lose.**

1. Receiving fixed = owning a fixed-rate bond funded at the floating rate: you gain when rates fall. Paying fixed is the mirror image.
2. The floating leg resets to market, so it carries almost no duration: all the DV01 is in the fixed leg.

</details>

**Q10** (`s3_l1_forward`, topic `duration:forward_swaps`, seed 1775917)

You receive fixed on a **1Y4Y forward-starting swap**. Where along the curve is your duration?

- *Exposure*: **Long duration around 5Y, short around 1Y**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Long duration around 5Y, short around 1Y.** A 1Y4Y receiver = receive 5Y and pay 1Y: the near cash flows cancel, leaving a bet on the 1Y4Y forward rate (long the 5Y point, short the 1Y point).

</details>

### Level 2: combinations, light calculations with every input given

**Q1** (`s3_l2_swap_pnl`, topic `duration:swaps`, seed 1880367)

You pay fixed on GBP 100m 5Y SONIA at par. Using the Givens, estimate your P&L if rates move +25bp.

Givens:

| Given | Value |
|---|---|
| Position DV01 (GBP per bp, + = long duration) | -46,675 |
| Parallel move (bp) | 25 |

- *P&L (GBP thousands)*: **1,167 k**
- *Duration*: **Short**
- *Written*: Explain, and say why the exact P&L differs slightly.

<details><summary>Model answer</summary>

**About +GBP 1.17m.**

(a) First order: -DV01 x move = +GBP 1.17m.
(b) Exact (engine, curve shifted and repriced): +GBP 1.16m. Gap -GBP 7.0k: the swap's convexity (hurts here).

</details>

**Q2** (`s3_l2_swap_pnl`, topic `duration:swaps`, seed 1880398)

You receive fixed on GBP 100m 10Y SONIA at par. Using the Givens, estimate your P&L if rates move +50bp.

Givens:

| Given | Value |
|---|---|
| Position DV01 (GBP per bp, + = long duration) | 83,885 |
| Parallel move (bp) | 50 |

- *P&L (GBP thousands)*: **-4,194 k**
- *Duration*: **Long**
- *Written*: Explain, and say why the exact P&L differs slightly.

<details><summary>Model answer</summary>

**About -GBP 4.19m.**

(a) First order: -DV01 x move = -GBP 4.19m.
(b) Exact (engine, curve shifted and repriced): -GBP 4.10m. Gap +GBP 96.3k: the swap's convexity (helps here).

</details>

**Q3** (`s3_l2_swap_pnl`, topic `duration:swaps`, seed 1880429)

You pay fixed on GBP 100m 10Y SONIA at par. Using the Givens, estimate your P&L if rates move -25bp.

Givens:

| Given | Value |
|---|---|
| Position DV01 (GBP per bp, + = long duration) | -83,885 |
| Parallel move (bp) | -25 |

- *P&L (GBP thousands)*: **-2,097 k**
- *Duration*: **Short**
- *Written*: Explain, and say why the exact P&L differs slightly.

<details><summary>Model answer</summary>

**About -GBP 2.10m.**

(a) First order: -DV01 x move = -GBP 2.10m.
(b) Exact (engine, curve shifted and repriced): -GBP 2.12m. Gap -GBP 24.7k: the swap's convexity (hurts here).

</details>

**Q4** (`s3_l2_swap_pnl`, topic `duration:swaps`, seed 1880460)

You pay fixed on GBP 100m 5Y SONIA at par. Using the Givens, estimate your P&L if rates move +50bp.

Givens:

| Given | Value |
|---|---|
| Position DV01 (GBP per bp, + = long duration) | -46,675 |
| Parallel move (bp) | 50 |

- *P&L (GBP thousands)*: **2,334 k**
- *Duration*: **Short**
- *Written*: Explain, and say why the exact P&L differs slightly.

<details><summary>Model answer</summary>

**About +GBP 2.33m.**

(a) First order: -DV01 x move = +GBP 2.33m.
(b) Exact (engine, curve shifted and repriced): +GBP 2.31m. Gap -GBP 28.1k: the swap's convexity (hurts here).

</details>

**Q5** (`s3_l2_swap_pnl`, topic `duration:swaps`, seed 1880491)

You pay fixed on GBP 100m 10Y SONIA at par. Using the Givens, estimate your P&L if rates move -50bp.

Givens:

| Given | Value |
|---|---|
| Position DV01 (GBP per bp, + = long duration) | -83,885 |
| Parallel move (bp) | -50 |

- *P&L (GBP thousands)*: **-4,194 k**
- *Duration*: **Short**
- *Written*: Explain, and say why the exact P&L differs slightly.

<details><summary>Model answer</summary>

**About -GBP 4.19m.**

(a) First order: -DV01 x move = -GBP 4.19m.
(b) Exact (engine, curve shifted and repriced): -GBP 4.29m. Gap -GBP 99.4k: the swap's convexity (hurts here).

</details>

**Q6** (`s3_l2_swap_pnl`, topic `duration:swaps`, seed 1880522)

You receive fixed on GBP 100m 10Y SONIA at par. Using the Givens, estimate your P&L if rates move +50bp.

Givens:

| Given | Value |
|---|---|
| Position DV01 (GBP per bp, + = long duration) | 83,885 |
| Parallel move (bp) | 50 |

- *P&L (GBP thousands)*: **-4,194 k**
- *Duration*: **Long**
- *Written*: Explain, and say why the exact P&L differs slightly.

<details><summary>Model answer</summary>

**About -GBP 4.19m.**

(a) First order: -DV01 x move = -GBP 4.19m.
(b) Exact (engine, curve shifted and repriced): -GBP 4.10m. Gap +GBP 96.3k: the swap's convexity (helps here).

</details>

**Q7** (`s3_l2_swap_pnl`, topic `duration:swaps`, seed 1880553)

You receive fixed on GBP 100m 5Y SONIA at par. Using the Givens, estimate your P&L if rates move +50bp.

Givens:

| Given | Value |
|---|---|
| Position DV01 (GBP per bp, + = long duration) | 46,675 |
| Parallel move (bp) | 50 |

- *P&L (GBP thousands)*: **-2,334 k**
- *Duration*: **Long**
- *Written*: Explain, and say why the exact P&L differs slightly.

<details><summary>Model answer</summary>

**About -GBP 2.33m.**

(a) First order: -DV01 x move = -GBP 2.33m.
(b) Exact (engine, curve shifted and repriced): -GBP 2.31m. Gap +GBP 28.1k: the swap's convexity (helps here).

</details>

**Q8** (`s3_l2_swap_pnl`, topic `duration:swaps`, seed 1880584)

You receive fixed on GBP 100m 5Y SONIA at par. Using the Givens, estimate your P&L if rates move -25bp.

Givens:

| Given | Value |
|---|---|
| Position DV01 (GBP per bp, + = long duration) | 46,675 |
| Parallel move (bp) | -25 |

- *P&L (GBP thousands)*: **1,167 k**
- *Duration*: **Long**
- *Written*: Explain, and say why the exact P&L differs slightly.

<details><summary>Model answer</summary>

**About +GBP 1.17m.**

(a) First order: -DV01 x move = +GBP 1.17m.
(b) Exact (engine, curve shifted and repriced): +GBP 1.17m. Gap +GBP 7.1k: the swap's convexity (helps here).

</details>

**Q9** (`s3_l2_swap_pnl`, topic `duration:swaps`, seed 1880615)

You receive fixed on GBP 100m 10Y SONIA at par. Using the Givens, estimate your P&L if rates move +50bp.

Givens:

| Given | Value |
|---|---|
| Position DV01 (GBP per bp, + = long duration) | 83,885 |
| Parallel move (bp) | 50 |

- *P&L (GBP thousands)*: **-4,194 k**
- *Duration*: **Long**
- *Written*: Explain, and say why the exact P&L differs slightly.

<details><summary>Model answer</summary>

**About -GBP 4.19m.**

(a) First order: -DV01 x move = -GBP 4.19m.
(b) Exact (engine, curve shifted and repriced): -GBP 4.10m. Gap +GBP 96.3k: the swap's convexity (helps here).

</details>

**Q10** (`s3_l2_swap_pnl`, topic `duration:swaps`, seed 1880646)

You pay fixed on GBP 100m 5Y SONIA at par. Using the Givens, estimate your P&L if rates move -25bp.

Givens:

| Given | Value |
|---|---|
| Position DV01 (GBP per bp, + = long duration) | -46,675 |
| Parallel move (bp) | -25 |

- *P&L (GBP thousands)*: **-1,167 k**
- *Duration*: **Short**
- *Written*: Explain, and say why the exact P&L differs slightly.

<details><summary>Model answer</summary>

**About -GBP 1.17m.**

(a) First order: -DV01 x move = -GBP 1.17m.
(b) Exact (engine, curve shifted and repriced): -GBP 1.17m. Gap -GBP 7.1k: the swap's convexity (hurts here).

</details>

### Level 3: calculations plus subtler concepts

**Q1** (`s3_l3_annuity`, topic `duration:swap_dv01`, seed 1985096)

Using the annuity factors in the Givens, compute (a) the DV01 of receiving fixed on GBP 100m 10Y spot-start, and (b) the DV01 of receiving fixed on GBP 100m 5Y5Y forward-start.

Givens:

| Given | Value |
|---|---|
| Notional (GBP) | 100,000,000 |
| Annuity factor, 0 to 10Y (sum of DF x accrual) | 8.199 |
| Annuity factor, 0 to 5Y | 4.5226 |

- *(a) 10Y DV01 (GBP per bp)*: **81,990**
- *(b) 5Y5Y DV01 (GBP per bp)*: **36,764**
- *Written*: Explain why the forward swap's DV01 is the difference.

<details><summary>Model answer</summary>

**(a) +GBP 82.0k, (b) +GBP 36.8k per bp.**

1. A 1bp change in the fixed rate changes the fixed leg's PV by notional x annuity x 0.0001.
2. The forward swap's fixed payments run from 5Y to 10Y, so its annuity = A(0,10) - A(0,5).
3. This is the par-rate DV01; a zero-curve bump gives a very similar number.

</details>

**Q2** (`s3_l3_annuity`, topic `duration:swap_dv01`, seed 1985127)

Using the annuity factors in the Givens, compute (a) the DV01 of receiving fixed on GBP 100m 5Y spot-start, and (b) the DV01 of receiving fixed on GBP 100m 2Y3Y forward-start.

Givens:

| Given | Value |
|---|---|
| Notional (GBP) | 100,000,000 |
| Annuity factor, 0 to 5Y (sum of DF x accrual) | 4.5226 |
| Annuity factor, 0 to 2Y | 1.9046 |

- *(a) 5Y DV01 (GBP per bp)*: **45,226**
- *(b) 2Y3Y DV01 (GBP per bp)*: **26,180**
- *Written*: Explain why the forward swap's DV01 is the difference.

<details><summary>Model answer</summary>

**(a) +GBP 45.2k, (b) +GBP 26.2k per bp.**

1. A 1bp change in the fixed rate changes the fixed leg's PV by notional x annuity x 0.0001.
2. The forward swap's fixed payments run from 2Y to 5Y, so its annuity = A(0,5) - A(0,2).
3. This is the par-rate DV01; a zero-curve bump gives a very similar number.

</details>

**Q3** (`s3_l3_annuity`, topic `duration:swap_dv01`, seed 1985158)

Using the annuity factors in the Givens, compute (a) the DV01 of receiving fixed on GBP 100m 7Y spot-start, and (b) the DV01 of receiving fixed on GBP 100m 2Y5Y forward-start.

Givens:

| Given | Value |
|---|---|
| Notional (GBP) | 100,000,000 |
| Annuity factor, 0 to 7Y (sum of DF x accrual) | 6.0963 |
| Annuity factor, 0 to 2Y | 1.9046 |

- *(a) 7Y DV01 (GBP per bp)*: **60,963**
- *(b) 2Y5Y DV01 (GBP per bp)*: **41,917**
- *Written*: Explain why the forward swap's DV01 is the difference.

<details><summary>Model answer</summary>

**(a) +GBP 61.0k, (b) +GBP 41.9k per bp.**

1. A 1bp change in the fixed rate changes the fixed leg's PV by notional x annuity x 0.0001.
2. The forward swap's fixed payments run from 2Y to 7Y, so its annuity = A(0,7) - A(0,2).
3. This is the par-rate DV01; a zero-curve bump gives a very similar number.

</details>

**Q4** (`s3_l3_annuity`, topic `duration:swap_dv01`, seed 1985189)

Using the annuity factors in the Givens, compute (a) the DV01 of receiving fixed on GBP 100m 7Y spot-start, and (b) the DV01 of receiving fixed on GBP 100m 2Y5Y forward-start.

Givens:

| Given | Value |
|---|---|
| Notional (GBP) | 100,000,000 |
| Annuity factor, 0 to 7Y (sum of DF x accrual) | 6.0963 |
| Annuity factor, 0 to 2Y | 1.9046 |

- *(a) 7Y DV01 (GBP per bp)*: **60,963**
- *(b) 2Y5Y DV01 (GBP per bp)*: **41,917**
- *Written*: Explain why the forward swap's DV01 is the difference.

<details><summary>Model answer</summary>

**(a) +GBP 61.0k, (b) +GBP 41.9k per bp.**

1. A 1bp change in the fixed rate changes the fixed leg's PV by notional x annuity x 0.0001.
2. The forward swap's fixed payments run from 2Y to 7Y, so its annuity = A(0,7) - A(0,2).
3. This is the par-rate DV01; a zero-curve bump gives a very similar number.

</details>

**Q5** (`s3_l3_annuity`, topic `duration:swap_dv01`, seed 1985220)

Using the annuity factors in the Givens, compute (a) the DV01 of receiving fixed on GBP 100m 7Y spot-start, and (b) the DV01 of receiving fixed on GBP 100m 2Y5Y forward-start.

Givens:

| Given | Value |
|---|---|
| Notional (GBP) | 100,000,000 |
| Annuity factor, 0 to 7Y (sum of DF x accrual) | 6.0963 |
| Annuity factor, 0 to 2Y | 1.9046 |

- *(a) 7Y DV01 (GBP per bp)*: **60,963**
- *(b) 2Y5Y DV01 (GBP per bp)*: **41,917**
- *Written*: Explain why the forward swap's DV01 is the difference.

<details><summary>Model answer</summary>

**(a) +GBP 61.0k, (b) +GBP 41.9k per bp.**

1. A 1bp change in the fixed rate changes the fixed leg's PV by notional x annuity x 0.0001.
2. The forward swap's fixed payments run from 2Y to 7Y, so its annuity = A(0,7) - A(0,2).
3. This is the par-rate DV01; a zero-curve bump gives a very similar number.

</details>

**Q6** (`s3_l3_annuity`, topic `duration:swap_dv01`, seed 1985251)

Using the annuity factors in the Givens, compute (a) the DV01 of receiving fixed on GBP 100m 7Y spot-start, and (b) the DV01 of receiving fixed on GBP 100m 2Y5Y forward-start.

Givens:

| Given | Value |
|---|---|
| Notional (GBP) | 100,000,000 |
| Annuity factor, 0 to 7Y (sum of DF x accrual) | 6.0963 |
| Annuity factor, 0 to 2Y | 1.9046 |

- *(a) 7Y DV01 (GBP per bp)*: **60,963**
- *(b) 2Y5Y DV01 (GBP per bp)*: **41,917**
- *Written*: Explain why the forward swap's DV01 is the difference.

<details><summary>Model answer</summary>

**(a) +GBP 61.0k, (b) +GBP 41.9k per bp.**

1. A 1bp change in the fixed rate changes the fixed leg's PV by notional x annuity x 0.0001.
2. The forward swap's fixed payments run from 2Y to 7Y, so its annuity = A(0,7) - A(0,2).
3. This is the par-rate DV01; a zero-curve bump gives a very similar number.

</details>

**Q7** (`s3_l3_annuity`, topic `duration:swap_dv01`, seed 1985282)

Using the annuity factors in the Givens, compute (a) the DV01 of receiving fixed on GBP 100m 8Y spot-start, and (b) the DV01 of receiving fixed on GBP 100m 5Y3Y forward-start.

Givens:

| Given | Value |
|---|---|
| Notional (GBP) | 100,000,000 |
| Annuity factor, 0 to 8Y (sum of DF x accrual) | 6.8312 |
| Annuity factor, 0 to 5Y | 4.5226 |

- *(a) 8Y DV01 (GBP per bp)*: **68,312**
- *(b) 5Y3Y DV01 (GBP per bp)*: **23,086**
- *Written*: Explain why the forward swap's DV01 is the difference.

<details><summary>Model answer</summary>

**(a) +GBP 68.3k, (b) +GBP 23.1k per bp.**

1. A 1bp change in the fixed rate changes the fixed leg's PV by notional x annuity x 0.0001.
2. The forward swap's fixed payments run from 5Y to 8Y, so its annuity = A(0,8) - A(0,5).
3. This is the par-rate DV01; a zero-curve bump gives a very similar number.

</details>

**Q8** (`s3_l3_annuity`, topic `duration:swap_dv01`, seed 1985313)

Using the annuity factors in the Givens, compute (a) the DV01 of receiving fixed on GBP 100m 10Y spot-start, and (b) the DV01 of receiving fixed on GBP 100m 5Y5Y forward-start.

Givens:

| Given | Value |
|---|---|
| Notional (GBP) | 100,000,000 |
| Annuity factor, 0 to 10Y (sum of DF x accrual) | 8.199 |
| Annuity factor, 0 to 5Y | 4.5226 |

- *(a) 10Y DV01 (GBP per bp)*: **81,990**
- *(b) 5Y5Y DV01 (GBP per bp)*: **36,764**
- *Written*: Explain why the forward swap's DV01 is the difference.

<details><summary>Model answer</summary>

**(a) +GBP 82.0k, (b) +GBP 36.8k per bp.**

1. A 1bp change in the fixed rate changes the fixed leg's PV by notional x annuity x 0.0001.
2. The forward swap's fixed payments run from 5Y to 10Y, so its annuity = A(0,10) - A(0,5).
3. This is the par-rate DV01; a zero-curve bump gives a very similar number.

</details>

**Q9** (`s3_l3_annuity`, topic `duration:swap_dv01`, seed 1985344)

Using the annuity factors in the Givens, compute (a) the DV01 of receiving fixed on GBP 100m 5Y spot-start, and (b) the DV01 of receiving fixed on GBP 100m 2Y3Y forward-start.

Givens:

| Given | Value |
|---|---|
| Notional (GBP) | 100,000,000 |
| Annuity factor, 0 to 5Y (sum of DF x accrual) | 4.5226 |
| Annuity factor, 0 to 2Y | 1.9046 |

- *(a) 5Y DV01 (GBP per bp)*: **45,226**
- *(b) 2Y3Y DV01 (GBP per bp)*: **26,180**
- *Written*: Explain why the forward swap's DV01 is the difference.

<details><summary>Model answer</summary>

**(a) +GBP 45.2k, (b) +GBP 26.2k per bp.**

1. A 1bp change in the fixed rate changes the fixed leg's PV by notional x annuity x 0.0001.
2. The forward swap's fixed payments run from 2Y to 5Y, so its annuity = A(0,5) - A(0,2).
3. This is the par-rate DV01; a zero-curve bump gives a very similar number.

</details>

**Q10** (`s3_l3_annuity`, topic `duration:swap_dv01`, seed 1985375)

Using the annuity factors in the Givens, compute (a) the DV01 of receiving fixed on GBP 100m 10Y spot-start, and (b) the DV01 of receiving fixed on GBP 100m 5Y5Y forward-start.

Givens:

| Given | Value |
|---|---|
| Notional (GBP) | 100,000,000 |
| Annuity factor, 0 to 10Y (sum of DF x accrual) | 8.199 |
| Annuity factor, 0 to 5Y | 4.5226 |

- *(a) 10Y DV01 (GBP per bp)*: **81,990**
- *(b) 5Y5Y DV01 (GBP per bp)*: **36,764**
- *Written*: Explain why the forward swap's DV01 is the difference.

<details><summary>Model answer</summary>

**(a) +GBP 82.0k, (b) +GBP 36.8k per bp.**

1. A 1bp change in the fixed rate changes the fixed leg's PV by notional x annuity x 0.0001.
2. The forward swap's fixed payments run from 5Y to 10Y, so its annuity = A(0,10) - A(0,5).
3. This is the par-rate DV01; a zero-curve bump gives a very similar number.

</details>

## 2A-4 Stage 4: Swaptions

### Level 1: directional intuition, no calculations

**Q1** (`s4_l1_signs`, topic `convexity:swaptions`, seed 1783557)

You are **short 1Y-into-10Y ATM receiver swaptions**. Fill in your exposures (+ long, - short).

- *Exposure*: **Duration: -, Convexity: -**
- *Written*: Explain each sign.

<details><summary>Model answer</summary>

**Duration -, convexity -.**

1. Receiver = right to receive fixed: gains when rates fall, so long duration. Payer = short duration.
2. Any long option is long convexity (long gamma): its duration grows in the direction that makes money. Short either one and you are short convexity.

</details>

**Q2** (`s4_l1_signs`, topic `convexity:swaptions`, seed 1783588)

You are **short 1Y-into-10Y ATM receiver swaptions**. Fill in your exposures (+ long, - short).

- *Exposure*: **Duration: -, Convexity: -**
- *Written*: Explain each sign.

<details><summary>Model answer</summary>

**Duration -, convexity -.**

1. Receiver = right to receive fixed: gains when rates fall, so long duration. Payer = short duration.
2. Any long option is long convexity (long gamma): its duration grows in the direction that makes money. Short either one and you are short convexity.

</details>

**Q3** (`s4_l1_signs`, topic `convexity:swaptions`, seed 1783619)

You are **short 1Y-into-10Y ATM payer swaptions**. Fill in your exposures (+ long, - short).

- *Exposure*: **Duration: +, Convexity: -**
- *Written*: Explain each sign.

<details><summary>Model answer</summary>

**Duration +, convexity -.**

1. Receiver = right to receive fixed: gains when rates fall, so long duration. Payer = short duration.
2. Any long option is long convexity (long gamma): its duration grows in the direction that makes money. Short either one and you are short convexity.

</details>

**Q4** (`s4_l1_signs`, topic `convexity:swaptions`, seed 1783650)

You are **long 1Y-into-10Y ATM receiver swaptions**. Fill in your exposures (+ long, - short).

- *Exposure*: **Duration: +, Convexity: +**
- *Written*: Explain each sign.

<details><summary>Model answer</summary>

**Duration +, convexity +.**

1. Receiver = right to receive fixed: gains when rates fall, so long duration. Payer = short duration.
2. Any long option is long convexity (long gamma): its duration grows in the direction that makes money. Short either one and you are short convexity.

</details>

**Q5** (`s4_l1_signs`, topic `convexity:swaptions`, seed 1783681)

You are **long 1Y-into-10Y ATM receiver swaptions**. Fill in your exposures (+ long, - short).

- *Exposure*: **Duration: +, Convexity: +**
- *Written*: Explain each sign.

<details><summary>Model answer</summary>

**Duration +, convexity +.**

1. Receiver = right to receive fixed: gains when rates fall, so long duration. Payer = short duration.
2. Any long option is long convexity (long gamma): its duration grows in the direction that makes money. Short either one and you are short convexity.

</details>

**Q6** (`s4_l1_signs`, topic `convexity:swaptions`, seed 1783712)

You are **short 1Y-into-10Y ATM payer swaptions**. Fill in your exposures (+ long, - short).

- *Exposure*: **Duration: +, Convexity: -**
- *Written*: Explain each sign.

<details><summary>Model answer</summary>

**Duration +, convexity -.**

1. Receiver = right to receive fixed: gains when rates fall, so long duration. Payer = short duration.
2. Any long option is long convexity (long gamma): its duration grows in the direction that makes money. Short either one and you are short convexity.

</details>

**Q7** (`s4_l1_signs`, topic `convexity:swaptions`, seed 1783743)

You are **long 1Y-into-10Y ATM receiver swaptions**. Fill in your exposures (+ long, - short).

- *Exposure*: **Duration: +, Convexity: +**
- *Written*: Explain each sign.

<details><summary>Model answer</summary>

**Duration +, convexity +.**

1. Receiver = right to receive fixed: gains when rates fall, so long duration. Payer = short duration.
2. Any long option is long convexity (long gamma): its duration grows in the direction that makes money. Short either one and you are short convexity.

</details>

**Q8** (`s4_l1_signs`, topic `convexity:swaptions`, seed 1783774)

You are **long 1Y-into-10Y ATM payer swaptions**. Fill in your exposures (+ long, - short).

- *Exposure*: **Duration: -, Convexity: +**
- *Written*: Explain each sign.

<details><summary>Model answer</summary>

**Duration -, convexity +.**

1. Receiver = right to receive fixed: gains when rates fall, so long duration. Payer = short duration.
2. Any long option is long convexity (long gamma): its duration grows in the direction that makes money. Short either one and you are short convexity.

</details>

**Q9** (`s4_l1_signs`, topic `convexity:swaptions`, seed 1783805)

You are **long 1Y-into-10Y ATM payer swaptions**. Fill in your exposures (+ long, - short).

- *Exposure*: **Duration: -, Convexity: +**
- *Written*: Explain each sign.

<details><summary>Model answer</summary>

**Duration -, convexity +.**

1. Receiver = right to receive fixed: gains when rates fall, so long duration. Payer = short duration.
2. Any long option is long convexity (long gamma): its duration grows in the direction that makes money. Short either one and you are short convexity.

</details>

**Q10** (`s4_l1_signs`, topic `convexity:swaptions`, seed 1783836)

You are **short 1Y-into-10Y ATM payer swaptions**. Fill in your exposures (+ long, - short).

- *Exposure*: **Duration: +, Convexity: -**
- *Written*: Explain each sign.

<details><summary>Model answer</summary>

**Duration +, convexity -.**

1. Receiver = right to receive fixed: gains when rates fall, so long duration. Payer = short duration.
2. Any long option is long convexity (long gamma): its duration grows in the direction that makes money. Short either one and you are short convexity.

</details>

### Level 2: combinations, light calculations with every input given

**Q1** (`s4_l2_delta`, topic `convexity:swaption_delta`, seed 1888286)

You are **short 1Y10Y ATM payer swaptions, delta-hedged with swaps** (flat duration today). Rates move +50bp. Are you now long or short duration?

- *Duration after the move*: **Long**
- *Written*: Explain using the option analogy.

<details><summary>Model answer</summary>

**Long duration** (net DV01 +GBP 15.4k).

1. A swaption's DV01 behaves like an option delta: it grows as the option moves into the money.
2. Short the option, your duration moves against you (short convexity): you end up long duration in a selloff and short in a rally.

</details>

**Q2** (`s4_l2_delta`, topic `convexity:swaption_delta`, seed 1888317)

You are **long 1Y10Y ATM receiver swaptions**. Rates move -50bp. Does the size of your duration exposure grow or shrink?

- *Duration exposure*: **Grows**
- *Written*: Explain using the option analogy.

<details><summary>Model answer</summary>

**It grows: DV01 +GBP 42.0k to +GBP 63.4k.**

1. A swaption's DV01 behaves like an option delta: it grows as the option moves into the money.
2. Long the option, your duration always moves in your favour (long convexity): after a hedge you end up long duration in a rally and short in a selloff.

</details>

**Q3** (`s4_l2_delta`, topic `convexity:swaption_delta`, seed 1888348)

You are **long 1Y10Y ATM receiver swaptions**. Rates move +50bp. Does the size of your duration exposure grow or shrink?

- *Duration exposure*: **Shrinks**
- *Written*: Explain using the option analogy.

<details><summary>Model answer</summary>

**It shrinks: DV01 +GBP 42.0k to +GBP 22.1k.**

1. A swaption's DV01 behaves like an option delta: it grows as the option moves into the money.
2. Long the option, your duration always moves in your favour (long convexity): after a hedge you end up long duration in a rally and short in a selloff.

</details>

**Q4** (`s4_l2_delta`, topic `convexity:swaption_delta`, seed 1888379)

You are **short 1Y10Y ATM receiver swaptions, delta-hedged with swaps** (flat duration today). Rates move -50bp. Are you now long or short duration?

- *Duration after the move*: **Short**
- *Written*: Explain using the option analogy.

<details><summary>Model answer</summary>

**Short duration** (net DV01 -GBP 21.5k).

1. A swaption's DV01 behaves like an option delta: it grows as the option moves into the money.
2. Short the option, your duration moves against you (short convexity): you end up long duration in a selloff and short in a rally.

</details>

**Q5** (`s4_l2_delta`, topic `convexity:swaption_delta`, seed 1888410)

You are **short 1Y10Y ATM payer swaptions, delta-hedged with swaps** (flat duration today). Rates move -25bp. Are you now long or short duration?

- *Duration after the move*: **Short**
- *Written*: Explain using the option analogy.

<details><summary>Model answer</summary>

**Short duration** (net DV01 -GBP 8.6k).

1. A swaption's DV01 behaves like an option delta: it grows as the option moves into the money.
2. Short the option, your duration moves against you (short convexity): you end up long duration in a selloff and short in a rally.

</details>

**Q6** (`s4_l2_delta`, topic `convexity:swaption_delta`, seed 1888441)

You are **long 1Y10Y ATM receiver swaptions, delta-hedged with swaps** (flat duration today). Rates move +25bp. Are you now long or short duration?

- *Duration after the move*: **Short**
- *Written*: Explain using the option analogy.

<details><summary>Model answer</summary>

**Short duration** (net DV01 -GBP 10.5k).

1. A swaption's DV01 behaves like an option delta: it grows as the option moves into the money.
2. Long the option, your duration always moves in your favour (long convexity): after a hedge you end up long duration in a rally and short in a selloff.

</details>

**Q7** (`s4_l2_delta`, topic `convexity:swaption_delta`, seed 1888472)

You are **short 1Y10Y ATM receiver swaptions, delta-hedged with swaps** (flat duration today). Rates move -25bp. Are you now long or short duration?

- *Duration after the move*: **Short**
- *Written*: Explain using the option analogy.

<details><summary>Model answer</summary>

**Short duration** (net DV01 -GBP 10.9k).

1. A swaption's DV01 behaves like an option delta: it grows as the option moves into the money.
2. Short the option, your duration moves against you (short convexity): you end up long duration in a selloff and short in a rally.

</details>

**Q8** (`s4_l2_delta`, topic `convexity:swaption_delta`, seed 1888503)

You are **long 1Y10Y ATM receiver swaptions**. Rates move +25bp. Does the size of your duration exposure grow or shrink?

- *Duration exposure*: **Shrinks**
- *Written*: Explain using the option analogy.

<details><summary>Model answer</summary>

**It shrinks: DV01 +GBP 42.0k to +GBP 31.5k.**

1. A swaption's DV01 behaves like an option delta: it grows as the option moves into the money.
2. Long the option, your duration always moves in your favour (long convexity): after a hedge you end up long duration in a rally and short in a selloff.

</details>

**Q9** (`s4_l2_delta`, topic `convexity:swaption_delta`, seed 1888534)

You are **short 1Y10Y ATM payer swaptions, delta-hedged with swaps** (flat duration today). Rates move -50bp. Are you now long or short duration?

- *Duration after the move*: **Short**
- *Written*: Explain using the option analogy.

<details><summary>Model answer</summary>

**Short duration** (net DV01 -GBP 16.8k).

1. A swaption's DV01 behaves like an option delta: it grows as the option moves into the money.
2. Short the option, your duration moves against you (short convexity): you end up long duration in a selloff and short in a rally.

</details>

**Q10** (`s4_l2_delta`, topic `convexity:swaption_delta`, seed 1888565)

You are **short 1Y10Y ATM payer swaptions, delta-hedged with swaps** (flat duration today). Rates move -75bp. Are you now long or short duration?

- *Duration after the move*: **Short**
- *Written*: Explain using the option analogy.

<details><summary>Model answer</summary>

**Short duration** (net DV01 -GBP 23.7k).

1. A swaption's DV01 behaves like an option delta: it grows as the option moves into the money.
2. Short the option, your duration moves against you (short convexity): you end up long duration in a selloff and short in a rally.

</details>

### Level 3: calculations plus subtler concepts

**Q1** (`s4_l3_bachelier`, topic `convexity:swaption_pricing`, seed 1993015)

Price a long GBP 100m 1Y-into-10Y **receiver** swaption (-25bp from ATM) under Bachelier (normal) vol, and give its DV01 (+ = long duration). All inputs in the Givens.

Givens:

| Given | Value |
|---|---|
| Swaption type (you are long) | receiver |
| Forward swap rate (%) | 4.2009 |
| Strike (%) | 3.9509 |
| Normal vol (bp a year) | 85 |
| Expiry (years) | 1 |
| Forward annuity factor | 7.8685 |
| Notional (GBP) | 100,000,000 |

- *Premium (GBP thousands)*: **1,799 k**
- *DV01 (GBP per bp)*: **30,241**
- *Written*: Explain the formula and the sign of the DV01.

<details><summary>Model answer</summary>

**Premium +GBP 1.80m, DV01 +GBP 30.2k.**

1. d = (F - K) / (sigma_N sqrt T); payer PV = A [(F-K) N(d) + sigma_N sqrt(T) n(d)], receiver PV = A [(K-F) N(-d) + sigma_N sqrt(T) n(d)].
2. Delta to the forward rate: payer A N(d), receiver -A N(-d); DV01 (long duration +) = -delta x 1bp, so payers are short duration.
3. ATM: PV = A sigma_N sqrt(T/2pi).

</details>

**Q2** (`s4_l3_bachelier`, topic `convexity:swaption_pricing`, seed 1993046)

Price a long GBP 100m 1Y-into-10Y **receiver** swaption (+25bp from ATM) under Bachelier (normal) vol, and give its DV01 (+ = long duration). All inputs in the Givens.

Givens:

| Given | Value |
|---|---|
| Swaption type (you are long) | receiver |
| Forward swap rate (%) | 4.2009 |
| Strike (%) | 4.4509 |
| Normal vol (bp a year) | 85 |
| Expiry (years) | 1 |
| Forward annuity factor | 7.8685 |
| Notional (GBP) | 100,000,000 |

- *Premium (GBP thousands)*: **3,766 k**
- *DV01 (GBP per bp)*: **48,443**
- *Written*: Explain the formula and the sign of the DV01.

<details><summary>Model answer</summary>

**Premium +GBP 3.77m, DV01 +GBP 48.4k.**

1. d = (F - K) / (sigma_N sqrt T); payer PV = A [(F-K) N(d) + sigma_N sqrt(T) n(d)], receiver PV = A [(K-F) N(-d) + sigma_N sqrt(T) n(d)].
2. Delta to the forward rate: payer A N(d), receiver -A N(-d); DV01 (long duration +) = -delta x 1bp, so payers are short duration.
3. ATM: PV = A sigma_N sqrt(T/2pi).

</details>

**Q3** (`s4_l3_bachelier`, topic `convexity:swaption_pricing`, seed 1993077)

Price a long GBP 100m 1Y-into-10Y **receiver** swaption (-25bp from ATM) under Bachelier (normal) vol, and give its DV01 (+ = long duration). All inputs in the Givens.

Givens:

| Given | Value |
|---|---|
| Swaption type (you are long) | receiver |
| Forward swap rate (%) | 4.2009 |
| Strike (%) | 3.9509 |
| Normal vol (bp a year) | 85 |
| Expiry (years) | 1 |
| Forward annuity factor | 7.8685 |
| Notional (GBP) | 100,000,000 |

- *Premium (GBP thousands)*: **1,799 k**
- *DV01 (GBP per bp)*: **30,241**
- *Written*: Explain the formula and the sign of the DV01.

<details><summary>Model answer</summary>

**Premium +GBP 1.80m, DV01 +GBP 30.2k.**

1. d = (F - K) / (sigma_N sqrt T); payer PV = A [(F-K) N(d) + sigma_N sqrt(T) n(d)], receiver PV = A [(K-F) N(-d) + sigma_N sqrt(T) n(d)].
2. Delta to the forward rate: payer A N(d), receiver -A N(-d); DV01 (long duration +) = -delta x 1bp, so payers are short duration.
3. ATM: PV = A sigma_N sqrt(T/2pi).

</details>

**Q4** (`s4_l3_bachelier`, topic `convexity:swaption_pricing`, seed 1993108)

Price a long GBP 100m 1Y-into-10Y **receiver** swaption (+25bp from ATM) under Bachelier (normal) vol, and give its DV01 (+ = long duration). All inputs in the Givens.

Givens:

| Given | Value |
|---|---|
| Swaption type (you are long) | receiver |
| Forward swap rate (%) | 4.2009 |
| Strike (%) | 4.4509 |
| Normal vol (bp a year) | 85 |
| Expiry (years) | 1 |
| Forward annuity factor | 7.8685 |
| Notional (GBP) | 100,000,000 |

- *Premium (GBP thousands)*: **3,766 k**
- *DV01 (GBP per bp)*: **48,443**
- *Written*: Explain the formula and the sign of the DV01.

<details><summary>Model answer</summary>

**Premium +GBP 3.77m, DV01 +GBP 48.4k.**

1. d = (F - K) / (sigma_N sqrt T); payer PV = A [(F-K) N(d) + sigma_N sqrt(T) n(d)], receiver PV = A [(K-F) N(-d) + sigma_N sqrt(T) n(d)].
2. Delta to the forward rate: payer A N(d), receiver -A N(-d); DV01 (long duration +) = -delta x 1bp, so payers are short duration.
3. ATM: PV = A sigma_N sqrt(T/2pi).

</details>

**Q5** (`s4_l3_bachelier`, topic `convexity:swaption_pricing`, seed 1993139)

Price a long GBP 100m 1Y-into-10Y **payer** swaption (+25bp from ATM) under Bachelier (normal) vol, and give its DV01 (+ = long duration). All inputs in the Givens.

Givens:

| Given | Value |
|---|---|
| Swaption type (you are long) | payer |
| Forward swap rate (%) | 4.2009 |
| Strike (%) | 4.4509 |
| Normal vol (bp a year) | 85 |
| Expiry (years) | 1 |
| Forward annuity factor | 7.8685 |
| Notional (GBP) | 100,000,000 |

- *Premium (GBP thousands)*: **1,799 k**
- *DV01 (GBP per bp)*: **-30,241**
- *Written*: Explain the formula and the sign of the DV01.

<details><summary>Model answer</summary>

**Premium +GBP 1.80m, DV01 -GBP 30.2k.**

1. d = (F - K) / (sigma_N sqrt T); payer PV = A [(F-K) N(d) + sigma_N sqrt(T) n(d)], receiver PV = A [(K-F) N(-d) + sigma_N sqrt(T) n(d)].
2. Delta to the forward rate: payer A N(d), receiver -A N(-d); DV01 (long duration +) = -delta x 1bp, so payers are short duration.
3. ATM: PV = A sigma_N sqrt(T/2pi).

</details>

**Q6** (`s4_l3_bachelier`, topic `convexity:swaption_pricing`, seed 1993170)

Price a long GBP 100m 1Y-into-10Y **receiver** swaption (ATM) under Bachelier (normal) vol, and give its DV01 (+ = long duration). All inputs in the Givens.

Givens:

| Given | Value |
|---|---|
| Swaption type (you are long) | receiver |
| Forward swap rate (%) | 4.2009 |
| Strike (%) | 4.2009 |
| Normal vol (bp a year) | 85 |
| Expiry (years) | 1 |
| Forward annuity factor | 7.8685 |
| Notional (GBP) | 100,000,000 |

- *Premium (GBP thousands)*: **2,668 k**
- *DV01 (GBP per bp)*: **39,342**
- *Written*: Explain the formula and the sign of the DV01.

<details><summary>Model answer</summary>

**Premium +GBP 2.67m, DV01 +GBP 39.3k.**

1. d = (F - K) / (sigma_N sqrt T); payer PV = A [(F-K) N(d) + sigma_N sqrt(T) n(d)], receiver PV = A [(K-F) N(-d) + sigma_N sqrt(T) n(d)].
2. Delta to the forward rate: payer A N(d), receiver -A N(-d); DV01 (long duration +) = -delta x 1bp, so payers are short duration.
3. ATM: PV = A sigma_N sqrt(T/2pi).

</details>

**Q7** (`s4_l3_bachelier`, topic `convexity:swaption_pricing`, seed 1993201)

Price a long GBP 100m 1Y-into-10Y **receiver** swaption (+25bp from ATM) under Bachelier (normal) vol, and give its DV01 (+ = long duration). All inputs in the Givens.

Givens:

| Given | Value |
|---|---|
| Swaption type (you are long) | receiver |
| Forward swap rate (%) | 4.2009 |
| Strike (%) | 4.4509 |
| Normal vol (bp a year) | 85 |
| Expiry (years) | 1 |
| Forward annuity factor | 7.8685 |
| Notional (GBP) | 100,000,000 |

- *Premium (GBP thousands)*: **3,766 k**
- *DV01 (GBP per bp)*: **48,443**
- *Written*: Explain the formula and the sign of the DV01.

<details><summary>Model answer</summary>

**Premium +GBP 3.77m, DV01 +GBP 48.4k.**

1. d = (F - K) / (sigma_N sqrt T); payer PV = A [(F-K) N(d) + sigma_N sqrt(T) n(d)], receiver PV = A [(K-F) N(-d) + sigma_N sqrt(T) n(d)].
2. Delta to the forward rate: payer A N(d), receiver -A N(-d); DV01 (long duration +) = -delta x 1bp, so payers are short duration.
3. ATM: PV = A sigma_N sqrt(T/2pi).

</details>

**Q8** (`s4_l3_bachelier`, topic `convexity:swaption_pricing`, seed 1993232)

Price a long GBP 100m 1Y-into-10Y **receiver** swaption (ATM) under Bachelier (normal) vol, and give its DV01 (+ = long duration). All inputs in the Givens.

Givens:

| Given | Value |
|---|---|
| Swaption type (you are long) | receiver |
| Forward swap rate (%) | 4.2009 |
| Strike (%) | 4.2009 |
| Normal vol (bp a year) | 85 |
| Expiry (years) | 1 |
| Forward annuity factor | 7.8685 |
| Notional (GBP) | 100,000,000 |

- *Premium (GBP thousands)*: **2,668 k**
- *DV01 (GBP per bp)*: **39,342**
- *Written*: Explain the formula and the sign of the DV01.

<details><summary>Model answer</summary>

**Premium +GBP 2.67m, DV01 +GBP 39.3k.**

1. d = (F - K) / (sigma_N sqrt T); payer PV = A [(F-K) N(d) + sigma_N sqrt(T) n(d)], receiver PV = A [(K-F) N(-d) + sigma_N sqrt(T) n(d)].
2. Delta to the forward rate: payer A N(d), receiver -A N(-d); DV01 (long duration +) = -delta x 1bp, so payers are short duration.
3. ATM: PV = A sigma_N sqrt(T/2pi).

</details>

**Q9** (`s4_l3_bachelier`, topic `convexity:swaption_pricing`, seed 1993263)

Price a long GBP 100m 1Y-into-10Y **receiver** swaption (ATM) under Bachelier (normal) vol, and give its DV01 (+ = long duration). All inputs in the Givens.

Givens:

| Given | Value |
|---|---|
| Swaption type (you are long) | receiver |
| Forward swap rate (%) | 4.2009 |
| Strike (%) | 4.2009 |
| Normal vol (bp a year) | 85 |
| Expiry (years) | 1 |
| Forward annuity factor | 7.8685 |
| Notional (GBP) | 100,000,000 |

- *Premium (GBP thousands)*: **2,668 k**
- *DV01 (GBP per bp)*: **39,342**
- *Written*: Explain the formula and the sign of the DV01.

<details><summary>Model answer</summary>

**Premium +GBP 2.67m, DV01 +GBP 39.3k.**

1. d = (F - K) / (sigma_N sqrt T); payer PV = A [(F-K) N(d) + sigma_N sqrt(T) n(d)], receiver PV = A [(K-F) N(-d) + sigma_N sqrt(T) n(d)].
2. Delta to the forward rate: payer A N(d), receiver -A N(-d); DV01 (long duration +) = -delta x 1bp, so payers are short duration.
3. ATM: PV = A sigma_N sqrt(T/2pi).

</details>

**Q10** (`s4_l3_bachelier`, topic `convexity:swaption_pricing`, seed 1993294)

Price a long GBP 100m 1Y-into-10Y **payer** swaption (ATM) under Bachelier (normal) vol, and give its DV01 (+ = long duration). All inputs in the Givens.

Givens:

| Given | Value |
|---|---|
| Swaption type (you are long) | payer |
| Forward swap rate (%) | 4.2009 |
| Strike (%) | 4.2009 |
| Normal vol (bp a year) | 85 |
| Expiry (years) | 1 |
| Forward annuity factor | 7.8685 |
| Notional (GBP) | 100,000,000 |

- *Premium (GBP thousands)*: **2,668 k**
- *DV01 (GBP per bp)*: **-39,342**
- *Written*: Explain the formula and the sign of the DV01.

<details><summary>Model answer</summary>

**Premium +GBP 2.67m, DV01 -GBP 39.3k.**

1. d = (F - K) / (sigma_N sqrt T); payer PV = A [(F-K) N(d) + sigma_N sqrt(T) n(d)], receiver PV = A [(K-F) N(-d) + sigma_N sqrt(T) n(d)].
2. Delta to the forward rate: payer A N(d), receiver -A N(-d); DV01 (long duration +) = -delta x 1bp, so payers are short duration.
3. ATM: PV = A sigma_N sqrt(T/2pi).

</details>

## 2A-5 Stage 5: Mixed books

### Level 1: directional intuition, no calculations

**Q1** (`s5_l1_signs`, topic `mixed:signs`, seed 1791476)

The desk is **long GBP 100m 1Y-into-10Y ATM payer swaptions, delta-hedged by receiving 10Y**.

Fill in the book's exposures today (+ long, - short, 0 roughly flat).

- *Exposure*: **Duration: 0, Convexity: +**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Duration 0, convexity +.**

A delta-hedged long payer is flat duration but long convexity: after a selloff you are short duration (you made money), after a rally long. Long gamma in rates.

</details>

**Q2** (`s5_l1_signs`, topic `mixed:signs`, seed 1791507)

The desk owns **GBP 100m of an MBS-like 4.5% 10Y callable bond, duration-hedged by paying fixed in 10Y swaps**.

Fill in the book's exposures today (+ long, - short, 0 roughly flat).

- *Exposure*: **Duration: 0, Convexity: -**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Duration 0, convexity -.**

Duration-hedged MBS is flat duration today but short convexity: after a rally you are short duration, after a selloff long. Hedgers chase the move (convexity hedging).

</details>

**Q3** (`s5_l1_signs`, topic `mixed:signs`, seed 1791538)

The desk owns **GBP 100m of a 4.5% 10Y callable bond** (callable at par in 2 years), MBS-like.

Fill in the book's exposures today (+ long, - short, 0 roughly flat).

- *Exposure*: **Duration: +, Convexity: -**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Duration +, convexity -.**

A callable bond = bullet bond minus the issuer's call (a receiver swaption you are short). When rates fall it gets called, so duration shortens just when you want more: long duration, short convexity.

</details>

**Q4** (`s5_l1_signs`, topic `mixed:signs`, seed 1791569)

The desk is **long GBP 100m 1Y-into-10Y ATM payer swaptions, delta-hedged by receiving 10Y**.

Fill in the book's exposures today (+ long, - short, 0 roughly flat).

- *Exposure*: **Duration: 0, Convexity: +**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Duration 0, convexity +.**

A delta-hedged long payer is flat duration but long convexity: after a selloff you are short duration (you made money), after a rally long. Long gamma in rates.

</details>

**Q5** (`s5_l1_signs`, topic `mixed:signs`, seed 1791600)

The desk owns **GBP 100m of an MBS-like 4.5% 10Y callable bond, duration-hedged by paying fixed in 10Y swaps**.

Fill in the book's exposures today (+ long, - short, 0 roughly flat).

- *Exposure*: **Duration: 0, Convexity: -**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Duration 0, convexity -.**

Duration-hedged MBS is flat duration today but short convexity: after a rally you are short duration, after a selloff long. Hedgers chase the move (convexity hedging).

</details>

**Q6** (`s5_l1_signs`, topic `mixed:signs`, seed 1791631)

The desk owns **GBP 100m of a 4.5% 10Y gilt** and has **sold GBP 100m 1Y-into-9Y receiver swaptions** 25bp OTM.

Fill in the book's exposures today (+ long, - short, 0 roughly flat).

- *Exposure*: **Duration: +, Convexity: -**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Duration +, convexity -.**

Selling receivers adds long duration that grows as rates fall and vanishes as they rise: short convexity, paid for with premium. Same shape as a callable bond or MBS.

</details>

**Q7** (`s5_l1_signs`, topic `mixed:signs`, seed 1791662)

The desk **receives fixed on GBP 100m 10Y** and is **long GBP 100m 2Y-into-10Y ATM payer swaptions**.

Fill in the book's exposures today (+ long, - short, 0 roughly flat).

- *Exposure*: **Duration: +, Convexity: +**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Duration +, convexity +.**

Receiving 10Y is long duration with little convexity; the long payers are short duration and long convexity. In a selloff the payers' delta grows and offsets more of the swap loss.

</details>

**Q8** (`s5_l1_signs`, topic `mixed:signs`, seed 1791693)

The desk **receives fixed on GBP 100m 10Y** and is **long GBP 50m 2Y-into-10Y ATM payer swaptions**.

Fill in the book's exposures today (+ long, - short, 0 roughly flat).

- *Exposure*: **Duration: +, Convexity: +**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Duration +, convexity +.**

Receiving 10Y is long duration with little convexity; the long payers are short duration and long convexity. In a selloff the payers' delta grows and offsets more of the swap loss.

</details>

**Q9** (`s5_l1_signs`, topic `mixed:signs`, seed 1791724)

The desk is **long GBP 100m 1Y-into-10Y ATM payer swaptions, delta-hedged by receiving 10Y**.

Fill in the book's exposures today (+ long, - short, 0 roughly flat).

- *Exposure*: **Duration: 0, Convexity: +**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Duration 0, convexity +.**

A delta-hedged long payer is flat duration but long convexity: after a selloff you are short duration (you made money), after a rally long. Long gamma in rates.

</details>

**Q10** (`s5_l1_signs`, topic `mixed:signs`, seed 1791755)

The desk owns **GBP 100m of an MBS-like 4.5% 10Y callable bond, duration-hedged by paying fixed in 10Y swaps**.

Fill in the book's exposures today (+ long, - short, 0 roughly flat).

- *Exposure*: **Duration: 0, Convexity: -**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Duration 0, convexity -.**

Duration-hedged MBS is flat duration today but short convexity: after a rally you are short duration, after a selloff long. Hedgers chase the move (convexity hedging).

</details>

### Level 2: combinations, light calculations with every input given

**Q1** (`s5_l2_move`, topic `mixed:books`, seed 1896205)

The desk owns **GBP 100m of a 4.5% 10Y callable bond** (callable at par in 2 years), MBS-like.

Rates move **-50bp** in parallel. Fill in the sign of your P&L and of your exposures after the move, then walk through why.

- *After the move*: **P&L: +, Duration after: +, Convexity after: -**
- *Written*: Walk through the P&L by component and the change in risk.

<details><summary>Model answer</summary>

**P&L +, duration +, convexity -.**

A callable bond = bullet bond minus the issuer's call (a receiver swaption you are short). When rates fall it gets called, so duration shortens just when you want more: long duration, short convexity.

Illustration (engine): P&L +GBP 2.10m; DV01 +GBP 46.5k to +GBP 37.6k.

</details>

**Q2** (`s5_l2_move`, topic `mixed:books`, seed 1896236)

The desk **receives fixed on GBP 100m 10Y** and is **long GBP 100m 2Y-into-10Y ATM payer swaptions**.

Rates move **+75bp** in parallel. Fill in the sign of your P&L and of your exposures after the move, then walk through why.

- *After the move*: **P&L: -, Duration after: +, Convexity after: +**
- *Written*: Walk through the P&L by component and the change in risk.

<details><summary>Model answer</summary>

**P&L -, duration +, convexity +.**

Receiving 10Y is long duration with little convexity; the long payers are short duration and long convexity. In a selloff the payers' delta grows and offsets more of the swap loss.

Illustration (engine): P&L -GBP 2.80m; DV01 +GBP 47.6k to +GBP 28.1k.

</details>

**Q3** (`s5_l2_move`, topic `mixed:books`, seed 1896267)

The desk owns **GBP 100m of a 4.5% 10Y callable bond** (callable at par in 2 years), MBS-like.

Rates move **+50bp** in parallel. Fill in the sign of your P&L and of your exposures after the move, then walk through why.

- *After the move*: **P&L: -, Duration after: +, Convexity after: -**
- *Written*: Walk through the P&L by component and the change in risk.

<details><summary>Model answer</summary>

**P&L -, duration +, convexity -.**

A callable bond = bullet bond minus the issuer's call (a receiver swaption you are short). When rates fall it gets called, so duration shortens just when you want more: long duration, short convexity.

Illustration (engine): P&L -GBP 2.55m; DV01 +GBP 46.5k to +GBP 55.3k.

</details>

**Q4** (`s5_l2_move`, topic `mixed:books`, seed 1896298)

The desk owns **GBP 100m of an MBS-like 4.5% 10Y callable bond, duration-hedged by paying fixed in 10Y swaps**.

Rates move **+75bp** in parallel. Fill in the sign of your P&L and of your exposures after the move, then walk through why.

- *After the move*: **P&L: -, Duration after: +, Convexity after: -**
- *Written*: Walk through the P&L by component and the change in risk.

<details><summary>Model answer</summary>

**P&L -, duration +, convexity -.**

Duration-hedged MBS is flat duration today but short convexity: after a rally you are short duration, after a selloff long. Hedgers chase the move (convexity hedging).

Illustration (engine): P&L -GBP 615.3k; DV01 +GBP 0 to +GBP 15.8k.

</details>

**Q5** (`s5_l2_move`, topic `mixed:books`, seed 1896329)

The desk owns **GBP 100m of an MBS-like 4.5% 10Y callable bond, duration-hedged by paying fixed in 10Y swaps**.

Rates move **-75bp** in parallel. Fill in the sign of your P&L and of your exposures after the move, then walk through why.

- *After the move*: **P&L: -, Duration after: -, Convexity after: -**
- *Written*: Walk through the P&L by component and the change in risk.

<details><summary>Model answer</summary>

**P&L -, duration -, convexity -.**

Duration-hedged MBS is flat duration today but short convexity: after a rally you are short duration, after a selloff long. Hedgers chase the move (convexity hedging).

Illustration (engine): P&L -GBP 620.9k; DV01 +GBP 0 to -GBP 16.1k.

</details>

**Q6** (`s5_l2_move`, topic `mixed:books`, seed 1896360)

The desk is **long GBP 100m 1Y-into-10Y ATM payer swaptions, delta-hedged by receiving 10Y**.

Rates move **-75bp** in parallel. Fill in the sign of your P&L and of your exposures after the move, then walk through why.

- *After the move*: **P&L: +, Duration after: +, Convexity after: +**
- *Written*: Walk through the P&L by component and the change in risk.

<details><summary>Model answer</summary>

**P&L +, duration +, convexity +.**

A delta-hedged long payer is flat duration but long convexity: after a selloff you are short duration (you made money), after a rally long. Long gamma in rates.

Illustration (engine): P&L +GBP 1.04m; DV01 +GBP 0 to +GBP 26.6k.

</details>

**Q7** (`s5_l2_move`, topic `mixed:books`, seed 1896391)

The desk is **long GBP 100m 1Y-into-10Y ATM payer swaptions, delta-hedged by receiving 10Y**.

Rates move **+75bp** in parallel. Fill in the sign of your P&L and of your exposures after the move, then walk through why.

- *After the move*: **P&L: +, Duration after: -, Convexity after: +**
- *Written*: Walk through the P&L by component and the change in risk.

<details><summary>Model answer</summary>

**P&L +, duration -, convexity +.**

A delta-hedged long payer is flat duration but long convexity: after a selloff you are short duration (you made money), after a rally long. Long gamma in rates.

Illustration (engine): P&L +GBP 962.3k; DV01 +GBP 0 to -GBP 23.5k.

</details>

**Q8** (`s5_l2_move`, topic `mixed:books`, seed 1896422)

The desk owns **GBP 100m of an MBS-like 4.5% 10Y callable bond, duration-hedged by paying fixed in 10Y swaps**.

Rates move **-75bp** in parallel. Fill in the sign of your P&L and of your exposures after the move, then walk through why.

- *After the move*: **P&L: -, Duration after: -, Convexity after: -**
- *Written*: Walk through the P&L by component and the change in risk.

<details><summary>Model answer</summary>

**P&L -, duration -, convexity -.**

Duration-hedged MBS is flat duration today but short convexity: after a rally you are short duration, after a selloff long. Hedgers chase the move (convexity hedging).

Illustration (engine): P&L -GBP 620.9k; DV01 +GBP 0 to -GBP 16.1k.

</details>

**Q9** (`s5_l2_move`, topic `mixed:books`, seed 1896453)

The desk owns **GBP 100m of an MBS-like 4.5% 10Y callable bond, duration-hedged by paying fixed in 10Y swaps**.

Rates move **+75bp** in parallel. Fill in the sign of your P&L and of your exposures after the move, then walk through why.

- *After the move*: **P&L: -, Duration after: +, Convexity after: -**
- *Written*: Walk through the P&L by component and the change in risk.

<details><summary>Model answer</summary>

**P&L -, duration +, convexity -.**

Duration-hedged MBS is flat duration today but short convexity: after a rally you are short duration, after a selloff long. Hedgers chase the move (convexity hedging).

Illustration (engine): P&L -GBP 615.3k; DV01 +GBP 0 to +GBP 15.8k.

</details>

**Q10** (`s5_l2_move`, topic `mixed:books`, seed 1896484)

The desk **receives fixed on GBP 100m 10Y** and is **long GBP 100m 2Y-into-10Y ATM payer swaptions**.

Rates move **+75bp** in parallel. Fill in the sign of your P&L and of your exposures after the move, then walk through why.

- *After the move*: **P&L: -, Duration after: +, Convexity after: +**
- *Written*: Walk through the P&L by component and the change in risk.

<details><summary>Model answer</summary>

**P&L -, duration +, convexity +.**

Receiving 10Y is long duration with little convexity; the long payers are short duration and long convexity. In a selloff the payers' delta grows and offsets more of the swap loss.

Illustration (engine): P&L -GBP 2.80m; DV01 +GBP 47.6k to +GBP 28.1k.

</details>

### Level 3: calculations plus subtler concepts

**Q1** (`s5_l3_taylor`, topic `mixed:books_sized`, seed 2000934)

The desk **receives fixed on GBP 100m 10Y** and is **long GBP 100m 2Y-into-10Y ATM payer swaptions**.

Rates move **-50bp**. Using the DV01s and gammas in the Givens, estimate the book's P&L. Then explain how the risk has changed.

Givens:

| Given | Value |
|---|---|
| swap: DV01 (GBP/bp, + long duration) | 83,885 |
| swap: change in DV01 per +1bp (GBP/bp per bp) | -78.27 |
| swaption: DV01 (GBP/bp, + long duration) | -36,260 |
| swaption: change in DV01 per +1bp (GBP/bp per bp) | -216.14 |
| Parallel move (bp) | -50 |

- *P&L (GBP thousands)*: **2,749 k**
- *Written*: Walk through the P&L and the change in risk.

<details><summary>Model answer</summary>

**About +GBP 2.75m.**

1. Each leg: P&L ~ -DV01 x dy - 0.5 x G x dy^2, where G is how much the DV01 changes per +1bp (negative for long convexity).
2. Exact (engine, repriced): +GBP 2.75m; gap +GBP 5.6k from higher-order option terms.
3. Receiving 10Y is long duration with little convexity; the long payers are short duration and long convexity. In a selloff the payers' delta grows and offsets more of the swap loss.

</details>

**Q2** (`s5_l3_taylor`, topic `mixed:books_sized`, seed 2000965)

The desk owns **GBP 100m of an MBS-like 4.5% 10Y callable bond, duration-hedged by paying fixed in 10Y swaps**.

Rates move **-50bp**. Using the DV01s and gammas in the Givens, estimate the book's P&L. Then explain how the risk has changed.

Givens:

| Given | Value |
|---|---|
| callable bond: DV01 (GBP/bp, + long duration) | 46,479 |
| callable bond: change in DV01 per +1bp (GBP/bp per bp) | 183.50 |
| swap: DV01 (GBP/bp, + long duration) | -46,479 |
| swap: change in DV01 per +1bp (GBP/bp per bp) | 43.37 |
| Parallel move (bp) | -50 |

- *P&L (GBP thousands)*: **-283.59 k**
- *Written*: Walk through the P&L and the change in risk.

<details><summary>Model answer</summary>

**About -GBP 283.6k.**

1. Each leg: P&L ~ -DV01 x dy - 0.5 x G x dy^2, where G is how much the DV01 changes per +1bp (negative for long convexity).
2. Exact (engine, repriced): -GBP 280.3k; gap +GBP 3.3k from higher-order option terms.
3. Duration-hedged MBS is flat duration today but short convexity: after a rally you are short duration, after a selloff long. Hedgers chase the move (convexity hedging).

</details>

**Q3** (`s5_l3_taylor`, topic `mixed:books_sized`, seed 2000996)

The desk owns **GBP 100m of a 4.5% 10Y callable bond** (callable at par in 2 years), MBS-like.

Rates move **-50bp**. Using the DV01s and gammas in the Givens, estimate the book's P&L. Then explain how the risk has changed.

Givens:

| Given | Value |
|---|---|
| bond: DV01 (GBP/bp, + long duration) | 85,739 |
| bond: change in DV01 per +1bp (GBP/bp per bp) | -79.52 |
| swaption: DV01 (GBP/bp, + long duration) | -39,261 |
| swaption: change in DV01 per +1bp (GBP/bp per bp) | 263.02 |
| Parallel move (bp) | -50 |

- *P&L (GBP thousands)*: **2,095 k**
- *Written*: Walk through the P&L and the change in risk.

<details><summary>Model answer</summary>

**About +GBP 2.09m.**

1. Each leg: P&L ~ -DV01 x dy - 0.5 x G x dy^2, where G is how much the DV01 changes per +1bp (negative for long convexity).
2. Exact (engine, repriced): +GBP 2.10m; gap +GBP 4.2k from higher-order option terms.
3. A callable bond = bullet bond minus the issuer's call (a receiver swaption you are short). When rates fall it gets called, so duration shortens just when you want more: long duration, short convexity.

</details>

**Q4** (`s5_l3_taylor`, topic `mixed:books_sized`, seed 2001027)

The desk is **long GBP 100m 1Y-into-10Y ATM payer swaptions, delta-hedged by receiving 10Y**.

Rates move **-50bp**. Using the DV01s and gammas in the Givens, estimate the book's P&L. Then explain how the risk has changed.

Givens:

| Given | Value |
|---|---|
| swaption: DV01 (GBP/bp, + long duration) | -38,714 |
| swaption: change in DV01 per +1bp (GBP/bp per bp) | -344.10 |
| swap: DV01 (GBP/bp, + long duration) | 38,714 |
| swap: change in DV01 per +1bp (GBP/bp per bp) | -36.12 |
| Parallel move (bp) | -50 |

- *P&L (GBP thousands)*: **475.27 k**
- *Written*: Walk through the P&L and the change in risk.

<details><summary>Model answer</summary>

**About +GBP 475.3k.**

1. Each leg: P&L ~ -DV01 x dy - 0.5 x G x dy^2, where G is how much the DV01 changes per +1bp (negative for long convexity).
2. Exact (engine, repriced): +GBP 473.3k; gap -GBP 2.0k from higher-order option terms.
3. A delta-hedged long payer is flat duration but long convexity: after a selloff you are short duration (you made money), after a rally long. Long gamma in rates.

</details>

**Q5** (`s5_l3_taylor`, topic `mixed:books_sized`, seed 2001058)

The desk owns **GBP 100m of an MBS-like 4.5% 10Y callable bond, duration-hedged by paying fixed in 10Y swaps**.

Rates move **-50bp**. Using the DV01s and gammas in the Givens, estimate the book's P&L. Then explain how the risk has changed.

Givens:

| Given | Value |
|---|---|
| callable bond: DV01 (GBP/bp, + long duration) | 46,479 |
| callable bond: change in DV01 per +1bp (GBP/bp per bp) | 183.50 |
| swap: DV01 (GBP/bp, + long duration) | -46,479 |
| swap: change in DV01 per +1bp (GBP/bp per bp) | 43.37 |
| Parallel move (bp) | -50 |

- *P&L (GBP thousands)*: **-283.59 k**
- *Written*: Walk through the P&L and the change in risk.

<details><summary>Model answer</summary>

**About -GBP 283.6k.**

1. Each leg: P&L ~ -DV01 x dy - 0.5 x G x dy^2, where G is how much the DV01 changes per +1bp (negative for long convexity).
2. Exact (engine, repriced): -GBP 280.3k; gap +GBP 3.3k from higher-order option terms.
3. Duration-hedged MBS is flat duration today but short convexity: after a rally you are short duration, after a selloff long. Hedgers chase the move (convexity hedging).

</details>

**Q6** (`s5_l3_taylor`, topic `mixed:books_sized`, seed 2001089)

The desk owns **GBP 100m of a 4.5% 10Y gilt** and has **sold GBP 100m 1Y-into-9Y receiver swaptions** 25bp OTM.

Rates move **+50bp**. Using the DV01s and gammas in the Givens, estimate the book's P&L. Then explain how the risk has changed.

Givens:

| Given | Value |
|---|---|
| bond: DV01 (GBP/bp, + long duration) | 85,008 |
| bond: change in DV01 per +1bp (GBP/bp per bp) | -78.74 |
| swaption: DV01 (GBP/bp, + long duration) | -29,466 |
| swaption: change in DV01 per +1bp (GBP/bp per bp) | 372.71 |
| Parallel move (bp) | 50 |

- *P&L (GBP thousands)*: **-3,145 k**
- *Written*: Walk through the P&L and the change in risk.

<details><summary>Model answer</summary>

**About -GBP 3.14m.**

1. Each leg: P&L ~ -DV01 x dy - 0.5 x G x dy^2, where G is how much the DV01 changes per +1bp (negative for long convexity).
2. Exact (engine, repriced): -GBP 3.10m; gap +GBP 43.8k from higher-order option terms.
3. Selling receivers adds long duration that grows as rates fall and vanishes as they rise: short convexity, paid for with premium. Same shape as a callable bond or MBS.

</details>

**Q7** (`s5_l3_taylor`, topic `mixed:books_sized`, seed 2001120)

The desk owns **GBP 100m of an MBS-like 4.5% 10Y callable bond, duration-hedged by paying fixed in 10Y swaps**.

Rates move **+50bp**. Using the DV01s and gammas in the Givens, estimate the book's P&L. Then explain how the risk has changed.

Givens:

| Given | Value |
|---|---|
| callable bond: DV01 (GBP/bp, + long duration) | 46,479 |
| callable bond: change in DV01 per +1bp (GBP/bp per bp) | 183.50 |
| swap: DV01 (GBP/bp, + long duration) | -46,479 |
| swap: change in DV01 per +1bp (GBP/bp per bp) | 43.37 |
| Parallel move (bp) | 50 |

- *P&L (GBP thousands)*: **-283.59 k**
- *Written*: Walk through the P&L and the change in risk.

<details><summary>Model answer</summary>

**About -GBP 283.6k.**

1. Each leg: P&L ~ -DV01 x dy - 0.5 x G x dy^2, where G is how much the DV01 changes per +1bp (negative for long convexity).
2. Exact (engine, repriced): -GBP 278.8k; gap +GBP 4.7k from higher-order option terms.
3. Duration-hedged MBS is flat duration today but short convexity: after a rally you are short duration, after a selloff long. Hedgers chase the move (convexity hedging).

</details>

**Q8** (`s5_l3_taylor`, topic `mixed:books_sized`, seed 2001151)

The desk owns **GBP 100m of a 4.5% 10Y callable bond** (callable at par in 2 years), MBS-like.

Rates move **-75bp**. Using the DV01s and gammas in the Givens, estimate the book's P&L. Then explain how the risk has changed.

Givens:

| Given | Value |
|---|---|
| bond: DV01 (GBP/bp, + long duration) | 85,739 |
| bond: change in DV01 per +1bp (GBP/bp per bp) | -79.52 |
| swaption: DV01 (GBP/bp, + long duration) | -39,261 |
| swaption: change in DV01 per +1bp (GBP/bp per bp) | 263.02 |
| Parallel move (bp) | -75 |

- *P&L (GBP thousands)*: **2,970 k**
- *Written*: Walk through the P&L and the change in risk.

<details><summary>Model answer</summary>

**About +GBP 2.97m.**

1. Each leg: P&L ~ -DV01 x dy - 0.5 x G x dy^2, where G is how much the DV01 changes per +1bp (negative for long convexity).
2. Exact (engine, repriced): +GBP 2.99m; gap +GBP 20.2k from higher-order option terms.
3. A callable bond = bullet bond minus the issuer's call (a receiver swaption you are short). When rates fall it gets called, so duration shortens just when you want more: long duration, short convexity.

</details>

**Q9** (`s5_l3_taylor`, topic `mixed:books_sized`, seed 2001182)

The desk owns **GBP 100m of a 4.5% 10Y callable bond** (callable at par in 2 years), MBS-like.

Rates move **+50bp**. Using the DV01s and gammas in the Givens, estimate the book's P&L. Then explain how the risk has changed.

Givens:

| Given | Value |
|---|---|
| bond: DV01 (GBP/bp, + long duration) | 85,739 |
| bond: change in DV01 per +1bp (GBP/bp per bp) | -79.52 |
| swaption: DV01 (GBP/bp, + long duration) | -39,261 |
| swaption: change in DV01 per +1bp (GBP/bp per bp) | 263.02 |
| Parallel move (bp) | 50 |

- *P&L (GBP thousands)*: **-2,553 k**
- *Written*: Walk through the P&L and the change in risk.

<details><summary>Model answer</summary>

**About -GBP 2.55m.**

1. Each leg: P&L ~ -DV01 x dy - 0.5 x G x dy^2, where G is how much the DV01 changes per +1bp (negative for long convexity).
2. Exact (engine, repriced): -GBP 2.55m; gap +GBP 3.8k from higher-order option terms.
3. A callable bond = bullet bond minus the issuer's call (a receiver swaption you are short). When rates fall it gets called, so duration shortens just when you want more: long duration, short convexity.

</details>

**Q10** (`s5_l3_taylor`, topic `mixed:books_sized`, seed 2001213)

The desk owns **GBP 100m of a 4.5% 10Y gilt** and has **sold GBP 100m 1Y-into-9Y receiver swaptions** 25bp OTM.

Rates move **-50bp**. Using the DV01s and gammas in the Givens, estimate the book's P&L. Then explain how the risk has changed.

Givens:

| Given | Value |
|---|---|
| bond: DV01 (GBP/bp, + long duration) | 85,008 |
| bond: change in DV01 per +1bp (GBP/bp per bp) | -78.74 |
| swaption: DV01 (GBP/bp, + long duration) | -29,466 |
| swaption: change in DV01 per +1bp (GBP/bp per bp) | 372.71 |
| Parallel move (bp) | -50 |

- *P&L (GBP thousands)*: **2,410 k**
- *Written*: Walk through the P&L and the change in risk.

<details><summary>Model answer</summary>

**About +GBP 2.41m.**

1. Each leg: P&L ~ -DV01 x dy - 0.5 x G x dy^2, where G is how much the DV01 changes per +1bp (negative for long convexity).
2. Exact (engine, repriced): +GBP 2.39m; gap -GBP 22.2k from higher-order option terms.
3. Selling receivers adds long duration that grows as rates fall and vanishes as they rise: short convexity, paid for with premium. Same shape as a callable bond or MBS.

</details>

## 2B Convexity intuition

### Level 1: directional intuition, no calculations

**Q1** (`b_l1_barbell`, topic `convexity:barbell`, seed 1023333)

A 10Y zero (bullet) vs a 2Y/30Y zero barbell with the **same PV and DV01**. Yields jump 100bp, up or down. Which does better? What do you give up for that?

- *Better in a big parallel move*: **The barbell, in either direction**
- *Written*: Explain, including the cost.

<details><summary>Model answer</summary>

**The barbell, both ways.**

1. Same duration, but the barbell's cash flows are spread out, and convexity grows roughly with maturity squared: the 30Y wing adds far more convexity than the 2Y wing loses.
2. You pay for it: lower yield/carry in a fair market, and the barbell is SHORT the belly vs the wings, so it loses if the 10Y richens relative to 2Y and 30Y.
3. Same trade-off as gamma vs theta.

</details>

**Q2** (`b_l1_mbs`, topic `convexity:mortgage`, seed 1023364)

Rates rally hard. What do MBS holders who hedge their duration do, and what does it do to the market?

- *Hedging flow*: **Receive fixed / buy duration, pushing yields lower still**
- *Written*: Explain the chain.

<details><summary>Model answer</summary>

**They buy duration.** MBS holders are short the borrowers' prepayment option: as rates fall, borrowers refinance, the MBS shortens (negative convexity), so hedgers must receive fixed or buy long bonds to get duration back. That flow chases the move and amplifies it.

</details>

**Q3** (`b_l1_cost`, topic `convexity:cost`, seed 1023395)

You add long convexity to a rates book (buy a swaption straddle, or swap a bullet for a barbell). What do you pay for it?

- *Cost*: **Premium or lower yield/carry: you pay for convexity like you pay theta for gamma**
- *Written*: Explain the analogy with options.

<details><summary>Model answer</summary>

**You pay premium or give up yield.** Long convexity gains from big moves either way, so the market charges for it: option premium decays (theta), or the higher-convexity bond yields less. If rates sit still, you bleed.

</details>

**Q4** (`b_l1_mbs`, topic `convexity:mortgage`, seed 1023426)

Rates rally hard. What do MBS holders who hedge their duration do, and what does it do to the market?

- *Hedging flow*: **Receive fixed / buy duration, pushing yields lower still**
- *Written*: Explain the chain.

<details><summary>Model answer</summary>

**They buy duration.** MBS holders are short the borrowers' prepayment option: as rates fall, borrowers refinance, the MBS shortens (negative convexity), so hedgers must receive fixed or buy long bonds to get duration back. That flow chases the move and amplifies it.

</details>

**Q5** (`b_l1_barbell`, topic `convexity:barbell`, seed 1023457)

A 10Y zero (bullet) vs a 2Y/30Y zero barbell with the **same PV and DV01**. Yields jump 100bp, up or down. Which does better? What do you give up for that?

- *Better in a big parallel move*: **The barbell, in either direction**
- *Written*: Explain, including the cost.

<details><summary>Model answer</summary>

**The barbell, both ways.**

1. Same duration, but the barbell's cash flows are spread out, and convexity grows roughly with maturity squared: the 30Y wing adds far more convexity than the 2Y wing loses.
2. You pay for it: lower yield/carry in a fair market, and the barbell is SHORT the belly vs the wings, so it loses if the 10Y richens relative to 2Y and 30Y.
3. Same trade-off as gamma vs theta.

</details>

**Q6** (`b_l1_mbs`, topic `convexity:mortgage`, seed 1023488)

Rates rally hard. What do MBS holders who hedge their duration do, and what does it do to the market?

- *Hedging flow*: **Receive fixed / buy duration, pushing yields lower still**
- *Written*: Explain the chain.

<details><summary>Model answer</summary>

**They buy duration.** MBS holders are short the borrowers' prepayment option: as rates fall, borrowers refinance, the MBS shortens (negative convexity), so hedgers must receive fixed or buy long bonds to get duration back. That flow chases the move and amplifies it.

</details>

**Q7** (`b_l1_mbs`, topic `convexity:mortgage`, seed 1023519)

Rates rally hard. What do MBS holders who hedge their duration do, and what does it do to the market?

- *Hedging flow*: **Receive fixed / buy duration, pushing yields lower still**
- *Written*: Explain the chain.

<details><summary>Model answer</summary>

**They buy duration.** MBS holders are short the borrowers' prepayment option: as rates fall, borrowers refinance, the MBS shortens (negative convexity), so hedgers must receive fixed or buy long bonds to get duration back. That flow chases the move and amplifies it.

</details>

**Q8** (`b_l1_mbs`, topic `convexity:mortgage`, seed 1023550)

Rates rally hard. What do MBS holders who hedge their duration do, and what does it do to the market?

- *Hedging flow*: **Receive fixed / buy duration, pushing yields lower still**
- *Written*: Explain the chain.

<details><summary>Model answer</summary>

**They buy duration.** MBS holders are short the borrowers' prepayment option: as rates fall, borrowers refinance, the MBS shortens (negative convexity), so hedgers must receive fixed or buy long bonds to get duration back. That flow chases the move and amplifies it.

</details>

**Q9** (`b_l1_mbs`, topic `convexity:mortgage`, seed 1023581)

Rates rally hard. What do MBS holders who hedge their duration do, and what does it do to the market?

- *Hedging flow*: **Receive fixed / buy duration, pushing yields lower still**
- *Written*: Explain the chain.

<details><summary>Model answer</summary>

**They buy duration.** MBS holders are short the borrowers' prepayment option: as rates fall, borrowers refinance, the MBS shortens (negative convexity), so hedgers must receive fixed or buy long bonds to get duration back. That flow chases the move and amplifies it.

</details>

**Q10** (`b_l1_mbs`, topic `convexity:mortgage`, seed 1023612)

Rates rally hard. What do MBS holders who hedge their duration do, and what does it do to the market?

- *Hedging flow*: **Receive fixed / buy duration, pushing yields lower still**
- *Written*: Explain the chain.

<details><summary>Model answer</summary>

**They buy duration.** MBS holders are short the borrowers' prepayment option: as rates fall, borrowers refinance, the MBS shortens (negative convexity), so hedgers must receive fixed or buy long bonds to get duration back. That flow chases the move and amplifies it.

</details>

### Level 2: combinations, light calculations with every input given

**Q1** (`b_l2_barbell`, topic `convexity:barbell`, seed 1128062)

Bullet vs barbell with the same PV and duration (Givens). Estimate how much more the barbell makes than the bullet if yields move 150bp in either direction.

Givens:

| Given | Value |
|---|---|
| PV of each portfolio (GBP) | 66,697,681 |
| Bullet convexity (years^2) | 100.01 |
| Barbell convexity (years^2) | 260.12 |
| Parallel move (bp, either way) | 150 |

- *Barbell minus bullet (GBP k)*: **1,201 k**
- *Written*: What do you give up for it?

<details><summary>Model answer</summary>

**About +GBP 1.20m.**

1. Equal duration, so the duration terms cancel; only convexity is left: 0.5 x (C_barbell - C_bullet) x PV x dy^2.
2. Exact (engine, -150bp): +GBP 1.49m.
3. The cost: lower yield, and exposure to the belly richening vs the wings.

</details>

**Q2** (`b_l2_maturity`, topic `convexity:maturity`, seed 1128093)

For an annual zero, convexity = T(T+1)/(1+y)^2. How many times more convexity does the 30Y zero have than the 10Y zero?

Givens:

| Given | Value |
|---|---|
| Maturity of zero A (years) | 10 |
| Maturity of zero B (years) | 30 |
| Yield (%, annual comp.) | 4 |

- *Ratio*: **8.45 x**
- *Written*: Explain the scaling.

<details><summary>Model answer</summary>

**8.45x.** The (1+y)^2 terms cancel: 30x31 / (10x11) = 8.45. Engine check: 859.8 vs 101.7. Convexity lives at the long end.

</details>

**Q3** (`b_l2_maturity`, topic `convexity:maturity`, seed 1128124)

For an annual zero, convexity = T(T+1)/(1+y)^2. How many times more convexity does the 10Y zero have than the 5Y zero?

Givens:

| Given | Value |
|---|---|
| Maturity of zero A (years) | 5 |
| Maturity of zero B (years) | 10 |
| Yield (%, annual comp.) | 4 |

- *Ratio*: **3.67 x**
- *Written*: Explain the scaling.

<details><summary>Model answer</summary>

**3.67x.** The (1+y)^2 terms cancel: 10x11 / (5x6) = 3.67. Engine check: 101.7 vs 27.7. Convexity lives at the long end.

</details>

**Q4** (`b_l2_barbell`, topic `convexity:barbell`, seed 1128155)

Bullet vs barbell with the same PV and duration (Givens). Estimate how much more the barbell makes than the bullet if yields move 75bp in either direction.

Givens:

| Given | Value |
|---|---|
| PV of each portfolio (GBP) | 66,697,681 |
| Bullet convexity (years^2) | 100.01 |
| Barbell convexity (years^2) | 260.12 |
| Parallel move (bp, either way) | 75 |

- *Barbell minus bullet (GBP k)*: **300.35 k**
- *Written*: What do you give up for it?

<details><summary>Model answer</summary>

**About +GBP 300.3k.**

1. Equal duration, so the duration terms cancel; only convexity is left: 0.5 x (C_barbell - C_bullet) x PV x dy^2.
2. Exact (engine, -75bp): +GBP 333.7k.
3. The cost: lower yield, and exposure to the belly richening vs the wings.

</details>

**Q5** (`b_l2_maturity`, topic `convexity:maturity`, seed 1128186)

For an annual zero, convexity = T(T+1)/(1+y)^2. How many times more convexity does the 10Y zero have than the 5Y zero?

Givens:

| Given | Value |
|---|---|
| Maturity of zero A (years) | 5 |
| Maturity of zero B (years) | 10 |
| Yield (%, annual comp.) | 4 |

- *Ratio*: **3.67 x**
- *Written*: Explain the scaling.

<details><summary>Model answer</summary>

**3.67x.** The (1+y)^2 terms cancel: 10x11 / (5x6) = 3.67. Engine check: 101.7 vs 27.7. Convexity lives at the long end.

</details>

**Q6** (`b_l2_maturity`, topic `convexity:maturity`, seed 1128217)

For an annual zero, convexity = T(T+1)/(1+y)^2. How many times more convexity does the 20Y zero have than the 5Y zero?

Givens:

| Given | Value |
|---|---|
| Maturity of zero A (years) | 5 |
| Maturity of zero B (years) | 20 |
| Yield (%, annual comp.) | 4 |

- *Ratio*: **14.00 x**
- *Written*: Explain the scaling.

<details><summary>Model answer</summary>

**14.00x.** The (1+y)^2 terms cancel: 20x21 / (5x6) = 14.00. Engine check: 388.3 vs 27.7. Convexity lives at the long end.

</details>

**Q7** (`b_l2_maturity`, topic `convexity:maturity`, seed 1128248)

For an annual zero, convexity = T(T+1)/(1+y)^2. How many times more convexity does the 30Y zero have than the 10Y zero?

Givens:

| Given | Value |
|---|---|
| Maturity of zero A (years) | 10 |
| Maturity of zero B (years) | 30 |
| Yield (%, annual comp.) | 4 |

- *Ratio*: **8.45 x**
- *Written*: Explain the scaling.

<details><summary>Model answer</summary>

**8.45x.** The (1+y)^2 terms cancel: 30x31 / (10x11) = 8.45. Engine check: 859.8 vs 101.7. Convexity lives at the long end.

</details>

**Q8** (`b_l2_barbell`, topic `convexity:barbell`, seed 1128279)

Bullet vs barbell with the same PV and duration (Givens). Estimate how much more the barbell makes than the bullet if yields move 100bp in either direction.

Givens:

| Given | Value |
|---|---|
| PV of each portfolio (GBP) | 66,697,681 |
| Bullet convexity (years^2) | 100.01 |
| Barbell convexity (years^2) | 260.12 |
| Parallel move (bp, either way) | 100 |

- *Barbell minus bullet (GBP k)*: **533.95 k**
- *Written*: What do you give up for it?

<details><summary>Model answer</summary>

**About +GBP 533.9k.**

1. Equal duration, so the duration terms cancel; only convexity is left: 0.5 x (C_barbell - C_bullet) x PV x dy^2.
2. Exact (engine, -100bp): +GBP 614.8k.
3. The cost: lower yield, and exposure to the belly richening vs the wings.

</details>

**Q9** (`b_l2_barbell`, topic `convexity:barbell`, seed 1128310)

Bullet vs barbell with the same PV and duration (Givens). Estimate how much more the barbell makes than the bullet if yields move 75bp in either direction.

Givens:

| Given | Value |
|---|---|
| PV of each portfolio (GBP) | 66,697,681 |
| Bullet convexity (years^2) | 100.01 |
| Barbell convexity (years^2) | 260.12 |
| Parallel move (bp, either way) | 75 |

- *Barbell minus bullet (GBP k)*: **300.35 k**
- *Written*: What do you give up for it?

<details><summary>Model answer</summary>

**About +GBP 300.3k.**

1. Equal duration, so the duration terms cancel; only convexity is left: 0.5 x (C_barbell - C_bullet) x PV x dy^2.
2. Exact (engine, -75bp): +GBP 333.7k.
3. The cost: lower yield, and exposure to the belly richening vs the wings.

</details>

**Q10** (`b_l2_barbell`, topic `convexity:barbell`, seed 1128341)

Bullet vs barbell with the same PV and duration (Givens). Estimate how much more the barbell makes than the bullet if yields move 150bp in either direction.

Givens:

| Given | Value |
|---|---|
| PV of each portfolio (GBP) | 66,697,681 |
| Bullet convexity (years^2) | 100.01 |
| Barbell convexity (years^2) | 260.12 |
| Parallel move (bp, either way) | 150 |

- *Barbell minus bullet (GBP k)*: **1,201 k**
- *Written*: What do you give up for it?

<details><summary>Model answer</summary>

**About +GBP 1.20m.**

1. Equal duration, so the duration terms cancel; only convexity is left: 0.5 x (C_barbell - C_bullet) x PV x dy^2.
2. Exact (engine, -150bp): +GBP 1.49m.
3. The cost: lower yield, and exposure to the belly richening vs the wings.

</details>

### Level 3: calculations plus subtler concepts

**Q1** (`b_l3_straddle`, topic `convexity:cost`, seed 1232791)

You buy GBP 100m of a 1Y-into-10Y ATM swaption straddle (implied normal vol 85bp). (a) How far must the forward swap rate move by expiry, either way, to break even? (b) If the rate's realised normal vol over the year turns out to be 65bp, what is your expected P&L at expiry? (E|move| = sigma x sqrt(2/pi).)

Givens:

| Given | Value |
|---|---|
| Straddle premium (GBP) | 5,336,411 |
| Forward annuity PV per bp (GBP) | 78,685 |
| Realised normal vol of the forward rate over the year (bp) | 65 |

- *(a) Breakeven (bp)*: **67.82 bp**
- *(b) Expected P&L (GBP k)*: **-1,256 k**
- *Written*: How is this like gamma vs theta?

<details><summary>Model answer</summary>

**(a) 68bp, (b) -GBP 1.26m.**

1. At expiry the straddle pays annuity x |move|, so breakeven = premium / (annuity PV per bp).
2. Expected payoff = annuity x E|move| = annuity x 65 x 0.798 = +GBP 4.08m; minus the premium gives (b).
3. For an ATM straddle the breakeven equals E|move| at the IMPLIED vol (85bp x 0.798), so you make money exactly when realised beats implied: pure long convexity, paid for up front (theta).

</details>

**Q2** (`b_l3_straddle`, topic `convexity:cost`, seed 1232822)

You buy GBP 100m of a 1Y-into-10Y ATM swaption straddle (implied normal vol 85bp). (a) How far must the forward swap rate move by expiry, either way, to break even? (b) If the rate's realised normal vol over the year turns out to be 55bp, what is your expected P&L at expiry? (E|move| = sigma x sqrt(2/pi).)

Givens:

| Given | Value |
|---|---|
| Straddle premium (GBP) | 5,336,411 |
| Forward annuity PV per bp (GBP) | 78,685 |
| Realised normal vol of the forward rate over the year (bp) | 55 |

- *(a) Breakeven (bp)*: **67.82 bp**
- *(b) Expected P&L (GBP k)*: **-1,883 k**
- *Written*: How is this like gamma vs theta?

<details><summary>Model answer</summary>

**(a) 68bp, (b) -GBP 1.88m.**

1. At expiry the straddle pays annuity x |move|, so breakeven = premium / (annuity PV per bp).
2. Expected payoff = annuity x E|move| = annuity x 55 x 0.798 = +GBP 3.45m; minus the premium gives (b).
3. For an ATM straddle the breakeven equals E|move| at the IMPLIED vol (85bp x 0.798), so you make money exactly when realised beats implied: pure long convexity, paid for up front (theta).

</details>

**Q3** (`b_l3_straddle`, topic `convexity:cost`, seed 1232853)

You buy GBP 100m of a 1Y-into-10Y ATM swaption straddle (implied normal vol 85bp). (a) How far must the forward swap rate move by expiry, either way, to break even? (b) If the rate's realised normal vol over the year turns out to be 110bp, what is your expected P&L at expiry? (E|move| = sigma x sqrt(2/pi).)

Givens:

| Given | Value |
|---|---|
| Straddle premium (GBP) | 5,336,411 |
| Forward annuity PV per bp (GBP) | 78,685 |
| Realised normal vol of the forward rate over the year (bp) | 110 |

- *(a) Breakeven (bp)*: **67.82 bp**
- *(b) Expected P&L (GBP k)*: **1,570 k**
- *Written*: How is this like gamma vs theta?

<details><summary>Model answer</summary>

**(a) 68bp, (b) +GBP 1.57m.**

1. At expiry the straddle pays annuity x |move|, so breakeven = premium / (annuity PV per bp).
2. Expected payoff = annuity x E|move| = annuity x 110 x 0.798 = +GBP 6.91m; minus the premium gives (b).
3. For an ATM straddle the breakeven equals E|move| at the IMPLIED vol (85bp x 0.798), so you make money exactly when realised beats implied: pure long convexity, paid for up front (theta).

</details>

**Q4** (`b_l3_straddle`, topic `convexity:cost`, seed 1232884)

You buy GBP 100m of a 1Y-into-10Y ATM swaption straddle (implied normal vol 85bp). (a) How far must the forward swap rate move by expiry, either way, to break even? (b) If the rate's realised normal vol over the year turns out to be 95bp, what is your expected P&L at expiry? (E|move| = sigma x sqrt(2/pi).)

Givens:

| Given | Value |
|---|---|
| Straddle premium (GBP) | 5,336,411 |
| Forward annuity PV per bp (GBP) | 78,685 |
| Realised normal vol of the forward rate over the year (bp) | 95 |

- *(a) Breakeven (bp)*: **67.82 bp**
- *(b) Expected P&L (GBP k)*: **627.95 k**
- *Written*: How is this like gamma vs theta?

<details><summary>Model answer</summary>

**(a) 68bp, (b) +GBP 628.0k.**

1. At expiry the straddle pays annuity x |move|, so breakeven = premium / (annuity PV per bp).
2. Expected payoff = annuity x E|move| = annuity x 95 x 0.798 = +GBP 5.96m; minus the premium gives (b).
3. For an ATM straddle the breakeven equals E|move| at the IMPLIED vol (85bp x 0.798), so you make money exactly when realised beats implied: pure long convexity, paid for up front (theta).

</details>

**Q5** (`b_l3_straddle`, topic `convexity:cost`, seed 1232915)

You buy GBP 100m of a 1Y-into-10Y ATM swaption straddle (implied normal vol 85bp). (a) How far must the forward swap rate move by expiry, either way, to break even? (b) If the rate's realised normal vol over the year turns out to be 110bp, what is your expected P&L at expiry? (E|move| = sigma x sqrt(2/pi).)

Givens:

| Given | Value |
|---|---|
| Straddle premium (GBP) | 5,336,411 |
| Forward annuity PV per bp (GBP) | 78,685 |
| Realised normal vol of the forward rate over the year (bp) | 110 |

- *(a) Breakeven (bp)*: **67.82 bp**
- *(b) Expected P&L (GBP k)*: **1,570 k**
- *Written*: How is this like gamma vs theta?

<details><summary>Model answer</summary>

**(a) 68bp, (b) +GBP 1.57m.**

1. At expiry the straddle pays annuity x |move|, so breakeven = premium / (annuity PV per bp).
2. Expected payoff = annuity x E|move| = annuity x 110 x 0.798 = +GBP 6.91m; minus the premium gives (b).
3. For an ATM straddle the breakeven equals E|move| at the IMPLIED vol (85bp x 0.798), so you make money exactly when realised beats implied: pure long convexity, paid for up front (theta).

</details>

**Q6** (`b_l3_straddle`, topic `convexity:cost`, seed 1232946)

You buy GBP 100m of a 1Y-into-10Y ATM swaption straddle (implied normal vol 85bp). (a) How far must the forward swap rate move by expiry, either way, to break even? (b) If the rate's realised normal vol over the year turns out to be 65bp, what is your expected P&L at expiry? (E|move| = sigma x sqrt(2/pi).)

Givens:

| Given | Value |
|---|---|
| Straddle premium (GBP) | 5,336,411 |
| Forward annuity PV per bp (GBP) | 78,685 |
| Realised normal vol of the forward rate over the year (bp) | 65 |

- *(a) Breakeven (bp)*: **67.82 bp**
- *(b) Expected P&L (GBP k)*: **-1,256 k**
- *Written*: How is this like gamma vs theta?

<details><summary>Model answer</summary>

**(a) 68bp, (b) -GBP 1.26m.**

1. At expiry the straddle pays annuity x |move|, so breakeven = premium / (annuity PV per bp).
2. Expected payoff = annuity x E|move| = annuity x 65 x 0.798 = +GBP 4.08m; minus the premium gives (b).
3. For an ATM straddle the breakeven equals E|move| at the IMPLIED vol (85bp x 0.798), so you make money exactly when realised beats implied: pure long convexity, paid for up front (theta).

</details>

**Q7** (`b_l3_straddle`, topic `convexity:cost`, seed 1232977)

You buy GBP 100m of a 1Y-into-10Y ATM swaption straddle (implied normal vol 85bp). (a) How far must the forward swap rate move by expiry, either way, to break even? (b) If the rate's realised normal vol over the year turns out to be 55bp, what is your expected P&L at expiry? (E|move| = sigma x sqrt(2/pi).)

Givens:

| Given | Value |
|---|---|
| Straddle premium (GBP) | 5,336,411 |
| Forward annuity PV per bp (GBP) | 78,685 |
| Realised normal vol of the forward rate over the year (bp) | 55 |

- *(a) Breakeven (bp)*: **67.82 bp**
- *(b) Expected P&L (GBP k)*: **-1,883 k**
- *Written*: How is this like gamma vs theta?

<details><summary>Model answer</summary>

**(a) 68bp, (b) -GBP 1.88m.**

1. At expiry the straddle pays annuity x |move|, so breakeven = premium / (annuity PV per bp).
2. Expected payoff = annuity x E|move| = annuity x 55 x 0.798 = +GBP 3.45m; minus the premium gives (b).
3. For an ATM straddle the breakeven equals E|move| at the IMPLIED vol (85bp x 0.798), so you make money exactly when realised beats implied: pure long convexity, paid for up front (theta).

</details>

**Q8** (`b_l3_straddle`, topic `convexity:cost`, seed 1233008)

You buy GBP 100m of a 1Y-into-10Y ATM swaption straddle (implied normal vol 85bp). (a) How far must the forward swap rate move by expiry, either way, to break even? (b) If the rate's realised normal vol over the year turns out to be 95bp, what is your expected P&L at expiry? (E|move| = sigma x sqrt(2/pi).)

Givens:

| Given | Value |
|---|---|
| Straddle premium (GBP) | 5,336,411 |
| Forward annuity PV per bp (GBP) | 78,685 |
| Realised normal vol of the forward rate over the year (bp) | 95 |

- *(a) Breakeven (bp)*: **67.82 bp**
- *(b) Expected P&L (GBP k)*: **627.95 k**
- *Written*: How is this like gamma vs theta?

<details><summary>Model answer</summary>

**(a) 68bp, (b) +GBP 628.0k.**

1. At expiry the straddle pays annuity x |move|, so breakeven = premium / (annuity PV per bp).
2. Expected payoff = annuity x E|move| = annuity x 95 x 0.798 = +GBP 5.96m; minus the premium gives (b).
3. For an ATM straddle the breakeven equals E|move| at the IMPLIED vol (85bp x 0.798), so you make money exactly when realised beats implied: pure long convexity, paid for up front (theta).

</details>

**Q9** (`b_l3_straddle`, topic `convexity:cost`, seed 1233039)

You buy GBP 100m of a 1Y-into-10Y ATM swaption straddle (implied normal vol 85bp). (a) How far must the forward swap rate move by expiry, either way, to break even? (b) If the rate's realised normal vol over the year turns out to be 55bp, what is your expected P&L at expiry? (E|move| = sigma x sqrt(2/pi).)

Givens:

| Given | Value |
|---|---|
| Straddle premium (GBP) | 5,336,411 |
| Forward annuity PV per bp (GBP) | 78,685 |
| Realised normal vol of the forward rate over the year (bp) | 55 |

- *(a) Breakeven (bp)*: **67.82 bp**
- *(b) Expected P&L (GBP k)*: **-1,883 k**
- *Written*: How is this like gamma vs theta?

<details><summary>Model answer</summary>

**(a) 68bp, (b) -GBP 1.88m.**

1. At expiry the straddle pays annuity x |move|, so breakeven = premium / (annuity PV per bp).
2. Expected payoff = annuity x E|move| = annuity x 55 x 0.798 = +GBP 3.45m; minus the premium gives (b).
3. For an ATM straddle the breakeven equals E|move| at the IMPLIED vol (85bp x 0.798), so you make money exactly when realised beats implied: pure long convexity, paid for up front (theta).

</details>

**Q10** (`b_l3_straddle`, topic `convexity:cost`, seed 1233070)

You buy GBP 100m of a 1Y-into-10Y ATM swaption straddle (implied normal vol 85bp). (a) How far must the forward swap rate move by expiry, either way, to break even? (b) If the rate's realised normal vol over the year turns out to be 75bp, what is your expected P&L at expiry? (E|move| = sigma x sqrt(2/pi).)

Givens:

| Given | Value |
|---|---|
| Straddle premium (GBP) | 5,336,411 |
| Forward annuity PV per bp (GBP) | 78,685 |
| Realised normal vol of the forward rate over the year (bp) | 75 |

- *(a) Breakeven (bp)*: **67.82 bp**
- *(b) Expected P&L (GBP k)*: **-627.70 k**
- *Written*: How is this like gamma vs theta?

<details><summary>Model answer</summary>

**(a) 68bp, (b) -GBP 627.7k.**

1. At expiry the straddle pays annuity x |move|, so breakeven = premium / (annuity PV per bp).
2. Expected payoff = annuity x E|move| = annuity x 75 x 0.798 = +GBP 4.71m; minus the premium gives (b).
3. For an ATM straddle the breakeven equals E|move| at the IMPLIED vol (85bp x 0.798), so you make money exactly when realised beats implied: pure long convexity, paid for up front (theta).

</details>

## 2C Curve trades

### Level 1: directional intuition, no calculations

**Q1** (`c_l1_boe`, topic `curve:expression`, seed 1031252)

You think the BoE cuts sooner than the market prices. What curve trade expresses it?

- *Trade*: **Receive 2Y vs pay 10Y, DV01-weighted (steepener)**
- *Written*: Explain, including the main risks.

<details><summary>Model answer</summary>

**Receive the front end: a DV01-neutral 2s10s steepener.** Earlier cuts pull down expected policy rates over the next 1-2 years, so the front end rallies most (bull steepener). DV01 weighting removes the bet on the level. Risks: growth fears rally the long end too (bull flattener), and the steepener is short convexity.

</details>

**Q2** (`c_l1_convexity_sign`, topic `curve:convexity`, seed 1031283)

You hold a **DV01-neutral 2s10s flattener**. Are you long or short convexity, and why?

- *Convexity*: **Long**
- *Written*: Explain using convexity per unit of DV01, and how it interacts with a bull or bear move.

<details><summary>Model answer</summary>

**A DV01-neutral steepener is SHORT convexity; a flattener is LONG convexity.**

1. Convexity per unit of DV01 rises with maturity, so the 10Y leg carries far more convexity than the 2Y leg for the same DV01.
2. A steepener pays fixed in 10Y (short the 10Y's convexity) and receives 2Y (long a little): net short. Big parallel moves either way hurt the steepener and help the flattener, all else equal.
3. Interaction: in a bull steepener the slope gain is partly offset by the convexity loss; in a large bear flattener the flattener earns both slope and convexity.
4. Illustration (engine): +/-25bp convexity P&L of this flattener = +GBP 38.5k.

</details>

**Q3** (`c_l1_label`, topic `curve:labels`, seed 1031314)

2Y SONIA swaps move **+5bp** and 10Y move **+39bp**. What kind of move is this? Does a DV01-neutral 2s10s steepener make or lose money?

- *Curve move*: **Bear steepener**
- *Steepener*: **Makes money**
- *Written*: What typically drives this kind of move?

<details><summary>Model answer</summary>

**Bear steepener; the steepener makes money.**

1. Bull = yields fall, bear = yields rise; steepener = 10Y minus 2Y widens.
2. The curve steepened by 34bp. A DV01-neutral steepener (receive 2Y, pay 10Y) earns DV01 x (change in 10Y - change in 2Y).
3. Typical driver: long end sells off more: term premium, supply, fiscal or inflation worries.

</details>

**Q4** (`c_l1_label`, topic `curve:labels`, seed 1031345)

2Y SONIA swaps move **-11bp** and 10Y move **-27bp**. What kind of move is this? Does a DV01-neutral 2s10s steepener make or lose money?

- *Curve move*: **Bull flattener**
- *Steepener*: **Loses money**
- *Written*: What typically drives this kind of move?

<details><summary>Model answer</summary>

**Bull flattener; the steepener loses money.**

1. Bull = yields fall, bear = yields rise; steepener = 10Y minus 2Y widens.
2. The curve flattened by 16bp. A DV01-neutral steepener (receive 2Y, pay 10Y) earns DV01 x (change in 10Y - change in 2Y).
3. Typical driver: long end rallies more: growth/inflation fears, flight to duration, long-end demand.

</details>

**Q5** (`c_l1_convexity_big_move`, topic `curve:convexity`, seed 1031376)

You hold a **DV01-neutral 2s10s flattener**. The whole curve moves -75bp in parallel (no change in slope). Do you make or lose money?

- *P&L*: **Gain**
- *Written*: Explain using convexity per unit of DV01, and how it interacts with a bull or bear move.

<details><summary>Model answer</summary>

**A DV01-neutral steepener is SHORT convexity; a flattener is LONG convexity.**

1. Convexity per unit of DV01 rises with maturity, so the 10Y leg carries far more convexity than the 2Y leg for the same DV01.
2. A steepener pays fixed in 10Y (short the 10Y's convexity) and receives 2Y (long a little): net short. Big parallel moves either way hurt the steepener and help the flattener, all else equal.
3. Interaction: in a bull steepener the slope gain is partly offset by the convexity loss; in a large bear flattener the flattener earns both slope and convexity.
4. Illustration (engine): +/-25bp convexity P&L of this flattener = +GBP 38.5k.

</details>

**Q6** (`c_l1_label`, topic `curve:labels`, seed 1031407)

2Y SONIA swaps move **+26bp** and 10Y move **+7bp**. What kind of move is this? Does a DV01-neutral 2s10s steepener make or lose money?

- *Curve move*: **Bear flattener**
- *Steepener*: **Loses money**
- *Written*: What typically drives this kind of move?

<details><summary>Model answer</summary>

**Bear flattener; the steepener loses money.**

1. Bull = yields fall, bear = yields rise; steepener = 10Y minus 2Y widens.
2. The curve flattened by 19bp. A DV01-neutral steepener (receive 2Y, pay 10Y) earns DV01 x (change in 10Y - change in 2Y).
3. Typical driver: front end sells off more: hikes, or cuts priced out.

</details>

**Q7** (`c_l1_boe`, topic `curve:expression`, seed 1031438)

You think the BoE cuts sooner than the market prices. What curve trade expresses it?

- *Trade*: **Receive 2Y vs pay 10Y, DV01-weighted (steepener)**
- *Written*: Explain, including the main risks.

<details><summary>Model answer</summary>

**Receive the front end: a DV01-neutral 2s10s steepener.** Earlier cuts pull down expected policy rates over the next 1-2 years, so the front end rallies most (bull steepener). DV01 weighting removes the bet on the level. Risks: growth fears rally the long end too (bull flattener), and the steepener is short convexity.

</details>

**Q8** (`c_l1_boe`, topic `curve:expression`, seed 1031469)

You think the BoE cuts sooner than the market prices. What curve trade expresses it?

- *Trade*: **Receive 2Y vs pay 10Y, DV01-weighted (steepener)**
- *Written*: Explain, including the main risks.

<details><summary>Model answer</summary>

**Receive the front end: a DV01-neutral 2s10s steepener.** Earlier cuts pull down expected policy rates over the next 1-2 years, so the front end rallies most (bull steepener). DV01 weighting removes the bet on the level. Risks: growth fears rally the long end too (bull flattener), and the steepener is short convexity.

</details>

**Q9** (`c_l1_convexity_big_move`, topic `curve:convexity`, seed 1031500)

You hold a **DV01-neutral 2s10s flattener**. The whole curve moves -100bp in parallel (no change in slope). Do you make or lose money?

- *P&L*: **Gain**
- *Written*: Explain using convexity per unit of DV01, and how it interacts with a bull or bear move.

<details><summary>Model answer</summary>

**A DV01-neutral steepener is SHORT convexity; a flattener is LONG convexity.**

1. Convexity per unit of DV01 rises with maturity, so the 10Y leg carries far more convexity than the 2Y leg for the same DV01.
2. A steepener pays fixed in 10Y (short the 10Y's convexity) and receives 2Y (long a little): net short. Big parallel moves either way hurt the steepener and help the flattener, all else equal.
3. Interaction: in a bull steepener the slope gain is partly offset by the convexity loss; in a large bear flattener the flattener earns both slope and convexity.
4. Illustration (engine): +/-25bp convexity P&L of this flattener = +GBP 38.5k.

</details>

**Q10** (`c_l1_label`, topic `curve:labels`, seed 1031531)

2Y SONIA swaps move **-8bp** and 10Y move **-23bp**. What kind of move is this? Does a DV01-neutral 2s10s steepener make or lose money?

- *Curve move*: **Bull flattener**
- *Steepener*: **Loses money**
- *Written*: What typically drives this kind of move?

<details><summary>Model answer</summary>

**Bull flattener; the steepener loses money.**

1. Bull = yields fall, bear = yields rise; steepener = 10Y minus 2Y widens.
2. The curve flattened by 15bp. A DV01-neutral steepener (receive 2Y, pay 10Y) earns DV01 x (change in 10Y - change in 2Y).
3. Typical driver: long end rallies more: growth/inflation fears, flight to duration, long-end demand.

</details>

### Level 2: combinations, light calculations with every input given

**Q1** (`c_l2_pnl`, topic `curve:pnl`, seed 1135981)

DV01-neutral 2s10s steepener, GBP 100m on the 10Y leg (Givens). 2Y moves -21bp, 10Y -6bp. What kind of move is it, and what is your P&L?

Givens:

| Given | Value |
|---|---|
| DV01 of the receive-2Y leg (GBP/bp, + long duration) | 83,885 |
| DV01 of the pay-10Y leg (GBP/bp, - short duration) | -83,885 |
| 2Y move (bp) | -21 |
| 10Y move (bp) | -6 |

- *Curve move*: **Bull steepener**
- *P&L (GBP thousands)*: **1,258 k**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Bull steepener; P&L about +GBP 1.26m.**

1. Each leg: -DV01 x its own move: 2Y +GBP 1.76m, 10Y -GBP 503.3k.
2. With matched DV01s that is DV01 x (change in 10Y - change in 2Y).
3. Exact (engine, curve repriced): +GBP 1.16m.

</details>

**Q2** (`c_l2_convexity_pnl`, topic `curve:convexity`, seed 1136012)

Your DV01-neutral 2s10s steepener (GBP 100m 10Y leg) sees a 150bp parallel move with no change in slope. Using the Givens, estimate the convexity P&L. Long or short convexity?

Givens:

| Given | Value |
|---|---|
| Receive-2Y leg: change in DV01 per +1bp (GBP/bp per bp) | -16.64 |
| Pay-10Y leg: change in DV01 per +1bp (GBP/bp per bp) | 78.27 |
| Parallel move (bp, either way) | 150 |

- *Convexity P&L (GBP thousands)*: **-693.34 k**
- *Convexity*: **Short**
- *Written*: Explain why a steepener is short convexity.

<details><summary>Model answer</summary>

**About -GBP 693.3k: short convexity.**

1. DV01-neutral, so the first-order terms cancel. What is left: -0.5 x (G_2Y + G_10Y) x dy^2.
2. Paying 10Y makes the 10Y leg's DV01 move against you as rates move, and per unit of DV01 the 10Y has much more convexity than the 2Y.
3. Exact (engine, +150bp): -GBP 654.2k.

</details>

**Q3** (`c_l2_convexity_pnl`, topic `curve:convexity`, seed 1136043)

Your DV01-neutral 2s10s steepener (GBP 100m 10Y leg) sees a 150bp parallel move with no change in slope. Using the Givens, estimate the convexity P&L. Long or short convexity?

Givens:

| Given | Value |
|---|---|
| Receive-2Y leg: change in DV01 per +1bp (GBP/bp per bp) | -16.64 |
| Pay-10Y leg: change in DV01 per +1bp (GBP/bp per bp) | 78.27 |
| Parallel move (bp, either way) | 150 |

- *Convexity P&L (GBP thousands)*: **-693.34 k**
- *Convexity*: **Short**
- *Written*: Explain why a steepener is short convexity.

<details><summary>Model answer</summary>

**About -GBP 693.3k: short convexity.**

1. DV01-neutral, so the first-order terms cancel. What is left: -0.5 x (G_2Y + G_10Y) x dy^2.
2. Paying 10Y makes the 10Y leg's DV01 move against you as rates move, and per unit of DV01 the 10Y has much more convexity than the 2Y.
3. Exact (engine, +150bp): -GBP 654.2k.

</details>

**Q4** (`c_l2_pnl`, topic `curve:pnl`, seed 1136074)

DV01-neutral 2s10s steepener, GBP 100m on the 10Y leg (Givens). 2Y moves +13bp, 10Y +29bp. What kind of move is it, and what is your P&L?

Givens:

| Given | Value |
|---|---|
| DV01 of the receive-2Y leg (GBP/bp, + long duration) | 83,885 |
| DV01 of the pay-10Y leg (GBP/bp, - short duration) | -83,885 |
| 2Y move (bp) | 13 |
| 10Y move (bp) | 29 |

- *Curve move*: **Bear steepener**
- *P&L (GBP thousands)*: **1,342 k**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Bear steepener; P&L about +GBP 1.34m.**

1. Each leg: -DV01 x its own move: 2Y -GBP 1.09m, 10Y +GBP 2.43m.
2. With matched DV01s that is DV01 x (change in 10Y - change in 2Y).
3. Exact (engine, curve repriced): +GBP 1.20m.

</details>

**Q5** (`c_l2_convexity_pnl`, topic `curve:convexity`, seed 1136105)

Your DV01-neutral 2s10s steepener (GBP 100m 10Y leg) sees a 100bp parallel move with no change in slope. Using the Givens, estimate the convexity P&L. Long or short convexity?

Givens:

| Given | Value |
|---|---|
| Receive-2Y leg: change in DV01 per +1bp (GBP/bp per bp) | -16.64 |
| Pay-10Y leg: change in DV01 per +1bp (GBP/bp per bp) | 78.27 |
| Parallel move (bp, either way) | 100 |

- *Convexity P&L (GBP thousands)*: **-308.15 k**
- *Convexity*: **Short**
- *Written*: Explain why a steepener is short convexity.

<details><summary>Model answer</summary>

**About -GBP 308.1k: short convexity.**

1. DV01-neutral, so the first-order terms cancel. What is left: -0.5 x (G_2Y + G_10Y) x dy^2.
2. Paying 10Y makes the 10Y leg's DV01 move against you as rates move, and per unit of DV01 the 10Y has much more convexity than the 2Y.
3. Exact (engine, +100bp): -GBP 296.4k.

</details>

**Q6** (`c_l2_sizing`, topic `curve:sizing`, seed 1136136)

You want a 2s10s steepener: pay fixed on GBP 50m 10Y. Using the DV01s in the Givens, how much 2Y should you receive to be DV01-neutral?

Givens:

| Given | Value |
|---|---|
| 10Y notional (GBP m) | 50 |
| 2Y swap DV01 per GBP 1m (GBP/bp) | 196.80 |
| 10Y swap DV01 per GBP 1m (GBP/bp) | 838.85 |

- *2Y notional (GBP m)*: **213.12 m**
- *Written*: Why match DV01 rather than notional?

<details><summary>Model answer</summary>

**About GBP 213m.**

1. A curve trade should make money from the shape, not the level, so the two legs' DV01s must match.
2. 50m x 838.85 / 196.8 = 213m.

</details>

**Q7** (`c_l2_convexity_pnl`, topic `curve:convexity`, seed 1136167)

Your DV01-neutral 2s10s steepener (GBP 100m 10Y leg) sees a 100bp parallel move with no change in slope. Using the Givens, estimate the convexity P&L. Long or short convexity?

Givens:

| Given | Value |
|---|---|
| Receive-2Y leg: change in DV01 per +1bp (GBP/bp per bp) | -16.64 |
| Pay-10Y leg: change in DV01 per +1bp (GBP/bp per bp) | 78.27 |
| Parallel move (bp, either way) | 100 |

- *Convexity P&L (GBP thousands)*: **-308.15 k**
- *Convexity*: **Short**
- *Written*: Explain why a steepener is short convexity.

<details><summary>Model answer</summary>

**About -GBP 308.1k: short convexity.**

1. DV01-neutral, so the first-order terms cancel. What is left: -0.5 x (G_2Y + G_10Y) x dy^2.
2. Paying 10Y makes the 10Y leg's DV01 move against you as rates move, and per unit of DV01 the 10Y has much more convexity than the 2Y.
3. Exact (engine, +100bp): -GBP 296.4k.

</details>

**Q8** (`c_l2_pnl`, topic `curve:pnl`, seed 1136198)

DV01-neutral 2s10s steepener, GBP 100m on the 10Y leg (Givens). 2Y moves +28bp, 10Y +8bp. What kind of move is it, and what is your P&L?

Givens:

| Given | Value |
|---|---|
| DV01 of the receive-2Y leg (GBP/bp, + long duration) | 83,885 |
| DV01 of the pay-10Y leg (GBP/bp, - short duration) | -83,885 |
| 2Y move (bp) | 28 |
| 10Y move (bp) | 8 |

- *Curve move*: **Bear flattener**
- *P&L (GBP thousands)*: **-1,678 k**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Bear flattener; P&L about -GBP 1.68m.**

1. Each leg: -DV01 x its own move: 2Y -GBP 2.35m, 10Y +GBP 671.1k.
2. With matched DV01s that is DV01 x (change in 10Y - change in 2Y).
3. Exact (engine, curve repriced): -GBP 1.54m.

</details>

**Q9** (`c_l2_pnl`, topic `curve:pnl`, seed 1136229)

DV01-neutral 2s10s steepener, GBP 100m on the 10Y leg (Givens). 2Y moves -11bp, 10Y -33bp. What kind of move is it, and what is your P&L?

Givens:

| Given | Value |
|---|---|
| DV01 of the receive-2Y leg (GBP/bp, + long duration) | 83,885 |
| DV01 of the pay-10Y leg (GBP/bp, - short duration) | -83,885 |
| 2Y move (bp) | -11 |
| 10Y move (bp) | -33 |

- *Curve move*: **Bull flattener**
- *P&L (GBP thousands)*: **-1,845 k**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Bull flattener; P&L about -GBP 1.85m.**

1. Each leg: -DV01 x its own move: 2Y +GBP 922.7k, 10Y -GBP 2.77m.
2. With matched DV01s that is DV01 x (change in 10Y - change in 2Y).
3. Exact (engine, curve repriced): -GBP 1.73m.

</details>

**Q10** (`c_l2_pnl`, topic `curve:pnl`, seed 1136260)

DV01-neutral 2s10s steepener, GBP 100m on the 10Y leg (Givens). 2Y moves -24bp, 10Y -13bp. What kind of move is it, and what is your P&L?

Givens:

| Given | Value |
|---|---|
| DV01 of the receive-2Y leg (GBP/bp, + long duration) | 83,885 |
| DV01 of the pay-10Y leg (GBP/bp, - short duration) | -83,885 |
| 2Y move (bp) | -24 |
| 10Y move (bp) | -13 |

- *Curve move*: **Bull steepener**
- *P&L (GBP thousands)*: **922.74 k**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Bull steepener; P&L about +GBP 922.7k.**

1. Each leg: -DV01 x its own move: 2Y +GBP 2.01m, 10Y -GBP 1.09m.
2. With matched DV01s that is DV01 x (change in 10Y - change in 2Y).
3. Exact (engine, curve repriced): +GBP 843.7k.

</details>

### Level 3: calculations plus subtler concepts

**Q1** (`c_l3_fly`, topic `curve:fly_pca`, seed 1240710)

You receive the 5Y in a 2s5s10s butterfly (belly DV01 in the Givens) and pay the wings. Choose wing DV01s so the trade is neutral to the first two PCA factors (level and slope), using the loadings given (bp move per unit factor move).

Givens:

| Given | Value |
|---|---|
| Belly (5Y) DV01 you receive (GBP/bp) | 100,000 |
| Level loading 2Y | 0.89 |
| Level loading 5Y | 1.02 |
| Level loading 10Y | 0.96 |
| Slope loading 2Y | -0.59 |
| Slope loading 5Y | 0.02 |
| Slope loading 10Y | 0.55 |

- *2Y wing DV01 to pay (GBP/bp)*: **51,312**
- *10Y wing DV01 to pay (GBP/bp)*: **58,680**
- *Written*: Why PCA weights rather than 50/50 DV01 weights?

<details><summary>Model answer</summary>

**Pay about 51,312 (2Y) and 58,680 (10Y) DV01.**

1. Exposure to a factor = sum of DV01 x loading. Set level and slope exposure of the wings equal to the belly's:
   w2 x L2 + w10 x L10 = B x L5 and w2 x S2 + w10 x S10 = B x S5.
2. Solving gives the weights above (not 50/50).
3. A 50/50 DV01 fly is hedged for parallel moves only; when the curve steepens the wings move differently and you get slope P&L. PCA weights leave mostly curvature.

</details>

**Q2** (`c_l3_full`, topic `curve:sizing`, seed 1240741)

2s10s steepener paying fixed on GBP 50m 10Y. (a) How much 2Y do you receive to be DV01-neutral? (b) If you used equal notionals instead, what would a +50bp parallel move do to your P&L?

Givens:

| Given | Value |
|---|---|
| 10Y notional paid (GBP m) | 50 |
| 2Y DV01 per GBP 1m (GBP/bp) | 196.80 |
| 10Y DV01 per GBP 1m (GBP/bp) | 838.85 |
| Parallel move (bp) | 50 |

- *(a) 2Y notional (GBP m)*: **213.12 m**
- *(b) Equal-notional P&L (GBP k)*: **1,605 k**
- *Written*: Explain what goes wrong with equal notionals.

<details><summary>Model answer</summary>

**(a) GBP 213m; (b) about +GBP 1.61m.**

1. Equal notionals leave you net short duration: net DV01 = 50m x (196.8 - 838.85) per bp.
2. A parallel move then creates P&L that has nothing to do with the slope view.
3. Exact (engine): +GBP 1.56m; the residual is convexity.

</details>

**Q3** (`c_l3_fly`, topic `curve:fly_pca`, seed 1240772)

You receive the 5Y in a 2s5s10s butterfly (belly DV01 in the Givens) and pay the wings. Choose wing DV01s so the trade is neutral to the first two PCA factors (level and slope), using the loadings given (bp move per unit factor move).

Givens:

| Given | Value |
|---|---|
| Belly (5Y) DV01 you receive (GBP/bp) | 100,000 |
| Level loading 2Y | 1.01 |
| Level loading 5Y | 1.02 |
| Level loading 10Y | 0.95 |
| Slope loading 2Y | -0.61 |
| Slope loading 5Y | 0.07 |
| Slope loading 10Y | 0.54 |

- *2Y wing DV01 to pay (GBP/bp)*: **43,053**
- *10Y wing DV01 to pay (GBP/bp)*: **61,597**
- *Written*: Why PCA weights rather than 50/50 DV01 weights?

<details><summary>Model answer</summary>

**Pay about 43,053 (2Y) and 61,597 (10Y) DV01.**

1. Exposure to a factor = sum of DV01 x loading. Set level and slope exposure of the wings equal to the belly's:
   w2 x L2 + w10 x L10 = B x L5 and w2 x S2 + w10 x S10 = B x S5.
2. Solving gives the weights above (not 50/50).
3. A 50/50 DV01 fly is hedged for parallel moves only; when the curve steepens the wings move differently and you get slope P&L. PCA weights leave mostly curvature.

</details>

**Q4** (`c_l3_fly`, topic `curve:fly_pca`, seed 1240803)

You receive the 5Y in a 2s5s10s butterfly (belly DV01 in the Givens) and pay the wings. Choose wing DV01s so the trade is neutral to the first two PCA factors (level and slope), using the loadings given (bp move per unit factor move).

Givens:

| Given | Value |
|---|---|
| Belly (5Y) DV01 you receive (GBP/bp) | 100,000 |
| Level loading 2Y | 0.99 |
| Level loading 5Y | 1.06 |
| Level loading 10Y | 0.96 |
| Slope loading 2Y | -0.6 |
| Slope loading 5Y | 0.06 |
| Slope loading 10Y | 0.55 |

- *2Y wing DV01 to pay (GBP/bp)*: **46,890**
- *10Y wing DV01 to pay (GBP/bp)*: **62,062**
- *Written*: Why PCA weights rather than 50/50 DV01 weights?

<details><summary>Model answer</summary>

**Pay about 46,890 (2Y) and 62,062 (10Y) DV01.**

1. Exposure to a factor = sum of DV01 x loading. Set level and slope exposure of the wings equal to the belly's:
   w2 x L2 + w10 x L10 = B x L5 and w2 x S2 + w10 x S10 = B x S5.
2. Solving gives the weights above (not 50/50).
3. A 50/50 DV01 fly is hedged for parallel moves only; when the curve steepens the wings move differently and you get slope P&L. PCA weights leave mostly curvature.

</details>

**Q5** (`c_l3_fly`, topic `curve:fly_pca`, seed 1240834)

You receive the 5Y in a 2s5s10s butterfly (belly DV01 in the Givens) and pay the wings. Choose wing DV01s so the trade is neutral to the first two PCA factors (level and slope), using the loadings given (bp move per unit factor move).

Givens:

| Given | Value |
|---|---|
| Belly (5Y) DV01 you receive (GBP/bp) | 100,000 |
| Level loading 2Y | 1 |
| Level loading 5Y | 1.07 |
| Level loading 10Y | 0.92 |
| Slope loading 2Y | -0.61 |
| Slope loading 5Y | 0.08 |
| Slope loading 10Y | 0.55 |

- *2Y wing DV01 to pay (GBP/bp)*: **46,337**
- *10Y wing DV01 to pay (GBP/bp)*: **65,938**
- *Written*: Why PCA weights rather than 50/50 DV01 weights?

<details><summary>Model answer</summary>

**Pay about 46,337 (2Y) and 65,938 (10Y) DV01.**

1. Exposure to a factor = sum of DV01 x loading. Set level and slope exposure of the wings equal to the belly's:
   w2 x L2 + w10 x L10 = B x L5 and w2 x S2 + w10 x S10 = B x S5.
2. Solving gives the weights above (not 50/50).
3. A 50/50 DV01 fly is hedged for parallel moves only; when the curve steepens the wings move differently and you get slope P&L. PCA weights leave mostly curvature.

</details>

**Q6** (`c_l3_full`, topic `curve:sizing`, seed 1240865)

2s10s steepener paying fixed on GBP 100m 10Y. (a) How much 2Y do you receive to be DV01-neutral? (b) If you used equal notionals instead, what would a -25bp parallel move do to your P&L?

Givens:

| Given | Value |
|---|---|
| 10Y notional paid (GBP m) | 100 |
| 2Y DV01 per GBP 1m (GBP/bp) | 196.80 |
| 10Y DV01 per GBP 1m (GBP/bp) | 838.85 |
| Parallel move (bp) | -25 |

- *(a) 2Y notional (GBP m)*: **426.24 m**
- *(b) Equal-notional P&L (GBP k)*: **-1,605 k**
- *Written*: Explain what goes wrong with equal notionals.

<details><summary>Model answer</summary>

**(a) GBP 426m; (b) about -GBP 1.61m.**

1. Equal notionals leave you net short duration: net DV01 = 100m x (196.8 - 838.85) per bp.
2. A parallel move then creates P&L that has nothing to do with the slope view.
3. Exact (engine): -GBP 1.63m; the residual is convexity.

</details>

**Q7** (`c_l3_fly`, topic `curve:fly_pca`, seed 1240896)

You receive the 5Y in a 2s5s10s butterfly (belly DV01 in the Givens) and pay the wings. Choose wing DV01s so the trade is neutral to the first two PCA factors (level and slope), using the loadings given (bp move per unit factor move).

Givens:

| Given | Value |
|---|---|
| Belly (5Y) DV01 you receive (GBP/bp) | 100,000 |
| Level loading 2Y | 1.03 |
| Level loading 5Y | 1.1 |
| Level loading 10Y | 0.95 |
| Slope loading 2Y | -0.56 |
| Slope loading 5Y | 0.05 |
| Slope loading 10Y | 0.55 |

- *2Y wing DV01 to pay (GBP/bp)*: **50,751**
- *10Y wing DV01 to pay (GBP/bp)*: **60,765**
- *Written*: Why PCA weights rather than 50/50 DV01 weights?

<details><summary>Model answer</summary>

**Pay about 50,751 (2Y) and 60,765 (10Y) DV01.**

1. Exposure to a factor = sum of DV01 x loading. Set level and slope exposure of the wings equal to the belly's:
   w2 x L2 + w10 x L10 = B x L5 and w2 x S2 + w10 x S10 = B x S5.
2. Solving gives the weights above (not 50/50).
3. A 50/50 DV01 fly is hedged for parallel moves only; when the curve steepens the wings move differently and you get slope P&L. PCA weights leave mostly curvature.

</details>

**Q8** (`c_l3_full`, topic `curve:sizing`, seed 1240927)

2s10s steepener paying fixed on GBP 100m 10Y. (a) How much 2Y do you receive to be DV01-neutral? (b) If you used equal notionals instead, what would a -50bp parallel move do to your P&L?

Givens:

| Given | Value |
|---|---|
| 10Y notional paid (GBP m) | 100 |
| 2Y DV01 per GBP 1m (GBP/bp) | 196.80 |
| 10Y DV01 per GBP 1m (GBP/bp) | 838.85 |
| Parallel move (bp) | -50 |

- *(a) 2Y notional (GBP m)*: **426.24 m**
- *(b) Equal-notional P&L (GBP k)*: **-3,210 k**
- *Written*: Explain what goes wrong with equal notionals.

<details><summary>Model answer</summary>

**(a) GBP 426m; (b) about -GBP 3.21m.**

1. Equal notionals leave you net short duration: net DV01 = 100m x (196.8 - 838.85) per bp.
2. A parallel move then creates P&L that has nothing to do with the slope view.
3. Exact (engine): -GBP 3.30m; the residual is convexity.

</details>

**Q9** (`c_l3_full`, topic `curve:sizing`, seed 1240958)

2s10s steepener paying fixed on GBP 100m 10Y. (a) How much 2Y do you receive to be DV01-neutral? (b) If you used equal notionals instead, what would a +25bp parallel move do to your P&L?

Givens:

| Given | Value |
|---|---|
| 10Y notional paid (GBP m) | 100 |
| 2Y DV01 per GBP 1m (GBP/bp) | 196.80 |
| 10Y DV01 per GBP 1m (GBP/bp) | 838.85 |
| Parallel move (bp) | 25 |

- *(a) 2Y notional (GBP m)*: **426.24 m**
- *(b) Equal-notional P&L (GBP k)*: **1,605 k**
- *Written*: Explain what goes wrong with equal notionals.

<details><summary>Model answer</summary>

**(a) GBP 426m; (b) about +GBP 1.61m.**

1. Equal notionals leave you net short duration: net DV01 = 100m x (196.8 - 838.85) per bp.
2. A parallel move then creates P&L that has nothing to do with the slope view.
3. Exact (engine): +GBP 1.58m; the residual is convexity.

</details>

**Q10** (`c_l3_fly`, topic `curve:fly_pca`, seed 1240989)

You receive the 5Y in a 2s5s10s butterfly (belly DV01 in the Givens) and pay the wings. Choose wing DV01s so the trade is neutral to the first two PCA factors (level and slope), using the loadings given (bp move per unit factor move).

Givens:

| Given | Value |
|---|---|
| Belly (5Y) DV01 you receive (GBP/bp) | 100,000 |
| Level loading 2Y | 0.96 |
| Level loading 5Y | 1.05 |
| Level loading 10Y | 0.93 |
| Slope loading 2Y | -0.61 |
| Slope loading 5Y | 0.08 |
| Slope loading 10Y | 0.52 |

- *2Y wing DV01 to pay (GBP/bp)*: **44,219**
- *10Y wing DV01 to pay (GBP/bp)*: **67,257**
- *Written*: Why PCA weights rather than 50/50 DV01 weights?

<details><summary>Model answer</summary>

**Pay about 44,219 (2Y) and 67,257 (10Y) DV01.**

1. Exposure to a factor = sum of DV01 x loading. Set level and slope exposure of the wings equal to the belly's:
   w2 x L2 + w10 x L10 = B x L5 and w2 x S2 + w10 x S10 = B x S5.
2. Solving gives the weights above (not 50/50).
3. A 50/50 DV01 fly is hedged for parallel moves only; when the curve steepens the wings move differently and you get slope P&L. PCA weights leave mostly curvature.

</details>

## 2D Carry and roll-down

### Level 1: directional intuition, no calculations

**Q1** (`d_l1_kills`, topic `carry:breakeven`, seed 1039171)

You receive 10Y on a steep curve for its carry and roll-down. What makes the trade lose money?

- *Loses if*: **Rates rise by more than the carry plus roll over the horizon**
- *Written*: Explain the breakeven.

<details><summary>Model answer</summary>

**A rise in rates bigger than carry + roll.** Carry and roll are what you earn if nothing moves; they are your cushion. The breakeven is how many bp the rate can rise over the horizon before the duration loss eats it.

</details>

**Q2** (`d_l1_sign`, topic `carry:roll`, seed 1039202)

The curve is steep and upward-sloping (3M SONIA 2.75%, 5Y 3.9%, 10Y 4.4%). You receive fixed in 5Y. Is your carry positive or negative? Does roll-down help or hurt you?

- *Carry*: **Positive**
- *Roll-down*: **Helps**
- *Written*: Explain carry and roll-down.

<details><summary>Model answer</summary>

**Positive carry, and roll-down helps.**

1. Carry: you receive the 5Y fixed rate and pay the lower short-term floating rate.
2. Roll-down: on an unchanged curve your 5Y swap becomes a shorter swap, which is priced at a lower rate, so receiving the original higher rate gains value.

</details>

**Q3** (`d_l1_sign`, topic `carry:roll`, seed 1039233)

The curve is steep and upward-sloping (3M SONIA 2.75%, 5Y 3.9%, 10Y 4.4%). You receive fixed in 5Y. Is your carry positive or negative? Does roll-down help or hurt you?

- *Carry*: **Positive**
- *Roll-down*: **Helps**
- *Written*: Explain carry and roll-down.

<details><summary>Model answer</summary>

**Positive carry, and roll-down helps.**

1. Carry: you receive the 5Y fixed rate and pay the lower short-term floating rate.
2. Roll-down: on an unchanged curve your 5Y swap becomes a shorter swap, which is priced at a lower rate, so receiving the original higher rate gains value.

</details>

**Q4** (`d_l1_sign`, topic `carry:roll`, seed 1039264)

The curve is steep and upward-sloping (3M SONIA 2.75%, 5Y 3.9%, 10Y 4.4%). You receive fixed in 5Y. Is your carry positive or negative? Does roll-down help or hurt you?

- *Carry*: **Positive**
- *Roll-down*: **Helps**
- *Written*: Explain carry and roll-down.

<details><summary>Model answer</summary>

**Positive carry, and roll-down helps.**

1. Carry: you receive the 5Y fixed rate and pay the lower short-term floating rate.
2. Roll-down: on an unchanged curve your 5Y swap becomes a shorter swap, which is priced at a lower rate, so receiving the original higher rate gains value.

</details>

**Q5** (`d_l1_kills`, topic `carry:breakeven`, seed 1039295)

You receive 10Y on a steep curve for its carry and roll-down. What makes the trade lose money?

- *Loses if*: **Rates rise by more than the carry plus roll over the horizon**
- *Written*: Explain the breakeven.

<details><summary>Model answer</summary>

**A rise in rates bigger than carry + roll.** Carry and roll are what you earn if nothing moves; they are your cushion. The breakeven is how many bp the rate can rise over the horizon before the duration loss eats it.

</details>

**Q6** (`d_l1_kills`, topic `carry:breakeven`, seed 1039326)

You receive 10Y on a steep curve for its carry and roll-down. What makes the trade lose money?

- *Loses if*: **Rates rise by more than the carry plus roll over the horizon**
- *Written*: Explain the breakeven.

<details><summary>Model answer</summary>

**A rise in rates bigger than carry + roll.** Carry and roll are what you earn if nothing moves; they are your cushion. The breakeven is how many bp the rate can rise over the horizon before the duration loss eats it.

</details>

**Q7** (`d_l1_sign`, topic `carry:roll`, seed 1039357)

The curve is steep and upward-sloping (3M SONIA 2.75%, 5Y 3.9%, 10Y 4.4%). You receive fixed in 5Y. Is your carry positive or negative? Does roll-down help or hurt you?

- *Carry*: **Positive**
- *Roll-down*: **Helps**
- *Written*: Explain carry and roll-down.

<details><summary>Model answer</summary>

**Positive carry, and roll-down helps.**

1. Carry: you receive the 5Y fixed rate and pay the lower short-term floating rate.
2. Roll-down: on an unchanged curve your 5Y swap becomes a shorter swap, which is priced at a lower rate, so receiving the original higher rate gains value.

</details>

**Q8** (`d_l1_kills`, topic `carry:breakeven`, seed 1039388)

You receive 10Y on a steep curve for its carry and roll-down. What makes the trade lose money?

- *Loses if*: **Rates rise by more than the carry plus roll over the horizon**
- *Written*: Explain the breakeven.

<details><summary>Model answer</summary>

**A rise in rates bigger than carry + roll.** Carry and roll are what you earn if nothing moves; they are your cushion. The breakeven is how many bp the rate can rise over the horizon before the duration loss eats it.

</details>

**Q9** (`d_l1_kills`, topic `carry:breakeven`, seed 1039419)

You receive 10Y on a steep curve for its carry and roll-down. What makes the trade lose money?

- *Loses if*: **Rates rise by more than the carry plus roll over the horizon**
- *Written*: Explain the breakeven.

<details><summary>Model answer</summary>

**A rise in rates bigger than carry + roll.** Carry and roll are what you earn if nothing moves; they are your cushion. The breakeven is how many bp the rate can rise over the horizon before the duration loss eats it.

</details>

**Q10** (`d_l1_kills`, topic `carry:breakeven`, seed 1039450)

You receive 10Y on a steep curve for its carry and roll-down. What makes the trade lose money?

- *Loses if*: **Rates rise by more than the carry plus roll over the horizon**
- *Written*: Explain the breakeven.

<details><summary>Model answer</summary>

**A rise in rates bigger than carry + roll.** Carry and roll are what you earn if nothing moves; they are your cushion. The breakeven is how many bp the rate can rise over the horizon before the duration loss eats it.

</details>

### Level 2: combinations, light calculations with every input given

**Q1** (`d_l2`, topic `carry:roll`, seed 1143900)

You receive fixed in 5Y. Using the Givens, what are the 3-month carry and roll-down, in bp of rate?

Givens:

| Given | Value |
|---|---|
| 5Y par swap rate (%) | 3.9439 |
| 4.75Y par swap rate (%) | 3.7204 |
| 3M floating rate (%) | 2.7595 |
| Horizon (years) | 0.25 |

- *Carry (bp)*: **29.61 bp**
- *Roll-down (bp)*: **22.35 bp**
- *Written*: Explain each piece.

<details><summary>Model answer</summary>

**Carry 29.6bp, roll 22.4bp.**

1. Carry = (3.9439 - 2.7595)% x 0.25.
2. Roll: in 3 months your swap is a 4.75Y swap, priced at 3.7204%; receiving 3.9439% vs that is the roll-down.

</details>

**Q2** (`d_l2`, topic `carry:roll`, seed 1143931)

You receive fixed in 5Y. Using the Givens, what are the 3-month carry and roll-down, in bp of rate?

Givens:

| Given | Value |
|---|---|
| 5Y par swap rate (%) | 3.9439 |
| 4.75Y par swap rate (%) | 3.7204 |
| 3M floating rate (%) | 2.7595 |
| Horizon (years) | 0.25 |

- *Carry (bp)*: **29.61 bp**
- *Roll-down (bp)*: **22.35 bp**
- *Written*: Explain each piece.

<details><summary>Model answer</summary>

**Carry 29.6bp, roll 22.4bp.**

1. Carry = (3.9439 - 2.7595)% x 0.25.
2. Roll: in 3 months your swap is a 4.75Y swap, priced at 3.7204%; receiving 3.9439% vs that is the roll-down.

</details>

**Q3** (`d_l2`, topic `carry:roll`, seed 1143962)

You receive fixed in 10Y. Using the Givens, what are the 3-month carry and roll-down, in bp of rate?

Givens:

| Given | Value |
|---|---|
| 10Y par swap rate (%) | 4.4126 |
| 9.75Y par swap rate (%) | 4.3046 |
| 3M floating rate (%) | 2.7595 |
| Horizon (years) | 0.25 |

- *Carry (bp)*: **41.33 bp**
- *Roll-down (bp)*: **10.80 bp**
- *Written*: Explain each piece.

<details><summary>Model answer</summary>

**Carry 41.3bp, roll 10.8bp.**

1. Carry = (4.4126 - 2.7595)% x 0.25.
2. Roll: in 3 months your swap is a 9.75Y swap, priced at 4.3046%; receiving 4.4126% vs that is the roll-down.

</details>

**Q4** (`d_l2`, topic `carry:roll`, seed 1143993)

You receive fixed in 10Y. Using the Givens, what are the 3-month carry and roll-down, in bp of rate?

Givens:

| Given | Value |
|---|---|
| 10Y par swap rate (%) | 4.4126 |
| 9.75Y par swap rate (%) | 4.3046 |
| 3M floating rate (%) | 2.7595 |
| Horizon (years) | 0.25 |

- *Carry (bp)*: **41.33 bp**
- *Roll-down (bp)*: **10.80 bp**
- *Written*: Explain each piece.

<details><summary>Model answer</summary>

**Carry 41.3bp, roll 10.8bp.**

1. Carry = (4.4126 - 2.7595)% x 0.25.
2. Roll: in 3 months your swap is a 9.75Y swap, priced at 4.3046%; receiving 4.4126% vs that is the roll-down.

</details>

**Q5** (`d_l2`, topic `carry:roll`, seed 1144024)

You receive fixed in 10Y. Using the Givens, what are the 3-month carry and roll-down, in bp of rate?

Givens:

| Given | Value |
|---|---|
| 10Y par swap rate (%) | 4.4126 |
| 9.75Y par swap rate (%) | 4.3046 |
| 3M floating rate (%) | 2.7595 |
| Horizon (years) | 0.25 |

- *Carry (bp)*: **41.33 bp**
- *Roll-down (bp)*: **10.80 bp**
- *Written*: Explain each piece.

<details><summary>Model answer</summary>

**Carry 41.3bp, roll 10.8bp.**

1. Carry = (4.4126 - 2.7595)% x 0.25.
2. Roll: in 3 months your swap is a 9.75Y swap, priced at 4.3046%; receiving 4.4126% vs that is the roll-down.

</details>

**Q6** (`d_l2`, topic `carry:roll`, seed 1144055)

You receive fixed in 5Y. Using the Givens, what are the 3-month carry and roll-down, in bp of rate?

Givens:

| Given | Value |
|---|---|
| 5Y par swap rate (%) | 3.9439 |
| 4.75Y par swap rate (%) | 3.7204 |
| 3M floating rate (%) | 2.7595 |
| Horizon (years) | 0.25 |

- *Carry (bp)*: **29.61 bp**
- *Roll-down (bp)*: **22.35 bp**
- *Written*: Explain each piece.

<details><summary>Model answer</summary>

**Carry 29.6bp, roll 22.4bp.**

1. Carry = (3.9439 - 2.7595)% x 0.25.
2. Roll: in 3 months your swap is a 4.75Y swap, priced at 3.7204%; receiving 3.9439% vs that is the roll-down.

</details>

**Q7** (`d_l2`, topic `carry:roll`, seed 1144086)

You receive fixed in 10Y. Using the Givens, what are the 3-month carry and roll-down, in bp of rate?

Givens:

| Given | Value |
|---|---|
| 10Y par swap rate (%) | 4.4126 |
| 9.75Y par swap rate (%) | 4.3046 |
| 3M floating rate (%) | 2.7595 |
| Horizon (years) | 0.25 |

- *Carry (bp)*: **41.33 bp**
- *Roll-down (bp)*: **10.80 bp**
- *Written*: Explain each piece.

<details><summary>Model answer</summary>

**Carry 41.3bp, roll 10.8bp.**

1. Carry = (4.4126 - 2.7595)% x 0.25.
2. Roll: in 3 months your swap is a 9.75Y swap, priced at 4.3046%; receiving 4.4126% vs that is the roll-down.

</details>

**Q8** (`d_l2`, topic `carry:roll`, seed 1144117)

You receive fixed in 5Y. Using the Givens, what are the 3-month carry and roll-down, in bp of rate?

Givens:

| Given | Value |
|---|---|
| 5Y par swap rate (%) | 3.9439 |
| 4.75Y par swap rate (%) | 3.7204 |
| 3M floating rate (%) | 2.7595 |
| Horizon (years) | 0.25 |

- *Carry (bp)*: **29.61 bp**
- *Roll-down (bp)*: **22.35 bp**
- *Written*: Explain each piece.

<details><summary>Model answer</summary>

**Carry 29.6bp, roll 22.4bp.**

1. Carry = (3.9439 - 2.7595)% x 0.25.
2. Roll: in 3 months your swap is a 4.75Y swap, priced at 3.7204%; receiving 3.9439% vs that is the roll-down.

</details>

**Q9** (`d_l2`, topic `carry:roll`, seed 1144148)

You receive fixed in 10Y. Using the Givens, what are the 3-month carry and roll-down, in bp of rate?

Givens:

| Given | Value |
|---|---|
| 10Y par swap rate (%) | 4.4126 |
| 9.75Y par swap rate (%) | 4.3046 |
| 3M floating rate (%) | 2.7595 |
| Horizon (years) | 0.25 |

- *Carry (bp)*: **41.33 bp**
- *Roll-down (bp)*: **10.80 bp**
- *Written*: Explain each piece.

<details><summary>Model answer</summary>

**Carry 41.3bp, roll 10.8bp.**

1. Carry = (4.4126 - 2.7595)% x 0.25.
2. Roll: in 3 months your swap is a 9.75Y swap, priced at 4.3046%; receiving 4.4126% vs that is the roll-down.

</details>

**Q10** (`d_l2`, topic `carry:roll`, seed 1144179)

You receive fixed in 5Y. Using the Givens, what are the 3-month carry and roll-down, in bp of rate?

Givens:

| Given | Value |
|---|---|
| 5Y par swap rate (%) | 3.9439 |
| 4.75Y par swap rate (%) | 3.7204 |
| 3M floating rate (%) | 2.7595 |
| Horizon (years) | 0.25 |

- *Carry (bp)*: **29.61 bp**
- *Roll-down (bp)*: **22.35 bp**
- *Written*: Explain each piece.

<details><summary>Model answer</summary>

**Carry 29.6bp, roll 22.4bp.**

1. Carry = (3.9439 - 2.7595)% x 0.25.
2. Roll: in 3 months your swap is a 4.75Y swap, priced at 3.7204%; receiving 3.9439% vs that is the roll-down.

</details>

### Level 3: calculations plus subtler concepts

**Q1** (`d_l3`, topic `carry:breakeven`, seed 1248629)

Using the Givens: (a) 3-month carry + roll (bp) for receiving 5Y, (b) the same for 10Y, (c) the GBP value of the 10Y carry+roll on GBP 100m. Which tenor is better per unit of DV01, and what is the 10Y breakeven?

Givens:

| Given | Value |
|---|---|
| 5Y par (%) | 3.9439 |
| 4.75Y par (%) | 3.7204 |
| 10Y par (%) | 4.4126 |
| 9.75Y par (%) | 4.3046 |
| 3M floating (%) | 2.7595 |
| DV01 of receiving GBP 100m 10Y (GBP/bp) | 82,650 |

- *(a) 5Y carry+roll (bp)*: **51.96 bp**
- *(b) 10Y carry+roll (bp)*: **52.13 bp**
- *(c) 10Y carry+roll (GBP k)*: **4,308 k**
- *Written*: Compare the two per DV01 and give the breakeven.

<details><summary>Model answer</summary>

**5Y 52.0bp, 10Y 52.1bp; 10Y worth +GBP 4.31m.**

1. Carry + roll in bp of rate is already per unit of DV01, so compare them directly: 10Y is better.
2. The 10Y breakeven is a 52.1bp rise over 3 months before the trade loses.

</details>

**Q2** (`d_l3`, topic `carry:breakeven`, seed 1248660)

Using the Givens: (a) 3-month carry + roll (bp) for receiving 5Y, (b) the same for 10Y, (c) the GBP value of the 10Y carry+roll on GBP 100m. Which tenor is better per unit of DV01, and what is the 10Y breakeven?

Givens:

| Given | Value |
|---|---|
| 5Y par (%) | 3.9439 |
| 4.75Y par (%) | 3.7204 |
| 10Y par (%) | 4.4126 |
| 9.75Y par (%) | 4.3046 |
| 3M floating (%) | 2.7595 |
| DV01 of receiving GBP 100m 10Y (GBP/bp) | 82,650 |

- *(a) 5Y carry+roll (bp)*: **51.96 bp**
- *(b) 10Y carry+roll (bp)*: **52.13 bp**
- *(c) 10Y carry+roll (GBP k)*: **4,308 k**
- *Written*: Compare the two per DV01 and give the breakeven.

<details><summary>Model answer</summary>

**5Y 52.0bp, 10Y 52.1bp; 10Y worth +GBP 4.31m.**

1. Carry + roll in bp of rate is already per unit of DV01, so compare them directly: 10Y is better.
2. The 10Y breakeven is a 52.1bp rise over 3 months before the trade loses.

</details>

**Q3** (`d_l3`, topic `carry:breakeven`, seed 1248691)

Using the Givens: (a) 3-month carry + roll (bp) for receiving 5Y, (b) the same for 10Y, (c) the GBP value of the 10Y carry+roll on GBP 100m. Which tenor is better per unit of DV01, and what is the 10Y breakeven?

Givens:

| Given | Value |
|---|---|
| 5Y par (%) | 3.9439 |
| 4.75Y par (%) | 3.7204 |
| 10Y par (%) | 4.4126 |
| 9.75Y par (%) | 4.3046 |
| 3M floating (%) | 2.7595 |
| DV01 of receiving GBP 100m 10Y (GBP/bp) | 82,650 |

- *(a) 5Y carry+roll (bp)*: **51.96 bp**
- *(b) 10Y carry+roll (bp)*: **52.13 bp**
- *(c) 10Y carry+roll (GBP k)*: **4,308 k**
- *Written*: Compare the two per DV01 and give the breakeven.

<details><summary>Model answer</summary>

**5Y 52.0bp, 10Y 52.1bp; 10Y worth +GBP 4.31m.**

1. Carry + roll in bp of rate is already per unit of DV01, so compare them directly: 10Y is better.
2. The 10Y breakeven is a 52.1bp rise over 3 months before the trade loses.

</details>

**Q4** (`d_l3`, topic `carry:breakeven`, seed 1248722)

Using the Givens: (a) 3-month carry + roll (bp) for receiving 5Y, (b) the same for 10Y, (c) the GBP value of the 10Y carry+roll on GBP 100m. Which tenor is better per unit of DV01, and what is the 10Y breakeven?

Givens:

| Given | Value |
|---|---|
| 5Y par (%) | 3.9439 |
| 4.75Y par (%) | 3.7204 |
| 10Y par (%) | 4.4126 |
| 9.75Y par (%) | 4.3046 |
| 3M floating (%) | 2.7595 |
| DV01 of receiving GBP 100m 10Y (GBP/bp) | 82,650 |

- *(a) 5Y carry+roll (bp)*: **51.96 bp**
- *(b) 10Y carry+roll (bp)*: **52.13 bp**
- *(c) 10Y carry+roll (GBP k)*: **4,308 k**
- *Written*: Compare the two per DV01 and give the breakeven.

<details><summary>Model answer</summary>

**5Y 52.0bp, 10Y 52.1bp; 10Y worth +GBP 4.31m.**

1. Carry + roll in bp of rate is already per unit of DV01, so compare them directly: 10Y is better.
2. The 10Y breakeven is a 52.1bp rise over 3 months before the trade loses.

</details>

**Q5** (`d_l3`, topic `carry:breakeven`, seed 1248753)

Using the Givens: (a) 3-month carry + roll (bp) for receiving 5Y, (b) the same for 10Y, (c) the GBP value of the 10Y carry+roll on GBP 100m. Which tenor is better per unit of DV01, and what is the 10Y breakeven?

Givens:

| Given | Value |
|---|---|
| 5Y par (%) | 3.9439 |
| 4.75Y par (%) | 3.7204 |
| 10Y par (%) | 4.4126 |
| 9.75Y par (%) | 4.3046 |
| 3M floating (%) | 2.7595 |
| DV01 of receiving GBP 100m 10Y (GBP/bp) | 82,650 |

- *(a) 5Y carry+roll (bp)*: **51.96 bp**
- *(b) 10Y carry+roll (bp)*: **52.13 bp**
- *(c) 10Y carry+roll (GBP k)*: **4,308 k**
- *Written*: Compare the two per DV01 and give the breakeven.

<details><summary>Model answer</summary>

**5Y 52.0bp, 10Y 52.1bp; 10Y worth +GBP 4.31m.**

1. Carry + roll in bp of rate is already per unit of DV01, so compare them directly: 10Y is better.
2. The 10Y breakeven is a 52.1bp rise over 3 months before the trade loses.

</details>

**Q6** (`d_l3`, topic `carry:breakeven`, seed 1248784)

Using the Givens: (a) 3-month carry + roll (bp) for receiving 5Y, (b) the same for 10Y, (c) the GBP value of the 10Y carry+roll on GBP 100m. Which tenor is better per unit of DV01, and what is the 10Y breakeven?

Givens:

| Given | Value |
|---|---|
| 5Y par (%) | 3.9439 |
| 4.75Y par (%) | 3.7204 |
| 10Y par (%) | 4.4126 |
| 9.75Y par (%) | 4.3046 |
| 3M floating (%) | 2.7595 |
| DV01 of receiving GBP 100m 10Y (GBP/bp) | 82,650 |

- *(a) 5Y carry+roll (bp)*: **51.96 bp**
- *(b) 10Y carry+roll (bp)*: **52.13 bp**
- *(c) 10Y carry+roll (GBP k)*: **4,308 k**
- *Written*: Compare the two per DV01 and give the breakeven.

<details><summary>Model answer</summary>

**5Y 52.0bp, 10Y 52.1bp; 10Y worth +GBP 4.31m.**

1. Carry + roll in bp of rate is already per unit of DV01, so compare them directly: 10Y is better.
2. The 10Y breakeven is a 52.1bp rise over 3 months before the trade loses.

</details>

**Q7** (`d_l3`, topic `carry:breakeven`, seed 1248815)

Using the Givens: (a) 3-month carry + roll (bp) for receiving 5Y, (b) the same for 10Y, (c) the GBP value of the 10Y carry+roll on GBP 100m. Which tenor is better per unit of DV01, and what is the 10Y breakeven?

Givens:

| Given | Value |
|---|---|
| 5Y par (%) | 3.9439 |
| 4.75Y par (%) | 3.7204 |
| 10Y par (%) | 4.4126 |
| 9.75Y par (%) | 4.3046 |
| 3M floating (%) | 2.7595 |
| DV01 of receiving GBP 100m 10Y (GBP/bp) | 82,650 |

- *(a) 5Y carry+roll (bp)*: **51.96 bp**
- *(b) 10Y carry+roll (bp)*: **52.13 bp**
- *(c) 10Y carry+roll (GBP k)*: **4,308 k**
- *Written*: Compare the two per DV01 and give the breakeven.

<details><summary>Model answer</summary>

**5Y 52.0bp, 10Y 52.1bp; 10Y worth +GBP 4.31m.**

1. Carry + roll in bp of rate is already per unit of DV01, so compare them directly: 10Y is better.
2. The 10Y breakeven is a 52.1bp rise over 3 months before the trade loses.

</details>

**Q8** (`d_l3`, topic `carry:breakeven`, seed 1248846)

Using the Givens: (a) 3-month carry + roll (bp) for receiving 5Y, (b) the same for 10Y, (c) the GBP value of the 10Y carry+roll on GBP 100m. Which tenor is better per unit of DV01, and what is the 10Y breakeven?

Givens:

| Given | Value |
|---|---|
| 5Y par (%) | 3.9439 |
| 4.75Y par (%) | 3.7204 |
| 10Y par (%) | 4.4126 |
| 9.75Y par (%) | 4.3046 |
| 3M floating (%) | 2.7595 |
| DV01 of receiving GBP 100m 10Y (GBP/bp) | 82,650 |

- *(a) 5Y carry+roll (bp)*: **51.96 bp**
- *(b) 10Y carry+roll (bp)*: **52.13 bp**
- *(c) 10Y carry+roll (GBP k)*: **4,308 k**
- *Written*: Compare the two per DV01 and give the breakeven.

<details><summary>Model answer</summary>

**5Y 52.0bp, 10Y 52.1bp; 10Y worth +GBP 4.31m.**

1. Carry + roll in bp of rate is already per unit of DV01, so compare them directly: 10Y is better.
2. The 10Y breakeven is a 52.1bp rise over 3 months before the trade loses.

</details>

**Q9** (`d_l3`, topic `carry:breakeven`, seed 1248877)

Using the Givens: (a) 3-month carry + roll (bp) for receiving 5Y, (b) the same for 10Y, (c) the GBP value of the 10Y carry+roll on GBP 100m. Which tenor is better per unit of DV01, and what is the 10Y breakeven?

Givens:

| Given | Value |
|---|---|
| 5Y par (%) | 3.9439 |
| 4.75Y par (%) | 3.7204 |
| 10Y par (%) | 4.4126 |
| 9.75Y par (%) | 4.3046 |
| 3M floating (%) | 2.7595 |
| DV01 of receiving GBP 100m 10Y (GBP/bp) | 82,650 |

- *(a) 5Y carry+roll (bp)*: **51.96 bp**
- *(b) 10Y carry+roll (bp)*: **52.13 bp**
- *(c) 10Y carry+roll (GBP k)*: **4,308 k**
- *Written*: Compare the two per DV01 and give the breakeven.

<details><summary>Model answer</summary>

**5Y 52.0bp, 10Y 52.1bp; 10Y worth +GBP 4.31m.**

1. Carry + roll in bp of rate is already per unit of DV01, so compare them directly: 10Y is better.
2. The 10Y breakeven is a 52.1bp rise over 3 months before the trade loses.

</details>

**Q10** (`d_l3`, topic `carry:breakeven`, seed 1248908)

Using the Givens: (a) 3-month carry + roll (bp) for receiving 5Y, (b) the same for 10Y, (c) the GBP value of the 10Y carry+roll on GBP 100m. Which tenor is better per unit of DV01, and what is the 10Y breakeven?

Givens:

| Given | Value |
|---|---|
| 5Y par (%) | 3.9439 |
| 4.75Y par (%) | 3.7204 |
| 10Y par (%) | 4.4126 |
| 9.75Y par (%) | 4.3046 |
| 3M floating (%) | 2.7595 |
| DV01 of receiving GBP 100m 10Y (GBP/bp) | 82,650 |

- *(a) 5Y carry+roll (bp)*: **51.96 bp**
- *(b) 10Y carry+roll (bp)*: **52.13 bp**
- *(c) 10Y carry+roll (GBP k)*: **4,308 k**
- *Written*: Compare the two per DV01 and give the breakeven.

<details><summary>Model answer</summary>

**5Y 52.0bp, 10Y 52.1bp; 10Y worth +GBP 4.31m.**

1. Carry + roll in bp of rate is already per unit of DV01, so compare them directly: 10Y is better.
2. The 10Y breakeven is a 52.1bp rise over 3 months before the trade loses.

</details>

## 2E Pricing central banks

### Level 1: directional intuition, no calculations

**Q1** (`e_l1_react`, topic `cb:reaction`, seed 1047090)

SONIA prices -20bp for the next BoE meeting and the BoE holds. What happens to the front end?

- *Reaction*: **2Y yields rise: the market removes the cuts it had priced**
- *Written*: Explain.

<details><summary>Model answer</summary>

**The front end sells off.** A hold surprises by about +20bp on that meeting and usually pushes out later cuts; 2Y reprices most, typically a bear flattener.

</details>

**Q2** (`e_l1_react`, topic `cb:reaction`, seed 1047121)

SONIA prices -20bp for the next BoE meeting and the BoE holds. What happens to the front end?

- *Reaction*: **2Y yields rise: the market removes the cuts it had priced**
- *Written*: Explain.

<details><summary>Model answer</summary>

**The front end sells off.** A hold surprises by about +20bp on that meeting and usually pushes out later cuts; 2Y reprices most, typically a bear flattener.

</details>

**Q3** (`e_l1_read`, topic `cb:probabilities`, seed 1047152)

SONIA prices **-18bp** for the next BoE meeting (moves come in 25bp). Does the market think a cut is more or less likely than not?

- *Market view*: **More likely than not**
- *Written*: Explain.

<details><summary>Model answer</summary>

**More likely than not.** With only hold or a 25bp cut, priced change = p x (-25bp), so 18bp means p above 50% (12.5bp would be a coin toss).

</details>

**Q4** (`e_l1_read`, topic `cb:probabilities`, seed 1047183)

SONIA prices **-20bp** for the next BoE meeting (moves come in 25bp). Does the market think a cut is more or less likely than not?

- *Market view*: **More likely than not**
- *Written*: Explain.

<details><summary>Model answer</summary>

**More likely than not.** With only hold or a 25bp cut, priced change = p x (-25bp), so 20bp means p above 50% (12.5bp would be a coin toss).

</details>

**Q5** (`e_l1_react`, topic `cb:reaction`, seed 1047214)

SONIA prices -20bp for the next BoE meeting and the BoE holds. What happens to the front end?

- *Reaction*: **2Y yields rise: the market removes the cuts it had priced**
- *Written*: Explain.

<details><summary>Model answer</summary>

**The front end sells off.** A hold surprises by about +20bp on that meeting and usually pushes out later cuts; 2Y reprices most, typically a bear flattener.

</details>

**Q6** (`e_l1_read`, topic `cb:probabilities`, seed 1047245)

SONIA prices **-8bp** for the next BoE meeting (moves come in 25bp). Does the market think a cut is more or less likely than not?

- *Market view*: **Less likely than not**
- *Written*: Explain.

<details><summary>Model answer</summary>

**Less likely than not.** With only hold or a 25bp cut, priced change = p x (-25bp), so 8bp means p below 50% (12.5bp would be a coin toss).

</details>

**Q7** (`e_l1_react`, topic `cb:reaction`, seed 1047276)

SONIA prices -20bp for the next BoE meeting and the BoE holds. What happens to the front end?

- *Reaction*: **2Y yields rise: the market removes the cuts it had priced**
- *Written*: Explain.

<details><summary>Model answer</summary>

**The front end sells off.** A hold surprises by about +20bp on that meeting and usually pushes out later cuts; 2Y reprices most, typically a bear flattener.

</details>

**Q8** (`e_l1_react`, topic `cb:reaction`, seed 1047307)

SONIA prices -20bp for the next BoE meeting and the BoE holds. What happens to the front end?

- *Reaction*: **2Y yields rise: the market removes the cuts it had priced**
- *Written*: Explain.

<details><summary>Model answer</summary>

**The front end sells off.** A hold surprises by about +20bp on that meeting and usually pushes out later cuts; 2Y reprices most, typically a bear flattener.

</details>

**Q9** (`e_l1_react`, topic `cb:reaction`, seed 1047338)

SONIA prices -20bp for the next BoE meeting and the BoE holds. What happens to the front end?

- *Reaction*: **2Y yields rise: the market removes the cuts it had priced**
- *Written*: Explain.

<details><summary>Model answer</summary>

**The front end sells off.** A hold surprises by about +20bp on that meeting and usually pushes out later cuts; 2Y reprices most, typically a bear flattener.

</details>

**Q10** (`e_l1_react`, topic `cb:reaction`, seed 1047369)

SONIA prices -20bp for the next BoE meeting and the BoE holds. What happens to the front end?

- *Reaction*: **2Y yields rise: the market removes the cuts it had priced**
- *Written*: Explain.

<details><summary>Model answer</summary>

**The front end sells off.** A hold surprises by about +20bp on that meeting and usually pushes out later cuts; 2Y reprices most, typically a bear flattener.

</details>

### Level 2: combinations, light calculations with every input given

**Q1** (`e_l2`, topic `cb:probabilities`, seed 1151819)

SONIA pricing for the next BoE meeting is in the Givens. Assuming moves come in whole steps and any full step is certain, what probability is priced for the next (partial) step?

Givens:

| Given | Value |
|---|---|
| Change priced for the meeting (bp) | -35 |
| Size of one move (bp) | 25 |

- *Probability (%)*: **40.00 %**
- *Written*: Explain the calculation and its caveats.

<details><summary>Model answer</summary>

**40% on top of 1 certain 25bp cut.**

 Expected change = full steps + p x 25bp. Caveats: meeting date vs averaging periods, term premium, and the chance of a 50bp move.

</details>

**Q2** (`e_l2`, topic `cb:probabilities`, seed 1151850)

SONIA pricing for the next BoE meeting is in the Givens. Assuming moves come in whole steps and any full step is certain, what probability is priced for the next (partial) step?

Givens:

| Given | Value |
|---|---|
| Change priced for the meeting (bp) | -35 |
| Size of one move (bp) | 25 |

- *Probability (%)*: **40.00 %**
- *Written*: Explain the calculation and its caveats.

<details><summary>Model answer</summary>

**40% on top of 1 certain 25bp cut.**

 Expected change = full steps + p x 25bp. Caveats: meeting date vs averaging periods, term premium, and the chance of a 50bp move.

</details>

**Q3** (`e_l2`, topic `cb:probabilities`, seed 1151881)

SONIA pricing for the next BoE meeting is in the Givens. Assuming moves come in whole steps and any full step is certain, what probability is priced for the next (partial) step?

Givens:

| Given | Value |
|---|---|
| Change priced for the meeting (bp) | -30 |
| Size of one move (bp) | 25 |

- *Probability (%)*: **20.00 %**
- *Written*: Explain the calculation and its caveats.

<details><summary>Model answer</summary>

**20% on top of 1 certain 25bp cut.**

 Expected change = full steps + p x 25bp. Caveats: meeting date vs averaging periods, term premium, and the chance of a 50bp move.

</details>

**Q4** (`e_l2`, topic `cb:probabilities`, seed 1151912)

SONIA pricing for the next BoE meeting is in the Givens. Assuming moves come in whole steps and any full step is certain, what probability is priced for the next (partial) step?

Givens:

| Given | Value |
|---|---|
| Change priced for the meeting (bp) | -30 |
| Size of one move (bp) | 25 |

- *Probability (%)*: **20.00 %**
- *Written*: Explain the calculation and its caveats.

<details><summary>Model answer</summary>

**20% on top of 1 certain 25bp cut.**

 Expected change = full steps + p x 25bp. Caveats: meeting date vs averaging periods, term premium, and the chance of a 50bp move.

</details>

**Q5** (`e_l2`, topic `cb:probabilities`, seed 1151943)

SONIA pricing for the next BoE meeting is in the Givens. Assuming moves come in whole steps and any full step is certain, what probability is priced for the next (partial) step?

Givens:

| Given | Value |
|---|---|
| Change priced for the meeting (bp) | -10 |
| Size of one move (bp) | 25 |

- *Probability (%)*: **40.00 %**
- *Written*: Explain the calculation and its caveats.

<details><summary>Model answer</summary>

**40%.**

 Expected change = full steps + p x 25bp. Caveats: meeting date vs averaging periods, term premium, and the chance of a 50bp move.

</details>

**Q6** (`e_l2`, topic `cb:probabilities`, seed 1151974)

SONIA pricing for the next BoE meeting is in the Givens. Assuming moves come in whole steps and any full step is certain, what probability is priced for the next (partial) step?

Givens:

| Given | Value |
|---|---|
| Change priced for the meeting (bp) | -30 |
| Size of one move (bp) | 25 |

- *Probability (%)*: **20.00 %**
- *Written*: Explain the calculation and its caveats.

<details><summary>Model answer</summary>

**20% on top of 1 certain 25bp cut.**

 Expected change = full steps + p x 25bp. Caveats: meeting date vs averaging periods, term premium, and the chance of a 50bp move.

</details>

**Q7** (`e_l2`, topic `cb:probabilities`, seed 1152005)

SONIA pricing for the next BoE meeting is in the Givens. Assuming moves come in whole steps and any full step is certain, what probability is priced for the next (partial) step?

Givens:

| Given | Value |
|---|---|
| Change priced for the meeting (bp) | -20 |
| Size of one move (bp) | 25 |

- *Probability (%)*: **80.00 %**
- *Written*: Explain the calculation and its caveats.

<details><summary>Model answer</summary>

**80%.**

 Expected change = full steps + p x 25bp. Caveats: meeting date vs averaging periods, term premium, and the chance of a 50bp move.

</details>

**Q8** (`e_l2`, topic `cb:probabilities`, seed 1152036)

SONIA pricing for the next BoE meeting is in the Givens. Assuming moves come in whole steps and any full step is certain, what probability is priced for the next (partial) step?

Givens:

| Given | Value |
|---|---|
| Change priced for the meeting (bp) | -20 |
| Size of one move (bp) | 25 |

- *Probability (%)*: **80.00 %**
- *Written*: Explain the calculation and its caveats.

<details><summary>Model answer</summary>

**80%.**

 Expected change = full steps + p x 25bp. Caveats: meeting date vs averaging periods, term premium, and the chance of a 50bp move.

</details>

**Q9** (`e_l2`, topic `cb:probabilities`, seed 1152067)

SONIA pricing for the next BoE meeting is in the Givens. Assuming moves come in whole steps and any full step is certain, what probability is priced for the next (partial) step?

Givens:

| Given | Value |
|---|---|
| Change priced for the meeting (bp) | -20 |
| Size of one move (bp) | 25 |

- *Probability (%)*: **80.00 %**
- *Written*: Explain the calculation and its caveats.

<details><summary>Model answer</summary>

**80%.**

 Expected change = full steps + p x 25bp. Caveats: meeting date vs averaging periods, term premium, and the chance of a 50bp move.

</details>

**Q10** (`e_l2`, topic `cb:probabilities`, seed 1152098)

SONIA pricing for the next BoE meeting is in the Givens. Assuming moves come in whole steps and any full step is certain, what probability is priced for the next (partial) step?

Givens:

| Given | Value |
|---|---|
| Change priced for the meeting (bp) | -20 |
| Size of one move (bp) | 25 |

- *Probability (%)*: **80.00 %**
- *Written*: Explain the calculation and its caveats.

<details><summary>Model answer</summary>

**80%.**

 Expected change = full steps + p x 25bp. Caveats: meeting date vs averaging periods, term premium, and the chance of a 50bp move.

</details>

### Level 3: calculations plus subtler concepts

**Q1** (`e_l3`, topic `cb:path`, seed 1256548)

Using the Givens: (a) what probability of a 25bp cut is priced AT meeting 2 (taking meeting 1's pricing as given)? (b) What expected Bank Rate is priced after meeting 2?

Givens:

| Given | Value |
|---|---|
| Bank Rate now (%) | 3.75 |
| Cumulative pricing by meeting 1 (bp) | -20 |
| Cumulative pricing by meeting 2 (bp) | -40 |
| Step size (bp) | 25 |

- *(a) Probability at meeting 2 (%)*: **80.00 %**
- *(b) Expected rate after meeting 2 (%)*: **3.35 %**
- *Written*: Explain how you read a meeting path.

<details><summary>Model answer</summary>

**(a) 80%, (b) 3.350%.**

1. Meeting 2's own pricing = cumulative by 2 minus cumulative by 1 = -20bp, so p = 20/25.
2. Expected rate = 3.75% + (-40bp).

</details>

**Q2** (`e_l3`, topic `cb:path`, seed 1256579)

Using the Givens: (a) what probability of a 25bp cut is priced AT meeting 2 (taking meeting 1's pricing as given)? (b) What expected Bank Rate is priced after meeting 2?

Givens:

| Given | Value |
|---|---|
| Bank Rate now (%) | 3.75 |
| Cumulative pricing by meeting 1 (bp) | -15 |
| Cumulative pricing by meeting 2 (bp) | -30 |
| Step size (bp) | 25 |

- *(a) Probability at meeting 2 (%)*: **60.00 %**
- *(b) Expected rate after meeting 2 (%)*: **3.45 %**
- *Written*: Explain how you read a meeting path.

<details><summary>Model answer</summary>

**(a) 60%, (b) 3.450%.**

1. Meeting 2's own pricing = cumulative by 2 minus cumulative by 1 = -15bp, so p = 15/25.
2. Expected rate = 3.75% + (-30bp).

</details>

**Q3** (`e_l3`, topic `cb:path`, seed 1256610)

Using the Givens: (a) what probability of a 25bp cut is priced AT meeting 2 (taking meeting 1's pricing as given)? (b) What expected Bank Rate is priced after meeting 2?

Givens:

| Given | Value |
|---|---|
| Bank Rate now (%) | 3.75 |
| Cumulative pricing by meeting 1 (bp) | -5 |
| Cumulative pricing by meeting 2 (bp) | -20 |
| Step size (bp) | 25 |

- *(a) Probability at meeting 2 (%)*: **60.00 %**
- *(b) Expected rate after meeting 2 (%)*: **3.55 %**
- *Written*: Explain how you read a meeting path.

<details><summary>Model answer</summary>

**(a) 60%, (b) 3.550%.**

1. Meeting 2's own pricing = cumulative by 2 minus cumulative by 1 = -15bp, so p = 15/25.
2. Expected rate = 3.75% + (-20bp).

</details>

**Q4** (`e_l3`, topic `cb:path`, seed 1256641)

Using the Givens: (a) what probability of a 25bp cut is priced AT meeting 2 (taking meeting 1's pricing as given)? (b) What expected Bank Rate is priced after meeting 2?

Givens:

| Given | Value |
|---|---|
| Bank Rate now (%) | 3.75 |
| Cumulative pricing by meeting 1 (bp) | -15 |
| Cumulative pricing by meeting 2 (bp) | -35 |
| Step size (bp) | 25 |

- *(a) Probability at meeting 2 (%)*: **80.00 %**
- *(b) Expected rate after meeting 2 (%)*: **3.40 %**
- *Written*: Explain how you read a meeting path.

<details><summary>Model answer</summary>

**(a) 80%, (b) 3.400%.**

1. Meeting 2's own pricing = cumulative by 2 minus cumulative by 1 = -20bp, so p = 20/25.
2. Expected rate = 3.75% + (-35bp).

</details>

**Q5** (`e_l3`, topic `cb:path`, seed 1256672)

Using the Givens: (a) what probability of a 25bp cut is priced AT meeting 2 (taking meeting 1's pricing as given)? (b) What expected Bank Rate is priced after meeting 2?

Givens:

| Given | Value |
|---|---|
| Bank Rate now (%) | 3.75 |
| Cumulative pricing by meeting 1 (bp) | -5 |
| Cumulative pricing by meeting 2 (bp) | -25 |
| Step size (bp) | 25 |

- *(a) Probability at meeting 2 (%)*: **80.00 %**
- *(b) Expected rate after meeting 2 (%)*: **3.50 %**
- *Written*: Explain how you read a meeting path.

<details><summary>Model answer</summary>

**(a) 80%, (b) 3.500%.**

1. Meeting 2's own pricing = cumulative by 2 minus cumulative by 1 = -20bp, so p = 20/25.
2. Expected rate = 3.75% + (-25bp).

</details>

**Q6** (`e_l3`, topic `cb:path`, seed 1256703)

Using the Givens: (a) what probability of a 25bp cut is priced AT meeting 2 (taking meeting 1's pricing as given)? (b) What expected Bank Rate is priced after meeting 2?

Givens:

| Given | Value |
|---|---|
| Bank Rate now (%) | 3.75 |
| Cumulative pricing by meeting 1 (bp) | -5 |
| Cumulative pricing by meeting 2 (bp) | -25 |
| Step size (bp) | 25 |

- *(a) Probability at meeting 2 (%)*: **80.00 %**
- *(b) Expected rate after meeting 2 (%)*: **3.50 %**
- *Written*: Explain how you read a meeting path.

<details><summary>Model answer</summary>

**(a) 80%, (b) 3.500%.**

1. Meeting 2's own pricing = cumulative by 2 minus cumulative by 1 = -20bp, so p = 20/25.
2. Expected rate = 3.75% + (-25bp).

</details>

**Q7** (`e_l3`, topic `cb:path`, seed 1256734)

Using the Givens: (a) what probability of a 25bp cut is priced AT meeting 2 (taking meeting 1's pricing as given)? (b) What expected Bank Rate is priced after meeting 2?

Givens:

| Given | Value |
|---|---|
| Bank Rate now (%) | 3.75 |
| Cumulative pricing by meeting 1 (bp) | -5 |
| Cumulative pricing by meeting 2 (bp) | -15 |
| Step size (bp) | 25 |

- *(a) Probability at meeting 2 (%)*: **40.00 %**
- *(b) Expected rate after meeting 2 (%)*: **3.60 %**
- *Written*: Explain how you read a meeting path.

<details><summary>Model answer</summary>

**(a) 40%, (b) 3.600%.**

1. Meeting 2's own pricing = cumulative by 2 minus cumulative by 1 = -10bp, so p = 10/25.
2. Expected rate = 3.75% + (-15bp).

</details>

**Q8** (`e_l3`, topic `cb:path`, seed 1256765)

Using the Givens: (a) what probability of a 25bp cut is priced AT meeting 2 (taking meeting 1's pricing as given)? (b) What expected Bank Rate is priced after meeting 2?

Givens:

| Given | Value |
|---|---|
| Bank Rate now (%) | 3.75 |
| Cumulative pricing by meeting 1 (bp) | -5 |
| Cumulative pricing by meeting 2 (bp) | -15 |
| Step size (bp) | 25 |

- *(a) Probability at meeting 2 (%)*: **40.00 %**
- *(b) Expected rate after meeting 2 (%)*: **3.60 %**
- *Written*: Explain how you read a meeting path.

<details><summary>Model answer</summary>

**(a) 40%, (b) 3.600%.**

1. Meeting 2's own pricing = cumulative by 2 minus cumulative by 1 = -10bp, so p = 10/25.
2. Expected rate = 3.75% + (-15bp).

</details>

**Q9** (`e_l3`, topic `cb:path`, seed 1256796)

Using the Givens: (a) what probability of a 25bp cut is priced AT meeting 2 (taking meeting 1's pricing as given)? (b) What expected Bank Rate is priced after meeting 2?

Givens:

| Given | Value |
|---|---|
| Bank Rate now (%) | 3.75 |
| Cumulative pricing by meeting 1 (bp) | -15 |
| Cumulative pricing by meeting 2 (bp) | -25 |
| Step size (bp) | 25 |

- *(a) Probability at meeting 2 (%)*: **40.00 %**
- *(b) Expected rate after meeting 2 (%)*: **3.50 %**
- *Written*: Explain how you read a meeting path.

<details><summary>Model answer</summary>

**(a) 40%, (b) 3.500%.**

1. Meeting 2's own pricing = cumulative by 2 minus cumulative by 1 = -10bp, so p = 10/25.
2. Expected rate = 3.75% + (-25bp).

</details>

**Q10** (`e_l3`, topic `cb:path`, seed 1256827)

Using the Givens: (a) what probability of a 25bp cut is priced AT meeting 2 (taking meeting 1's pricing as given)? (b) What expected Bank Rate is priced after meeting 2?

Givens:

| Given | Value |
|---|---|
| Bank Rate now (%) | 3.75 |
| Cumulative pricing by meeting 1 (bp) | -20 |
| Cumulative pricing by meeting 2 (bp) | -35 |
| Step size (bp) | 25 |

- *(a) Probability at meeting 2 (%)*: **60.00 %**
- *(b) Expected rate after meeting 2 (%)*: **3.40 %**
- *Written*: Explain how you read a meeting path.

<details><summary>Model answer</summary>

**(a) 60%, (b) 3.400%.**

1. Meeting 2's own pricing = cumulative by 2 minus cumulative by 1 = -15bp, so p = 15/25.
2. Expected rate = 3.75% + (-35bp).

</details>

## 2F Advanced

### Level 1: directional intuition, no calculations

**Q1** (`f_l1_concept`, topic `advanced:fly`, seed 1055009)

Why weight a 2s5s10s butterfly with PCA rather than 50/50 DV01?

- *Answer*: **PCA weights hedge level and slope as they actually co-move, isolating curvature**
- *Written*: Explain in your own words.

<details><summary>Model answer</summary>

**PCA weights hedge level and slope as they actually co-move, isolating curvature.**

A 50/50 DV01 fly is only hedged to parallel moves; steepening moves the wings differently. PCA weights hedge both level and slope.

</details>

**Q2** (`f_l1_concept`, topic `advanced:fly`, seed 1055040)

Why weight a 2s5s10s butterfly with PCA rather than 50/50 DV01?

- *Answer*: **PCA weights hedge level and slope as they actually co-move, isolating curvature**
- *Written*: Explain in your own words.

<details><summary>Model answer</summary>

**PCA weights hedge level and slope as they actually co-move, isolating curvature.**

A 50/50 DV01 fly is only hedged to parallel moves; steepening moves the wings differently. PCA weights hedge both level and slope.

</details>

**Q3** (`f_l1_concept`, topic `advanced:ldi_2022`, seed 1055071)

In September 2022, why did UK LDI funds sell gilts as yields spiked?

- *Answer*: **Leveraged long-duration hedges lost value, collateral calls had to be met fast, so they sold gilts into a falling market until the BoE stepped in**
- *Written*: Explain in your own words.

<details><summary>Model answer</summary>

**Leveraged long-duration hedges lost value, collateral calls had to be met fast, so they sold gilts into a falling market until the BoE stepped in.**

LDI funds hedge long liabilities with leveraged long duration. The mini-budget sent long yields up fast, the hedges needed collateral within days, and funds sold their most liquid asset: forced selling of duration, a doom loop.

</details>

**Q4** (`f_l1_concept`, topic `advanced:swap_spreads`, seed 1055102)

Why can swap spreads (swap rate minus government yield) be negative, as in 30Y USD?

- *Answer*: **Dealer balance-sheet costs make holding bonds expensive, heavy government supply cheapens bonds, and liability hedgers receive fixed, pushing swap rates below yields**
- *Written*: Explain in your own words.

<details><summary>Model answer</summary>

**Dealer balance-sheet costs make holding bonds expensive, heavy government supply cheapens bonds, and liability hedgers receive fixed, pushing swap rates below yields.**

Holding bonds uses scarce balance sheet; repo is not free; supply cheapens bonds; pensions receive long swaps. The 'arbitrage' needs balance sheet nobody has cheaply.

</details>

**Q5** (`f_l1_concept`, topic `advanced:swap_spreads`, seed 1055133)

Why can swap spreads (swap rate minus government yield) be negative, as in 30Y USD?

- *Answer*: **Dealer balance-sheet costs make holding bonds expensive, heavy government supply cheapens bonds, and liability hedgers receive fixed, pushing swap rates below yields**
- *Written*: Explain in your own words.

<details><summary>Model answer</summary>

**Dealer balance-sheet costs make holding bonds expensive, heavy government supply cheapens bonds, and liability hedgers receive fixed, pushing swap rates below yields.**

Holding bonds uses scarce balance sheet; repo is not free; supply cheapens bonds; pensions receive long swaps. The 'arbitrage' needs balance sheet nobody has cheaply.

</details>

**Q6** (`f_l1_concept`, topic `advanced:fly`, seed 1055164)

Why weight a 2s5s10s butterfly with PCA rather than 50/50 DV01?

- *Answer*: **PCA weights hedge level and slope as they actually co-move, isolating curvature**
- *Written*: Explain in your own words.

<details><summary>Model answer</summary>

**PCA weights hedge level and slope as they actually co-move, isolating curvature.**

A 50/50 DV01 fly is only hedged to parallel moves; steepening moves the wings differently. PCA weights hedge both level and slope.

</details>

**Q7** (`f_l1_concept`, topic `advanced:vol_owners`, seed 1055195)

Who is structurally SHORT rates volatility?

- *Answer*: **MBS and callable-bond investors (short the prepayment/call option)**
- *Written*: Explain in your own words.

<details><summary>Model answer</summary>

**MBS and callable-bond investors (short the prepayment/call option).**

Holders of MBS and callables are short the borrower's or issuer's option, so they are short vol and short convexity; callable issuance and structured notes also supply vol.

</details>

**Q8** (`f_l1_concept`, topic `advanced:swap_spreads`, seed 1055226)

Why can swap spreads (swap rate minus government yield) be negative, as in 30Y USD?

- *Answer*: **Dealer balance-sheet costs make holding bonds expensive, heavy government supply cheapens bonds, and liability hedgers receive fixed, pushing swap rates below yields**
- *Written*: Explain in your own words.

<details><summary>Model answer</summary>

**Dealer balance-sheet costs make holding bonds expensive, heavy government supply cheapens bonds, and liability hedgers receive fixed, pushing swap rates below yields.**

Holding bonds uses scarce balance sheet; repo is not free; supply cheapens bonds; pensions receive long swaps. The 'arbitrage' needs balance sheet nobody has cheaply.

</details>

**Q9** (`f_l1_concept`, topic `advanced:fly`, seed 1055257)

Why weight a 2s5s10s butterfly with PCA rather than 50/50 DV01?

- *Answer*: **PCA weights hedge level and slope as they actually co-move, isolating curvature**
- *Written*: Explain in your own words.

<details><summary>Model answer</summary>

**PCA weights hedge level and slope as they actually co-move, isolating curvature.**

A 50/50 DV01 fly is only hedged to parallel moves; steepening moves the wings differently. PCA weights hedge both level and slope.

</details>

**Q10** (`f_l1_concept`, topic `advanced:fly`, seed 1055288)

Why weight a 2s5s10s butterfly with PCA rather than 50/50 DV01?

- *Answer*: **PCA weights hedge level and slope as they actually co-move, isolating curvature**
- *Written*: Explain in your own words.

<details><summary>Model answer</summary>

**PCA weights hedge level and slope as they actually co-move, isolating curvature.**

A 50/50 DV01 fly is only hedged to parallel moves; steepening moves the wings differently. PCA weights hedge both level and slope.

</details>

### Level 2: combinations, light calculations with every input given

**Q1** (`f_l2_ctd`, topic `advanced:ctd`, seed 1159738)

Using the prices, conversion factors and futures price in the Givens, which bond is cheapest to deliver, and what is its gross basis?

Givens:

| Given | Value |
|---|---|
| Futures price | 81.06 |
| 4.0% 8Y price | 79.227 |
| 4.0% 8Y conversion factor | 0.8744 |
| 5.0% 14Y price | 78.557 |
| 5.0% 14Y conversion factor | 0.9062 |
| 3.5% 25Y price | 55.131 |
| 3.5% 25Y conversion factor | 0.6784 |

- *CTD*: **3.5% 25Y**
- *CTD gross basis (price points)*: **0.1399**
- *Written*: Explain how the short chooses.

<details><summary>Model answer</summary>

**3.5% 25Y, basis 0.140.**

1. The short delivers the bond that costs least relative to what they are paid (futures x CF): lowest gross basis.
2. Bases: 4.0% 8Y 8.348, 5.0% 14Y 5.100, 3.5% 25Y 0.140.
3. At yields above the 6% notional coupon, high-duration bonds tend to be CTD.

</details>

**Q2** (`f_l2_ctd`, topic `advanced:ctd`, seed 1159769)

Using the prices, conversion factors and futures price in the Givens, which bond is cheapest to deliver, and what is its gross basis?

Givens:

| Given | Value |
|---|---|
| Futures price | 110.42 |
| 4.0% 8Y price | 96.672 |
| 4.0% 8Y conversion factor | 0.8744 |
| 5.0% 14Y price | 105.15 |
| 5.0% 14Y conversion factor | 0.9062 |
| 3.5% 25Y price | 85.083 |
| 3.5% 25Y conversion factor | 0.6784 |

- *CTD*: **4.0% 8Y**
- *CTD gross basis (price points)*: **0.119**
- *Written*: Explain how the short chooses.

<details><summary>Model answer</summary>

**4.0% 8Y, basis 0.119.**

1. The short delivers the bond that costs least relative to what they are paid (futures x CF): lowest gross basis.
2. Bases: 4.0% 8Y 0.119, 5.0% 14Y 5.088, 3.5% 25Y 10.173.
3. At yields below the 6% notional coupon, low-duration bonds tend to be CTD.

</details>

**Q3** (`f_l2_nvol`, topic `advanced:normal_vol`, seed 1159800)

Convert the lognormal vol in the Givens to an approximate normal (bp) vol, and to a daily bp move.

Givens:

| Given | Value |
|---|---|
| Forward swap rate (%) | 4.5 |
| Lognormal (Black) vol (%) | 22 |

- *Normal vol (bp/yr)*: **99.00 bp**
- *Daily move (bp, 252 days)*: **6.24 bp**
- *Written*: Why do rates desks quote normal vol?

<details><summary>Model answer</summary>

**About 99bp a year, 6.2bp a day.** Near the money sigma_N ~ sigma_B x F. Rate moves are closer to additive than proportional (and rates can go negative), so desks quote normal vol.

</details>

**Q4** (`f_l2_ctd`, topic `advanced:ctd`, seed 1159831)

Using the prices, conversion factors and futures price in the Givens, which bond is cheapest to deliver, and what is its gross basis?

Givens:

| Given | Value |
|---|---|
| Futures price | 122.24 |
| 4.0% 8Y price | 107.07 |
| 4.0% 8Y conversion factor | 0.8744 |
| 5.0% 14Y price | 122.73 |
| 5.0% 14Y conversion factor | 0.9062 |
| 3.5% 25Y price | 108.75 |
| 3.5% 25Y conversion factor | 0.6784 |

- *CTD*: **4.0% 8Y**
- *CTD gross basis (price points)*: **0.1828**
- *Written*: Explain how the short chooses.

<details><summary>Model answer</summary>

**4.0% 8Y, basis 0.183.**

1. The short delivers the bond that costs least relative to what they are paid (futures x CF): lowest gross basis.
2. Bases: 4.0% 8Y 0.183, 5.0% 14Y 11.957, 3.5% 25Y 25.825.
3. At yields below the 6% notional coupon, low-duration bonds tend to be CTD.

</details>

**Q5** (`f_l2_ctd`, topic `advanced:ctd`, seed 1159862)

Using the prices, conversion factors and futures price in the Givens, which bond is cheapest to deliver, and what is its gross basis?

Givens:

| Given | Value |
|---|---|
| Futures price | 81.054 |
| 4.0% 8Y price | 79.227 |
| 4.0% 8Y conversion factor | 0.8744 |
| 5.0% 14Y price | 78.557 |
| 5.0% 14Y conversion factor | 0.9062 |
| 3.5% 25Y price | 55.131 |
| 3.5% 25Y conversion factor | 0.6784 |

- *CTD*: **3.5% 25Y**
- *CTD gross basis (price points)*: **0.144**
- *Written*: Explain how the short chooses.

<details><summary>Model answer</summary>

**3.5% 25Y, basis 0.144.**

1. The short delivers the bond that costs least relative to what they are paid (futures x CF): lowest gross basis.
2. Bases: 4.0% 8Y 8.353, 5.0% 14Y 5.106, 3.5% 25Y 0.144.
3. At yields above the 6% notional coupon, high-duration bonds tend to be CTD.

</details>

**Q6** (`f_l2_nvol`, topic `advanced:normal_vol`, seed 1159893)

Convert the lognormal vol in the Givens to an approximate normal (bp) vol, and to a daily bp move.

Givens:

| Given | Value |
|---|---|
| Forward swap rate (%) | 4.5 |
| Lognormal (Black) vol (%) | 20 |

- *Normal vol (bp/yr)*: **90.00 bp**
- *Daily move (bp, 252 days)*: **5.67 bp**
- *Written*: Why do rates desks quote normal vol?

<details><summary>Model answer</summary>

**About 90bp a year, 5.7bp a day.** Near the money sigma_N ~ sigma_B x F. Rate moves are closer to additive than proportional (and rates can go negative), so desks quote normal vol.

</details>

**Q7** (`f_l2_nvol`, topic `advanced:normal_vol`, seed 1159924)

Convert the lognormal vol in the Givens to an approximate normal (bp) vol, and to a daily bp move.

Givens:

| Given | Value |
|---|---|
| Forward swap rate (%) | 4.5 |
| Lognormal (Black) vol (%) | 20 |

- *Normal vol (bp/yr)*: **90.00 bp**
- *Daily move (bp, 252 days)*: **5.67 bp**
- *Written*: Why do rates desks quote normal vol?

<details><summary>Model answer</summary>

**About 90bp a year, 5.7bp a day.** Near the money sigma_N ~ sigma_B x F. Rate moves are closer to additive than proportional (and rates can go negative), so desks quote normal vol.

</details>

**Q8** (`f_l2_ctd`, topic `advanced:ctd`, seed 1159955)

Using the prices, conversion factors and futures price in the Givens, which bond is cheapest to deliver, and what is its gross basis?

Givens:

| Given | Value |
|---|---|
| Futures price | 110.45 |
| 4.0% 8Y price | 96.672 |
| 4.0% 8Y conversion factor | 0.8744 |
| 5.0% 14Y price | 105.15 |
| 5.0% 14Y conversion factor | 0.9062 |
| 3.5% 25Y price | 85.083 |
| 3.5% 25Y conversion factor | 0.6784 |

- *CTD*: **4.0% 8Y**
- *CTD gross basis (price points)*: **0.09365**
- *Written*: Explain how the short chooses.

<details><summary>Model answer</summary>

**4.0% 8Y, basis 0.094.**

1. The short delivers the bond that costs least relative to what they are paid (futures x CF): lowest gross basis.
2. Bases: 4.0% 8Y 0.094, 5.0% 14Y 5.061, 3.5% 25Y 10.153.
3. At yields below the 6% notional coupon, low-duration bonds tend to be CTD.

</details>

**Q9** (`f_l2_nvol`, topic `advanced:normal_vol`, seed 1159986)

Convert the lognormal vol in the Givens to an approximate normal (bp) vol, and to a daily bp move.

Givens:

| Given | Value |
|---|---|
| Forward swap rate (%) | 3.5 |
| Lognormal (Black) vol (%) | 30 |

- *Normal vol (bp/yr)*: **105.00 bp**
- *Daily move (bp, 252 days)*: **6.61 bp**
- *Written*: Why do rates desks quote normal vol?

<details><summary>Model answer</summary>

**About 105bp a year, 6.6bp a day.** Near the money sigma_N ~ sigma_B x F. Rate moves are closer to additive than proportional (and rates can go negative), so desks quote normal vol.

</details>

**Q10** (`f_l2_nvol`, topic `advanced:normal_vol`, seed 1160017)

Convert the lognormal vol in the Givens to an approximate normal (bp) vol, and to a daily bp move.

Givens:

| Given | Value |
|---|---|
| Forward swap rate (%) | 3 |
| Lognormal (Black) vol (%) | 22 |

- *Normal vol (bp/yr)*: **66.00 bp**
- *Daily move (bp, 252 days)*: **4.16 bp**
- *Written*: Why do rates desks quote normal vol?

<details><summary>Model answer</summary>

**About 66bp a year, 4.2bp a day.** Near the money sigma_N ~ sigma_B x F. Rate moves are closer to additive than proportional (and rates can go negative), so desks quote normal vol.

</details>

### Level 3: calculations plus subtler concepts

**Q1** (`f_l3_ldi`, topic `advanced:ldi_2022`, seed 1264467)

An LDI fund hedges pension liabilities with leveraged long duration (Givens). Long gilt yields jump. (a) How much collateral is called (GBP m)? (b) How many bp can yields rise before the liquid collateral runs out?

Givens:

| Given | Value |
|---|---|
| DV01 of the fund's receive-fixed / repo gilt hedges (GBP/bp) | 3,000,000 |
| Rise in long gilt yields (bp) | 120 |
| Liquid collateral available (GBP) | 400,000,000 |

- *(a) Collateral call (GBP m)*: **360.00 m**
- *(b) bp until collateral is exhausted*: **133.33 bp**
- *Written*: Explain the 2022 doom loop.

<details><summary>Model answer</summary>

**(a) GBP 360m, (b) 133bp.**

1. The hedges lose ~DV01 x move, paid as variation margin. Liabilities fall in value too, but they need no cash.
2. Once liquid collateral runs out, funds sell gilts, which pushes yields up, which triggers more calls: a doom loop that the BoE broke by buying long gilts.

</details>

**Q2** (`f_l3_ldi`, topic `advanced:ldi_2022`, seed 1264498)

An LDI fund hedges pension liabilities with leveraged long duration (Givens). Long gilt yields jump. (a) How much collateral is called (GBP m)? (b) How many bp can yields rise before the liquid collateral runs out?

Givens:

| Given | Value |
|---|---|
| DV01 of the fund's receive-fixed / repo gilt hedges (GBP/bp) | 5,000,000 |
| Rise in long gilt yields (bp) | 100 |
| Liquid collateral available (GBP) | 600,000,000 |

- *(a) Collateral call (GBP m)*: **500.00 m**
- *(b) bp until collateral is exhausted*: **120.00 bp**
- *Written*: Explain the 2022 doom loop.

<details><summary>Model answer</summary>

**(a) GBP 500m, (b) 120bp.**

1. The hedges lose ~DV01 x move, paid as variation margin. Liabilities fall in value too, but they need no cash.
2. Once liquid collateral runs out, funds sell gilts, which pushes yields up, which triggers more calls: a doom loop that the BoE broke by buying long gilts.

</details>

**Q3** (`f_l3_krd`, topic `advanced:krd`, seed 1264529)

You own GBP 100m of a 4.5% 7Y gilt. Hedge its 5Y, 10Y and 20Y key-rate DV01s by paying fixed in 5Y, 10Y and 20Y swaps (assume each swap's DV01 sits in its own bucket). How much notional of each (GBP m)?

Givens:

| Given | Value |
|---|---|
| Bond key-rate DV01 at 2Y (GBP/bp) | 2,667 |
| Bond key-rate DV01 at 5Y (GBP/bp) | 38,451 |
| Bond key-rate DV01 at 10Y (GBP/bp) | 22,684 |
| Bond key-rate DV01 at 20Y (GBP/bp) | 0 |
| Bond key-rate DV01 at 30Y (GBP/bp) | 0 |
| DV01 of paying GBP 1m 5Y swap (GBP/bp) | -466.75 |
| DV01 of paying GBP 1m 10Y swap (GBP/bp) | -838.85 |
| DV01 of paying GBP 1m 20Y swap (GBP/bp) | -1,342.07 |

- *5Y swap (GBP m)*: **82.38 m**
- *10Y swap (GBP m)*: **27.04 m**
- *20Y swap (GBP m)*: **0 m**
- *Written*: What does key-rate DV01 tell you that parallel DV01 does not?

<details><summary>Model answer</summary>

**5Y 82.4m, 10Y 27.0m, 20Y 0.0m.**

1. Key-rate DV01 bumps one pillar at a time, showing WHERE the duration sits (here mostly 5Y and 10Y).
2. Each hedge = bucket DV01 / DV01 of paying GBP 1m in that tenor.
3. Simplification: real swaps spread DV01 across neighbouring buckets, so you would solve the full matrix.

</details>

**Q4** (`f_l3_krd`, topic `advanced:krd`, seed 1264560)

You own GBP 100m of a 4.5% 12Y gilt. Hedge its 5Y, 10Y and 20Y key-rate DV01s by paying fixed in 5Y, 10Y and 20Y swaps (assume each swap's DV01 sits in its own bucket). How much notional of each (GBP m)?

Givens:

| Given | Value |
|---|---|
| Bond key-rate DV01 at 2Y (GBP/bp) | 2,667 |
| Bond key-rate DV01 at 5Y (GBP/bp) | 8,153 |
| Bond key-rate DV01 at 10Y (GBP/bp) | 71,396 |
| Bond key-rate DV01 at 20Y (GBP/bp) | 15,390 |
| Bond key-rate DV01 at 30Y (GBP/bp) | 0 |
| DV01 of paying GBP 1m 5Y swap (GBP/bp) | -466.75 |
| DV01 of paying GBP 1m 10Y swap (GBP/bp) | -838.85 |
| DV01 of paying GBP 1m 20Y swap (GBP/bp) | -1,342.07 |

- *5Y swap (GBP m)*: **17.47 m**
- *10Y swap (GBP m)*: **85.11 m**
- *20Y swap (GBP m)*: **11.47 m**
- *Written*: What does key-rate DV01 tell you that parallel DV01 does not?

<details><summary>Model answer</summary>

**5Y 17.5m, 10Y 85.1m, 20Y 11.5m.**

1. Key-rate DV01 bumps one pillar at a time, showing WHERE the duration sits (here mostly 10Y and 20Y).
2. Each hedge = bucket DV01 / DV01 of paying GBP 1m in that tenor.
3. Simplification: real swaps spread DV01 across neighbouring buckets, so you would solve the full matrix.

</details>

**Q5** (`f_l3_krd`, topic `advanced:krd`, seed 1264591)

You own GBP 100m of a 4.5% 12Y gilt. Hedge its 5Y, 10Y and 20Y key-rate DV01s by paying fixed in 5Y, 10Y and 20Y swaps (assume each swap's DV01 sits in its own bucket). How much notional of each (GBP m)?

Givens:

| Given | Value |
|---|---|
| Bond key-rate DV01 at 2Y (GBP/bp) | 2,667 |
| Bond key-rate DV01 at 5Y (GBP/bp) | 8,153 |
| Bond key-rate DV01 at 10Y (GBP/bp) | 71,396 |
| Bond key-rate DV01 at 20Y (GBP/bp) | 15,390 |
| Bond key-rate DV01 at 30Y (GBP/bp) | 0 |
| DV01 of paying GBP 1m 5Y swap (GBP/bp) | -466.75 |
| DV01 of paying GBP 1m 10Y swap (GBP/bp) | -838.85 |
| DV01 of paying GBP 1m 20Y swap (GBP/bp) | -1,342.07 |

- *5Y swap (GBP m)*: **17.47 m**
- *10Y swap (GBP m)*: **85.11 m**
- *20Y swap (GBP m)*: **11.47 m**
- *Written*: What does key-rate DV01 tell you that parallel DV01 does not?

<details><summary>Model answer</summary>

**5Y 17.5m, 10Y 85.1m, 20Y 11.5m.**

1. Key-rate DV01 bumps one pillar at a time, showing WHERE the duration sits (here mostly 10Y and 20Y).
2. Each hedge = bucket DV01 / DV01 of paying GBP 1m in that tenor.
3. Simplification: real swaps spread DV01 across neighbouring buckets, so you would solve the full matrix.

</details>

**Q6** (`f_l3_ldi`, topic `advanced:ldi_2022`, seed 1264622)

An LDI fund hedges pension liabilities with leveraged long duration (Givens). Long gilt yields jump. (a) How much collateral is called (GBP m)? (b) How many bp can yields rise before the liquid collateral runs out?

Givens:

| Given | Value |
|---|---|
| DV01 of the fund's receive-fixed / repo gilt hedges (GBP/bp) | 2,000,000 |
| Rise in long gilt yields (bp) | 150 |
| Liquid collateral available (GBP) | 300,000,000 |

- *(a) Collateral call (GBP m)*: **300.00 m**
- *(b) bp until collateral is exhausted*: **150.00 bp**
- *Written*: Explain the 2022 doom loop.

<details><summary>Model answer</summary>

**(a) GBP 300m, (b) 150bp.**

1. The hedges lose ~DV01 x move, paid as variation margin. Liabilities fall in value too, but they need no cash.
2. Once liquid collateral runs out, funds sell gilts, which pushes yields up, which triggers more calls: a doom loop that the BoE broke by buying long gilts.

</details>

**Q7** (`f_l3_ldi`, topic `advanced:ldi_2022`, seed 1264653)

An LDI fund hedges pension liabilities with leveraged long duration (Givens). Long gilt yields jump. (a) How much collateral is called (GBP m)? (b) How many bp can yields rise before the liquid collateral runs out?

Givens:

| Given | Value |
|---|---|
| DV01 of the fund's receive-fixed / repo gilt hedges (GBP/bp) | 3,000,000 |
| Rise in long gilt yields (bp) | 150 |
| Liquid collateral available (GBP) | 400,000,000 |

- *(a) Collateral call (GBP m)*: **450.00 m**
- *(b) bp until collateral is exhausted*: **133.33 bp**
- *Written*: Explain the 2022 doom loop.

<details><summary>Model answer</summary>

**(a) GBP 450m, (b) 133bp.**

1. The hedges lose ~DV01 x move, paid as variation margin. Liabilities fall in value too, but they need no cash.
2. Once liquid collateral runs out, funds sell gilts, which pushes yields up, which triggers more calls: a doom loop that the BoE broke by buying long gilts.

</details>

**Q8** (`f_l3_ldi`, topic `advanced:ldi_2022`, seed 1264684)

An LDI fund hedges pension liabilities with leveraged long duration (Givens). Long gilt yields jump. (a) How much collateral is called (GBP m)? (b) How many bp can yields rise before the liquid collateral runs out?

Givens:

| Given | Value |
|---|---|
| DV01 of the fund's receive-fixed / repo gilt hedges (GBP/bp) | 5,000,000 |
| Rise in long gilt yields (bp) | 100 |
| Liquid collateral available (GBP) | 400,000,000 |

- *(a) Collateral call (GBP m)*: **500.00 m**
- *(b) bp until collateral is exhausted*: **80.00 bp**
- *Written*: Explain the 2022 doom loop.

<details><summary>Model answer</summary>

**(a) GBP 500m, (b) 80bp.**

1. The hedges lose ~DV01 x move, paid as variation margin. Liabilities fall in value too, but they need no cash.
2. Once liquid collateral runs out, funds sell gilts, which pushes yields up, which triggers more calls: a doom loop that the BoE broke by buying long gilts.

</details>

**Q9** (`f_l3_ldi`, topic `advanced:ldi_2022`, seed 1264715)

An LDI fund hedges pension liabilities with leveraged long duration (Givens). Long gilt yields jump. (a) How much collateral is called (GBP m)? (b) How many bp can yields rise before the liquid collateral runs out?

Givens:

| Given | Value |
|---|---|
| DV01 of the fund's receive-fixed / repo gilt hedges (GBP/bp) | 5,000,000 |
| Rise in long gilt yields (bp) | 120 |
| Liquid collateral available (GBP) | 600,000,000 |

- *(a) Collateral call (GBP m)*: **600.00 m**
- *(b) bp until collateral is exhausted*: **120.00 bp**
- *Written*: Explain the 2022 doom loop.

<details><summary>Model answer</summary>

**(a) GBP 600m, (b) 120bp.**

1. The hedges lose ~DV01 x move, paid as variation margin. Liabilities fall in value too, but they need no cash.
2. Once liquid collateral runs out, funds sell gilts, which pushes yields up, which triggers more calls: a doom loop that the BoE broke by buying long gilts.

</details>

**Q10** (`f_l3_krd`, topic `advanced:krd`, seed 1264746)

You own GBP 100m of a 4.5% 20Y gilt. Hedge its 5Y, 10Y and 20Y key-rate DV01s by paying fixed in 5Y, 10Y and 20Y swaps (assume each swap's DV01 sits in its own bucket). How much notional of each (GBP m)?

Givens:

| Given | Value |
|---|---|
| Bond key-rate DV01 at 2Y (GBP/bp) | 2,667 |
| Bond key-rate DV01 at 5Y (GBP/bp) | 8,153 |
| Bond key-rate DV01 at 10Y (GBP/bp) | 23,558 |
| Bond key-rate DV01 at 20Y (GBP/bp) | 99,238 |
| Bond key-rate DV01 at 30Y (GBP/bp) | 0 |
| DV01 of paying GBP 1m 5Y swap (GBP/bp) | -466.75 |
| DV01 of paying GBP 1m 10Y swap (GBP/bp) | -838.85 |
| DV01 of paying GBP 1m 20Y swap (GBP/bp) | -1,342.07 |

- *5Y swap (GBP m)*: **17.47 m**
- *10Y swap (GBP m)*: **28.08 m**
- *20Y swap (GBP m)*: **73.94 m**
- *Written*: What does key-rate DV01 tell you that parallel DV01 does not?

<details><summary>Model answer</summary>

**5Y 17.5m, 10Y 28.1m, 20Y 73.9m.**

1. Key-rate DV01 bumps one pillar at a time, showing WHERE the duration sits (here mostly 20Y and 10Y).
2. Each hedge = bucket DV01 / DV01 of paying GBP 1m in that tenor.
3. Simplification: real swaps spread DV01 across neighbouring buckets, so you would solve the full matrix.

</details>
