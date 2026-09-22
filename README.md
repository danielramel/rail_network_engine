# Rail Simulator: Integrated Railway Planning and Simulation

## Overview

Rail Simulator is a professional-grade decision-support application designed to bridge the gap between railway infrastructure engineering and service-oriented timetable planning. The application implements a **service-first paradigm** where infrastructure developments are derived from desired operational service levels rather than existing physical constraints.

---

# Functional Capabilities

## Infrastructure Construction

### Topological Modeling
Implements a **graph-based representation** of railway networks where:

- **Nodes** represent discrete geographic coordinates.
- **Edges** represent track segments with defined **speed limits** and **length attributes**.

### Geometric Constraints
Supports complex infrastructure geometry including:

- Multi-level track layouts  
- Flyovers  
- Tunnels  

Physical feasibility is enforced by restricting **invalid track curvature** and unrealistic track geometry.

### Facility Management
Hierarchical modeling of railway facilities:

- Stations
- Platforms
- Passenger service nodes

Facilities can be logically linked to the **primary track network** to represent operational passenger flow.

### Advanced Signaling
Implements a signaling interlocking system managing signal states:

| Aspect | Meaning |
|------|------|
| Clear | Track ahead available |
| Caution | Next block occupied or restricted |
| Danger | Stop — block occupied |

The interlocking logic ensures **safe separation of trains** and prevents route conflicts.

---

# Timetable Engineering

## Periodic Scheduling
Native support for **Integrated Periodic Timetables (ITF / Ütemes menetrend)** enabling:

- Predictable repeating schedules
- Structured transfer nodes
- Passenger-friendly clockface services

## Temporal Logic
Arrival and departure times are **automatically derived** from:

- User-defined dwell times
- Inter-station travel times
- Infrastructure speed limits

## Operational Monitoring
During simulation execution the system tracks:

- Train punctuality
- Delay propagation
- Schedule adherence relative to planned timetable

---

# Simulation and Analysis

## Kinematic Dynamics
Train movement simulation includes:

- Acceleration curves
- Deceleration profiles
- Braking distances
- Infrastructure speed limits

Vehicle behavior reacts dynamically to signaling and route availability.

## Interlocking and Routing
Route finding and signal path allocation utilize:

- **A\*** pathfinding algorithms
- **Graph traversal techniques**

Routes are automatically established between signaling nodes while maintaining **conflict-free operations**.

## Bottleneck Detection
Traffic simulation identifies:

- Capacity constraints
- Conflict-prone junctions
- Infrastructure limitations

This allows infrastructure redesign **before physical investment**.

## Temporal Control
Simulation runtime can be accelerated using **variable time scaling**:

- Up to **25× real-time speed**
- Enables long-term timetable stability analysis

---

# Technical Architecture

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Logic Engine | Python | High-level abstraction for rapid manipulation of complex data structures |
| Simulation | Pygame | Framebuffer-based rendering for precise 2D visualization |
| Administration UI | PyQt6 | Event-driven interface for professional data entry |
| Graph Logic | NetworkX | Optimized algorithms for topology and connectivity |
| Persistence | JSON | Human-readable project serialization and portability |

---

# Future Development Scope

## Advanced Interlocking
Implementation of:

- Route pre-booking
- Automated signal clearing
- Conflict anticipation logic

## Boundary Integration
Management of trains:

- Entering simulation boundaries
- Exiting simulated infrastructure

Supports integration with external railway networks.

## Quantitative Analytics
Integrated reporting tools for:

- Network capacity utilization
- Infrastructure resilience
- Timetable robustness
