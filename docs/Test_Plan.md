# Differential Active Probe - Test Plan

**Document:** Test Plan for Performance Validation
**Version:** 1.0
**Date:** 2026-02-06
**DUT:** Differential Active Probe with AD8130 (Rev 1)

---

## 1. Test Equipment

| Equipment | Model/Specs | Purpose |
|-----------|-------------|---------|
| Oscilloscope | 200MHz, 10MΩ/15pF probes | Output measurement, waveform analysis |
| Function Generator | 10MHz, 50Ω output | Test signal source |
| Bench Power Supply #1 | 0-30V, 3A | External ±5V supply (bypass internal) |
| Bench Power Supply #2 | 0-30V, 3A | Test signal generation |
| DC Electronic Load | LAN controllable | Load testing, battery simulation |
| Multimeter #1 | 6.5 digit DMM | DC voltage/current measurements |
| Multimeter #2 | 6.5 digit DMM | Differential measurements |
| 9V Battery | Alkaline, fresh | Normal operation testing |
| LiPo Battery | 3.7V, 300-500mAh | Battery operation testing |
| USB-C Power Source | 5V/2A | Charging tests |

### Test Fixtures Required

- BNC-to-banana adapter for function generator output
- BNC 50Ω terminator
- Precision resistor divider (for high voltage simulation)
- Twisted pair test leads
- Ground reference cable

---

## 2. Test Categories

| Category | Tests | Priority |
|----------|-------|----------|
| A. Power Supply | A1-A8 | Critical |
| B. DC Performance | B1-B6 | Critical |
| C. AC Performance | C1-C7 | Critical |
| D. Common Mode Rejection | D1-D4 | Critical |
| E. Input Protection | E1-E3 | Important |
| F. Environmental | F1-F2 | Optional |

---

## 3. Category A: Power Supply Tests

### A1. Power-On from 9V Battery

**Objective:** Verify probe powers on correctly from 9V battery

**Setup:**
1. Connect fresh 9V alkaline battery
2. Connect DMM to +5V test point (TP_VCC)
3. Connect second DMM to -5V test point (TP_VEE)

**Procedure:**
1. Verify power LED is OFF with switch in OFF position
2. Move switch to ON position
3. Record +5V rail voltage
4. Record -5V rail voltage
5. Verify power LED illuminates GREEN

**Pass Criteria:**
| Parameter | Min | Typical | Max |
|-----------|-----|---------|-----|
| +5V Rail | 4.95V | 5.00V | 5.05V |
| -5V Rail | -5.05V | -5.00V | -4.95V |
| Power LED | GREEN illuminated | | |

**Results:**
```
+5V Rail:    _______ V
-5V Rail:    _______ V
Power LED:   [ ] PASS  [ ] FAIL
```

---

### A2. Power-On from LiPo Battery

**Objective:** Verify probe powers on correctly from LiPo battery (no 9V)

**Setup:**
1. Disconnect 9V battery
2. Connect charged LiPo (measure initial voltage: _____ V)
3. Connect DMMs to ±5V test points

**Procedure:**
1. Move switch to ON position
2. Record +5V and -5V rail voltages
3. Verify power LED illuminates

**Pass Criteria:**
| Parameter | Min | Typical | Max |
|-----------|-----|---------|-----|
| +5V Rail | 4.90V | 5.00V | 5.05V |
| -5V Rail | -5.05V | -5.00V | -4.90V |

**Results:**
```
LiPo Initial Voltage: _______ V
+5V Rail:             _______ V
-5V Rail:             _______ V
```

---

### A3. Power Supply Noise Measurement

**Objective:** Verify ultra-low noise on power rails

**Setup:**
1. Power probe from 9V battery
2. Set oscilloscope: AC coupling, 20MHz bandwidth limit, 1mV/div
3. Connect scope probe to +5V test point (use short ground lead!)

**Procedure:**
1. Measure +5V rail noise (peak-to-peak and RMS if available)
2. Repeat for -5V rail
3. Note any switching frequency components (1MHz boost, 150kHz charge pump)

**Pass Criteria:**
| Parameter | Max |
|-----------|-----|
| +5V Noise (p-p) | 10mV |
| -5V Noise (p-p) | 10mV |
| +5V Noise (RMS) | 50µV (if measurable) |

