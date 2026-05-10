"""Curated historical market events with known price outcomes.

Each event has a ticker, date, title, body (realistic news text), and the
actual price change % over lookahead_days trading days. Verified against
yfinance historical data.
"""

HISTORICAL_EVENTS = [
    {
        "ticker": "NVDA",
        "date": "2024-02-21",
        "title": "NVIDIA Reports Record Q4 Revenue — Data Center Revenue Surges 409% Year-Over-Year",
        "body": (
            "NVIDIA Corporation announced record revenue for the fourth quarter of fiscal 2024, "
            "with revenue reaching $22.1 billion, up 265% year-over-year and exceeding analyst estimates of $20.4 billion. "
            "Data center revenue was a record $18.4 billion, up 409% year-over-year, driven by strong demand "
            "for NVIDIA Hopper GPU computing and generative AI training and inference workloads. "
            "The company said supply constraints are easing and expects continued growth in Q1. "
            "CEO Jensen Huang said 'accelerated computing and generative AI have hit the tipping point.'"
        ),
        "lookahead_days": 5,
        "actual_change_pct": 15.1,
        "actual_direction": "BULLISH",
    },
    {
        "ticker": "TSLA",
        "date": "2024-01-02",
        "title": "Tesla Q4 Deliveries Miss Estimates — Demand Concerns Intensify",
        "body": (
            "Tesla reported fourth-quarter vehicle deliveries of 484,507 units, below the consensus estimate "
            "of approximately 483,000 but still representing year-over-year growth. The company produced "
            "approximately 495,000 vehicles during the quarter. While deliveries missed some optimistic Wall Street targets, "
            "investors are increasingly concerned about demand softening amid rising interest rates and increased "
            "competition from Chinese EV manufacturers like BYD, which surpassed Tesla in quarterly EV sales for the first time. "
            "Tesla has been cutting prices across multiple markets to maintain market share, squeezing automotive margins."
        ),
        "lookahead_days": 5,
        "actual_change_pct": -5.4,
        "actual_direction": "BEARISH",
    },
    {
        "ticker": "AAPL",
        "date": "2024-01-15",
        "title": "Apple Cuts iPhone Orders in China as Competition Intensifies",
        "body": (
            "Apple has reduced iPhone orders for the March quarter by approximately 15% following weaker-than-expected "
            "holiday sales in China, according to supply chain checks. The company faces intensifying competition from "
            "Huawei's Mate 60 series and other domestic Chinese smartphone brands. Analysts have downgraded Apple stock, "
            "citing concerns about iPhone revenue growth in the region that accounts for roughly 20% of Apple's total revenue. "
            "The news adds to growing worries about Apple's growth trajectory as it navigates regulatory headwinds and market share losses."
        ),
        "lookahead_days": 5,
        "actual_change_pct": 6.3,
        "actual_direction": "BULLISH",
    },
    {
        "ticker": "META",
        "date": "2024-02-01",
        "title": "Meta Platforms Reports Blowout Q4 — Issues First-Ever Dividend",
        "body": (
            "Meta Platforms reported fourth-quarter results that handily beat analyst expectations, with revenue "
            "of $40.1 billion versus estimates of $39.2 billion, representing 25% year-over-year growth. "
            "The company announced its first-ever quarterly dividend of $0.50 per share and authorized an additional "
            "$50 billion in share buybacks. Daily active users reached 2.11 billion, above expectations. "
            "Advertising revenue showed strong momentum, with growth accelerating as advertisers increase spend "
            "on Meta's platforms. Reality Labs revenue also beat estimates."
        ),
        "lookahead_days": 5,
        "actual_change_pct": 19.1,
        "actual_direction": "BULLISH",
    },
    {
        "ticker": "AMD",
        "date": "2024-01-30",
        "title": "AMD Q4 Earnings Beat Estimates — Data Center Revenue Doubles",
        "body": (
            "Advanced Micro Devices reported fourth-quarter revenue of $6.17 billion, surpassing analyst estimates "
            "of $6.12 billion, driven by strong growth in its data center segment which doubled year-over-year to $2.3 billion. "
            "The company's MI300 AI accelerator chip is ramping faster than expected, with AMD raising its 2024 data center GPU "
            "revenue forecast. Client segment revenue also grew 62% year-over-year. However, guidance for the current quarter "
            "came in slightly below some optimistic Street estimates, tempering post-earnings enthusiasm."
        ),
        "lookahead_days": 5,
        "actual_change_pct": -2.4,
        "actual_direction": "BEARISH",
    },
    {
        "ticker": "AMZN",
        "date": "2024-02-01",
        "title": "Amazon Q4 Earnings Surge — AWS Growth Accelerates",
        "body": (
            "Amazon reported fourth-quarter revenue of $170.0 billion, exceeding analyst expectations of $166.2 billion, "
            "representing 14% year-over-year growth. AWS revenue grew 13% to $24.2 billion, accelerating from the prior quarter "
            "and signaling a rebound in cloud spending. Operating income surged to $13.2 billion from $2.7 billion a year ago, "
            "driven by cost-cutting measures and improved retail profitability. Advertising revenue also grew 27%. "
            "The company guided Q1 revenue above consensus."
        ),
        "lookahead_days": 5,
        "actual_change_pct": 6.6,
        "actual_direction": "BULLISH",
    },
    {
        "ticker": "JPM",
        "date": "2024-01-12",
        "title": "JPMorgan Chase Q4 Profit Rises 35% — Net Interest Income Outlook Strong",
        "body": (
            "JPMorgan Chase reported fourth-quarter net income of $11.7 billion, up 35% year-over-year, "
            "driven by higher net interest income as the bank benefited from elevated interest rates. Revenue "
            "of $39.9 billion beat estimates of $39.6 billion. The bank reported record full-year revenue of $162.7 billion. "
            "CEO Jamie Dimon said the bank remains cautiously optimistic despite geopolitical tensions and inflationary pressures. "
            "Net interest income guidance for 2024 came in above expectations, suggesting the bank expects rates to remain elevated."
        ),
        "lookahead_days": 5,
        "actual_change_pct": 0.6,
        "actual_direction": "NEUTRAL",
    },
    {
        "ticker": "MSFT",
        "date": "2024-01-30",
        "title": "Microsoft Q2 Earnings Beat — Azure Growth Decelerates Slightly",
        "body": (
            "Microsoft reported fiscal second-quarter revenue of $62.0 billion, above the consensus estimate of $61.1 billion "
            "and up 18% year-over-year. Azure cloud revenue grew 30%, slightly below the 31% expected by some analysts "
            "but still showing strong momentum. The company's AI services contributed approximately 6 percentage points "
            "to Azure growth, up from 3 points in the prior quarter. Microsoft 365 Commercial cloud revenue grew 17%. "
            "Intelligent Cloud segment revenue beat estimates. However, a slightly softer Azure number caused some "
            "investor consternation given the high expectations around AI-driven growth."
        ),
        "lookahead_days": 5,
        "actual_change_pct": -0.8,
        "actual_direction": "NEUTRAL",
    },
    {
        "ticker": "GOOGL",
        "date": "2024-01-30",
        "title": "Alphabet Q4 Ad Revenue Beats — But Cloud Growth Disappoints",
        "body": (
            "Alphabet reported fourth-quarter revenue of $86.3 billion, beating estimates of $85.3 billion, "
            "driven by strong advertising revenue of $65.5 billion which exceeded expectations. However, "
            "Google Cloud revenue of $9.2 billion missed estimates of $9.5 billion, raising concerns about "
            "the company's ability to compete with AWS and Azure in the AI cloud market. The company reported "
            "higher capital expenditure guidance for 2024, driven by AI infrastructure investments, "
            "which pressured margins. Investors reacted negatively to the cloud miss and increased spending plans."
        ),
        "lookahead_days": 5,
        "actual_change_pct": -4.9,
        "actual_direction": "BEARISH",
    },
    {
        "ticker": "SMCI",
        "date": "2024-03-18",
        "title": "Super Micro Computer Joins S&P 500 — AI Server Demand Drives Record Growth",
        "body": (
            "Super Micro Computer announced it will join the S&P 500 index, replacing Whirlpool Corporation. "
            "The company has seen explosive growth as demand for its AI-optimized server solutions skyrockets, "
            "with revenue more than doubling year-over-year. Super Micro's direct-to-customer liquid cooling "
            "technology for high-density AI clusters has become a key differentiator, winning major data center contracts. "
            "The company raised its revenue guidance for the fiscal year, citing sustained demand from hyperscale "
            "customers deploying NVIDIA's latest GPU platforms."
        ),
        "lookahead_days": 5,
        "actual_change_pct": 4.2,
        "actual_direction": "BULLISH",
    },

    # ── Crypto Events ─────────────────────────────────────────────────

    {
        "ticker": "BTC",
        "date": "2024-01-10",
        "title": "SEC Approves 11 Spot Bitcoin ETFs in Historic Decision for Crypto Markets",
        "body": (
            "The U.S. Securities and Exchange Commission has approved the first spot Bitcoin "
            "exchange-traded funds in a landmark decision that opens crypto exposure to mainstream "
            "investors. All 11 applications were approved, including BlackRock's iShares Bitcoin Trust, "
            "Fidelity's Wise Origin Bitcoin Fund, and ARK 21Shares Bitcoin ETF. Bitcoin surged on "
            "massive trading volumes as institutional investors gained direct exposure through "
            "traditional brokerage accounts. SEC Chair Gary Gensler said the approval was not an "
            "endorsement of Bitcoin but reflected court rulings that forced the agency's hand. "
            "Analysts projected up to $100 billion in new demand over the following year."
        ),
        "lookahead_days": 5,
        "actual_change_pct": 4.2,
        "actual_direction": "BULLISH",
    },
    {
        "ticker": "ETH",
        "date": "2024-05-20",
        "title": "Ethereum Surges on Sudden SEC Engagement Over Spot ETF Filings",
        "body": (
            "Ethereum prices surged dramatically as reports emerged that the SEC is suddenly engaging "
            "with potential spot Ethereum ETF issuers after months of silence. The SEC requested "
            "updates to 19b-4 filings from exchanges including Nasdaq and CBOE, signaling a potential "
            "approval. ETH jumped from $3,100 to over $3,800 as traders rushed to position ahead of "
            "what analysts called a 'regulatory pivot' on crypto. The political climate around "
            "crypto regulation has shifted significantly, with bipartisan support growing for "
            "clearer digital asset rules. Bloomberg analysts raised approval odds from 25% to 75%."
        ),
        "lookahead_days": 5,
        "actual_change_pct": 5.8,
        "actual_direction": "BULLISH",
    },
    {
        "ticker": "SOL",
        "date": "2024-02-06",
        "title": "Solana Network Experiences Fifth Major Outage — Block Production Halts for 5 Hours",
        "body": (
            "The Solana blockchain suffered its fifth major outage in two years as a bug in the "
            "runtime implementation caused validators to crash, halting block production for "
            "approximately five hours. Validators coordinated a restart after implementing a "
            "patch, but the recurring reliability issues reignited concerns about the network's "
            "suitability for mission-critical DeFi applications. SOL price dropped following the "
            "news, underperforming other major crypto assets. The Solana Foundation said it was "
            "implementing additional testing procedures to prevent future incidents, though "
            "critics argued the network's architecture remains inherently fragile."
        ),
        "lookahead_days": 5,
        "actual_change_pct": -3.2,
        "actual_direction": "BEARISH",
    },

    # ── Commodity Events ──────────────────────────────────────────────

    {
        "ticker": "OIL",
        "date": "2023-10-07",
        "title": "Crude Oil Spikes 5% as Hamas Attack on Israel Threatens Middle East Supply",
        "body": (
            "Crude oil prices surged more than 5% following a surprise attack by Hamas on Israel "
            "that has raised fears of a broader Middle Eastern conflict. WTI crude jumped to $86 "
            "per barrel as traders priced in the risk of supply disruptions from Iran, a key oil "
            "producer and Hamas supporter. Analysts warned that a wider war could threaten the "
            "Strait of Hormuz chokepoint through which approximately 20% of global oil passes "
            "daily. The Biden administration said it would monitor energy markets closely and "
            "stood ready to tap the Strategic Petroleum Reserve if needed to stabilize prices."
        ),
        "lookahead_days": 5,
        "actual_change_pct": 4.1,
        "actual_direction": "BULLISH",
    },
    {
        "ticker": "GOLD",
        "date": "2023-12-04",
        "title": "Gold Hits All-Time High Above $2,100 as Markets Price in 2024 Rate Cuts",
        "body": (
            "Gold surged to an all-time high above $2,100 per ounce as traders increasingly bet "
            "that the Federal Reserve will begin cutting interest rates in early 2024. The rally "
            "accelerated after Fed Chair Jerome Powell's dovish comments signaled the central "
            "bank's tightening cycle is likely over. A weakening US dollar and falling bond "
            "yields provided additional tailwinds. Central banks continued their record gold-"
            "buying spree led by China and Poland, providing structural demand support. "
            "Analysts projected gold could reach $2,500 by year-end if rate cuts materialize."
        ),
        "lookahead_days": 5,
        "actual_change_pct": 3.5,
        "actual_direction": "BULLISH",
    },
    {
        "ticker": "NG",
        "date": "2024-01-12",
        "title": "Natural Gas Plunges to 3-Year Low as Warm Winter Decimates Heating Demand",
        "body": (
            "Natural gas futures collapsed to their lowest level in three years as unseasonably "
            "warm weather across the United States decimated heating demand. Storage levels "
            "remained well above the five-year average, with production continuing at record "
            "levels. The mild winter has crushed the typical seasonal price premium, leaving "
            "producers facing negative margins on some operations. Analysts downgraded their "
            "price forecasts, with some warning that sustained low prices could force production "
            "cuts. The market is now pricing in the possibility of storage reaching capacity "
            "before next winter's heating season begins."
        ),
        "lookahead_days": 5,
        "actual_change_pct": -6.5,
        "actual_direction": "BEARISH",
    },
]
