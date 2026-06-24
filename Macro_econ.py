import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set up page configurations
st.set_page_config(page_title="Global Inflation Analytics", layout="wide")

st.title("🌐 Global Inflation Simulator & Historical Tracker")
st.markdown("Compare ideal Central Bank baseline targets against actual real-world historical averages.")

# 1. Expanded Database containing baseline metrics and 5-year historical average data blocks
COUNTRY_DATA = {
    "United States": {
        "target": 2.0, "historical_avg": 4.1, "flag": "🇺🇸", 
        "desc": "Fed Target: 2.0% | Recent Hist. Avg (incl. supply shock wave): ~4.1%"
    },
    "Eurozone": {
        "target": 2.0, "historical_avg": 4.9, "flag": "🇪🇺", 
        "desc": "ECB Target: 2.0% | Recent Hist. Avg (incl. energy price shock): ~4.9%"
    },
    "Canada": {
        "target": 2.0, "historical_avg": 3.9, "flag": "🇨🇦", 
        "desc": "BoC Target: 2.0% | Recent Hist. Avg: ~3.9%"
    },
    "Japan": {
        "target": 2.0, "historical_avg": 2.3, "flag": "🇯🇵", 
        "desc": "BoJ Target: 2.0% | Historical Avg (exit from deflation): ~2.3%"
    },
    "India": {
        "target": 4.0, "historical_avg": 5.1, "flag": "🇮🇳", 
        "desc": "RBI Target: 4.0% | Historical Avg: ~5.1%"
    },
    "Egypt": {
        "target": 5.0, "historical_avg": 19.5, "flag": "🇪🇬", 
        "desc": "CBE Target Baseline: 5.0% | Hist. Average Block (currency float adjustments): ~19.5%"
    },
    "Argentina": {
        "target": 20.0, "historical_avg": 115.0, "flag": "🇦🇷", 
        "desc": "Projected Stabilization Trend: ~20.0% | Hist. Average Block (hyperinflation peak eras): ~115.0%"
    }
}

# 2. Sidebar Inputs & Mode Selection Toggle
st.sidebar.header("Simulation Settings")
sim_mode = st.sidebar.radio(
    "Select Inflation Data Mode",
    options=["Central Bank Targets / Baseline", "Real-World Historical Averages"],
    help="Switch between official long-term targets and actual recent 5-year averages."
)

principal = st.sidebar.number_input("Initial Cash Value ($)", min_value=1.0, value=1000.0, step=100.0)
years = st.sidebar.slider("Simulation Horizon (Years)", min_value=1, max_value=30, value=10)

selected_countries = st.sidebar.multiselect(
    "Select Countries to Compare",
    options=list(COUNTRY_DATA.keys()),
    default=["United States", "Egypt", "Argentina"]
)

# Determine key based on toggle selection
rate_key = "target" if sim_mode == "Central Bank Targets / Baseline" else "historical_avg"

# 3. Calculation & Core App Logic
if selected_countries:
    time_steps = list(range(0, years + 1))
    df_plot = pd.DataFrame({"Year": time_steps})
    summary_data = []
    
    for country in selected_countries:
        rate = COUNTRY_DATA[country][rate_key]
        
        # Purchasing power decay formula: Principal / (1 + r)^t
        purchasing_power = [principal / ((1 + (rate / 100)) ** t) for t in time_steps]
        df_plot[country] = purchasing_power
        
        final_val = purchasing_power[-1]
        loss_pct = ((principal - final_val) / principal) * 100
        
        summary_data.append({
            "Country": f"{COUNTRY_DATA[country]['flag']} {country}",
            "Selected Mode Rate": f"{rate}%",
            "Final Purchasing Power": f"${final_val:,.2f}",
            "Total Value Destroyed": f"{loss_pct:.1f}%",
            "Context Info": COUNTRY_DATA[country]["desc"]
        })

    # 4. Display Interactive Chart
    fig = go.Figure()
    for country in selected_countries:
        current_rate = COUNTRY_DATA[country][rate_key]
        fig.add_trace(go.Scatter(
            x=df_plot["Year"], 
            y=df_plot[country], 
            mode='lines+markers', 
            name=f"{COUNTRY_DATA[country]['flag']} {country} ({current_rate}%)"
        ))
        
    fig.update_layout(
        title=f"Decay of ${principal:,.2f} Cash Value via {sim_mode}",
        xaxis_title="Years into the Future",
        yaxis_title="Real Value / Purchasing Power ($)",
        hovermode="x unified",
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 5. Display KPI Summary Data Table
    st.subheader("📊 Analytical Simulation Breakdown")
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True)

else:
    st.warning("Please select at least one country from the sidebar to visualize.")