**Results:**
```
+5V Noise (p-p):  _______ mV
-5V Noise (p-p):  _______ mV
Dominant frequency: _______ kHz
Notes: _________________________________
```

---

### A4. Supply Current Measurement

**Objective:** Verify quiescent and operating current draw

**Setup:**
1. Insert DMM (mA range) in series with 9V battery
2. No input signal applied to probe

**Procedure:**
1. Record quiescent current (no signal, no load)
2. Apply 1Vpp 1kHz differential signal, record current
3. Calculate power consumption

**Pass Criteria:**
| Parameter | Min | Typical | Max |
|-----------|-----|---------|-----|
| Quiescent Current | - | 15mA | 30mA |
| Operating Current | - | 20mA | 50mA |

**Results:**
```
Quiescent Current: _______ mA
Operating Current: _______ mA
Power (9V × Iq):   _______ mW
```

---

### A5. LiPo Charging Test

**Objective:** Verify USB-C charging functionality

**Setup:**
1. Connect partially discharged LiPo (3.5-3.8V)
2. Connect USB-C 5V power source
3. Probe must be OFF (switch in OFF position)

**Procedure:**
1. Record initial LiPo voltage
2. Connect USB-C power
3. Verify charging LED illuminates RED
4. Measure charge current (if possible, use USB power meter)
5. Wait for charge complete (LED turns OFF)
6. Record final LiPo voltage

**Pass Criteria:**
| Parameter | Min | Typical | Max |
|-----------|-----|---------|-----|
| Charge Current | 400mA | 500mA | 550mA |
| Final Voltage | 4.15V | 4.20V | 4.25V |
| Charging LED | RED when charging | | |

**Results:**
```
Initial LiPo Voltage: _______ V
Charge Current:       _______ mA
Final LiPo Voltage:   _______ V
Charge Time:          _______ minutes
```

---

### A6. Battery Switchover Test

**Objective:** Verify automatic switching between 9V and LiPo

**Setup:**
1. Connect both 9V battery and charged LiPo
2. Monitor +5V rail with DMM
3. Power ON the probe

**Procedure:**
1. Record +5V with both batteries connected
2. Disconnect 9V battery while monitoring +5V
3. Verify no dropout or glitch (continuous operation)
4. Reconnect 9V battery
5. Verify smooth transition back

**Pass Criteria:**
| Parameter | Criteria |
|-----------|----------|
| Switchover | No visible dropout on DMM |
| +5V stability | Remains within ±50mV during switch |

**Results:**
```
+5V (both batteries):  _______ V
+5V (LiPo only):       _______ V
Switchover glitch:     [ ] None observed  [ ] Glitch observed
```

---

### A7. Low Battery Operation (LiPo)

**Objective:** Verify operation down to minimum LiPo voltage

**Setup:**
1. Use DC electronic load to discharge LiPo (or use adjustable supply to simulate)
2. Monitor +5V rail and LiPo voltage simultaneously

**Procedure:**
1. Starting from 4.2V, reduce LiPo voltage in 0.1V steps
2. At each step, record +5V rail voltage
3. Continue until probe shuts down or +5V drops out of spec
4. Record cutoff voltage

**Pass Criteria:**
| LiPo Voltage | +5V Rail |
|--------------|----------|
| 4.2V | 4.95-5.05V |
| 3.7V | 4.95-5.05V |
| 3.3V | 4.90-5.05V |
| 3.0V | Shutdown OK |

**Results:**
```
LiPo 4.2V → +5V: _______ V
LiPo 3.7V → +5V: _______ V
LiPo 3.3V → +5V: _______ V
LiPo 3.0V → +5V: _______ V (or shutdown)
Cutoff Voltage:  _______ V
```

---

### A8. 9V Battery Voltage Range

**Objective:** Verify operation across 9V battery voltage range

**Setup:**
1. Use adjustable power supply instead of 9V battery
2. Monitor +5V rail

**Procedure:**
1. Set supply to 9.0V, record +5V
2. Reduce to 7.5V (depleted alkaline), record +5V
3. Reduce to 6.0V (minimum), record +5V
4. Increase to 9.5V (fresh battery), verify no damage

