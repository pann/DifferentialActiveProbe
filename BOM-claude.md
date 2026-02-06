# Bill of Materials - Differential Active Probe

**Project:** 200MHz Differential Probe with Dual ±5V Power Supply
**Version:** 1.1 (with JLCPCB Part Numbers)
**Date:** 2026-02-05

---

## Summary

| Category | Component Count | JLCPCB Est. Cost |
|----------|----------------|------------------|
| ICs (Power) | 7 | ~$14.50 |
| ICs (Analog) | 1 | ~$6.60 |
| Connectors | 5 | ~$2.50 |
| Diodes/LEDs | 6 | ~$0.10 |
| Inductors | 1 | ~$0.12 |
| Capacitors | 20 | ~$0.70 |
| Resistors | 16 | ~$0.10 |
| **Total (JLCPCB)** | **56** | **~$24.50** |

**Note:** Precision resistors (R1-R5) and Murata trimmer capacitors must be ordered separately from DigiKey (~$8 additional).

---

## 1. Integrated Circuits

### Power Supply ICs

| Ref | Value | Description | JLCPCB# | Price | Stock |
|-----|-------|-------------|---------|-------|-------|
| U2 | DW01A | Battery Protection IC | **C18164398** | $0.023 | 20k+ |
| U3 | TPS61220DCKR | Boost Converter | **C15421** | $0.82 | 966 |
| U5 | TPS60403DBVR | Charge Pump Inverter | **C11338** | $0.32 | 19k |
| U6 | ADP7142AUJZ-5.0-R7 | +5V Ultra-Low Noise LDO | **C659367** | $4.07 | 1,794 |
| U7 | MCP73831T-2ACI/OT | Li-Ion Charger IC | **C424093** | $0.70 | 14k |
| U8 | ADP7182AUJZ-5.0-R7 | -5V Ultra-Low Noise LDO | **C514357** | $2.36 | 2,787 |
| Q1 | FS8205A | Dual MOSFET (Batt Protect) | **C2830320** | $0.052 | 22k |

### Analog ICs

| Ref | Value | Description | JLCPCB# | Price | Stock |
|-----|-------|-------------|---------|-------|-------|
| U1 | AD8130ARZ-REEL7 | 270MHz Differential Receiver | **C41661** | $6.57 | 677 |

---

## 2. Connectors

| Ref | Value | Description | JLCPCB# | Price | Stock |
|-----|-------|-------------|---------|-------|-------|
| J2 | TYPE-C-31-M-12 | USB-C Receptacle | **C165948** | $0.17 | 322k |
| J3 | S2B-PH-K-S | JST-PH 2-pin (9V Battery) | **C173752** | $0.034 | 103k |
| J5 | BNC-KF | BNC PCB Mount (alternative) | **C20415781** | $0.89 | 1,400 |
| J6 | S2B-PH-K-S | JST-PH 2-pin (LiPo) | **C173752** | $0.034 | 103k |
| SW1 | PCM12SMTR | SPDT Slide Switch | **C221841** | $1.12 | 10k |

**Note:** Original Amphenol B6252HB-NPP3G-50 BNC is not available on JLCPCB. Alternative BNC-KF provided, or hand-solder from DigiKey.

---

## 3. Diodes and LEDs

| Ref | Value | Description | JLCPCB# | Price | Stock |
|-----|-------|-------------|---------|-------|-------|
| D1, D2 | PESD5V0S1BA | TVS Diode 5V (SOD-323) | **C2827694** | $0.015 | 588k |
| D3, D5 | BAT54C | Dual Schottky (SOT-23) | **C2135** | $0.016 | 401k |
| D4 | KT-0805R | Red LED 0805 | **C2295** | $0.0078 | 143k |
| D6 | KT-0805G | Green LED 0805 | **C2297** | $0.011 | 2.4M |

---

## 4. Inductors

| Ref | Value | Description | JLCPCB# | Price | Stock |
|-----|-------|-------------|---------|-------|-------|
| L1 | VLS3012ET-2R2M | 2.2µH Shielded Inductor | **C136233** | $0.12 | In stock |

---

## 5. Capacitors

### Power Supply Capacitors

| Ref | Value | Description | JLCPCB# | Price | Stock |
|-----|-------|-------------|---------|-------|-------|
| C7 | 100nF | Decoupling 0402 X7R | **C60474** | $0.003 | 14M |
| C8 | 1µF | MCP73831 Input 0603 | **C14664** | $0.008 | 481k |
| C11 | 1µF | ADP7142 Input 0603 | **C14664** | $0.008 | 481k |
| C12 | 10µF | ADP7142 Output 0603 | **C109457** | $0.041 | 49k |
| C13 | 1µF | TPS60403 Flying Cap 0603 | **C14664** | $0.008 | 481k |
| C14 | 1µF | TPS60403 Input 0603 | **C14664** | $0.008 | 481k |
| C15 | 100nF | ADP7182 Input 0402 | **C60474** | $0.003 | 14M |
| C16 | 10µF | ADP7182 Output 0603 | **C109457** | $0.041 | 49k |
| C17 | 1µF | ADP7182 Noise Red 0603 | **C14664** | $0.008 | 481k |
| C18 | 100nF | Decoupling 0402 | **C60474** | $0.003 | 14M |
| C19 | 100nF | Boost Input 0402 | **C60474** | $0.003 | 14M |
| C20 | 10nF | DW01A Delay 0402 | **C60133** | $0.004 | 3.5M |
| C21 | 22µF | Boost Output 0805 | **C49326685** | $0.009 | 5.7k |
| C22 | 10µF | TPS61220 Input 0603 | **C109457** | $0.041 | 49k |
| C23 | 10µF | Boost Output 2 0603 | **C109457** | $0.041 | 49k |

