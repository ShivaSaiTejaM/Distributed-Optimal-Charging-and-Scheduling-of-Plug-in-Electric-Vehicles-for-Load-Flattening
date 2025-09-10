import streamlit as st
import pandas as pd
import numpy as np
import time
from io import BytesIO

# Set page config
st.set_page_config(page_title="PEV Charging Optimizer", page_icon="⚡", layout="wide")

# Custom CSS for animations
st.markdown("""
<style>
    @keyframes charging {
        0% { background-color: #e6ffe6; }
        50% { background-color: #4CAF50; }
        100% { background-color: #e6ffe6; }
    }
    @keyframes discharging {
        0% { background-color: #ffe6e6; }
        50% { background-color: #FF5733; }
        100% { background-color: #ffe6e6; }
    }
    .charging-animation {
        animation: charging 2s infinite;
        padding: 15px;
        border-radius: 10px;
    }
    .discharging-animation {
        animation: discharging 2s infinite;
        padding: 15px;
        border-radius: 10px;
    }
    .metric-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .stDataFrame {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.title("Control Panel ⚙️")
    st.markdown("---")
    
    # File upload
    uploaded_file = st.file_uploader("Upload Vehicle Data (Excel)", type=["xlsx"])
    
    # Parameters
    time_val = st.slider("Current Time (in 15-minutes slot)", 0, 95, 54, 1)
    energy_diff = st.slider("power Difference (kWh)", -3000, 3000, -300, 10)
    
    st.markdown("---")
    if st.button("Run Optimization"):
        st.session_state.run = True
    else:
        st.session_state.run = False

# Main content
st.title("⚡ PEV Charging/Discharging Optimization System")
st.markdown("---")

if uploaded_file and st.session_state.get('run', False):
    try:
        df = pd.read_excel(uploaded_file)
        
        # Process data
        newdf = df[(df["Plug_in_Time"] < time_val) & (df["Estimated_plug_out_Time"] > time_val)].copy()
        
        # Calculate score
        newdf["SCORE_OUT_OF_100"] = (
            (0.3 * newdf["Battry_Capacity_kWh"] +
             0.4 * (1 - newdf["Present_SOC"]) +
             0.3 * (95 - (newdf["Estimated_plug_out_Time"] - time_val))
            ) * 100 / 54.07
        )

        if energy_diff > 0:
            # Charging mode
            with st.container():
                st.markdown('<div class="charging-animation">', unsafe_allow_html=True)
                st.success("## 🔌 CHARGING MODE ACTIVATED")
                st.markdown('</div>', unsafe_allow_html=True)
            
            newdf.sort_values(by=["SCORE_OUT_OF_100"], ascending=[False], inplace=True)
            
            # Vectorized charging rate calculation
            conditions = [
                (newdf["Present_SOC"] < 0.3),
                (newdf["Present_SOC"] < 0.7),
                (newdf["Present_SOC"] <= 1)
            ]
            choices = [
                0.5 * newdf["Battry_Capacity_kWh"],
                1.1 * newdf["Battry_Capacity_kWh"],
                0.5 * newdf["Battry_Capacity_kWh"]
            ]
            newdf["vehicle_charging_rate"] = np.select(conditions, choices, default=0)
            newdf["cumulative_charging"] = newdf["vehicle_charging_rate"].cumsum()
            
            # Filter vehicles
            if not newdf.empty:
                mask = newdf["cumulative_charging"] <= energy_diff
                if mask.any():
                    newdf = newdf.loc[mask]
                else:
                    newdf = newdf.iloc[:0]
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🚗 Vehicles Charging", len(newdf))
            with col2:
                st.metric("⚡ Total Charging Rate", f"{newdf['vehicle_charging_rate'].sum():.2f} kWh")
            with col3:
                st.metric("🔋 Capacity Utilized", f"{newdf['cumulative_charging'].max() if not newdf.empty else 0:.2f} kWh")
            
        else:
            # Discharging mode
            with st.container():
                st.markdown('<div class="discharging-animation">', unsafe_allow_html=True)
                st.error("## 🔋 DISCHARGING MODE ACTIVATED")
                st.markdown('</div>', unsafe_allow_html=True)
            
            newdf.sort_values(by=["SCORE_OUT_OF_100"], ascending=[True], inplace=True)
            
            # Vectorized discharging rate calculation
            conditions = [
                (newdf["Present_SOC"] < 0.3),
                (newdf["Present_SOC"] < 0.7),
                (newdf["Present_SOC"] <= 1)
            ]
            choices = [
                0.1 * newdf["Battry_Capacity_kWh"],
                0.2 * newdf["Battry_Capacity_kWh"],
                0.5 * newdf["Battry_Capacity_kWh"]
            ]
            newdf["vehicle_discharging_rate"] = np.select(conditions, choices, default=0)
            newdf["cumulative_discharging"] = newdf["vehicle_discharging_rate"].cumsum()
            
            # Filter vehicles
            if not newdf.empty:
                abs_diff = abs(energy_diff)
                mask = newdf["cumulative_discharging"] <= abs_diff
                if mask.any():
                    newdf = newdf.loc[mask]
                else:
                    newdf = newdf.iloc[:0]
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🚗 Vehicles Discharging", len(newdf))
            with col2:
                st.metric("⚡ Total Discharging Rate", f"{newdf['vehicle_discharging_rate'].sum():.2f} kWh")
            with col3:
                st.metric("🔌 Power Supplied", f"{newdf['cumulative_discharging'].max() if not newdf.empty else 0:.2f} kWh")
        
        # Display results
        st.markdown("---")
        st.subheader("Optimized Vehicle Schedule")
        
        if not newdf.empty:
            # Format the dataframe display
            formatted_df = newdf.copy()
            formatted_df["Present_SOC"] = formatted_df["Present_SOC"].apply(lambda x: f"{x:.0%}")
            
            # Show dataframe with custom formatting
            st.dataframe(
                formatted_df.style
                .background_gradient(subset=["SCORE_OUT_OF_100"], cmap="YlGnBu")
                .format({
                    "Battry_Capacity_kWh": "{:.1f}",
                    "SCORE_OUT_OF_100": "{:.1f}",
                    "vehicle_charging_rate": "{:.2f}",
                    "vehicle_discharging_rate": "{:.2f}",
                    "cumulative_charging": "{:.2f}",
                    "cumulative_discharging": "{:.2f}"
                }),
                height=600,
                use_container_width=True
            )
            
            # Download button
            csv = newdf.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="pev_optimization_results.csv",
                mime="text/csv"
            )
        else:
            st.warning("No vehicles available for the current parameters")
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    st.info("ℹ️ Please upload an Excel file and configure parameters in the sidebar")

# Add explanation section
with st.expander("ℹ️ How This System Works"):
    st.markdown("""
    **Optimization Logic:**
    - Vehicles are selected based on current time window
    - Priority score calculated using:
      - 30% Battery Capacity
      - 40% State of Charge (SOC)
      - 30% Remaining Plugged-in Time
    
    **Charging Mode:**
    - Prioritizes vehicles with lower SOC and more remaining time
    - Charging rates:
      - <30% SOC: 0.5C rate
      - 30-70% SOC: 1.1C rate
      - >70% SOC: 0.5C rate
    
    **Discharging Mode:**
    - Prioritizes vehicles with higher SOC and less remaining time
    - Discharging rates:
      - <30% SOC: 0.1C rate
      - 30-70% SOC: 0.2C rate
      - >70% SOC: 0.5C rate
    """)