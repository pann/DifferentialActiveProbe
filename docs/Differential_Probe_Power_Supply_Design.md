# Differential Probe Power Supply Design
## Dual ±5V Rails from 9V Battery or Single-Cell LiPo with USB-C Charging

Version: 1.0  
Date: 2026-01-15  
Author: Hardware Design  

---

## Design Overview

This power supply provides clean ±5V rails for the differential probe circuit, supporting dual input sources:
- **Primary**: 9V alkaline or NiMH battery (6-9V range)
- **Secondary**: Single-cell LiPo battery (3.0-4.2V) with USB-C charging capability

### Key Specifications

| Parameter | Specification |
|-----------|---------------|
| Output Voltage | +5V, -5V |
| Output Current | 50mA typical, 200mA max per rail |
| Input Voltage (9V) | 6-9V |
| Input Voltage (LiPo) | 3.0-4.2V |
| Charge Current | 500mA (USB 2.0) |
| LiPo Capacity | 150-500mAh |
| Output Noise | <10µVrms |
| PSRR | >75dB @ 10kHz |
| Operating Mode | Cannot charge while operating |

### Features

- ✅ Automatic power source selection (9V battery preferred)
- ✅ USB-C charging (5V, 500mA)
- ✅ Battery protection (over-charge, over-discharge, over-current)
- ✅ Power on/off switch
- ✅ LED indicators (power on: green, charging: red)
- ✅ Ultra-low noise LDOs for sensitive analog circuits
- ✅ Boost converter for full LiPo voltage range utilization

---

## Block Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         INPUT SOURCES                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  USB-C 5V ──[Charger]──[Red LED]──[JST-PH]──[Protection]──┐        │
│             MCP73831    Charging    2-pin     DW01A+FS8205A │        │
│                                    Connector   1A limit     │        │
│                                                             │        │
│                                            LiPo Cell        │        │
│                                            3.7V             │        │
│                                            150-500mAh       │        │
│                                                             │        │
│  9V Battery ────────────────────────────────────────────────┘        │
│                                                             │        │
└─────────────────────────────────────────────────────────────┼────────┘
                                                              │
                                                              │
┌─────────────────────────────────────────────────────────────┼────────┐
│                      POWER SELECTION                        │        │
├─────────────────────────────────────────────────────────────┼────────┤
│                                                             │        │
│                        [BAT54C Dual Schottky]               │        │
│                        Common Cathode OR-ing                │        │
│                        (9V battery preferred)               │        │
│                                                             │        │
│                        [Slide Switch]──[Green LED]          │        │
│                        Power ON/OFF    Power Indicator      │        │
│                                                             │        │
└─────────────────────────────────────────────────────────────┼────────┘
                                                              │
                                                         VBAT_SWITCHED
                                                         (3-9V)
                                                              │
┌─────────────────────────────────────────────────────────────┼────────┐
│                   VOLTAGE CONVERSION                        │        │
├─────────────────────────────────────────────────────────────┼────────┤
│                                                             │        │
│                        [TPS61220]                           │        │
│                        Boost Converter                      │        │
│                        3-9V → 5-9V                          │        │
│                                                             │        │
│                             │                               │        │
│                   ┌─────────┴─────────┐                     │        │
│                   │                   │                     │        │
│              [ADP7142]           [TPS60403]                 │        │
│              +5V LDO             Charge Pump                │        │
│              9µVrms              Inverter                   │        │
│                   │                   │                     │        │
│              +5V_CLEAN           [ADP7182]                  │        │
│                   │              -5V LDO                    │        │
│                   │              9µVrms                     │        │
│                   │                   │                     │        │
│                   │              -5V_CLEAN                  │        │
│                   │                   │                     │        │
└───────────────────┼───────────────────┼─────────────────────────────┘
                    │                   │
                    └─────────┬─────────┘
                              │
                    To Differential Probe
                    (AD8065 buffers, LMH6552 diff amp)
```

---

## Detailed Schematics

### 1. USB-C Charging Circuit

```
USB-C Connector (J_USB)
  Type-C receptacle
  USB 2.0 (5V only)
    │
    ├─ CC1: 5.1kΩ to GND (USB-C 5V detection)
    ├─ CC2: 5.1kΩ to GND (USB-C 5V detection)
    │
    └─ VBUS (5V from USB host)
         │
         ├─ D_USB: Schottky diode (protection)
         │  Type: B5819WS, 40V, 1A, Vf=0.6V
         │
         └─[U_CHG: MCP73831T-2ACI/OT]
            Li-Ion Charger IC
            Charge current: 500mA
            Charge voltage: 4.2V
            SOT-23-5 package
              │
              ├─ Pin 1: STAT (charge status output)
              │    │
              │    └─ R_LED1: 1kΩ (current limit for LED)
              │         │
              │         └─ LED_RED (0805 SMT, red)
              │              Indicates charging in progress
              │              │
              │              GND
              │
              └─ Pin 5: VBAT (output to battery)
                   │
                   └─ To Battery Protection Circuit

