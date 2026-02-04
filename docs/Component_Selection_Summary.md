# Power Supply Component Selection Summary
## Design Trade-offs and Alternatives Analysis

Version: 1.0  
Date: 2026-01-15  

---

## Overview

This document summarizes all component selection decisions made for the differential probe power supply, including alternatives considered, pros/cons, and reasoning for final choices.

---

## 1. USB-C Charging IC

### Selected: **MCP73831T-2ACI/OT** (Microchip)

**Specifications:**
- Package: SOT-23-5
- Charge voltage: 4.2V (fixed)
- Charge current: Programmable up to 500mA via external resistor
- Input voltage: 3.75V - 6V
- Charge termination: 7.5% of programmed current
- Cost: ~$0.50

**Pros:**
- ✅ Very simple, minimal external components (just 2 resistors + capacitors)
- ✅ Industry standard, proven reliability
- ✅ Small footprint (SOT-23-5)
- ✅ Built-in status output (for charging LED)
- ✅ Automatic charge termination
- ✅ Low cost
- ✅ No microcontroller needed

**Cons:**
- ❌ Fixed 4.2V charge voltage (not adjustable)
- ❌ Basic features only (no temperature monitoring)
- ❌ Cannot charge while powering the load (charge-only)

### Alternatives Considered:

#### Option A: **TP4056** (Chinese, generic)
- **Cost:** $0.20 (very cheap)
- **Pros:** Even simpler, DIP package available
- **Cons:** 
  - Lower quality control
  - No official datasheet from reputable source
  - Less reliable in industrial applications
- **Reason NOT chosen:** Quality/reliability concerns for precision measurement equipment

#### Option B: **BQ24075** (Texas Instruments)
- **Cost:** $1.50
- **Pros:** 
  - Can power system while charging
  - Built-in power path management
  - Better thermal regulation
  - Higher charge current (1.5A)
- **Cons:** 
  - More expensive
  - Larger package (VQFN-16)
  - More complex (requires more external components)
- **Reason NOT chosen:** Overkill for this application; we don't need to operate while charging

#### Option C: **MCP73871** (Microchip)
- **Cost:** $1.20
- **Pros:** 
  - Power path management (load sharing)
  - System can run while charging
  - Same family as MCP73831
- **Cons:** 
  - More expensive
  - Requires more board space
  - More complex design
- **Reason NOT chosen:** Added complexity not needed; spec explicitly states "does not have to work when charging"

**Final Decision Reasoning:**
The MCP73831 hits the sweet spot: simple, reliable, low-cost, and perfectly adequate for our 500mA charging requirement. Since we don't need to operate while charging, the added complexity of power path management ICs is unnecessary.

---

## 2. Battery Protection IC

### Selected: **DW01A** + **FS8205A** (Combo)

**DW01A Specifications:**
- Package: SOT-23-6
- Over-charge protection: 4.25V ±0.05V
- Over-discharge protection: 2.4V ±0.1V
- Over-current detection: Via external sense resistor
- Cost: ~$0.15

**FS8205A Specifications:**
- Package: TSSOP-8
- Dual N-channel MOSFET
- RDS(on): 25mΩ @ 4.5V
- Voltage rating: 20V
- Cost: ~$0.10

**Combined Pros:**
- ✅ Complete protection solution (OVP, UVP, OCP)
- ✅ Very low cost (~$0.25 total)
- ✅ Standard solution, widely available
- ✅ Small footprint
- ✅ Proven track record in consumer electronics
- ✅ Low voltage drop (25mΩ × 2 = 50mΩ total)

**Combined Cons:**
- ❌ Requires two separate ICs
- ❌ Basic protection only (no fancy features)
- ❌ No fuel gauge or state-of-charge indication

### Alternatives Considered:

#### Option A: **AP9101C** (Diodes Inc.)
- **Cost:** $0.30
- **Pros:** 
  - Single IC solution with integrated MOSFETs
  - Smaller footprint