**Pass Criteria:**
| Input Voltage | +5V Rail |
|---------------|----------|
| 9.0V | 4.95-5.05V |
| 7.5V | 4.95-5.05V |
| 6.0V | 4.90-5.05V |

**Results:**
```
9.0V input → +5V: _______ V
7.5V input → +5V: _______ V
6.0V input → +5V: _______ V
9.5V input → +5V: _______ V (verify no damage)
```

---

## 4. Category B: DC Performance Tests

### B1. DC Attenuation Ratio

**Objective:** Verify 10:1 attenuation ratio at DC

**Setup:**
1. Connect adjustable DC supply to probe inputs (+ to INPUT_POS, - to INPUT_NEG)
2. Connect DMM #1 to measure input differential voltage
3. Connect DMM #2 to probe output (BNC)

**Procedure:**
1. Apply +1.000V differential (INPUT_POS=+0.5V, INPUT_NEG=-0.5V relative to probe GND)
2. Record output voltage
3. Repeat for +5V, +10V, -5V, -10V differential
4. Calculate attenuation ratio for each

**Pass Criteria:**
| Input (diff) | Expected Output | Tolerance |
|--------------|-----------------|-----------|
| +1.000V | +0.100V | ±1% |
| +5.000V | +0.500V | ±1% |
| +10.000V | +1.000V | ±1% |
| -5.000V | -0.500V | ±1% |

**Results:**
```
Input +1.000V → Output: _______ V  Ratio: _______:1
Input +5.000V → Output: _______ V  Ratio: _______:1
Input +10.00V → Output: _______ V  Ratio: _______:1
Input -5.000V → Output: _______ V  Ratio: _______:1
Input -10.00V → Output: _______ V  Ratio: _______:1

Average Attenuation Ratio: _______:1
```

---

### B2. DC Offset

**Objective:** Measure DC offset with inputs shorted

**Setup:**
1. Short both inputs to probe ground (INPUT_POS = INPUT_NEG = GND)
2. Connect DMM to probe output

**Procedure:**
1. Allow probe to warm up for 5 minutes
2. Record output DC voltage (should be near 0V)
3. Repeat measurement after 15 minutes

**Pass Criteria:**
| Parameter | Max |
|-----------|-----|
| DC Offset | ±10mV |
| Offset Drift (15 min) | ±2mV |

**Results:**
```
DC Offset (5 min):   _______ mV
DC Offset (15 min):  _______ mV
Drift:               _______ mV
```

---

### B3. Input Impedance (DC)

**Objective:** Verify 10MΩ input impedance

**Setup:**
1. Connect 1MΩ precision resistor in series with INPUT_POS
2. Apply 10V DC through the 1MΩ resistor
3. Measure voltage at INPUT_POS

**Procedure:**
1. Without probe: measure voltage at INPUT_POS (should be 10V)
2. With probe connected: measure voltage at INPUT_POS
3. Calculate input impedance: Rin = Rmeas × V_in / (V_source - V_in)

**Calculation:**
```
V_source = 10V
R_series = 1MΩ
V_measured = voltage at INPUT_POS with probe connected

I = (V_source - V_measured) / R_series
R_input = V_measured / I
```

**Pass Criteria:**
| Parameter | Min | Typical | Max |
|-----------|-----|---------|-----|
| Input Impedance | 9MΩ | 10MΩ | 11MΩ |

**Results:**
```
V_source:    10.000 V
V_measured:  _______ V
Calculated Rin: _______ MΩ
```

---

### B4. Maximum Input Voltage (Differential)

**Objective:** Verify operation at maximum rated differential input

**Setup:**
1. Use two power supplies to create ±25V (50V differential)
2. Connect through 100kΩ current-limiting resistors (safety)
3. Monitor output on scope

**Procedure:**
1. Slowly increase differential voltage from 0 to ±25V
2. Verify output tracks correctly (should be ±2.5V at output)
3. Verify no clipping or distortion
4. Verify probe survives (no damage)

**WARNING:** High voltage test - use current-limiting resistors!

**Pass Criteria:**
| Input (diff) | Expected Output | Result |
|--------------|-----------------|--------|
| ±50V | ±5V (10:1) | Linear, no clipping |