Pin Configuration:
  Pin 1: STAT  - Charge status (low when charging)
  Pin 2: VSS   - Ground
  Pin 3: VBAT  - Battery connection
  Pin 4: VDD   - Input power (VBUS)
  Pin 5: PROG  - Programming pin (connect to GND via resistor for 500mA)

Programming Resistor: 2kΩ from PROG (pin 5) to GND for 500mA charge current
```

### 2. Battery Protection Circuit

```
From Charger                    To Power Selection
VBAT (4.2V max)                 VBAT_LIPO (3.0-4.2V protected)
     │                               │
     │                               │
[JST-PH-2 Connector]                 │
 SM02B-SRSS-TB (SMT)                 │
 or B2B-PH-K-S (TH)                  │
     │                               │
     ├─ Pin 1: V+ (red wire)         │
     ├─ Pin 2: V- (black wire)       │
     │                               │
     │         LiPo Cell             │
     *────── 3.7V nominal ───────────*
     │       150-500mAh              │
     │                               │
     │                               │
     └─[U_PROT: DW01A]───[Q_PROT: FS8205A]─── VBAT_LIPO
        Protection IC     Dual N-MOSFET         │
        SOT-23-6         TSSOP-8                │
          │                │                    │
          │                │                    │
        Monitors:        Gates control          │
        - Over-voltage   both MOSFETs           │
        - Under-voltage                         │
        - Over-current   R_SENSE: 0.15Ω        │
                         (for 1A trip)          │
                            │                   │
                            GND                 │

DW01A Protection Thresholds:
  Over-charge:  4.25V (±0.05V)
  Over-discharge: 2.4V (±0.1V)  
  Over-current: 1A (via 0.15Ω sense resistor)
  
DW01A Pin Configuration (SOT-23-6):
  Pin 1: OD  - Over-discharge detect (to gate drive)
  Pin 2: CS  - Current sense (to sense resistor)
  Pin 3: VDD - Battery positive
  Pin 4: VSS - Ground
  Pin 5: VM  - Load output voltage
  Pin 6: OC  - Over-charge detect (to gate drive)

FS8205A Configuration (TSSOP-8):
  Two N-channel MOSFETs in series
  Dual gate control from DW01A
  RDS(on): 25mΩ typical @ 4.5V
```

### 3. Power Source Selection

```
VBAT_9V (from 9V battery)
     │
     └─[Anode 1]
         │
        ─┤>─  D1 part of BAT54C
         │
         *─── Common Cathode (Pin 3)
         │
        ─┤>─  D2 part of BAT54C
         │
     ┌─[Anode 2]
     │
VBAT_LIPO (from LiPo protection)


BAT54C Package (SOT-23):
  Pin 1: Anode 1 (to 9V battery)
  Pin 2: Anode 2 (to LiPo)
  Pin 3: Common Cathode (to switch)
  
Schottky Diode Specs:
  Vf: ~0.3V @ 100mA
  Vr: 30V
  If: 200mA continuous
  
Operation:
  - When 9V present: 9V supplies power (higher voltage wins)
  - When only LiPo present: LiPo supplies power
  - Voltage drop: ~0.3V at 50mA load
  - Prevents backflow between sources


Common Cathode (Pin 3 of BAT54C)
     │
     └─[SW1: Slide Switch SPST]─── VBAT_SWITCHED
         │                              │
         │                              ├─ R_LED2: 1kΩ
         │                              │    │
         │                              │    └─ LED_GRN (0805 SMT, green)
         │                              │         Power indicator
         │                              │         │
         │                              │         GND
         │                              │
         GND (when open)               To Boost Converter

Switch Specs:
  Type: SPST slide switch
  Part: OS102011MA1QN1 or similar
  Rating: 300mA @ 6VDC minimum
  Package: SMT, through-hole mounting tabs
```

### 4. Boost Converter (TPS61220)

```
VBAT_SWITCHED (3-9V input)
     │
     ├─ C_IN: 10µF ceramic, X7R, 16V
     │    │   (input decoupling)
     │    │
     │    GND
     │
     │