### Diff Amp Decoupling

| Ref | Value | Description | JLCPCB# | Price | Stock |
|-----|-------|-------------|---------|-------|-------|
| C3 | 100nF | AD8130 -VS 0402 | **C60474** | $0.003 | 14M |
| C9 | 100nF | AD8130 +VS 0402 | **C60474** | $0.003 | 14M |

### Input Attenuator Trimmer Capacitors

| Ref | Value | Description | JLCPCB# | Price | Notes |
|-----|-------|-------------|---------|-------|-------|
| C1 | 2-6pF | Input Comp Trimmer + | **C22468120** | $0.32 | SEHWA alternative |
| C2 | 2-6pF | BW Comp Trimmer + | **C22468120** | $0.32 | Range differs from design |
| C5 | 2-6pF | Input Comp Trimmer - | **C22468120** | $0.32 | SEHWA alternative |
| C6 | 2-6pF | BW Comp Trimmer - | **C22468120** | $0.32 | Range differs from design |

**Note:** Original Murata TZC3 trimmers (TZC3Z020A110R00, TZC3Z100A110R00) not available on JLCPCB. SEHWA STC3MA06-T1 (2-6pF) is an alternative. For exact ranges, order from DigiKey.

---

## 6. Resistors

### Power Supply Resistors (0402)

| Ref | Value | Description | JLCPCB# | Price | Stock |
|-----|-------|-------------|---------|-------|-------|
| R3 | 1k | Status LED limit | **C11702** | $0.0007 | 3M |
| R8 | 10Ω | Battery sense | **C25077** | $0.0005 | 964k |
| R9 | 1k | Power LED limit | **C11702** | $0.0007 | 3M |
| R10 | 100k | TPS61220 FB high | **C25741** | $0.001 | 7.5M |
| R11 | 1M | DW01A OC sense | **C26083** | $0.0007 | 4.5M |
| R12 | 5.1k | USB-C CC1 | **C25905** | $0.0005 | 2.6M |
| R13 | 5.1k | USB-C CC2 | **C25905** | $0.0005 | 2.6M |
| R14 | 1k | ADP7182 VSET | **C11702** | $0.0007 | 3M |
| R15 | 2k | MCP73831 PROG | **C4109** | $0.0005 | 1.8M |

### Diff Amp and Output Resistors (0402)

| Ref | Value | Description | JLCPCB# | Price | Stock |
|-----|-------|-------------|---------|-------|-------|
| R6 | 10k | AD8130 PD pullup | **C25744** | $0.0006 | 5.5M |
| RF2 | 1k | AD8130 feedback | **C11702** | $0.0007 | 3M |
| ROUT1 | 49.9Ω | Output termination | **C325388** | $0.0087 | 8.7k |
| ROUT2 | 0Ω | AC coupling jumper | **C17168** | $0.003 | 2.4M |

### Input Attenuator Precision Resistors (NOT on JLCPCB)

| Ref | Value | Tolerance | DigiKey PN | Est. Price |
|-----|-------|-----------|------------|------------|
| R1 | 9MΩ | 0.1% | CRCW06039M00FKEAHP | $1.50 |
| R2 | 1MΩ | 0.1% | CRCW06031M00FKEAHP | $0.80 |
| R4 | 9MΩ | 0.1% | CRCW06039M00FKEAHP | $1.50 |
| R5 | 1MΩ | 0.1% | CRCW06031M00FKEAHP | $0.80 |

**IMPORTANT:** Precision 0.1% resistors (R1-R5) are NOT available on JLCPCB. Order from DigiKey and hand-solder or use JLCPCB's parts consignment service.

---

## 7. Assembly Options

### Option A: Full JLCPCB Assembly (~$24.50 parts)
- All parts from JLCPCB catalog
- Use alternative trimmer caps (C22468120)
- Use alternative BNC (C20415781)
- **Requires:** Hand-solder precision resistors R1-R5 after assembly

### Option B: Hybrid Assembly (~$32 total)
- JLCPCB assembly for standard parts
- Order from DigiKey:
  - 4x Precision resistors (R1-R5): ~$5
  - 4x Murata trimmer caps (TZC3): ~$3
  - 1x Amphenol BNC: ~$2.50
- Hand-solder specialty parts

---

## 8. JLCPCB Part Number Quick Reference

### Basic Parts (Usually in stock, low cost)
```
C60474   - 100nF 0402 X7R (decoupling)
C14664   - 1uF 0603 X5R
C109457  - 10uF 0603 X5R
C11702   - 1k 0402 1%
C25744   - 10k 0402 1%
C25741   - 100k 0402 1%
C26083   - 1M 0402 1%
C25905   - 5.1k 0402 1%
C2135    - BAT54C SOT-23
C2295    - Red LED 0805
C2297    - Green LED 0805
```

### Extended Parts (May have setup fee)
```
C41661   - AD8130ARZ-REEL7
C659367  - ADP7142AUJZ-5.0-R7
C514357  - ADP7182AUJZ-5.0-R7
C15421   - TPS61220DCKR
C11338   - TPS60403DBVR
C424093  - MCP73831T-2ACI/OT
C221841  - PCM12SMTR switch
C136233  - VLS3012ET-2R2M inductor
```

---

## 9. Not Available on JLCPCB (Order Separately)

| Component | Reason | Source |
|-----------|--------|--------|
| R1-R5 (9M/1M 0.1%) | Precision thin film not stocked | DigiKey |
| Murata TZC3 trimmers | Specialty NP0/C0G trimmer | DigiKey |
| Amphenol B6252HB BNC | Out of stock | DigiKey |

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-05 | Initial BOM |
| 1.1 | 2026-02-05 | Added JLCPCB part numbers |

---

*Generated for DifferentialActiveProbe project - JLCPCB Assembly Ready*