**Results:**
```
+50V differential → Output: _______ V
-50V differential → Output: _______ V
Clipping observed: [ ] No  [ ] Yes, at ___V input
Probe survived:    [ ] Yes [ ] No
```

---

### B5. Common Mode DC Voltage

**Objective:** Verify operation with common mode DC offset

**Setup:**
1. Apply common mode voltage to both inputs (same voltage on + and -)
2. Apply small differential signal on top of common mode
3. Monitor output

**Procedure:**
1. Set common mode to +5V, apply 1V differential
2. Verify output = 100mV (differential only, CM rejected)
3. Repeat for common mode = -5V, 0V, +10V

**Pass Criteria:**
| Common Mode | Differential In | Expected Out |
|-------------|-----------------|--------------|
| +5V | 1V | 100mV ±5% |
| -5V | 1V | 100mV ±5% |
| +10V | 1V | 100mV ±5% |

**Results:**
```
CM=+5V, Diff=1V  → Output: _______ mV
CM=-5V, Diff=1V  → Output: _______ mV
CM=+10V, Diff=1V → Output: _______ mV
CM=0V, Diff=1V   → Output: _______ mV (reference)
```

---

### B6. Channel Balance (Symmetry)

**Objective:** Verify positive and negative channels are matched

**Setup:**
1. Apply +5V to INPUT_POS only (INPUT_NEG grounded)
2. Record output
3. Apply +5V to INPUT_NEG only (INPUT_POS grounded)
4. Record output (should be inverted but equal magnitude)

**Procedure:**
1. INPUT_POS = +5V, INPUT_NEG = GND → Record output
2. INPUT_POS = GND, INPUT_NEG = +5V → Record output
3. Calculate mismatch: (|V1| - |V2|) / ((|V1| + |V2|)/2) × 100%

**Pass Criteria:**
| Parameter | Max |
|-----------|-----|
| Channel Mismatch | 1% |

**Results:**
```
+5V on POS only: Output = _______ mV
+5V on NEG only: Output = _______ mV
Mismatch: _______ %
```

---

## 5. Category C: AC Performance Tests

### C1. Frequency Response (10Hz - 10MHz)

**Objective:** Verify flat frequency response within available test range

**Setup:**
1. Connect function generator to probe inputs (use twisted pair)
2. Set generator to 1Vpp sine wave
3. Connect probe output to oscilloscope
4. Terminate scope input with 50Ω (or use 50Ω input mode)

**Procedure:**
1. Measure output amplitude at each frequency
2. Calculate gain relative to 1kHz reference
3. Plot frequency response

**Test Frequencies:**
| Frequency | Output (Vpp) | Gain (dB) |
|-----------|--------------|-----------|
| 10 Hz | | |
| 100 Hz | | |
| 1 kHz (ref) | | 0 dB |
| 10 kHz | | |
| 100 kHz | | |
| 1 MHz | | |
| 5 MHz | | |
| 10 MHz | | |

**Pass Criteria:**
| Frequency Range | Gain Deviation |
|-----------------|----------------|
| 10Hz - 1MHz | ±0.5 dB |
| 1MHz - 10MHz | ±1.0 dB |

**Results:**
```
See table above - fill in measured values

Flatness 10Hz-1MHz:  _______ dB
Flatness 1MHz-10MHz: _______ dB
```

---

### C2. Step Response

**Objective:** Verify transient response and compensation

**Setup:**
1. Set function generator to 1kHz square wave, 1Vpp
2. Connect to probe inputs
3. View output on oscilloscope, 1µs/div timebase

**Procedure:**
1. Observe rising edge response
2. Check for overshoot, ringing, or undershoot
3. Adjust trimmer capacitors if necessary (C1-C4)
4. Measure rise time (10%-90%)

**Pass Criteria:**
| Parameter | Max |
|-----------|-----|
| Overshoot | 5% |
| Rise time | 3.5ns (limited by scope) |
| Settling time (to 1%) | 50ns |

**Results:**
```
Overshoot:     _______ %
Undershoot:    _______ %
Rise Time:     _______ ns
Settling Time: _______ ns
Ringing:       [ ] None  [ ] Minor  [ ] Significant
```