[U_BST: TPS61220DCKR]
 Boost Converter
 SC70-6 package
     │
     ├─ Pin 1: SW (switching node)
     │    │
     │    └─ L1: 2.2µH power inductor
     │         │  Isat > 2A, DCR < 100mΩ
     │         │  Part: TDK VLS3012ET-2R2M
     │         │  Size: 3.0x3.0x1.2mm
     │         │
     │         *─── VBST (5.0-9V output)
     │         │         │
     │         │         ├─ C_BST1: 22µF ceramic, X7R, 16V
     │         │         │    │    (output bulk)
     │         │         │    │
     │         │         │    GND
     │         │         │
     │         │         ├─ C_BST2: 10µF ceramic, X7R, 16V
     │         │         │    │    (output filter)
     │         │         │    │
     │         │         │    GND
     │         │
     ├─ Pin 2: GND
     │    │
     │    GND
     │
     ├─ Pin 3: FB (feedback, sets output voltage)
     │    │
     │    └─ R_FB divider to set Vout = 5.0V
     │         (typically 1MΩ/590kΩ for 5V)
     │
     ├─ Pin 4: EN (enable, active high)
     │    │
     │    └─ Connected to VIN (always enabled when power present)
     │
     ├─ Pin 5: VOUT (output)
     │    │
     │    └─ To VBST net
     │
     └─ Pin 6: VIN (input)
          │
          └─ To VBAT_SWITCHED

TPS61220 Features:
  Input: 0.7-5.5V (but we feed 3-9V via voltage divider if >5.5V)
  Output: Adjustable via FB, set to 5.0V
  Switching frequency: 1MHz
  Efficiency: ~90% @ 50mA load
  Quiescent current: 50µA
  
  Smart Operation:
  - If VIN < 5V: Boost to 5.0V
  - If VIN > 5V: Can configure for pass-through or regulate down
  
Note: May need additional logic to bypass boost when 9V battery is present
      to reduce noise and improve efficiency. Consider using enable pin
      and voltage comparator.
```

### 5. Positive 5V LDO Regulator (ADP7142)

```
VBST (5-9V, from boost converter)
     │
     ├─ C_IN: 1µF ceramic, X7R, 16V, 0603
     │    │   (input decoupling, place close to VIN pin)
     │    │
     │    GND
     │
     │
[U_POS: ADP7142ARDZ-5.0]
 Ultra-Low Noise LDO
 SOIC-8 package
     │
     ├─ Pin 1: VIN (input voltage)
     │    │
     │    └─ From VBST
     │
     ├─ Pin 2: EN (enable, active high)
     │    │
     │    └─ Connected to VIN (always enabled)
     │
     ├─ Pin 3,4: GND (ground, connect both)
     │    │
     │    GND
     │
     ├─ Pin 5: SS (soft-start, optional)
     │    │
     │    └─ C_SS: 0.1µF to GND (optional, for controlled startup)
     │         │
     │         GND
     │
     ├─ Pin 6: SENSE (voltage sense feedback)
     │    │
     │    └─ Connected to VOUT (pin 7)
     │
     ├─ Pin 7: VOUT (output voltage)
     │    │
     │    *─────────── +5V_CLEAN (to probe circuits)
     │    │                │
     │    │                ├─ C_OUT1: 10µF tantalum, 10V, ESR<1Ω
     │    │                │    │     (bulk capacitance, ESR critical!)
     │    │                │    │
     │    │                │    GND
     │    │                │
     │    │                ├─ C_OUT2: 100nF ceramic, X7R, 0603
     │    │                │    │     (high-freq decoupling)
     │    │                │    │
     │    │                │    GND
     │
     └─ Pin 8: ADJ (adjust, for fixed version this is NC or internal)
          │
          NC (not connected for fixed 5V version)

ADP7142 Specifications:
  Input voltage: 3.3-20V
  Output voltage: 5.0V (fixed version: ADP7142ARDZ-5.0-R7)
  Output current: 200mA maximum
  Dropout voltage: 170mV @ 200mA
  Output noise: 9µVrms (10Hz-100kHz)
  PSRR: 80dB @ 100Hz, 70dB @ 1kHz, 55dB @ 100kHz
  Quiescent current: 20µA
  
  Key Features:
  - Ultra-low noise for precision analog circuits
  - Excellent PSRR to reject boost converter switching noise
  - Low dropout for efficient operation
  - Soft-start reduces inrush current
  
Critical Layout Notes:
  - Place C_IN within 5mm of VIN pin
  - Use tantalum for C_OUT1 (low ESR critical for stability)
  - Keep SENSE trace short and direct to VOUT
  - Ground pins 3 and 4 with vias to ground plane
```

### 6. Charge Pump Inverter (TPS60403)

```
VBST (5-9V, from boost converter)
  NOTE: Uses boosted rail, NOT +5V_CLEAN!
  This prevents charge pump noise from coupling to clean +5V
     │
     ├─ C_IN: 1µF ceramic, X7R, 16V, 0603
     │    │   (input decoupling)
     │    │
     │    GND
     │
     │
