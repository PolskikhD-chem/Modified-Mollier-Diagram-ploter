<b>Modified Mollier Diagran</b>

This program provides the capability to automatically generate isolines of the Polanyi potential of water vapor on a temperature versus moisture content chart. Additionally, isolines of relative humidity can be plotted. A double-click allows a new Polanyi potential isoline to be added.

Developed by Aristov Yu.I.; ORCID: 0000-0003-1460-3972 

Software by Polskikh D.A.; ORCID:0009-0009-4682-0104



![Example_MMDploter](https://raw.githubusercontent.com/PolskikhD-chem/Modified-Mollier-Diagram-ploter/main/Versions/MMDploterV001/MMDploterV001.jpg)

# Construction of the Modified Diagram

The construction of the modified diagram involves calculating a set of lines \( t(x)|_{\Delta F=const} \). These lines correspond to constant values of the Polanyi adsorption potential \( \Delta F[t(x)] \) in the coordinates of the conventional Mollier diagram: air temperature \( t \) (in °C) and its moisture content \( x \) (in g_water/g_dry_air).

## Theoretical Background

Typically, this potential is expressed as a function of absolute temperature \( T \) (K) and water vapor partial pressure \( P_v \):

\[
\Delta F(P_v, T) = - R T \ln\left[\frac{P_v}{P_0(T)}\right] \tag{1}
\]

where \( P_0(T) \) is the saturated vapor pressure of the adsorbate at temperature \( T \) [1].

The relationship between the temperatures is straightforward:

\[
t = T - 273.15 \text{ K}
\]

The moisture content \( x \) can be calculated from the partial pressure \( P_v \) by assuming both air and vapor behave as ideal gases.

## Derivation of Moisture Content

### 1. Partial Densities

The partial density \( \rho_{da} \) of dry air in the humid air mixture is:

\[
\rho_{da} = \frac{P_{da} M_{da}}{R T} \tag{2}
\]

The partial density \( \rho_{v} \) of water vapor is:

\[
\rho_{v} = \frac{P_{v} M_{v}}{R T} \tag{3}
\]

### 2. Moisture Content Equation

Moisture content \( x \) is defined as the ratio of the mass of vapor to the mass of dry air \( m_v / m_{da} \), which simplifies to the ratio of their densities:

\[
x = \frac{m_v}{m_{da}} = \frac{\rho_v}{\rho_{da}} = \frac{P_v M_v}{P_{da} M_{da}} \tag{4}
\]

Since \( P_{da} = P - P_v \) (where \( P \) is the total pressure), this becomes:

\[
x = 0.6220 \cdot \frac{P_v}{P - P_v} \cdot 1000 \tag{4a}
\]

**Where:**
*   \( P = 101.325 \text{ kPa} \) — total atmospheric pressure
*   \( M_{da} = 0.0290 \text{ kg/mol} \) — molar mass of dry air
*   \( M_{v} = 0.0180 \text{ kg/mol} \) — molar mass of water vapor

## Calculating the Isolines

To construct an isoline for a **fixed value of the adsorption potential \( \Delta F \)**:

1.  For a chosen temperature \( t \), calculate the corresponding vapor partial pressure \( P_v \):

    \[
    P_v = P_0(t + 273.15 \text{ K}) \cdot \exp\left\{ \frac{-\Delta F}{R \cdot (t + 273.15 \text{ K})} \right\} \tag{5}
    \]

2.  Substitute \( P_v \) from (5) into equation (4) to compute the corresponding moisture content \( x(\Delta F, t) \).

3.  By repeating this calculation for a range of temperatures \( t \) at a constant \( \Delta F \), a single line \( t(x)|_{\Delta F=const} \) is generated. A family of such lines, each for a different constant value of \( \Delta F \), forms the modified diagram.

---
*Note: Equation (4a) includes a factor of 1000 to convert the result to g_water/kg_dry_air, a common unit. Please verify this scaling factor matches your intended output unit (g_water/g_dry_air).*