**Step Response Sketch:**
```
     ┌────────────────
     │
     │
─────┘

Mark overshoot, settling here
```

---

### C3. Compensation Adjustment

**Objective:** Optimize frequency compensation trimmers

**Trimmer Functions:**
| Trimmer | Function | Adjustment Effect |
|---------|----------|-------------------|
| C1 | Input compensation (+) | Primary tuning for + channel frequency response |
| C2 | Bandwidth comp (+) | Sets bandwidth, also used for AC CMRR |
| C3 | Input compensation (-) | Primary tuning for - channel frequency response |
| C4 | Bandwidth comp (-) | Sets bandwidth, also used for AC CMRR |

**Compensation Relationship:** C2 = 9 × C1 (approximately, for R1=9MΩ, R2=1MΩ)

**Setup:**
1. Apply 1MHz square wave, 1Vpp differential
2. Monitor output on scope (use BNC output to avoid probe loading)

**Procedure - Step 1: Individual Channel Compensation**
1. Set C2 to middle position (~7pF)
2. Adjust C1 for flat top on square wave (no overshoot, no rounding)
3. Repeat with C4 at middle, adjust C3 for negative channel
4. Verify with 10MHz sine: amplitude should match 100kHz amplitude (±5%)

**Procedure - Step 2: AC CMRR Optimization (after Step 1)**
1. Connect both inputs together (common mode)
2. Apply 1MHz, 1Vpp sine wave
3. Adjust C2 slightly to minimize output
4. Adjust C4 slightly to minimize output
5. Re-verify differential response is still flat
6. Target: <15mV output for 1V common-mode (60dB CMRR)

**Compensation States:**
```
Under-compensated:    Over-compensated:     Correct:
    ╱─────────           ┌──╮                ┌────────
   ╱                     │  ╰────            │
  ╱                      │                   │
──╱                    ──┘                 ──┘
(slow rise, rounded)   (overshoot)         (flat top)
→ Increase C1           → Decrease C1       = CORRECT
```

**Results:**
```
Step 1 - Differential Response:
C1 Setting: _______ (turns from min)
C2 Setting: _______ (turns from min)
C3 Setting: _______ (turns from min)
C4 Setting: _______ (turns from min)
Square wave quality: [ ] Excellent  [ ] Good  [ ] Needs work

Step 2 - AC CMRR Optimization:
CM output @ 1MHz before trim: _______ mVpp
CM output @ 1MHz after trim:  _______ mVpp
C2 final: _______ (turns)
C4 final: _______ (turns)
Differential response still flat: [ ] Yes  [ ] No (re-iterate)
```

---

### C4. Phase Response

**Objective:** Verify minimal phase shift at test frequencies

**Setup:**
1. Split function generator output: one to scope CH1 (reference), one to probe
2. Probe output to scope CH2
3. Measure phase difference at various frequencies

**Procedure:**
1. At 1kHz, adjust scope to show both channels
2. Measure phase shift between CH1 and CH2
3. Repeat at 100kHz, 1MHz, 10MHz

**Pass Criteria:**
| Frequency | Max Phase Shift |
|-----------|-----------------|
| 1 kHz | ±2° |
| 100 kHz | ±5° |
| 1 MHz | ±10° |
| 10 MHz | ±30° |

**Results:**
```
Phase @ 1kHz:   _______ °
Phase @ 100kHz: _______ °
Phase @ 1MHz:   _______ °
Phase @ 10MHz:  _______ °
```

---

### C5. Slew Rate

**Objective:** Measure maximum slew rate

**Setup:**
1. Apply fast edge signal (fastest available from generator)
2. Use maximum input amplitude within spec (e.g., 10V differential)

**Procedure:**
1. Measure output rise time for large signal
2. Calculate slew rate: SR = ΔV / Δt

**Calculation:**
```
Output swing: ΔV = _______ V
Rise time (10-90%): Δt = _______ ns
Slew Rate = ΔV / Δt = _______ V/µs
```

**Pass Criteria:**
| Parameter | Min |
|-----------|-----|
| Slew Rate | 100 V/µs |

**Results:**
```
Measured Slew Rate: _______ V/µs
```

---

### C6. Output Drive Capability