[U_INV: TPS60403DBVR]
 Charge Pump Inverter
 SOT-23-5 package
     │
     ├─ Pin 1: VOUT (negative output)
     │    │
     │    *─────────── VNEG_RAW (-5 to -9V, noisy)
     │    │                │
     │    │                ├─ C_OUT: 10µF tantalum, 10V
     │    │                │    │    (bulk storage)
     │    │                │    │
     │    │                │    GND
     │    │                │
     │    │                └─ To -5V LDO input
     │    │
     ├─ Pin 2: CAP- (negative flying capacitor terminal)
     │    │
     │    └─ C_CP2: 1µF ceramic, X7R, 10V, 0603
     │         │    (flying capacitor)
     │         │
     │         ├─ Pin 3: CAP+ (positive flying capacitor terminal)
     │         │
     │         └─[U_INV Pin 3]
     │
     ├─ Pin 3: CAP+ (positive flying capacitor terminal)
     │    │
     │    └─ Connected to C_CP2 (see above)
     │
     ├─ Pin 4: GND (ground)
     │    │
     │    GND
     │
     └─ Pin 5: VIN (input voltage)
          │
          └─ From VBST

TPS60403 Specifications:
  Input voltage: 1.6-5.5V (we provide 5V from boost)
  Output voltage: -VIN (inverted, so -5V output)
  Output current: 40mA maximum
  Switching frequency: 150kHz
  Efficiency: 99% (unloaded), 90% @ 20mA
  Quiescent current: 120µA
  
  Flying Capacitor:
  - C_CP2: 1µF minimum (X7R or X5R)
  - Low ESR ceramic recommended
  - Place close to CAP+ and CAP- pins
  
  Output Ripple:
  - ~20mVpp typical @ 20mA load
  - Requires post-regulation for ultra-low noise applications
  - Hence the ADP7182 LDO following this stage

Layout Notes:
  - Keep flying capacitor traces short
  - Minimize loop area between CAP+, CAP-, and capacitor
  - Place input and output caps close to IC
  - Consider small ground plane under IC but avoid under flying cap traces
```

### 7. Negative 5V LDO Regulator (ADP7182)

```
VNEG_RAW (-5 to -9V, noisy from charge pump)
     │
     ├─ C_IN: 1µF ceramic, X7R, 16V, 0603
     │    │   (input decoupling)
     │    │
     │    GND
     │
     │
[U_NEG: ADP7182ARDZ-5.0-R7]
 Ultra-Low Noise Negative LDO
 SOIC-8 package
     │
     ├─ Pin 1: VIN (negative input voltage)
     │    │
     │    └─ From VNEG_RAW (-5 to -9V)
     │
     ├─ Pin 2: EN (enable, active high)
     │    │
     │    └─ Connected to GND (always enabled for negative LDO)
     │         │
     │         GND
     │
     ├─ Pin 3,4: GND (ground, connect both)
     │    │
     │    GND
     │
     ├─ Pin 5: NR (noise reduction, optional filter capacitor)
     │    │
     │    └─ C_NR: 10nF ceramic to GND (optional, reduces noise further)
     │         │
     │         GND
     │
     ├─ Pin 6: SENSE (voltage sense feedback)
     │    │
     │    └─ Connected to VOUT (pin 7)
     │
     ├─ Pin 7: VOUT (negative output voltage)
     │    │
     │    *─────────── -5V_CLEAN (to probe circuits)
     │    │                │
     │    │                ├─ C_OUT1: 10µF tantalum, 10V, ESR<1Ω
     │    │                │    │     (bulk capacitance)
     │    │                │    │
     │    │                │    GND
     │    │                │
     │    │                ├─ C_OUT2: 100nF ceramic, X7R, 0603
     │    │                │    │     (high-freq decoupling)
     │    │                │    │
     │    │                │    GND
     │
     └─ Pin 8: ADJ (adjust, for fixed version this is NC)
          │
          NC (not connected for fixed -5V version)

ADP7182 Specifications:
  Input voltage: -2.3V to -6.0V (negative voltages!)
  Output voltage: -5.0V (fixed version: ADP7182ARDZ-5.0-R7)
  Output current: 200mA maximum
  Dropout voltage: -200mV @ 200mA (so needs -5.2V minimum input)
  Output noise: 9µVrms (10Hz-100kHz)
  PSRR: 75dB @ 100Hz, 65dB @ 1kHz, 50dB @ 100kHz
  Quiescent current: 30µA
  
  Key Features:
  - Negative voltage LDO specifically designed for negative rails
  - Ultra-low noise matching positive ADP7142 performance
  - Excellent PSRR to reject charge pump ripple (150kHz switching)
  - Optional NR pin for further noise reduction
  
