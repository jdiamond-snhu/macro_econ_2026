import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set up page configurations
st.set_page_config(page_title="Global Inflation Analytics", layout="wide")

st.title("🌐 Global Inflation Simulator & Macro Era Tracker")
st.markdown("Analyze how purchasing power decays under distinct economic regimes and historical eras.")

# 1. Multi-Era Macroeconomic Database 
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

# 2. Sidebar Navigation & Macro Era Selection Buttons
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
years = st.sidebar.slider("Timeline (Years)", min_value=1, max_value=30, value=15)

selected_countries = st.sidebar.multiselect(
    "Compare Regions:",
    options=list(COUNTRY_DATA.keys()),
    default=["United States", "Canada", "Japan"]
)

# 3. Calculation & Modeling Logic
if selected_countries:
    time_steps = list(range(0, years + 1))
    df_plot = pd.DataFrame({"Year": time_steps})
    summary_data = []
    active_countries_to_graph = []
    
    for country in selected_countries:
        rate = COUNTRY_DATA[country][rate_key]
        
        # Guard clause if data is unavailable for that specific historical era
        if rate is None:
            continue
            
        active_countries_to_graph.append(country)
        
        # Exponential compounding decay curve math
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

    # 4. Render Interactive Chart Interface
    if active_countries_to_graph:
        fig = go.Figure()
        for country in active_countries_to_graph:
            current_rate = COUNTRY_DATA[country][rate_key]
            fig.add_trace(go.Scatter(
                x=df_plot["Year"], 
                y=df_plot[country], 
                mode='lines+markers', 
                name=f"{COUNTRY_DATA[country]['flag']} {country} ({current_rate}%)"
            ))
            
        fig.update_layout(
            title=f"Decay of ${principal:,.2f} over {years} Years under the {selected_era}",
            xaxis_title="Years Compounded Forward",
            yaxis_title="Real Purchasing Power / Value ($)",
            hovermode="x unified",
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 5. Display KPI Summary Table
        st.subheader(f"📊 Summary Analysis: {selected_era}")
        st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
    else:
        st.error("No historical data available for the selected regions during this precise macroeconomic era.")

else:
    st.warning("Please select at least one region from the sidebar menu to start mapping the graph.")