- **Cons:** 
  - Higher RDS(on) → more voltage drop
  - Lower current capability
  - Less common, harder to source
- **Reason NOT chosen:** DW01A+FS8205A combo is more standard and flexible

#### Option B: **BQ29700** (Texas Instruments)
- **Cost:** $0.80
- **Pros:** 
  - More precise protection thresholds
  - Better specs from TI
  - Separate CHG and DSG FET control
- **Cons:** 
  - More expensive
  - Still requires external MOSFETs
  - Overkill for simple single-cell application
- **Reason NOT chosen:** Cost not justified for this simple application

#### Option C: **Built-in battery protection**
- Many LiPo cells come with built-in protection PCB
- **Pros:** 
  - No external components needed
  - Even smaller board space
- **Cons:** 
  - Less control over protection thresholds
  - May not have optimal current limit (often too high at 3A+)
  - Less reliable (varies by battery manufacturer)
- **Reason NOT chosen:** We want consistent, controlled protection at 1A for this precision instrument

**Final Decision Reasoning:**
The DW01A + FS8205A is the industry-standard combo for single-cell LiPo protection. It's proven, cheap, widely available, and provides exactly the protection we need. The 1A current limit (via 0.15Ω sense resistor) is appropriate for our 50mA load with good safety margin.

---

## 3. Power Source Selection (OR-ing)

### Selected: **BAT54C** (Dual Schottky, Common Cathode)

**Specifications:**
- Package: SOT-23
- Configuration: Dual Schottky, common cathode
- Forward voltage: ~0.3V @ 100mA
- Reverse voltage: 30V
- Forward current: 200mA continuous
- Cost: ~$0.05

**Pros:**
- ✅ Extremely simple (passive)
- ✅ Automatic source selection (higher voltage wins)
- ✅ Very low cost
- ✅ Tiny footprint (SOT-23)
- ✅ No control logic needed
- ✅ Zero quiescent current
- ✅ Reliable (no active components)

**Cons:**
- ❌ Voltage drop (~0.3V at 50mA)
- ❌ No "ideal" diode behavior (not zero drop)
- ❌ Power loss in diodes (15mW per diode at 50mA)
- ❌ Cannot actively control source priority

### Alternatives Considered:

#### Option A: **TPS2115A** (Texas Instruments, PowerMux)
- **Cost:** $1.50
- **Pros:** 
  - Active ideal diode (near-zero voltage drop)
  - Programmable priority selection
  - Smooth transition between sources
  - Very low RDS(on): 84mΩ
  - Break-before-make switching
- **Cons:** 
  - Significantly more expensive
  - Larger footprint (WSON-8)
  - Requires control logic
  - Quiescent current: 40µA
- **Reason NOT chosen:** The 0.3V drop is acceptable for our application (we have boost converter downstream anyway). The $1.45 savings and simplicity outweigh the small efficiency gain.

#### Option B: **LM66100** (Texas Instruments, Ideal Diode)
- **Cost:** $0.80
- **Pros:** 
  - Very low forward drop (35mV typical)
  - Automatic direction control
  - Can protect against reverse current
- **Cons:** 
  - Only single-channel (need 2 ICs)
  - More expensive than Schottky
  - Requires enable logic
- **Reason NOT chosen:** Cost and complexity not justified

#### Option C: **P-channel MOSFET + control logic**
- DIY ideal diode using MOSFETs and comparators
- **Pros:** 
  - Can achieve near-zero voltage drop
  - Fully customizable behavior
- **Cons:** 
  - Complex design
  - Requires several external components
  - Higher component count
  - More prone to design errors
- **Reason NOT chosen:** Over-engineering for this application

**Final Decision Reasoning:**
For our application, the passive Schottky OR-ing is perfectly adequate. The 0.3V drop represents only ~3% loss at 9V input and ~8% at 3.7V LiPo, which is acceptable. The boost converter downstream will compensate anyway. The simplicity, reliability, and cost savings make this the clear winner.

---

## 4. Boost Converter

### Selected: **TPS61220DCKR** (Texas Instruments)