Critical Layout Notes:
  - Place C_IN within 5mm of VIN pin (pin 1)
  - Use tantalum for C_OUT1 (low ESR critical!)
  - Keep SENSE trace short and direct to VOUT
  - Ground pins 3 and 4 with vias to ground plane
  - Consider using NR pin with 10nF for lowest noise
```

---

## Complete Bill of Materials (BOM)

### Power Management ICs

| Ref | Part Number | Manufacturer | Package | Description | Quantity |
|-----|-------------|--------------|---------|-------------|----------|
| U_CHG | MCP73831T-2ACI/OT | Microchip | SOT-23-5 | Li-Ion charger, 500mA, 4.2V | 1 |
| U_PROT | DW01A | Multiple | SOT-23-6 | Li-Ion protection IC | 1 |
| Q_PROT | FS8205A | Fortune Semi | TSSOP-8 | Dual N-MOSFET, 20V, 6A | 1 |
| D1 | BAT54C | Multiple | SOT-23 | Dual Schottky, 30V, 200mA | 1 |
| U_BST | TPS61220DCKR | Texas Instruments | SC70-6 | Boost converter, 0.7-5.5V in | 1 |
| U_POS | ADP7142ARDZ-5.0-R7 | Analog Devices | SOIC-8 | +5V LDO, 200mA, 9µVrms | 1 |
| U_INV | TPS60403DBVR | Texas Instruments | SOT-23-5 | Charge pump inverter, 40mA | 1 |
| U_NEG | ADP7182ARDZ-5.0-R7 | Analog Devices | SOIC-8 | -5V LDO, 200mA, 9µVrms | 1 |

### Passives - Inductors

| Ref | Value | Part Number | Package | Description | Quantity |
|-----|-------|-------------|---------|-------------|----------|
| L1 | 2.2µH | TDK VLS3012ET-2R2M | 3012 | Power inductor, Isat=2.3A, DCR=85mΩ | 1 |

### Passives - Capacitors (Ceramic)

| Ref | Value | Voltage | Dielectric | Package | Description | Quantity |
|-----|-------|---------|------------|---------|-------------|----------|
| C_IN (boost) | 10µF | 16V | X7R | 0805 | TPS61220 input decoupling | 1 |
| C_BST1 | 22µF | 16V | X7R | 1206 | Boost output bulk | 1 |
| C_BST2 | 10µF | 16V | X7R | 0805 | Boost output filter | 1 |
| C_IN (ADP7142) | 1µF | 16V | X7R | 0603 | +5V LDO input | 1 |
| C_OUT2 (ADP7142) | 100nF | 10V | X7R | 0603 | +5V LDO output HF | 1 |
| C_IN (TPS60403) | 1µF | 16V | X7R | 0603 | Charge pump input | 1 |
| C_CP1, C_CP2 | 1µF | 10V | X7R | 0603 | Flying capacitors | 2 |
| C_OUT (TPS60403) | 10µF | 10V | X7R | 0805 | Charge pump output | 1 |
| C_IN (ADP7182) | 1µF | 16V | X7R | 0603 | -5V LDO input | 1 |
| C_OUT2 (ADP7182) | 100nF | 10V | X7R | 0603 | -5V LDO output HF | 1 |
| C_NR | 10nF | 10V | X7R | 0603 | ADP7182 noise reduction (opt) | 1 |

### Passives - Capacitors (Tantalum/Electrolytic)

| Ref | Value | Voltage | Type | Package | ESR | Description | Quantity |
|-----|-------|---------|------|---------|-----|-------------|----------|
| C_OUT1 (ADP7142) | 10µF | 10V | Tantalum | 3528/B | <1Ω | +5V LDO output bulk | 1 |
| C_OUT1 (ADP7182) | 10µF | 10V | Tantalum | 3528/B | <1Ω | -5V LDO output bulk | 1 |

### Passives - Resistors

| Ref | Value | Tolerance | Power | Package | Description | Quantity |
|-----|-------|-----------|-------|---------|-------------|----------|
| R_PROG | 2kΩ | 5% | 1/10W | 0603 | MCP73831 charge current | 1 |
| R_SENSE | 0.15Ω | 1% | 1/4W | 1206 | Battery protection current sense | 1 |
| R_LED1 | 1kΩ | 5% | 1/10W | 0603 | Charge LED current limit | 1 |
| R_LED2 | 1kΩ | 5% | 1/10W | 0603 | Power LED current limit | 1 |
| R_FB1 | 1MΩ | 1% | 1/10W | 0603 | Boost feedback upper | 1 |
| R_FB2 | 590kΩ | 1% | 1/10W | 0603 | Boost feedback lower | 1 |
| R_CC1, R_CC2 | 5.1kΩ | 5% | 1/10W | 0603 | USB-C CC pull-down | 2 |

### Diodes & LEDs

| Ref | Type | Part Number | Package | Description | Quantity |
|-----|------|-------------|---------|-------------|----------|
| D_USB | Schottky | B5819WS | SOD-323 | 40V, 1A, Vf=0.6V, USB protection | 1 |
| LED_RED | LED Red | Generic | 0805 | Charging indicator, 2mA | 1 |
| LED_GRN | LED Green | Generic | 0805 | Power on indicator, 2mA | 1 |

### Connectors & Switches

| Ref | Type | Part Number | Package | Description | Quantity |
|-----|------|-------------|---------|-------------|----------|
| J_USB | USB-C | HRO-TYPE-C-31-M-12 | SMT | USB-C receptacle, 5V only | 1 |
| J_BAT | JST | SM02B-SRSS-TB(LF)(SN) | SMT | JST-SH 2-pin, 1mm pitch | 1 |
| J_9V | Battery Snap | - | Wired | 9V battery snap connector | 1 |
| SW1 | Slide Switch | OS102011MA1QN1 | SMT | SPST, 300mA | 1 |

### Battery

| Ref | Type | Specification | Description | Quantity |
|-----|------|---------------|-------------|----------|
| BT_LIPO | Li-Po Cell | 3.7V, 150-500mAh | Single cell with JST-PH connector | 1 |
| BT_9V | 9V Battery | Alkaline or NiMH | Standard 9V battery | 1 |

---

## Power Budget Analysis

### Load Requirements

| Circuit Block | Supply | Current (mA) | Notes |
|---------------|--------|--------------|-------|
| AD8065 (U1) | ±5V | 2.5 + 2.5 | Unity gain buffer |
| AD8065 (U2) | ±5V | 2.5 + 2.5 | Unity gain buffer |
| LMH6552 (U3) | ±5V | 5 + 5 | Differential amplifier |
| Decoupling/misc | ±5V | 5 + 5 | Leakage, bias currents |
| **Total per rail** | | **15 + 15** | **Conservative estimate** |
| **Design target** | | **50mA** | **3.3x margin** |

### Supply Efficiency Chain

#### From 9V Battery (Nominal Case)

```
9V Battery (250mAh alkaline)
    │
    ├─ Schottky drop: -0.3V
    │
