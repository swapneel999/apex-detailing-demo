---
name: Orbital Precision
colors:
  surface: '#071424'
  surface-dim: '#071424'
  surface-bright: '#2e3a4b'
  surface-container-lowest: '#030f1e'
  surface-container-low: '#101c2c'
  surface-container: '#142031'
  surface-container-high: '#1f2b3c'
  surface-container-highest: '#2a3547'
  on-surface: '#d7e3fa'
  on-surface-variant: '#b9cac9'
  inverse-surface: '#d7e3fa'
  inverse-on-surface: '#253142'
  outline: '#839493'
  outline-variant: '#3a4a49'
  surface-tint: '#00dddd'
  primary: '#ffffff'
  on-primary: '#003737'
  primary-container: '#00fbfb'
  on-primary-container: '#007070'
  inverse-primary: '#006a6a'
  secondary: '#b8c3ff'
  on-secondary: '#002388'
  secondary-container: '#0043eb'
  on-secondary-container: '#c6ceff'
  tertiary: '#ffffff'
  on-tertiary: '#313030'
  tertiary-container: '#e5e2e1'
  on-tertiary-container: '#656464'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#00fbfb'
  primary-fixed-dim: '#00dddd'
  on-primary-fixed: '#002020'
  on-primary-fixed-variant: '#004f4f'
  secondary-fixed: '#dde1ff'
  secondary-fixed-dim: '#b8c3ff'
  on-secondary-fixed: '#001356'
  on-secondary-fixed-variant: '#0035be'
  tertiary-fixed: '#e5e2e1'
  tertiary-fixed-dim: '#c9c6c5'
  on-tertiary-fixed: '#1c1b1b'
  on-tertiary-fixed-variant: '#474646'
  background: '#071424'
  on-background: '#d7e3fa'
  surface-variant: '#2a3547'
typography:
  display-lg:
    fontFamily: JetBrains Mono
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: JetBrains Mono
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: JetBrains Mono
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
  technical-md:
    fontFamily: JetBrains Mono
    fontSize: 16px
    fontWeight: '500'
    lineHeight: '1.5'
    letterSpacing: 0.05em
  body-lg:
    fontFamily: Geist
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1.0'
    letterSpacing: 0.1em
spacing:
  unit: 4px
  gutter: 24px
  margin-desktop: 64px
  margin-mobile: 20px
  column-gap: 16px
---

## Brand & Style

The design system is engineered for a high-performance space-tech agency, evoking an atmosphere of rigor, technical superiority, and autonomous precision. The brand personality is "The Silent Engineer"—sophisticated, cold, and hyper-efficient. It prioritizes information density and clarity over decorative elements, utilizing a cinematic, high-contrast aesthetic that feels like a mission control interface.

The style is a fusion of **Technical Minimalism** and **Cyber-Structuralism**. It utilizes deep obsidian surfaces, razor-sharp edges, and concentrated bursts of "luminescent data" (glowing cyan) to guide the eye. Every element must feel intentional, as if designed for zero-latency execution in high-stakes environments. There is no room for soft shadows or organic curves; the interface is built on a foundation of structural integrity and digital clarity.

## Colors

This design system operates exclusively in a high-contrast dark mode to simulate the vastness of deep space and minimize ocular strain during long-duration technical monitoring.

- **Primary (Signal Cyan):** Used for critical data points, active states, and interactive triggers. It represents "Active Power."
- **Secondary (Engine Blue):** Used for structural accents, progress indicators, and secondary navigation. It represents "Autonomous Flow."
- **Background (Void Black):** The absolute #050505 base. It provides the infinite canvas required for high-contrast legibility.
- **Surface (Slate System):** A range of cool grays used for borders, inactive labels, and secondary text to maintain a hierarchy that doesn't compete with the primary data signals.

## Typography

Typography is treated as a structural component. We use a dual-font strategy to balance engineering rigor with readability.

- **JetBrains Mono** is the primary technical font. It is used for all headlines, data readouts, labels, and navigation elements. It reinforces the "terminal-inspired" aesthetic and suggests mathematical precision.
- **Geist** provides a clean, neutral sans-serif balance for long-form body text, ensuring that documentation and complex descriptions remain highly legible without the fatigue sometimes caused by monospaced blocks.

**Styling Note:** Technical labels should frequently use `text-transform: uppercase` and tracking (letter-spacing) to mimic aerospace HUD (Heads-Up Display) interfaces.

## Layout & Spacing

The layout philosophy is based on a **Rigid Technical Grid**. All spacing is derived from a 4px base unit to ensure pixel-perfect alignment. 

- **Desktop:** A 12-column fixed grid with wide 64px margins to create a "letterboxed" cinematic feel. 
- **Internal Spacing:** Components are separated by generous "void space" (vertical margins) to prevent information density from becoming visual clutter.
- **Gutters:** Tight 16px or 24px gutters emphasize the interconnectedness of technical modules.

Elements should be aligned to the grid with mathematical strictness. Reflow for mobile should prioritize a single-column stack while maintaining the 4px vertical rhythm.

## Elevation & Depth

Depth is not communicated through shadows, but through **Luminance and Layering**.

- **Level 0 (Base):** The #050505 background.
- **Level 1 (Sub-surface):** Thin 1px borders in Slate Gray (#1A1A1A) to define container boundaries.
- **Level 2 (Active High-light):** Subtle 1px borders using the Secondary Blue or Primary Cyan, often accompanied by a very tight `0px 0px 8px` outer glow (bloom) of the same color.
- **Glassmorphism:** Used sparingly for overlays and command palettes. Use a heavy background blur (20px+) with a 5% white tint to simulate a reinforced polycarbonate screen.

Avoid all drop shadows. Use "inner-glow" or "rim-lighting" effects on borders to suggest that the UI elements are self-illuminated.

## Shapes

The design system uses **Sharp (0px) roundedness** for all primary containers, buttons, and input fields. This communicates industrial durability and structural engineering. 

The only exception to the "sharp" rule is for circular status indicators or specialized orbital diagrams. Otherwise, every corner must be a perfect 90-degree angle. This reinforces the high-performance, autonomous vibe of the brand.

## Components

### Buttons
- **Primary:** Sharp-edged, background #00FFFF, text #050505. No hover transition—the change should be instantaneous (zero-latency).
- **Ghost:** 1px Cyan border, transparent background. Hover state fills the background with a 10% Cyan tint.
- **Action Label:** Accompanied by a small technical ID (e.g., `[CMD_01]`) in the corner.

### Inputs & Text Fields
- Sharp 1px Slate borders. On focus, the border turns Electric Blue with a subtle glow. 
- Placeholder text uses the Monospace font at 50% opacity.

### Chips & Status Indicators
- Status chips use a "bracket" style instead of a background fill: `[ ACTIVE ]`.
- Pulsing "Signal" dot: A 4px square (not circle) that pulses with a cyan glow to indicate live data streams.

### Cards & Modules
- No background color (keep it #050505). Use a 1px border to define the shape.
- Header of the card should be separated by a horizontal 1px line, featuring a technical timestamp or "Sector ID" in the top right.

### Terminal Output (Special Component)
- A monospaced text block with a scanline overlay (1px horizontal lines at 10% opacity) to mimic a high-tech monitor.