**Specifications:**
- Package: SC70-6 (very small)
- Input voltage: 0.7V - 5.5V
- Output voltage: Adjustable (set to 5.0V)
- Output current: 150mA (@ 3.3V in, 5V out)
- Switching frequency: 1MHz
- Efficiency: ~90% @ 50mA load
- Quiescent current: 50µA
- Cost: ~$1.20

**Pros:**
- ✅ Wide input range (0.7-5.5V) covers LiPo range
- ✅ High efficiency (90%+)
- ✅ Very small footprint (SC70-6)
- ✅ High switching frequency (1MHz) = small inductor
- ✅ Low quiescent current (important for battery life)
- ✅ Integrated switches (no external FETs needed)
- ✅ Can work with 9V input (via voltage divider or pass-through)

**Cons:**
- ❌ Input limited to 5.5V (need special handling for 9V battery)
- ❌ Generates switching noise (1MHz)
- ❌ Requires careful PCB layout
- ❌ External inductor needed

### Alternatives Considered:

#### Option A: **TPS61202** (Texas Instruments)
- **Cost:** $1.00
- **Pros:** 
  - Cheaper
  - Similar specs
  - Fixed 5V output version available
- **Cons:** 
  - Lower efficiency (~85%)
  - Larger package
  - Higher quiescent current (180µA)
- **Reason NOT chosen:** TPS61220 has better efficiency and lower quiescent current, worth the extra $0.20

#### Option B: **MCP1640** (Microchip)
- **Cost:** $0.80
- **Pros:** 
  - Even cheaper
  - Simple design
- **Cons:** 
  - Lower switching frequency (500kHz) = bigger inductor
  - Lower efficiency
  - Worse line regulation
- **Reason NOT chosen:** For precision analog work, we want the better specs of the TPS61220

#### Option C: **MAX1724** (Maxim/Analog Devices)
- **Cost:** $2.50
- **Pros:** 
  - Excellent efficiency (>95%)
  - Ultra-low noise
  - Wide input range
- **Cons:** 
  - Much more expensive
  - Harder to source
  - Overkill for this application
- **Reason NOT chosen:** Cost not justified; noise will be filtered by LDOs anyway

#### Option D: **Skip boost converter entirely**
- Just use buck or LDO from 9V
- **Pros:** 
  - Simpler
  - No boost noise
  - Lower cost
- **Cons:** 
  - LiPo unusable below ~5.5V
  - Wastes most of LiPo capacity
  - Battery "dies" at 70% capacity
- **Reason NOT chosen:** User requirement was to support LiPo with full voltage range (3.0-4.2V)

**Final Decision Reasoning:**
The TPS61220 is the optimal choice for this application. It provides excellent efficiency, small size, and low quiescent current. The 1MHz switching frequency allows a small 2.2µH inductor. While it generates some switching noise, this is acceptable because we have ultra-low-noise LDOs downstream that will filter it out with >50dB PSRR @ 1MHz.

**Important Note:** The boost may need bypass logic when 9V battery is present to avoid unnecessary switching noise and improve efficiency. This can be added with an enable pin control circuit if needed.

---

## 5. Positive Voltage LDO (+5V)

### Selected: **ADP7142ARDZ-5.0-R7** (Analog Devices)

**Specifications:**
- Package: SOIC-8
- Input voltage: 3.3V - 20V
- Output voltage: 5.0V (fixed)
- Output current: 200mA max
- Dropout voltage: 170mV @ 200mA
- Output noise: **9µVrms** (10Hz-100kHz)
- PSRR: 80dB @ 100Hz, 70dB @ 1kHz, 55dB @ 100kHz
- Quiescent current: 20µA
- Cost: ~$3.00

**Pros:**
- ✅ **Ultra-low noise** (9µVrms) - critical for 200MHz probe
- ✅ Excellent PSRR to reject boost converter noise
- ✅ Low dropout (170mV) for good efficiency
- ✅ Wide input range (handles boost output variations)
- ✅ Stable with low ESR capacitors
- ✅ Thermal shutdown protection
- ✅ Soft-start feature reduces inrush