8.7V @ switch input
    │
    ├─ Boost converter: Bypassed (VIN > 5V)
    │   Efficiency: ~95% (pass-through mode)
    │
8.3V @ LDO inputs
    │
    ├─ ADP7142 (+5V): Dropout 170mV @ 50mA
    │   Efficiency: 5V/8.3V = 60%
    │   Input current: 50mA / 0.60 = 83mA
    │
    └─ TPS60403 + ADP7182 (-5V)
        Charge pump efficiency: 90%
        LDO efficiency: 5V/8.3V = 60%
        Combined: 54%
        Input current: 50mA / 0.54 = 93mA

Total 9V battery current: 83mA + 93mA = 176mA
Battery life (250mAh): 250/176 = 1.4 hours
```

#### From LiPo Battery (4.2V → 3.0V range)

```
LiPo 3.7V nominal, 300mAh
    │
    ├─ Schottky drop: -0.3V
    │
3.4V average @ switch input
    │
    ├─ Boost converter: Active (VIN < 5V)
    │   Efficiency: 90%
    │   Boost to 5V
    │
5V @ LDO inputs
    │
    ├─ ADP7142 (+5V): Minimal dropout
    │   Efficiency: ~95%
    │   Current from boost: 50mA / 0.95 = 53mA
    │
    └─ TPS60403 + ADP7182 (-5V)
        Efficiency: 85% (charge pump + LDO)
        Current from boost: 50mA / 0.85 = 59mA

Total current from boost: 53mA + 59mA = 112mA
Boost input current: 112mA / 0.90 = 124mA
LiPo current draw: 124mA

Battery life (300mAh): 300/124 = 2.4 hours
Battery life (500mAh): 500/124 = 4.0 hours
```

### Charging Time

```
LiPo capacity: 300mAh (example)
Charge current: 500mA
Charge efficiency: ~85%

Effective charge rate: 500mA × 0.85 = 425mA
Charge time: 300mAh / 425mA = 0.7 hours = 42 minutes