**Objective:** Verify probe can drive 50Ω load

**Setup:**
1. Connect probe output to 50Ω termination
2. Apply 2Vpp differential input (should give 200mVpp output)
3. Measure output amplitude

**Procedure:**
1. Measure output with 50Ω load
2. Measure output with 1MΩ load (scope high-Z)
3. Calculate output impedance

**Pass Criteria:**
| Load | Output |
|------|--------|
| 50Ω | ≥90% of open circuit |
| 1MΩ | Reference (100%) |

**Results:**
```
Output @ 1MΩ load: _______ mVpp
Output @ 50Ω load: _______ mVpp
Ratio: _______ %
Calculated Zout: _______ Ω
```

---

### C7. Harmonic Distortion

**Objective:** Verify low distortion at 1MHz

**Setup:**
1. Apply 1MHz sine wave, 2Vpp differential
2. View output on scope in FFT mode

**Procedure:**
1. Identify fundamental (1MHz)
2. Measure 2nd harmonic (2MHz) level
3. Measure 3rd harmonic (3MHz) level
4. Calculate THD if possible

**Pass Criteria:**
| Parameter | Max |
|-----------|-----|
| 2nd Harmonic | -50 dBc |
| 3rd Harmonic | -50 dBc |

**Results:**
```
Fundamental (1MHz): _______ dBV
2nd Harmonic (2MHz): _______ dBc
3rd Harmonic (3MHz): _______ dBc
```

---

## 6. Category D: Common Mode Rejection Tests

### D1. CMRR at DC (Resistor Matching Test)

**Objective:** Measure common mode rejection at DC

**Theory:** DC CMRR depends *entirely* on resistor matching (R1/R3 and R2/R4).
Capacitors are open circuits at DC, so trimmers C1-C4 have NO effect on DC CMRR.
Any DC output offset indicates resistor mismatch and cannot be trimmed out.

**Setup:**
1. Connect both inputs together (INPUT_POS = INPUT_NEG)
2. Apply common mode DC voltage to both inputs
3. Measure output with high-resolution DMM (ideally 0V)

**Procedure:**
1. Apply +2V common mode, measure output
2. Apply +5V common mode, measure output
3. Apply -5V common mode, measure output
4. Calculate CMRR: CMRR = 20 × log10(Vcm / Vout)

**Calculation:**
```
Vcm_applied = 5.000V
Vout_measured = _______ mV
CMRR = 20 × log10(5000mV / Vout_mV) = _______ dB
```

**Pass Criteria:**
| Parameter | Min | Notes |
|-----------|-----|-------|
| CMRR @ DC | 60 dB | Depends on 0.1% resistor matching |
| DC Output | <5mV | For 5V common-mode input |

**Note:** If DC CMRR fails, the resistor pairs (R1/R3, R2/R4) are mismatched.
This requires replacing resistors - it cannot be adjusted with trimmers.

**Results:**
```
+2V CM → Output: _______ mV  CMRR: _______ dB
+5V CM → Output: _______ mV  CMRR: _______ dB
-5V CM → Output: _______ mV  CMRR: _______ dB
```

---

### D2. CMRR at 1kHz (Low Frequency AC)

**Objective:** Measure CMRR at audio frequency

**Theory:** At low AC frequencies, CMRR is primarily determined by resistor matching,
similar to DC. Capacitor effects are minimal at 1kHz.

**Setup:**
1. Connect both inputs together
2. Apply 5Vpp 1kHz sine wave (common mode)
3. Measure output amplitude

**Procedure:**
1. Apply 5Vpp common mode signal
2. Measure output (should be highly attenuated)
3. Calculate CMRR

**Pass Criteria:**
| Parameter | Min |
|-----------|-----|
| CMRR @ 1kHz | 70 dB |

**Results:**
```
CM Input: 5Vpp @ 1kHz
Output:   _______ mVpp
CMRR:     _______ dB
```

---

### D3. CMRR at 1MHz (High Frequency AC - Adjustable)

**Objective:** Measure CMRR at high frequency and optimize with trimmers

**Theory:** At higher frequencies, capacitor matching becomes important.
C2 and C4 (bandwidth compensation trimmers) can be adjusted to optimize
AC CMRR by balancing the frequency response between + and - channels.

