# 🔋 Electric Vehicle Charging for Managing the Duck Curve

##  Project Overview
This project aims to tackle the infamous *California Duck Curve* — a grid imbalance caused by high midday solar generation and steep evening ramp-ups in demand — using intelligent scheduling of Electric Vehicle (EV) charging and discharging via Vehicle-to-Grid (V2G) technology.

We explore **load shaping strategies** using distributed optimization techniques to align EV power flow with renewable generation profiles.

## ⚙️ Key Components

- **Synthetic Dataset Generation** for net load, solar/wind availability, and EV fleet status.
- **Dual Decomposition Framework** for distributed optimization of PEV charging schedules.
- **Gradient Ascent & ISGM Algorithms** for efficient solution of the dual problem.
- **SOC & Power Constraints**, battery degradation penalties, and plug-in availability integrated into the optimization model.
- **EV Ranking Algorithm**: Initial implementation of an optimal EV ranking system to prioritize charging/discharging based on grid demand, SoC, and plug-in duration.

## Features Implemented

- Optimization-based EV scheduling that **minimizes grid load variance** while preserving battery health.
- Load flattening through dynamic EV charging/discharging aligned with **renewable energy generation**.
- Comparative analysis of **Gradient Ascent vs Incremental Stochastic Gradient Method (ISGM)**.
- Graphs and simulations demonstrating convergence and impact on net load (flattening the duck curve).
- **Streamlit Interface** for real-time simulation, visualization, and interactive parameter tuning.

## Current Progress on EV Ranking
We’ve implemented a basic version of **optimal EV ranking** to decide which vehicles should charge or discharge at a given time, based on a scoring system that considers:
- State of Charge (SoC)
- Availability window
- Time-of-Use pricing
- Load contribution potential

> This ranking system is in early stages — in the coming weeks, we plan to make it **fully dynamic and robust** with support for real-time prioritization and scalability to large EV fleets.

## 📊 Data & Implementation

>  **Note:** This version uses **synthetically generated data** for simulation purposes.  
>  **Next Phase:** Real-time EV and grid data will be integrated for deployment and testing.

##  Web Interface (Streamlit)

The entire optimization pipeline has been deployed in a **Streamlit interface**, allowing:
- Interactive tuning of optimization and ranking parameters
- Real-time simulation of grid load with EV behavior
- Visualization of Duck Curve before and after load shaping
- Easy switching between algorithms (GA / ISGM)



