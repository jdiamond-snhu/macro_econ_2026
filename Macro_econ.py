import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set up page configurations
st.set_page_config(page_title="Global Inflation Analytics", layout="wide")

st.title("🌐 Global Inflation Simulator & Macro Era Tracker")
st.markdown("Analyze how purchasing power decays under distinct economic regimes and historical eras.")

# STEP 1: Multi-Era Macroeconomic Database 
COUNTRY_DATA = {
    "United States": {
        "flag": "🇺🇸",
        "target": 2.0, "accepted_avg": 2.5, "pandemic": 4.3, "volcker": 6.8,
        "notes": "Reagan-Volcker era CPI peaked near 14.5% before aggressive rate hikes crushed it."
    },
    "Eurozone": {
        "flag": "🇪🇺",
        "target": 2.0, "accepted_avg": 2.0, "pandemic": 4.9, "volcker": None,
        "notes": "Modern Eurozone did not exist in 1979; Pandemic saw unprecedented energy shocks."
    },
    "Canada": {
        "flag": "🇨🇦",
        "target": 2.0, "accepted_avg": 2.4, "pandemic": 3.9, "volcker": 6.9,
        "notes": "Canada closely tracked US monetary tightening cycles across both eras."
    },
    "Japan": {
        "flag": "🇯🇵",
        "target": 2.0, "accepted_avg": 0.5, "pandemic": 2.3, "volcker": 3.1,
        "notes": "Japan broke out of its multi-decade stagnation era during the pandemic cycle."
    },
    "India": {
        "flag": "🇮🇳",
        "target": 4.0, "accepted_avg": 5.5, "pandemic": 5.1, "volcker": 8.5,
        "notes": "India managed structural supply logistics to curb runaway post-pandemic prices."
    },
    "Egypt": {
        "flag": "🇪🇬",
        "target": 5.0, "accepted_avg": 11.2, "pandemic": 19.5, "volcker": None,
        "notes": "Pandemic era figures driven by aggressive structural currency floats."
    },
    "Argentina": {
        "flag": "🇦🇷",
        "target": 20.0, "accepted_avg": 65.0, "pandemic": 115.0, "volcker": 140.0,
        "notes": "Experienced hyper-inflationary spikes across both the 1980s and early 2020s."
    }
}

# STEP 2: Sidebar Navigation & Macro Era Selection (Defines rate_key FIRST)
st.sidebar.header("Economic Era Profiles")
selected_era = st.sidebar.radio(
    "Choose a Regime View:",
    options=[
        "Official Central Bank Target", 
        "Standard Financial Planning Baseline (2.5%)", 
        "💥 Pandemic Era Shock (2020–2026)", 
        "🦅 Reagan-Volcker Regime (1979–1987)"
    ]
)

# Map human-readable labels to our python keys
era_mapping = {
    "Official Central Bank Target": "target",
    "Standard Financial Planning Baseline (2.5%)": "accepted_avg",
    "💥 Pandemic Era Shock (2020–2026)": "pandemic",
    "🦅 Reagan-Volcker Regime (1979–1987)": "volcker"
}
rate_key = era_mapping[selected_era]

# Standard inputs
st.sidebar.markdown("---")
st.sidebar.header("Simulation Settings")
principal = st.sidebar.number_input("Starting Cash ($)", min_value=1.0, value=1000.0, step=100.0)

# DYNAMIC CONFIGURATION MATRIX: Snap fields tightly during the Volcker era
if selected_era == "🦅 Reagan-Volcker Regime (1979–1987)":
    default_years = 9
    slider_disabled = True
    default_selection = ["United States"]
    multiselect_disabled = True
else:
    default_years = 15
    slider_disabled = False
    default_selection = []  
    multiselect_disabled = False

years = st.sidebar.slider(
    "Timeline (Years)", 
    min_value=1, 
    max_value=30, 
    value=default_years,
    disabled=slider_disabled,
    help="Timeline is locked to exactly 9 years (1979–1987) during the Reagan-Volcker era."
)

selected_countries = st.sidebar.multiselect(
    "Compare Regions:",
    options=list(COUNTRY_DATA.keys()),
    default=default_selection,
    disabled=multiselect_disabled,
    help="Select one or more countries to plot. This field is locked to the U.S. during the Reagan-Volcker era."
)

# STEP 3: Federal Funds Rate Yield Optimizer Input Block
st.markdown("---")
st.header("🦅 Federal Funds Rate Yield Optimizer")
st.markdown("Calculate how earning an interest rate tied to the central bank counteracts inflation decay.")

# Lock/Adjust target numeric widget default if Volcker era is active
default_fed_input = 11.20 if selected_era == "🦅 Reagan-Volcker Regime (1979–1987)" else 3.63

fed_rate = st.number_input(
    "Effective Federal Funds Rate (%)", 
    min_value=0.0, 
    max_value=25.0, 
    value=default_fed_input, 
    step=0.25,
    disabled=slider_disabled, # Lock manual entry during Volcker tracking to prioritize historical curve
    help="The baseline interest rate set by the central bank."
)

# STEP 4: Calculations & Modeling Logic
us_inflation = COUNTRY_DATA["United States"][rate_key]
real_interest_rate = fed_rate - us_inflation

