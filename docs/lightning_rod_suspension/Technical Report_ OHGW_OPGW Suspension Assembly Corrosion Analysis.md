# **Technical Report on Corrosion Characteristics and Precision Maintenance for OHGW/OPGW Suspension Assemblies**

## **1\. Introduction and Functional Overview**

Ensuring the integrity of Overhead Ground Wires (OHGW) and Optical Ground Wires (OPGW) is essential for stable power system operation, as they protect phase conductors from direct lightning strikes and rapidly discharge fault currents to the ground. The suspension assembly, which fixes the ground wire to the tower cross-arm, is a critical hardware component that must simultaneously withstand severe mechanical loads—such as conductor weight, wind pressure, ice/snow, and aeolian vibrations—alongside electrical stress. Long-term operation leads to corrosion of metal components, which can cause conductor detachment due to reduced mechanical strength or protection failure due to increased contact resistance.

## **2\. Technical Configuration and Material Properties**

Suspension assemblies flexibly support the conductor, primarily bearing vertical loads and distributing stresses from vibrations. For OPGW, advanced hardware is used to protect optical fibers from mechanical and environmental stress.

### **Table 1: Components and Functions of Suspension Assemblies**

| Component | Primary Function | Material Characteristics   |
| :---- | :---- | :---- |
| Suspension Clamp | Supports vertical load of OHGW | Aluminum alloy or galvanized steel  |
| Armor Rods | Relieves bending stress and prevents abrasion | High-strength aluminum alloy  |
| Suspension Rods & Shackle | Provides flexible rotation moment | Hot-dip galvanized high-tensile steel |
| Vibration Damper | Prevents fatigue failure from vibrations | Galvanized steel and zinc/aluminum  |
| Tower Bond Clamp | Ensures electrical connection to tower  | Conductive aluminum or copper alloy  |

## **3\. Metal Corrosion Mechanisms**

Corrosion results from electrochemical reactions with moisture, oxygen, salt, and industrial pollutants. Hot-dip galvanizing protects steel via a physical barrier and sacrificial anode action.

* **Initial Phase:** A dense zinc oxide/carbonate film forms, slowing corrosion.  
* **White Rust:** Zinc hydroxide powder forms in humid or poorly ventilated conditions.  
* **Red Rust:** Iron oxide ($Fe\_{2}O\_{3}$) forms once the zinc layer is consumed and steel is exposed.

Environmental factors like airborne chlorides in coastal areas or sulfur dioxide in industrial zones significantly accelerate corrosion rates.

## **4\. Defect Analysis: Mechanical and Electrical Impact**

### **4.1. Mechanical Defects**

Corrosion creates pitting, which acts as a stress riser. Under constant aeolian vibration, this can lead to fatigue failure below standard endurance limits. The operating fatigue strength can be modeled as:  
$$\\sigma\_{f}' \= \\sigma\_{f} \\cdot K\_{surf} \\cdot K\_{corr}$$  
where $\\sigma\_{f}'$ is actual fatigue strength, $K\_{surf}$ is surface roughness, and $K\_{corr}$ is the corrosion correction factor.

### **4.2. Electrical Defects**

Corrosion forms high-resistance oxide films, increasing contact resistance. This leads to localized overheating during fault currents and increased surge impedance, which may trigger back-flashover (TTPR) accidents during lightning strikes.

## **5\. KEPCO Inspection Standards and Grading**

The Korea Electric Power Corporation (KEPCO) classifies degradation into five grades based on corrosion area and structural integrity.

### **Table 2: Corrosion Grading System**

| Grade | Appearance and Symptoms | Maintenance Action   |
| :---- | :---- | :---- |
| Grade 1 (Good) | Maintains luster; no corrosion  | Routine inspection |
| Grade 2 (Fair) | Loss of luster; white rust  | Monitoring progress |
| Grade 3 (Caution) | Localized red rust | Partial anti-corrosion repair |
| Grade 4 (Poor) | Extensive red rust; peeling | Replacement or full repainting |
| Grade 5 (Critical) | Cross-sectional loss; risk of drop  | Immediate replacement |

## **6\. Advanced Diagnostics and Maintenance Strategies**

Modern techniques use drones to capture high-resolution images, which are analyzed via AI algorithms to extract Regions of Interest (ROI) and calculate corrosion ratios through RGB analysis. Other technologies include Infrared (IR) thermography for hot spot detection and BATCAM for visualizing acoustic signatures of discharges.  
Maintenance strategies are shifting toward Condition-Based Maintenance (CBM), utilizing predictive models to assess remaining life based on environmental salinity and galvanizing thickness. In high-corrosion zones, upgrading to aluminum alloy clamps or utilizing elastomer inserts is recommended to prevent metal-to-metal contact corrosion.

## **7\. Conclusion**

Corrosion of suspension assemblies is a critical factor in transmission grid safety. Utilizing an Atmospheric Corrosion Map and high-precision diagnostic data allows for optimized replacement timing, ensuring long-term resilience of national power infrastructure.