import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Set page config
st.set_page_config(page_title="Duck Curve Optimization", layout="wide", page_icon="🦆")

# Custom formatter for y-axis
def thousands(x, pos):
    return '%1.0fK' % (x*1e-3)

formatter = FuncFormatter(thousands)

# Common data
D = np.array([10,9,8,7,6,6,7,8,9,10,5,4,3,3,4,5,8,12,15,18,16,14,12,11]) * 1000
hours = np.arange(24)

# Sidebar controls
st.sidebar.title("Configuration")
method = st.sidebar.radio("Select Optimization Method:", 
                          ["Gradient Ascent", "ISGM Constant Step", "ISGM Decreasing Step"])

if method == "Gradient Ascent":
    sigma_options = [50, 75, 100, 150, 200, 300]
    default_sigma = [50, 100, 200]
    alpha = 0.5
    max_iter = 200
    y_offset = 4500
elif method == "ISGM Constant Step":
    sigma_options = [0.25, 0.5, 1, 1.5, 2, 3, 5, 10]
    default_sigma = [0.5, 1, 2]
    alpha = 0.5
    max_iter = 2000
    y_offset = 3500
else:  # ISGM Decreasing Step
    sigma_options = [0.005, 0.5, 1, 1.5, 2, 3, 50, 1000]
    default_sigma = [0.5, 1, 2]
    max_iter = 100000
    y_offset = 3500

selected_sigmas = st.sidebar.multiselect("Select Sigma Values:", 
                                       sigma_options, 
                                       default=default_sigma)

# Main content
st.title("🦆 Duck Curve Optimization Visualizer")
st.markdown("""
This application demonstrates different optimization methods for flattening the duck curve:
- **Gradient Ascent**: Traditional gradient ascent with fixed step size
- **ISGM Constant Step**: Incremental Stochastic Gradient Method with constant step size
- **ISGM Decreasing Step**: ISGM with dynamically decreasing step size
""")

# Optimization functions
def gradient_ascent(sigma_values):
    optimized_loads = {}
    N = 200
    alpha = 0.5
    tolerance = 0.001
    
    for sigma in sigma_values:
        lambda_t = np.zeros_like(D, dtype=float)
        
        for k in range(max_iter):
            u_total = -N * lambda_t / (2 * sigma)
            optimized_load = D + u_total
            gradient = -lambda_t/2 + D + u_total
            new_lambda = lambda_t + alpha * gradient
            
            if np.linalg.norm(new_lambda - lambda_t) < tolerance:
                break
            lambda_t = new_lambda
        
        optimized_loads[sigma] = optimized_load + y_offset
    
    return optimized_loads

def isgm_constant_step(sigma_values):
    optimized_loads = {}
    N = 200
    alpha = 0.5
    tolerance = 1e-7
    
    for sigma in sigma_values:
        lambda_t = np.zeros_like(D, dtype=float)
        
        for k in range(max_iter):
            u_total = -lambda_t / (2 * sigma)
            optimized_load = D + u_total
            gradient = -lambda_t / 2 + D + u_total
            new_lambda = lambda_t + alpha * gradient
            
            if np.linalg.norm(new_lambda - lambda_t) < tolerance:
                break
            lambda_t = new_lambda

        optimized_load = D - lambda_t / (2 * sigma)
        optimized_loads[sigma] = optimized_load + y_offset
    
    return optimized_loads

def isgm_decreasing_step(sigma_values):
    optimized_loads = {}
    N = 200
    tolerance = 1e-7
    
    for sigma in sigma_values:
        lambda_t = np.zeros_like(D, dtype=float)
        
        for k in range(max_iter):
            alpha_k = 1 / (((1 + N / sigma)**2) + k)
            u_total = -lambda_t / (2 * sigma)
            optimized_load = D + u_total
            gradient = -lambda_t / 2 + D + u_total
            new_lambda = lambda_t + alpha_k * gradient
            
            if np.linalg.norm(new_lambda - lambda_t) < tolerance:
                break
            lambda_t = new_lambda

        optimized_load = D - lambda_t / (2 * sigma)
        optimized_loads[sigma] = optimized_load + y_offset
    
    return optimized_loads

# Run optimization based on selected method
if method == "Gradient Ascent":
    optimized_loads = gradient_ascent(selected_sigmas)
elif method == "ISGM Constant Step":
    optimized_loads = isgm_constant_step(selected_sigmas)
else:
    optimized_loads = isgm_decreasing_step(selected_sigmas)

# Create plots
tab1, tab2 = st.tabs(["Individual Plots", "Combined Plot"])

with tab1:
    st.subheader(f"Individual Results for {method}")
    cols = st.columns(2)
    
    for i, (sigma, load) in enumerate(optimized_loads.items()):
        with cols[i % 2]:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(hours, D, 'b-', label='Original Load', linewidth=2)
            ax.plot(hours, load, 'r--', label=f'Optimized (σ={sigma})', linewidth=2)
            ax.set_xlabel('Hour of Day')
            ax.set_ylabel('Load (kW)')
            ax.set_title(f'σ = {sigma}')
            ax.grid(True)
            ax.set_xticks(hours)
            ax.yaxis.set_major_formatter(formatter)
            ax.legend()
            st.pyplot(fig)

with tab2:
    st.subheader(f"Combined Results for {method}")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hours, D, 'k-', linewidth=3, label='Original Load')
    
    for sigma, load in optimized_loads.items():
        ax.plot(hours, load, '--', linewidth=2, label=f'σ={sigma}')
    
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Load (kW)')
    ax.set_title(f'Comparison of Different Sigma Values ({method})')
    ax.grid(True)
    ax.set_xticks(hours)
    ax.yaxis.set_major_formatter(formatter)
    ax.legend()
    st.pyplot(fig)

# Method explanation
st.subheader("Method Explanation")
if method == "Gradient Ascent":
    st.markdown("""
    **Gradient Ascent Method:**
    - Traditional optimization approach with fixed step size
    - Updates the dual variable λ using a constant learning rate α
    - Convergence depends on careful selection of step size
    - Simple implementation but may require tuning
    """)
elif method == "ISGM Constant Step":
    st.markdown("""
    **ISGM with Constant Step Size:**
    - Incremental Stochastic Gradient Method
    - Uses a fixed step size throughout optimization
    - More stable than basic gradient ascent for some problems
    - Still requires step size tuning for best performance
    """)
else:
    st.markdown("""
    **ISGM with Decreasing Step Size:**
    - Advanced version with dynamic step size αₖ = 1/((1 + N/σ)² + k)
    - Step size decreases with iterations (k)
    - Typically provides better convergence guarantees
    - More robust to initial parameter choices
    """)

# Add some styling
st.markdown("""
<style>
    .st-emotion-cache-1v0mbdj {
        border-radius: 10px;
    }
    .st-emotion-cache-1y4p8pa {
        padding: 2rem 1.5rem;
    }
</style>
""", unsafe_allow_html=True)