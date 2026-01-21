# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **KiCad 9 electronics design project** for a 200MHz differential probe with a dual ±5V power supply. The project uses a Python-based JSON-to-KiCad converter to generate schematics from JSON circuit definitions.

### Key Directories

- `DifferentialActiveProbe/` - Main active differential probe KiCad project (primary working directory)
- `power_supply/` - Standalone power supply KiCad project with JSON source definition
- `active-diff/` - Probe JSON source definition (`diff_probe_json.json`)
- `diff-probe/` - Earlier probe iteration
- `DifferentialActiveProbe/docs/` - Technical documentation (component selection, design rationale)

### JSON Source Files (Source of Truth)

- `power_supply/differential_probe_power_supply.json` - Power supply circuit definition
- `active-diff/diff_probe_json.json` - Differential probe circuit definition

## Build Commands

### Convert JSON circuit definition to KiCad schematic

```bash
# Basic conversion (components only, no wires)
python3 json_to_kicad.py input.json output.kicad_sch

# Full conversion with wire connections (recommended)
python3 json_to_kicad.py -w input.json output.kicad_sch
```

### Example usage with project files

```bash
# Convert power supply JSON to KiCad
python3 json_to_kicad.py power_supply/differential_probe_power_supply.json power_supply/power_supply.kicad_sch

# Convert differential probe JSON to KiCad (with wires)
python3 json_to_kicad.py -w active-diff/diff_probe_json.json DifferentialActiveProbe/active-diff.kicad_sch
```

### Typical Workflow

1. Edit the JSON circuit definition (human-readable, version-controllable)
2. Run converter with `-w` flag for full wire routing
3. Open generated `.kicad_sch` in KiCad 9 for review/refinement
4. Commit JSON file to git (schematic is regeneratable from JSON)

## Architecture

### JSON-to-KiCad Converter (`json_to_kicad.py`)

The converter transforms JSON circuit definitions into KiCad 9 schematic files. Key features:

1. **Symbol fetching**: Downloads symbol definitions from KiCad's GitLab repository and embeds them in the schematic
2. **Component rotation**: Supports 0°, 90°, 180°, 270° rotation with rotation-aware pin positions
3. **Functional blocks**: Auto-positions components inside rectangular functional block regions defined in JSON `layout_hints`
4. **Wire routing**: Generates orthogonal (L-shaped) wire connections between pins

### JSON Circuit Format

Circuit definitions use this structure:
```json
{
  "metadata": { "name": "...", "version": "...", "description": "..." },
  "components": [
    { "designator": "R1", "library": "Device", "symbol": "R", "value": "10k", "footprint": "..." }
  ],
  "nets": [
    { "name": "NET_NAME", "connections": [{"component": "R1", "pin": "1"}, ...] }
  ],
  "power_nets": ["GND", "+5V", "-5V"],
  "layout_hints": {
    "functional_blocks": {
      "block_name": { "label": "BLOCK LABEL", "x1": 0, "y1": 0, "x2": 100, "y2": 100 }
    }
  }
}
```

### Custom Symbol Library

The project uses a custom symbol library `differential_probe_symbols.kicad_sym` (symlinked to KiCad's user library path at `/home/pa/snap/kicad/current/.local/share/kicad/9.0/symbols/`) for components not in standard KiCad libraries.

### Schematic Hierarchy (DifferentialActiveProbe/)

The main project uses hierarchical schematics:
- `active-diff.kicad_sch` - Top-level schematic
- `InputAttenuator.kicad_sch` - 10:1 input attenuator with TVS protection
- `buffer.kicad_sch` - AD8065 unity-gain buffer amplifiers
- `DiffAmp.kicad_sch` - LMH6552 differential amplifier stage
- `Power.kicad_sch` - Dual ±5V power supply module

### Supported Libraries in Converter

The converter maps these library names to KiCad symbol files:
- `Device` - Standard passive components (R, C, L, LED)
- `Connector`, `Connector_Generic` - Connectors
- `Amplifier_Operational` - Op-amps
- `DifferentialProbe` - Custom library for project-specific components

## Circuit Design Notes

### Differential Probe Specifications
- Input: ±50V differential, ±10V common mode
- Attenuation: 10:1
- Input impedance: 10MΩ
- Bandwidth: DC to 200MHz
- Uses AD8065 buffer amplifiers and LMH6552 differential amplifier

### TVS Protection Circuit
Uses **PESD5V0S1BA** bidirectional TVS diodes (SOD-323 package):
- Pin 1: connects to signal (attenuator output, ATTEN_POS/ATTEN_NEG)
- Pin 2: connects to GND

**Voltage analysis:**
- Normal signal at attenuator output: ±5V (from ±50V input with 10:1 attenuation)
- TVS breakdown voltage: 6.0V
- Normal operation: TVS does not conduct (|±5V| < 6V breakdown)
- Fault/ESD: TVS clamps to GND when |signal| > 6V

This protects the AD8065 buffer inputs while allowing full ±5V signal swing.

### Power Supply Architecture
- Dual ±5V rails from 9V battery or single-cell LiPo with USB-C charging
- Ultra-low noise LDOs (ADP7142/ADP7182) with 9µVrms output noise
- Boost converter (TPS61220) for LiPo voltage range utilization
- Charge pump inverter (TPS60403) for negative rail generation