**Setup:**
1. Connect both inputs together
2. Apply 1Vpp 1MHz sine wave (common mode)
3. Measure output amplitude

**Procedure:**
1. Apply 1Vpp common mode signal at 1MHz
2. Measure output (should be highly attenuated)
3. If output is too high, adjust C2 and C4 to minimize output
4. Re-check differential mode response after adjustment (ensure still flat)
5. Calculate CMRR

**Optimization (if CMRR < 60dB):**
1. Slightly adjust C2, observe output change
2. Slightly adjust C4, observe output change
3. Find combination that minimizes common-mode output
4. Verify differential response is still correct after adjustment

**Pass Criteria:**
| Parameter | Min | Notes |
|-----------|-----|-------|
| CMRR @ 1MHz | 60 dB | Can be optimized with C2/C4 |
| CM Output | <15mV | For 1V common-mode input |

**Results:**
```
CM Input: 1Vpp @ 1MHz
Output (before trim): _______ mVpp  CMRR: _______ dB
Output (after trim):  _______ mVpp  CMRR: _______ dB
C2 adjustment: _______ (turns from initial)
C4 adjustment: _______ (turns from initial)
```

---

### D4. CMRR at 10MHz

**Objective:** Measure CMRR at maximum generator frequency

**Setup:**
1. Same as D2, but at 10MHz

**Procedure:**
1. Apply 5Vpp 10MHz common mode signal
2. Measure output amplitude
3. Calculate CMRR

**Pass Criteria:**
| Parameter | Min |
|-----------|-----|
| CMRR @ 10MHz | 50 dB (spec is 70dB, but test equipment limited) |

**Results:**
```
CM Input: 5Vpp @ 10MHz
Output:   _______ mVpp
CMRR:     _______ dB
```

---

## 7. Category E: Input Protection Tests

### E1. TVS Clamping Verification

**Objective:** Verify TVS diodes clamp overvoltage

**Setup:**
1. Apply slowly increasing voltage through 10kΩ current-limiting resistor
2. Monitor voltage at attenuator output (before AD8130)

**Procedure:**
1. Increase input voltage slowly while monitoring attenuator output
2. Note voltage at which clamping begins
3. Verify clamping voltage is within TVS spec

**WARNING:** Use current-limiting resistor to prevent damage!

**Pass Criteria:**
| Parameter | Min | Max |
|-----------|-----|-----|
| Clamp voltage | 5.5V | 6.5V |

**Results:**
```
Clamping begins at input: _______ V
Attenuator output clamps at: _______ V
TVS functioning: [ ] Yes  [ ] No
```

---

### E2. ESD Survival (Functional)

**Objective:** Verify probe survives ESD events

**Setup:**
1. Record initial DC attenuation ratio
2. Apply ESD pulse using ESD gun or static discharge

**Procedure:**
1. Apply ±2kV contact discharge to input terminals
2. Verify probe still functions
3. Re-measure DC attenuation ratio
4. Verify no degradation

**Pass Criteria:**
| Parameter | Criteria |
|-----------|----------|
| Post-ESD function | Probe operates normally |
| Attenuation change | <0.5% |

**Results:**
```
Pre-ESD attenuation:  _______:1
Post-ESD attenuation: _______:1
Change: _______ %
Probe functional: [ ] Yes  [ ] No
```

---

### E3. Reverse Polarity Protection

**Objective:** Verify probe survives reversed battery connection

**Setup:**
1. Prepare reversed polarity battery connection
2. Monitor for smoke/damage

**Procedure:**
1. Briefly (1 second) connect battery with reversed polarity
2. Disconnect immediately
3. Connect correctly and verify operation

**Pass Criteria:**
| Parameter | Criteria |
|-----------|----------|
| Reverse polarity | No damage, probe still works |

**Results:**
```
Reversed polarity applied: [ ] Yes
Duration: _______ seconds
Post-test function: [ ] Normal  [ ] Damaged
```

---

## 8. Category F: Environmental Tests (Optional)

### F1. Temperature Stability

**Objective:** Verify performance over temperature range

**Setup:**
1. Place probe in temperature chamber (if available)
2. Or test at room temperature, then after warming with heat gun