**Cons:**
- ❌ Relatively expensive (~$3)
- ❌ Requires tantalum output capacitor (specific ESR range)
- ❌ SOIC-8 with thermal pad (more complex assembly)

### Alternatives Considered:

#### Option A: **TPS7A4701RGWR** (Texas Instruments)
- **Cost:** $2.50
- **Pros:** 
  - Even better noise: **1µVrms** (!!)
  - Excellent PSRR: 70dB @ 1MHz
  - Can handle 1A output
  - Better specs overall
- **Cons:** 
  - Larger package (VQFN-20)
  - Higher dropout voltage (320mV @ 200mA)
  - More expensive
  - Overkill for 50mA application
- **Reason NOT chosen:** The 1µVrms noise is amazing but overkill. 9µVrms is already excellent for our application. The ADP7142 has lower dropout and is easier to layout (SOIC vs VQFN).

#### Option B: **LT3045** (Analog Devices)
- **Cost:** $4.50
- **Pros:** 
  - Incredible noise: **0.8µVrms** (best in class)
  - Parallel-able for higher current
  - Excellent transient response
  - Can use ceramic caps only
- **Cons:** 
  - Very expensive
  - Overkill for this application
  - Larger footprint
- **Reason NOT chosen:** Cost too high; 9µVrms is sufficient

#### Option C: **LM1117-5.0** (Generic)
- **Cost:** $0.30
- **Pros:** 
  - Very cheap
  - Simple, proven design
  - Easy to use
  - 800mA output capability
- **Cons:** 
  - **Output noise: ~40µVrms** (much worse)
  - High dropout (1.2V @ 800mA)
  - Poor PSRR at high frequencies
  - Not suitable for precision analog
- **Reason NOT chosen:** Noise performance unacceptable for 200MHz differential probe

#### Option D: **AMS1117-5.0** (Chinese generic)
- **Cost:** $0.10
- **Pros:** 
  - Extremely cheap
  - Pin-compatible with LM1117
- **Cons:** 
  - Even worse noise
  - Quality control issues
  - Poor PSRR
  - Not reliable enough
- **Reason NOT chosen:** Quality not suitable for precision measurement equipment

#### Option E: **REG1117-5.0** (TI, improved version)
- **Cost:** $0.50
- **Pros:** 
  - Cheap
  - Better than LM1117
  - Improved specs
- **Cons:** 
  - Still ~40µVrms noise
  - PSRR inadequate for rejecting 1MHz switching noise
- **Reason NOT chosen:** Noise still too high for precision work

**Final Decision Reasoning:**
For a precision differential probe operating at 200MHz, low noise is absolutely critical. The ADP7142's 9µVrms noise is excellent and well worth the $3 cost. Its 55dB PSRR @ 100kHz (extrapolating to ~50dB @ 1MHz) will effectively filter the boost converter's 1MHz switching noise. The 170mV dropout also keeps efficiency reasonable when running from the boost converter's 5V output.

**Cost-Performance Trade-off:**
- Cheap LDO ($0.30): 40µVrms noise → 15dB worse than ADP7142
- ADP7142 ($3.00): 9µVrms noise → excellent for precision analog
- Premium LDO ($4.50): 0.8µVrms → only 1dB better, not worth 50% more cost

The ADP7142 is the sweet spot for this application.

---

## 6. Charge Pump Inverter (Voltage Inverter)

### Selected: **TPS60403DBVR** (Texas Instruments)

**Specifications:**
- Package: SOT-23-5
- Input voltage: 1.6V - 5.5V
- Output voltage: -VIN (inverted)
- Output current: 40mA max
- Switching frequency: 150kHz
- Efficiency: 99% unloaded, 90% @ 20mA
- Quiescent current: 120µA
- Cost: ~$1.00