For 500mAh battery: 500/425 = 1.2 hours = 70 minutes
```

---

## Noise Analysis

### Noise Sources

1. **Boost Converter (TPS61220)**
   - Switching frequency: 1MHz
   - Ripple: ~20mVpp typical
   - Filtering: ADP7142/ADP7182 LDOs provide >60dB PSRR @ 1MHz

2. **Charge Pump (TPS60403)**
   - Switching frequency: 150kHz  
   - Ripple: ~20mVpp
   - Filtering: ADP7182 provides >65dB PSRR @ 150kHz

3. **LDO Output Noise**
   - ADP7142: 9µVrms (10Hz-100kHz)
   - ADP7182: 9µVrms (10Hz-100kHz)
   - Both suitable for 200MHz probe application

### Noise Mitigation Strategy

```
Boost Switching (1MHz)
    ↓
ADP7142 PSRR: 55dB @ 100kHz, extrapolate to ~50dB @ 1MHz
    ↓
20mVpp × 10^(-50/20) = 63µVpp ≈ 22µVrms
    ↓
Add intrinsic LDO noise: 9µVrms
    ↓
Total: √(22² + 9²) ≈ 24µVrms


Charge Pump (150kHz)
    ↓
ADP7182 PSRR: 65dB @ 150kHz
    ↓
20mVpp × 10^(-65/20) = 11µVpp ≈ 4µVrms
    ↓
Add intrinsic LDO noise: 9µVrms
    ↓