**Procedure:**
1. Measure DC offset at 25°C
2. Heat probe to 50°C, measure DC offset
3. Cool to 25°C, verify return to original

**Pass Criteria:**
| Parameter | Max |
|-----------|-----|
| Offset drift | 5mV over 25°C range |

**Results:**
```
Offset @ 25°C: _______ mV
Offset @ 50°C: _______ mV
Drift: _______ mV
```

---

### F2. Long-Term Stability

**Objective:** Verify stable operation over extended period

**Setup:**
1. Apply 1kHz, 1Vpp signal continuously
2. Monitor output over 4 hours

**Procedure:**
1. Record output amplitude every hour
2. Record DC offset every hour
3. Calculate drift

**Pass Criteria:**
| Parameter | Max Drift |
|-----------|-----------|
| Amplitude | ±1% over 4 hours |
| DC offset | ±5mV over 4 hours |

**Results:**
```
Time    Amplitude    DC Offset
0h      _______ mV   _______ mV
1h      _______ mV   _______ mV
2h      _______ mV   _______ mV
4h      _______ mV   _______ mV
```

---

## 9. Test Summary Sheet

### Unit Under Test
```
Serial Number: _________________
Build Date:    _________________
Firmware Ver:  N/A (analog)
Tester:        _________________
Test Date:     _________________
```

### Test Results Summary

| Test | Result | Notes |
|------|--------|-------|
| A1. Power-On (9V) | [ ] PASS [ ] FAIL | |
| A2. Power-On (LiPo) | [ ] PASS [ ] FAIL | |
| A3. Supply Noise | [ ] PASS [ ] FAIL | |
| A4. Supply Current | [ ] PASS [ ] FAIL | |
| A5. Charging | [ ] PASS [ ] FAIL | |
| A6. Switchover | [ ] PASS [ ] FAIL | |
| A7. Low Battery | [ ] PASS [ ] FAIL | |
| A8. 9V Range | [ ] PASS [ ] FAIL | |
| B1. Attenuation | [ ] PASS [ ] FAIL | |
| B2. DC Offset | [ ] PASS [ ] FAIL | |
| B3. Input Impedance | [ ] PASS [ ] FAIL | |
| B4. Max Input | [ ] PASS [ ] FAIL | |
| B5. CM DC | [ ] PASS [ ] FAIL | |
| B6. Channel Balance | [ ] PASS [ ] FAIL | |
| C1. Frequency Response | [ ] PASS [ ] FAIL | |
| C2. Step Response | [ ] PASS [ ] FAIL | |
| C3. Compensation | [ ] PASS [ ] FAIL | |
| C4. Phase | [ ] PASS [ ] FAIL | |
| C5. Slew Rate | [ ] PASS [ ] FAIL | |
| C6. Output Drive | [ ] PASS [ ] FAIL | |
| C7. Distortion | [ ] PASS [ ] FAIL | |
| D1. CMRR DC | [ ] PASS [ ] FAIL | |
| D2. CMRR 1kHz | [ ] PASS [ ] FAIL | |
| D3. CMRR 1MHz | [ ] PASS [ ] FAIL | |
| D4. CMRR 10MHz | [ ] PASS [ ] FAIL | |
| E1. TVS Clamping | [ ] PASS [ ] FAIL | |
| E2. ESD Survival | [ ] PASS [ ] FAIL | |
| E3. Reverse Polarity | [ ] PASS [ ] FAIL | |

### Overall Result

```
[ ] PASS - All critical tests passed
[ ] CONDITIONAL PASS - Minor issues noted: _________________
[ ] FAIL - Critical test(s) failed: _________________
```

### Sign-Off

```
Tested by:  _________________ Date: _________
Reviewed by: _________________ Date: _________
```

---

## 10. Appendix: Test Equipment Calibration

| Equipment | Cal Due Date | Cal Status |
|-----------|--------------|------------|
| Oscilloscope | | [ ] Valid |
| Function Generator | | [ ] Valid |
| DMM #1 | | [ ] Valid |
| DMM #2 | | [ ] Valid |
| Power Supply #1 | | [ ] Valid |
| Power Supply #2 | | [ ] Valid |

---

*End of Test Plan*
