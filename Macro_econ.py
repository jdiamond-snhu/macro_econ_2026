st.markdown("---")
st.header("🦅 Federal Funds Rate Yield Optimizer")
st.markdown("Calculate how earning an interest rate tied to the central bank counteracts inflation decay.")

# 1. Real-time Fed Rate Parameter Input
fed_rate = st.number_input(
    "Current Effective Federal Funds Rate (%)", 
    min_value=0.0, 
    max_value=20.0, 
    value=3.63, # Current mid-2026 effective rate baseline
    step=0.25,
    help="The sticker interest rate banks use, which influences high-yield savings and T-Bills."
)

# Use the United States data contextually from our existing selected simulation configuration
us_inflation = COUNTRY_DATA["United States"][rate_key]

# 2. Mathematical Modeling equations
real_interest_rate = fed_rate - us_inflation

# Compute compounded forward outcomes over the user's selected timeframe
cash_only = principal / ((1 + (us_inflation / 100)) ** years)
yield_protected_cash = principal * ((1 + (real_interest_rate / 100)) ** years)
nominal_savings_growth = principal * ((1 + (fed_rate / 100)) ** years)
true_purchasing_power_yield = nominal_savings_growth / ((1 + (us_inflation / 100)) ** years)

# 3. Render Visual KPI Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="U.S. Inflation Rate Context", 
        value=f"{us_inflation}%"
    )
with col2:
    st.metric(
        label="Net Real Interest Rate (Fisher Matrix)", 
        value=f"{real_interest_rate:.2f}%",
        delta=f"Positive Yield" if real_interest_rate >= 0 else "Negative Purchasing Drag",
        delta_color="normal" if real_interest_rate >= 0 else "inverse"
    )
with col3:
    st.metric(
        label="Final True Purchasing Power", 
        value=f"${true_purchasing_power_yield:,.2f}",
        delta=f"${true_purchasing_power_yield - cash_only:,.2f} Saved vs Pure Cash"
    )

# 4. Explanatory Context Data block
st.info(
    f"💡 **Analysis Footnote:** If you leave ${principal:,.2f} in a vault without yield, inflation reduces its value "
    f"to **${cash_only:,.2f}** in {years} years. However, by harvesting a **{fed_rate}%** Fed-linked nominal interest rate, "
    f"your true adjusted purchasing power over time preserves to **${true_purchasing_power_yield:,.2f}**."
)