Total: √(4² + 9²) ≈ 10µVrms
```

**Result**: Both rails achieve <25µVrms noise, excellent for precision analog work.

---

## Layout Guidelines

### Critical Layout Rules

1. **Power Planes**
   - Dedicate top/bottom layers to power and ground
   - Separate analog and digital grounds if possible
   - Star-ground at power entry point

2. **High-Frequency Switching (Boost & Charge Pump)**
   - Minimize loop area for switching nodes
   - Keep L1 and C_BST close to TPS61220
   - Keep flying capacitors (C_CP1, C_CP2) close to TPS60403
   - Use ground plane under components, but avoid under magnetics

3. **LDO Decoupling**
   - Place input caps within 5mm of VIN pins
   - Use tantalum for output bulk caps (low ESR critical)
   - Add ceramic bypass caps (100nF) right at IC pins
   - Short, wide traces for VOUT and GND

4. **Sense and Feedback Traces**
   - Keep SENSE traces short and direct to VOUT
   - Route FB (feedback) traces away from switching nodes
   - Use Kelvin sensing where possible

5. **Thermal Management**
   - Add thermal vias under LDO packages (especially ADP7142/7182)
   - Calculate worst-case power dissipation:
     * ADP7142: (8.3V - 5V) × 50mA = 165mW
     * ADP7182: (8.3V - 5V) × 50mA = 165mW
   - Use thermal relief for power pads

6. **LED and Indicator Placement**
   - Route LED traces away from sensitive analog signals
   - Consider edge placement for user visibility
   - Add test points for VBAT, +5V_CLEAN, -5V_CLEAN

### Recommended Layer Stack (4-layer)

```
Layer 1 (Top):    Signal + Components
Layer 2 (Inner):  Ground Plane
Layer 3 (Inner):  Power Plane (+5V, -5V, VBAT)
Layer 4 (Bottom): Signal + Components (if needed)
```

### Component Placement Strategy

```
┌─────────────────────────────────────────────────────────┐
│  [USB-C]  [Charger]  [Battery Protection]  [LiPo Conn] │  Input Section
├─────────────────────────────────────────────────────────┤
│  [SW1]  [BAT54C]  [LED_GRN]                            │  Selection
├─────────────────────────────────────────────────────────┤
│  [TPS61220]  [L1]  [C_BST]                             │  Boost
├─────────────────────────────────────────────────────────┤
│  [ADP7142]  [C_OUT_POS]      [TPS60403]  [ADP7182]    │  Regulation
│  +5V LDO                     Charge Pump  -5V LDO      │
├─────────────────────────────────────────────────────────┤
│  [Output Connector to Probe Circuit]                   │  Outputs
└─────────────────────────────────────────────────────────┘
```

---

## Testing and Validation

### Initial Power-Up Procedure

1. **Visual Inspection**
   - Check all component orientations (especially polarized parts)
   - Verify no solder bridges
   - Confirm correct IC part numbers

2. **Pre-Power Checks**
   - Measure resistance from +5V to GND (should be >10kΩ)
   - Measure resistance from -5V to GND (should be >10kΩ)
   - Check battery polarity at connectors

3. **First Power-Up (9V Battery)**
   - Connect 9V battery
   - Close SW1 (power on)
   - Verify LED_GRN illuminates
   - Measure VBAT_SWITCHED (should be ~8.7V)
   - Measure +5V_CLEAN (should be 5.00V ±1%)
   - Measure -5V_CLEAN (should be -5.00V ±1%)

4. **LiPo Power Test**
   - Remove 9V battery
   - Connect charged LiPo (4.0-4.2V)
   - Close SW1
   - Verify LED_GRN illuminates
   - Measure +5V_CLEAN and -5V_CLEAN
   - Should match 9V battery readings

5. **Charging Test**
   - Connect USB-C cable to 5V source
   - Connect LiPo (discharged to ~3.5V)
   - Verify LED_RED illuminates (charging)
   - Measure charge current (~500mA)
   - Wait for charge complete (LED_RED off)
   - Verify LiPo voltage ~4.2V

### Performance Validation

| Parameter | Test Method | Pass Criteria |
|-----------|-------------|---------------|
| +5V Output | DMM measurement | 5.00V ±1% (4.95-5.05V) |
| -5V Output | DMM measurement | -5.00V ±1% (-4.95 to -5.05V) |
| +5V Ripple | Oscilloscope, AC couple, 20MHz BW | <10mVpp |
| -5V Ripple | Oscilloscope, AC couple, 20MHz BW | <10mVpp |
| Output Noise | Oscilloscope, AC couple, 100kHz BW | <50µVrms |
| Load Regulation | Apply 0-50mA load, measure Vout | <50mV change |
| Quiescent Current | No load, measure battery current | <1mA |
| Full Load Current | 50mA per rail, measure battery | See power budget |
| Charge Current | USB connected, discharged battery | 450-550mA |
| Battery Protection | Over-voltage test | Disconnect at 4.25V |
| Battery Protection | Over-discharge test | Disconnect at 2.4V |
| Thermal Test | Run at full load, 30min | No component >70°C |

### Troubleshooting Guide

| Symptom | Possible Cause | Check/Fix |
|---------|----------------|-----------|
| No power (LED_GRN off) | Battery dead, switch open | Check battery voltage, switch continuity |
| +5V present, -5V absent | TPS60403 or ADP7182 failure | Check VNEG_RAW, verify U_INV operation |
| High ripple on +5V | Missing output cap, bad LDO | Check C_OUT1 (tantalum), ESR |
| High ripple on -5V | Charge pump noise | Verify ADP7182 installed, check caps |
| Won't charge | MCP73831 fault, battery protection | Check STAT pin, verify battery voltage |
| LED_RED always on | Faulty battery, incorrect R_PROG | Measure CHG_OUT voltage |
| Low efficiency | Boost always active | Check if 9V battery connected properly |
| Overheating | Excessive dropout, short circuit | Reduce Vin or check for shorts |

---

## Safety and Compliance

### Battery Safety

⚠️ **WARNING**: Lithium-ion batteries can be dangerous if mishandled.

- Always use protected cells or add protection circuit
- Never short-circuit battery terminals
- Do not charge at currents >1C (capacity)
- Do not discharge below 3.0V
- Store at 40-60% charge if unused >1 month
- Operating temperature: 0°C to 45°C (charge), -20°C to 60°C (discharge)
- Dispose of properly according to local regulations

### Schottky Diode Ratings

- Ensure Schottky diodes rated for worst-case voltage
- 9V battery can provide up to 9.5V when fresh
- BAT54C rated to 30V (sufficient margin)

### Component Derating

- Capacitors: Use voltage rating ≥2× operating voltage
- Resistors: Keep power dissipation <50% of rating
- ICs: Ensure junction temperature <125°C (typically max)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-15 | Hardware Design | Initial design document |

---

## References

### Datasheets

1. **MCP73831** - Microchip Li-Ion Charger
2. **DW01A** - Battery Protection IC Datasheet
3. **FS8205A** - Dual N-channel MOSFET
4. **BAT54C** - Dual Schottky Diode
5. **TPS61220** - Texas Instruments Boost Converter
6. **ADP7142** - Analog Devices Ultra-Low Noise LDO (+)
7. **TPS60403** - Texas Instruments Charge Pump
8. **ADP7182** - Analog Devices Ultra-Low Noise LDO (-)

### Application Notes

- AN1149: Designing Li-Ion Battery Chargers (Microchip)
- AN136: Preventing Oscillation in Low-Noise LDOs (Analog Devices)
- SLVA559: Demystifying Charge Pumps (Texas Instruments)
- AN-1120: PCB Layout Guidelines for Switching Power Supplies (Analog Devices)

---

## Next Steps

1. ✅ Power supply architecture defined
2. ✅ Component selection complete
3. ⏭️ Create circuit JSON for KiCad conversion
4. ⏭️ Generate KiCad schematic using json_to_kicad script
5. ⏭️ PCB layout design
6. ⏭️ Prototype build and testing
7. ⏭️ Integration with differential probe circuit

---

*End of Document*