# Compute compounded forward outcomes over the user's selected timeframe
cash_only = principal / ((1 + (us_inflation / 100)) ** years)
nominal_savings_growth = principal * ((1 + (fed_rate / 100)) ** years)
true_purchasing_power_yield = nominal_savings_growth / ((1 + (us_inflation / 100)) ** years)

# Render Visual KPI Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="U.S. Inflation Rate Context", value=f"{us_inflation}%")
with col2:
    st.metric(
        label="Net Real Interest Rate (Fisher Matrix)", 
        value=f"{real_interest_rate:.2f}%",
        delta="Positive Yield" if real_interest_rate >= 0 else "Negative Purchasing Drag",
        delta_color="normal" if real_interest_rate >= 0 else "inverse"
    )
with col3:
    st.metric(
        label="Final True Purchasing Power", 
        value=f"${true_purchasing_power_yield:,.2f}",
        delta=f"${true_purchasing_power_yield - cash_only:,.2f} Saved vs Pure Cash"
    )

st.info(
    f"💡 **Analysis Footnote:** If you leave ${principal:,.2f} in a vault without yield, inflation reduces its value "
    f"to **${cash_only:,.2f}** in {years} years. However, by harvesting a **{fed_rate}%** Fed-linked nominal interest rate, "
    f"your true adjusted purchasing power over time preserves to **${true_purchasing_power_yield:,.2f}**."
)

# STEP 5: Render Interactive Chart Interface with Dual-Axes Configuration
if selected_countries:
    time_steps = list(range(0, years + 1))
    df_plot = pd.DataFrame({"Year": time_steps})
    summary_data = []
    active_countries_to_graph = []
    
    for country in selected_countries:
        rate = COUNTRY_DATA[country][rate_key]
        if rate is None:
            continue
            
        active_countries_to_graph.append(country)
        purchasing_power = [principal / ((1 + (rate / 100)) ** t) for t in time_steps]
        df_plot[country] = purchasing_power
        
        final_val = purchasing_power[-1]
        loss_pct = ((principal - final_val) / principal) * 100
        
        summary_data.append({
            "Region / Nation": f"{COUNTRY_DATA[country]['flag']} {country}",
            "Era Average Inflation": f"{rate}%",
            "Projected Value": f"${final_val:,.2f}",
            "Wealth Destroyed": f"{loss_pct:.1f}%",
            "Historical Context / Footnote": COUNTRY_DATA[country]["notes"]
        })

    if active_countries_to_graph:
        fig = go.Figure()
        
        # --- THE HOOK: Generate Raw Rate Trend Values ---
        if selected_era == "🦅 Reagan-Volcker Regime (1979–1987)":
            # Map actual historical path across the 9 years (1979=11.2%, 1980=13.4%, 1981=19.1%, down to 1987=6.0%)
            fed_rate_path = [11.20, 13.35, 19.10, 12.26, 9.09, 10.23, 8.10, 6.83, 6.43, 6.05]
            # Clip array length safely to exactly match our time step slice array
            fed_rate_path = fed_rate_path[:len(time_steps)]
            legend_label = "🦅 Historical Fed Funds Path"
        else:
            # Standard flat line if using policy benchmarks
            fed_rate_path = [fed_rate] * len(time_steps)
            legend_label = f"🦅 Selected Fed Benchmark ({fed_rate}%)"

        # Add the Thin Solid Green Rate Line mapped precisely to the Secondary Right Axis
        fig.add_trace(go.Scatter(
            x=time_steps,
            y=fed_rate_path,
            mode='lines',
            name=legend_label,
            line=dict(color='#2ecc71', width=2.0), # Thin solid green trace
            yaxis="y2", # Map explicitly to the secondary y-axis coordinate frame
            hovertemplate="<b>%{text}</b><br>Year %{x}: %{y:.2f}%<extra></extra>",
            text=[legend_label] * len(time_steps)
        ))

        # Add the standard country currency breakdown line charts to the Primary Left Axis
        for country in active_countries_to_graph:
            current_rate = COUNTRY_DATA[country][rate_key]
            fig.add_trace(go.Scatter(
                x=df_plot["Year"], 
                y=df_plot[country], 
                mode='lines+markers', 
                name=f"{COUNTRY_DATA[country]['flag']} {country} ({current_rate}%)",
                yaxis="y" # Maps strictly onto Left Axis scale
            ))
            
        # Configure layout properties to manage dual-axis rendering engine layers cleanly
        fig.update_layout(
            title=f"Macro Wave: Currency Value vs. Raw Fed Interest Rate Movement",
            xaxis_title="Years Elapsed",
            
            # Left Axis Parameters
            yaxis=dict(
                title="Purchasing Power Value ($)",
                titlefont=dict(color="#1f77b4"),
                tickfont=dict(color="#1f77b4"),
                template="plotly_white"
            ),
            # Right Axis Parameters
            yaxis2=dict(
                title="Raw Federal Funds Interest Rate (%)",
                titlefont=dict(color="#2ecc71"),
                tickfont=dict(color="#2ecc71"),
                anchor="x",
                overlaying="y", # Overlay on top of primary graph footprint space safely
                side="right", # Pin neatly onto right side panel area
                range=[0, 22] # Give ample ceiling room for the 19.1% peak limits
            ),
            hovermode="x unified",
            template="plotly_white"

