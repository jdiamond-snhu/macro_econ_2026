import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set up page configurations
st.set_page_config(page_title="Global Inflation Simulator", layout="wide")

st.title("🌐 Global Inflation Simulator")
st.markdown("Simulate how standard accepted inflation rates impact purchasing power over time.")

# 1. Database of standard accepted / target baseline inflation rates
COUNTRY_DATA = {
    "United States": {"rate": 2.0, "flag": "🇺🇸", "desc": "Federal Reserve Long-term Target"},
    "Eurozone": {"rate": 2.0, "flag": "🇪🇺", "desc": "European Central Bank Medium-term Target"},
    "Canada": {"rate": 2.0, "flag": "🇨🇦", "desc": "Bank of Canada Target Midpoint"},
    "Japan": {"rate": 2.0, "flag": "🇯🇵", "desc": "Bank of Japan Price Stability Target"},
    "India": {"rate": 4.0, "flag": "🇮🇳", "desc": "Reserve Bank of India Target"},
    "Egypt": {"rate": 5.0, "flag": "🇪🇬", "desc": "Central Bank of Egypt Target Baseline"},
    "Argentina": {"rate": 30.0, "flag": "🇦🇷", "desc": "Projected Stabilization Trend Baseline"}
}

# 2. Sidebar Inputs
st.sidebar.header("Simulation Parameters")
principal = st.sidebar.number_input("Initial Amount (Cash Value)", min_value=1.0, value=1000.0, step=100.0)
years = st.sidebar.slider("Simulation Horizon (Years)", min_value=1, max_value=30, value=10)

selected_countries = st.sidebar.multiselect(
    "Select Countries to Compare",
    options=list(COUNTRY_DATA.keys()),
    default=["United States", "India", "Argentina"]
)

# 3. Calculation & Core App Logic
if selected_countries:
    # Generate data structure for calculations
    time_steps = list(range(0, years + 1))
    df_plot = pd.DataFrame({"Year": time_steps})
    
    summary_data = []
    
    for country in selected_countries:
        rate = COUNTRY_DATA[country]["rate"]
        # Purchasing power decay formula: Principal / (1 + r)^t
        purchasing_power = [principal / ((1 + (rate / 100)) ** t) for t in time_steps]
        df_plot[country] = purchasing_power
        
        final_val = purchasing_power[-1]
        loss_pct = ((principal - final_val) / principal) * 100
        summary_data.append({
            "Country": f"{COUNTRY_DATA[country]['flag']} {country}",
            "Accepted Target Rate": f"{rate}%",
            "Final Purchasing Power": f"${final_val:,.2f}",
            "Value Lost": f"{loss_pct:.1f}%"
        })

    # 4. Display Interactive Visualization
    fig = go.Figure()
    for country in selected_countries:
        fig.add_trace(go.Scatter(
            x=df_plot["Year"], 
            y=df_plot[country], 
            mode='lines+markers', 
            name=f"{COUNTRY_DATA[country]['flag']} {country} ({COUNTRY_DATA[country]['rate']}%)"
        ))
        
    fig.update_layout(
        title=f"Decay of ${principal:,.2f} Purchasing Power Over Time",
        xaxis_title="Years into the Future",
        yaxis_title="Real Value / Purchasing Power ($)",
        hovermode="x unified",
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 5. Display KPI Summary Data Table
    st.subheader("📊 Simulation Breakdown Summary")
    st.table(pd.DataFrame(summary_data))

else:
    st.warning("Please select at least one country from the sidebar to visualize.")
