# Rail Simulator: Integrated Railway Planning and Simulation

## Overview

Rail Simulator is my thesis project: a decision-support application for exploring the relationship between railway infrastructure and service-oriented timetable planning. It brings infrastructure design, timetable creation, and train movement simulation together in one environment, allowing users to evaluate how network changes influence day-to-day railway operations.

---

## Screenshots

<p align="center">
	<strong>Train status panels showing late and on-time trains</strong><br><br>
	<img src="dokumentacio/user/images/train_panels_late_on_time.png" alt="Train status panels showing late and on-time trains" width="70%">
</p>

<p align="center">
	<strong>Railway infrastructure construction and project view</strong><br><br>
	<img src="dokumentacio/user/images/project_view.png" alt="Railway infrastructure construction and project view" width="70%">
</p>

<p align="center">
	<strong>Preview of a calculated train route</strong><br><br>
	<img src="dokumentacio/user/images/route_preview.png" alt="Preview of a calculated train route" width="70%">
</p>

<p align="center">
	<strong>Railway network simulation</strong><br><br>
	<img src="dokumentacio/user/images/simulation_page.png" alt="Railway network simulation" width="70%">
</p>

<p align="center">
	<strong>Timetable overview and list of services</strong><br><br>
	<img src="dokumentacio/user/images/timetable_list.png" alt="Timetable overview and list of services" width="70%">
</p>

<p align="center">
	<strong>Timetable editor for configuring train services</strong><br><br>
	<img src="dokumentacio/user/images/timetable_editor.png" alt="Timetable editor for configuring train services" width="70%">
</p>

<p align="center">
	<strong>Selected station in the timetable editor</strong><br><br>
	<img src="dokumentacio/user/images/timetable_editor_selected_station.png" alt="Selected station in the timetable editor" width="70%">
</p>

# Functional Capabilities

## Infrastructure Construction

### Topological Modeling
Implements a **graph-based representation** of railway networks where:

- **Nodes** represent discrete geographic coordinates.
- **Edges** represent track segments with defined **speed limits** and **length attributes**.

### Geometric Constraints
Supports complex infrastructure geometry including:
- Flyovers  
- Tunnels  

Physical feasibility is enforced by restricting **invalid track curvature** and unrealistic track geometry.

### Facility Management
Hierarchical modeling of railway facilities:

- Stations
- Platforms

Platforms can be logically linked to the track network, enabling **train stopping and boarding operations**.

### Advanced Signaling
Implements an ETCS level-2 inspired signalling system with manually adjustable signal aspects and interlocking logic. The interlocking logic ensures **safe separation of trains** and prevents route conflicts.

---

# Timetable Engineering

## Periodic Scheduling
Native support for **Integrated Periodic Timetables (ITF)** enabling:

- Predictable repeating schedules
- Passenger-friendly clockface services

## Temporal Logic
Arrival and departure times are **automatically derived** from user-defined dwell times

## Operational Monitoring
During simulation execution the system tracks train punctuality and provides **real-time feedback** on operational performance.

---

# Simulation and Analysis

## Kinematic Dynamics
Train movement simulation includes:

- Acceleration curves
- Deceleration profiles
- Braking distances
- Infrastructure speed limits
- Signal aspects
- Dwell times
- Passenger boarding and alighting times

Vehicle behavior reacts dynamically to signaling and route availability.

## Interlocking and Routing
Route finding and signal path allocation utilize:

- **A\*** pathfinding algorithms
- **Graph traversal techniques**

Routes are automatically established between signaling nodes while maintaining **conflict-free operations**.


## Temporal Control
Simulation runtime can be accelerated using **variable time scaling**, which allows for rapid evaluation of timetable performance over extended periods.


# Technical Architecture

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Logic Engine | Python | High-level abstraction for rapid manipulation of complex data structures |
| Simulation | Pygame | Framebuffer-based rendering for precise 2D visualization |
| Administration UI | PyQt6 | Event-driven interface for professional data entry |
| Graph Logic | NetworkX | Optimized algorithms for topology and connectivity |
| Persistence | JSON | Human-readable project serialization and portability |