**Pros:**
- ✅ Small footprint (SOT-23-5)
- ✅ High efficiency (90%+)
- ✅ Sufficient current for our application (we need ~25mA)
- ✅ Lower switching frequency (150kHz) vs boost (1MHz)
- ✅ Minimal external components (just capacitors)
- ✅ Reliable, proven design

**Cons:**
- ❌ Generates switching noise (~20mVpp ripple)
- ❌ Limited output current (40mA max)
- ❌ Output voltage unregulated (-5V to -9V depending on input)
- ❌ Requires post-regulation for clean negative rail

### Alternatives Considered:

#### Option A: **ICL7660SCPA** (Maxim/Renesas)
- **Cost:** $0.50
- **Pros:** 
  - Classic design, very reliable
  - Higher current capability (up to 40mA)
  - Cheaper
  - DIP package available (easier prototyping)
- **Cons:** 
  - Lower switching frequency (10kHz)
  - Lower efficiency (~80%)
  - **Much noisier output**
  - Larger package
  - Older technology
- **Reason NOT chosen:** Lower frequency = more difficult to filter; worse noise performance

#### Option B: **LTC1983** (Analog Devices)
- **Cost:** $3.50
- **Pros:** 
  - Regulated output (doesn't need LDO)
  - Lower noise
  - Higher current (100mA)
- **Cons:** 
  - Very expensive
  - Larger package
  - Still needs filtering for ultra-low noise
- **Reason NOT chosen:** Since we need an LDO anyway for ultra-low noise, the regulated output isn't worth the 3.5× cost premium

#### Option C: **TC7660** (Microchip)
- **Cost:** $0.80
- **Pros:** 
  - Improved version of ICL7660
  - Slightly better efficiency
  - Pin-compatible
- **Cons:** 
  - Still 10kHz switching (hard to filter)
  - Noisier than TPS60403
  - Lower efficiency
- **Reason NOT chosen:** TPS60403 has better performance for similar cost

#### Option D: **Transformer-based isolated converter**
- Use small transformer and rectifier
- **Pros:** 
  - True isolation
  - Can generate multiple voltages
  - Low noise (no switching)
- **Cons:** 
  - Much larger
  - More expensive
  - Overkill for this application
  - Requires more components
- **Reason NOT chosen:** Isolation not needed; too complex

**Final Decision Reasoning:**
The TPS60403 is the best balance of performance, size, and cost. Its 150kHz switching frequency is high enough to use small capacitors but low enough that the downstream ADP7182 LDO can filter it effectively (ADP7182 has 65dB PSRR @ 150kHz). The 40mA current limit is adequate for our 25mA negative rail load with good margin.

**Critical Design Decision:** The TPS60403 connects to the VBST rail (boost output), NOT to the clean +5V_CLEAN rail. This prevents charge pump switching noise from coupling back into the sensitive +5V analog supply.

---

## 7. Negative Voltage LDO (-5V)

### Selected: **ADP7182ARDZ-5.0-R7** (Analog Devices)

**Specifications:**
- Package: SOIC-8
- Input voltage: -2.3V to -6.0V (negative voltages)
- Output voltage: -5.0V (fixed)
- Output current: 200mA max
- Dropout voltage: -200mV @ 200mA
- Output noise: **9µVrms** (10Hz-100kHz)
- PSRR: 75dB @ 100Hz, 65dB @ 1kHz, 50dB @ 100kHz
- Quiescent current: 30µA
- Cost: ~$3.00

**Pros:**
- ✅ **Ultra-low noise** (9µVrms) - matches positive rail
- ✅ Excellent PSRR to reject charge pump noise (65dB @ 150kHz)
- ✅ Designed specifically for negative voltages
- ✅ Low dropout for good efficiency
- ✅ Optional noise reduction pin for even lower noise
- ✅ Symmetric performance with ADP7142 (positive rail)

**Cons:**
- ❌ Relatively expensive (~$3)
- ❌ Requires tantalum output capacitor
- ❌ SOIC-8 with thermal pad

### Alternatives Considered:

#### Option A: **LM7905** (Generic negative regulator)
- **Cost:** $0.40
- **Pros:** 
  - Very cheap
  - Classic design
  - High current capability (1.5A)
  - TO-220 package (easy heat sinking)
- **Cons:** 
  - **High output noise** (~100µVrms+)
  - Poor PSRR (<40dB @ 10kHz)
  - High dropout (2V @ 1A)
  - Not suitable for precision work
  - Cannot filter 150kHz charge pump noise
- **Reason NOT chosen:** Completely inadequate for precision analog; would ruin the probe's noise performance

#### Option B: **TPS7A3001** (Texas Instruments, negative)
- **Cost:** $2.00
- **Pros:** 
  - Adjustable output (-1.2V to -20V)
  - Good noise: 14µVrms
  - Better PSRR than LM79xx
  - Lower cost than ADP7182
- **Cons:** 
  - Requires external resistor divider (not fixed 5V)
  - Noise slightly worse than ADP7182
  - PSRR not as good as ADP7182
- **Reason NOT chosen:** The fixed-voltage ADP7182 is simpler (no divider needed) and has better specs

#### Option C: **LT3015** (Analog Devices)
- **Cost:** $4.50
- **Pros:** 
  - Excellent noise: 3µVrms
  - Very high PSRR
  - Adjustable output
  - Can handle high input voltages
- **Cons:** 
  - Very expensive
  - Requires external divider
  - Overkill for this application
- **Reason NOT chosen:** Cost not justified; 9µVrms is already excellent

#### Option D: **DIY voltage inverter + positive LDO**
- Use OpAmp-based voltage inverter circuit
- **Pros:** 
  - Can use cheaper positive LDO
  - More flexible
- **Cons:** 
  - Complex design
  - Poor efficiency
  - Stability concerns
  - Higher component count
  - Not a professional solution
- **Reason NOT chosen:** Proper negative LDO is more reliable and efficient

#### Option E: **Skip negative LDO, use charge pump directly**
- Connect TPS60403 output directly to circuit
- **Pros:** 
  - Saves $3
  - Simpler
  - Smaller board space
- **Cons:** 
  - **~20mVpp ripple on negative rail**
  - 150kHz noise will modulate the analog circuits
  - Completely unacceptable for 200MHz differential probe
  - Would destroy measurement quality
- **Reason NOT chosen:** Noise performance would be catastrophically bad

**Final Decision Reasoning:**
The ADP7182 is absolutely essential for this design. The charge pump's 20mVpp ripple at 150kHz would completely ruin the probe's performance if applied directly to the amplifiers. The ADP7182's 65dB PSRR @ 150kHz reduces this to ~7µVpp, and combined with its intrinsic 9µVrms noise, gives us a clean -5V rail suitable for precision work.

The symmetric performance with the ADP7142 (both 9µVrms noise) ensures balanced noise on both supply rails, which is important for differential amplifier CMRR performance.

**Cost Justification:**
The $3 spent on the ADP7182 is absolutely critical. Using a cheap LM7905 would save $2.60 but would increase noise by >10× and make the probe essentially useless for precision measurements. This is not a place to cut costs.

---

## 8. Power Inductor (for Boost Converter)

### Selected: **TDK VLS3012ET-2R2M**

**Specifications:**
- Inductance: 2.2µH ±20%
- Saturation current: 2.3A
- DC resistance: 85mΩ max
- Package: 3012 (3.0mm × 3.0mm × 1.2mm)
- Shielded construction
- Cost: ~$0.30

**Pros:**
- ✅ Appropriate inductance for 1MHz boost converter
- ✅ High saturation current (2.3A >> our 200mA need)
- ✅ Low DCR (85mΩ) for good efficiency
- ✅ Small footprint (3.0 × 3.0 mm)
- ✅ Shielded to minimize EMI
- ✅ Good thermal performance

**Cons:**
- ❌ Relatively expensive for an inductor
- ❌ SMD package (hand soldering can be tricky)

### Alternatives Considered:

#### Option A: **Murata LQH3NPN2R2MMEL** (larger size)
- **Cost:** $0.20
- **Pros:** 
  - Cheaper
  - Same 2.2µH value
  - Good specs
- **Cons:** 
  - Larger footprint (3.2 × 2.5mm)
  - Unshielded (more EMI)
  - Lower saturation current (1.5A)
- **Reason NOT chosen:** TDK part is better shielded and has higher Isat

#### Option B: **4.7µH inductor**
- Higher inductance value
- **Pros:** 
  - Lower ripple current
  - Can use smaller output capacitor
- **Cons:** 
  - Larger physical size
  - Higher DCR (more losses)
  - Slower transient response
- **Reason NOT chosen:** 2.2µH is optimal for 1MHz switching frequency per TI app notes

#### Option C: **1µH inductor**
- Lower inductance value
- **Pros:** 
  - Smaller size
  - Lower DCR
  - Cheaper
- **Cons:** 
  - Higher ripple current
  - Less efficient
  - Requires larger output capacitor
- **Reason NOT chosen:** 2.2µH is the recommended value for TPS61220

**Final Decision Reasoning:**
The 2.2µH value is specifically recommended by TI's datasheet for the TPS61220 at 1MHz switching. The TDK part has excellent specs (high Isat, low DCR, shielded) and is small enough for compact design. The $0.30 cost is reasonable for a quality power inductor.

---

## 9. Capacitor Choices

### Boost Converter Capacitors

**C_BST_IN: 10µF, 16V, X7R, 0805**
- **Reasoning:** TI recommends 10µF minimum for input decoupling
- **X7R dielectric:** Stable across temperature
- **16V rating:** Derating (9V × 2 = 18V, closest standard is 16V)

**C_BST1: 22µF, 16V, X7R, 1206**
- **Reasoning:** TI recommends 20µF+ for output bulk storage
- **1206 package:** Needed for 22µF in X7R ceramic

**C_BST2: 10µF, 16V, X7R, 0805**
- **Reasoning:** Additional high-frequency filtering
- **Smaller package:** Easier placement close to IC

### LDO Output Capacitors (Critical Choice)

**Tantalum vs. Ceramic:**

For both ADP7142 and ADP7182, we selected:
- **10µF tantalum + 100nF ceramic** (parallel combination)

**Why Tantalum:**
- ✅ ADP7142/7182 datasheets require specific ESR range for stability
- ✅ Tantalum has controlled ESR (~1Ω)
- ✅ Better decoupling at audio frequencies
- ✅ Proven stability

**Why NOT all-ceramic:**
- ❌ Modern X7R ceramics have very low ESR (<10mΩ)
- ❌ Can cause instability in some LDOs
- ❌ Would need careful selection of specific capacitor models
- ❌ Tantalum + ceramic combo is safer and more reliable

**Alternative considered: All-ceramic**
- Some newer LDOs (like LT3045) are specifically designed for ceramic-only output caps
- **Reason NOT chosen:** ADP7142/7182 datasheets explicitly recommend tantalum for the bulk capacitor

---

## 10. Connectors

### USB-C Connector

**Selected: Generic USB-C receptacle (e.g., HRO-TYPE-C-31-M-12)**

**Why USB-C instead of Micro-USB:**
- ✅ Modern standard
- ✅ Reversible (better user experience)
- ✅ More robust connector
- ✅ CC pins allow simple 5V detection

**Cons:**
- ❌ Slightly more expensive (~$0.50 vs ~$0.20 for Micro-USB)
- ❌ Larger footprint

**Reason chosen:** USB-C is becoming universal; Micro-USB is obsolete. Worth the extra cost for future-proofing.

### Battery Connector

**Selected: JST-PH 2-pin (2mm pitch)**

**Alternatives:**
- **JST-SH (1mm pitch):** Smaller but more fragile
- **JST-XH (2.5mm pitch):** Larger, for higher current
- **Molex PicoBlade:** Alternative brand

**Reason chosen:** JST-PH is the most common LiPo connector in hobby/electronics. 2mm pitch is robust enough for this application. Most pre-made LiPo cells come with JST-PH connectors.

### 9V Battery Connector

**Selected: Standard 9V battery snap (wire connection)**

**Reason:** Industry standard, universally available, users can easily replace battery.

---

## 11. Switches and LEDs

### Power Switch

**Selected: Slide switch, SPST, SMT**

**Alternatives considered:**
- **Push-button with latching circuit:** More complex, requires MCU or latch IC
- **Toggle switch:** Larger, through-hole
- **Rocker switch:** Too large for portable instrument

**Reason chosen:** Slide switch is simple, reliable, clear on/off indication, and commonly used in portable electronics.

### LEDs

**Selected: 0805 SMT LEDs (Red for charging, Green for power)**

**Why 0805:**
- ✅ Visible but not huge
- ✅ Easy hand soldering
- ✅ Wide availability

**Alternative: 0603**
- Smaller, but harder to see and solder

**Reason chosen:** 0805 is the sweet spot for visibility and ease of assembly.

---

## Summary: Cost vs. Performance Analysis

### Total Component Cost Breakdown:

| Category | Component | Cost | Justification |
|----------|-----------|------|---------------|
| **Charging** | MCP73831 | $0.50 | Simple, adequate |
| **Protection** | DW01A + FS8205A | $0.25 | Standard solution |
| **Power Mux** | BAT54C | $0.05 | Passive, simple |
| **Boost** | TPS61220 | $1.20 | Efficiency critical |
| **+5V LDO** | ADP7142 | $3.00 | **Noise critical** |
| **Inverter** | TPS60403 | $1.00 | Good efficiency |
| **-5V LDO** | ADP7182 | $3.00 | **Noise critical** |
| **Inductor** | VLS3012ET | $0.30 | Quality needed |
| **Capacitors** | Various | $2.00 | Tantalums + ceramics |
| **Resistors** | Various | $0.50 | Standard |
| **Connectors** | USB-C, JST, etc | $1.50 | Standard |
| **Switch & LEDs** | Various | $0.50 | Standard |
| **TOTAL** | | **~$13.80** | Per unit in small qty |

### Where We Spent Money (and Why):

**High-Value Components ($3 each):**
1. **ADP7142 (+5V LDO):** $3.00
2. **ADP7182 (-5V LDO):** $3.00

These two components represent 43% of the total BOM cost, but they are absolutely essential for the probe's performance. There's no cheaper alternative that would maintain the required noise performance.

**Alternative "Budget" Design:**

If we used cheap components everywhere:
- LM1117 instead of ADP7142: Save $2.70
- LM7905 instead of ADP7182: Save $2.60
- ICL7660 instead of TPS60403: Save $0.50
- Skip boost converter: Save $1.50
- **Total savings: ~$7.30**
- **New total: ~$6.50**

**But the result would be:**
- ❌ 40µVrms noise on +5V (vs. 9µVrms) = 4.4× worse
- ❌ >100µVrms noise on -5V (vs. 9µVrms) = 11× worse
- ❌ Poor PSRR, insufficient filtering
- ❌ LiPo only usable down to 5.5V (wasting 70% of capacity)
- ❌ **Probe would be essentially unusable for precision work**

**Conclusion:**
The $13.80 BOM is justified. We spent money where it matters (ultra-low noise) and saved money where it doesn't (passive OR-ing vs. active mux). This is a professional design optimized for a 200MHz differential probe, not a hobbyist power supply.

---

## Key Design Principles Applied

1. **Spend money on noise performance** - The LDOs are expensive but essential
2. **Keep it simple where possible** - Passive Schottky OR-ing instead of active mux
3. **Use proven, reliable parts** - Industry-standard components (MCP73831, DW01A, etc.)
4. **Optimize for the application** - 200MHz probe needs ultra-low noise
5. **Don't over-engineer** - We don't need 1µVrms noise when 9µVrms is sufficient
6. **Consider the user** - USB-C charging, clear LED indicators, simple operation

---

*End of Component Selection Summary*
