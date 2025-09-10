# 🚗⚡Distributed Optimal Charging and Scheduling of Plug-in Electric Vehicles

## 📌 Project Overview

This project addresses the **California Duck Curve**, a grid imbalance caused by high midday solar generation and steep evening demand ramp-ups. We leverage **intelligent scheduling of Electric Vehicle (EV) charging and discharging** via **Vehicle-to-Grid (V2G) technology** to flatten the load curve, improve renewable energy utilization, and enhance grid stability.

The project combines **optimization, machine learning, and power system concepts** to align EV charging patterns with renewable energy availability.

---

## ⚙️ Key Components

* **Synthetic Dataset Generation** – Created datasets for net load, solar/wind availability, and EV fleet behavior.
* **Dual Decomposition Framework** – Applied for distributed optimization of PEV charging schedules.
* **Optimization Algorithms** – Implemented **Gradient Ascent** and **Incremental Stochastic Gradient Method (ISGM)** for solving the dual problem efficiently.
* **Constraints & Penalties** – Integrated State of Charge (SoC), power limits, plug-in availability, and battery degradation penalties into the model.
* **EV Ranking Algorithm** – Initial implementation of an **optimal EV ranking system** to prioritize vehicles for charging/discharging based on grid demand, SoC, and plug-in duration.

---

## 🌟 Features Implemented

* Optimization-based EV scheduling that minimizes **grid load variance** while preserving battery health.
* **Load flattening** through dynamic EV charging/discharging aligned with renewable energy profiles.
* Comparative analysis of **Gradient Ascent vs ISGM** algorithms in distributed optimization.
* Graphs and simulations showing **convergence** and **duck curve flattening**.
* **Streamlit Interface** for real-time simulation, visualization, and interactive parameter tuning.

---

## 🔄 Current Progress on EV Ranking

* Implemented a **basic version** of the ranking system that scores vehicles based on:

  * State of Charge (SoC)
  * Availability window
  * Time-of-Use pricing
  * Load contribution potential
* **Next steps**: extend to a fully dynamic, scalable, and real-time prioritization framework for large EV fleets.

---

## 📊 Data & Implementation

* Current version uses **synthetically generated data** for testing and simulations.
* **Next phase**: integration with **real-time EV and grid data** for practical deployment and field testing.

---

## 💻 Web Interface (Streamlit)

A full **Streamlit dashboard** has been built for:

* Interactive tuning of optimization and ranking parameters.
* Real-time simulation of grid load with EV charging/discharging behavior.
* Visualization of the **duck curve before and after** optimization.
* Switching between optimization algorithms (**Gradient Ascent / ISGM**) for performance comparison.

---


## 🚀 Next Steps

* Improve **EV Ranking Algorithm** for real-time adaptability and scalability.
* Integrate with **live EV fleet and grid data**.
* Incorporate **battery degradation models** with higher accuracy.
* Extend optimization to include **renewable forecasting uncertainty**.

---


## 👨‍💻 Author

**Shiva Sai Teja M**

* B.Tech Electrical Engineering, IIT Ropar
