---
name: Cyber-Minimalist Portfolio
colors:
  surface: '#12131a'
  surface-dim: '#12131a'
  surface-bright: '#383940'
  surface-container-lowest: '#0c0e14'
  surface-container-low: '#1a1b22'
  surface-container: '#1e1f26'
  surface-container-high: '#282a31'
  surface-container-highest: '#33343c'
  on-surface: '#e2e1eb'
  on-surface-variant: '#bcc9cd'
  inverse-surface: '#e2e1eb'
  inverse-on-surface: '#2f3037'
  outline: '#869397'
  outline-variant: '#3d494c'
  surface-tint: '#4cd7f6'
  primary: '#4cd7f6'
  on-primary: '#003640'
  primary-container: '#06b6d4'
  on-primary-container: '#00424f'
  inverse-primary: '#00687a'
  secondary: '#c3c0ff'
  on-secondary: '#1d00a5'
  secondary-container: '#3626ce'
  on-secondary-container: '#b3b1ff'
  tertiary: '#ffb873'
  on-tertiary: '#4b2800'
  tertiary-container: '#e89337'
  on-tertiary-container: '#5b3200'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#acedff'
  primary-fixed-dim: '#4cd7f6'
  on-primary-fixed: '#001f26'
  on-primary-fixed-variant: '#004e5c'
  secondary-fixed: '#e2dfff'
  secondary-fixed-dim: '#c3c0ff'
  on-secondary-fixed: '#0f0069'
  on-secondary-fixed-variant: '#3323cc'
  tertiary-fixed: '#ffdcbf'
  tertiary-fixed-dim: '#ffb873'
  on-tertiary-fixed: '#2d1600'
  on-tertiary-fixed-variant: '#6a3b00'
  background: '#12131a'
  on-background: '#e2e1eb'
  surface-variant: '#33343c'
typography:
  display-2xl:
    fontFamily: Syne
    fontSize: 120px
    fontWeight: '800'
    lineHeight: 110px
    letterSpacing: -0.04em
  display-lg:
    fontFamily: Syne
    fontSize: 72px
    fontWeight: '700'
    lineHeight: 72px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Syne
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Syne
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0.05em
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
spacing:
  unit: 8px
  gutter: 24px
  margin-mobile: 24px
  margin-desktop: 80px
  section-gap: 160px
---

## Brand & Style
This design system is engineered for an Applied AI Specialist, blending **Cyber-Minimalism** with a **Deep Tech** aesthetic. It prioritizes high-end editorial layouts, extreme negative space, and a clinical, professional atmosphere. 

The visual narrative is "The Architect of Intelligence"—clean, precise, and unapologetically digital. It utilizes a mix of **Brutalism** (sharp edges, massive type) and **Glassmorphism** (translucent layering) to create a sense of depth within a flat, high-contrast environment. The emotional response should be one of awe, technical authority, and futuristic sophistication.

## Colors
The palette is rooted in an absolute dark mode to maximize contrast and focus.

*   **Background:** Absolute Black (#050505) provides an infinite canvas.
*   **Neural Cyan:** Used for primary actions, data visualizations, and active states.
*   **Electric Indigo:** Used for secondary accents, hover states, and deep gradients.
*   **Neutral Gray:** Zinc/Slate tones are used for body text and inactive elements to ensure the primary colors remain impactful.
*   **Borders:** Subtle, 1px translucent white borders provide structure without breaking the dark immersion.

## Typography
The typography system uses a high-contrast pairing to distinguish between "The Visionary" (Headlines) and "The Engineer" (Technical subtext).

*   **Syne:** Utilized for massive, brutalist headings. It should be typeset with tight tracking to create a rhythmic, architectural feel.
*   **Inter:** Used for body copy to maintain readability amidst the high-contrast aesthetic.
*   **JetBrains Mono:** Dedicated to technical metadata, labels, tags, and small captions, emphasizing the "Applied AI" nature of the work.

## Layout & Spacing
The layout follows a **fixed 12-column grid** on desktop with wide margins to create a high-end editorial feel. 

*   **Extreme Negative Space:** Vertical spacing between major sections is aggressive (160px+) to allow the portfolio pieces to breathe.
*   **Asymmetry:** Elements should often be offset from the center or occupy specific grid spans (e.g., body text spanning columns 5-10) to create dynamic visual interest.
*   **Mobile:** Transition to a 4-column grid with 24px gutters. Typography scales aggressively to maintain the "display" impact.

## Elevation & Depth
Depth is created through transparency and light rather than shadows.

*   **Glassmorphism:** Cards and modals utilize a `backdrop-filter: blur(20px)` with a semi-transparent black fill (`rgba(5, 5, 5, 0.7)`).
*   **Translucent Borders:** Surfaces are defined by 1px borders of `rgba(255, 255, 255, 0.1)`.
*   **Glow Accents:** Use "Neural Cyan" as a soft, low-opacity radial gradient background behind key sections to simulate a digital screen glow.
*   **Layering:** Elements should feel like they are floating on glass sheets over a void.

## Shapes
The shape language is strictly **Brutalist and Sharp**. 

*   **0px Radius:** All buttons, cards, inputs, and image containers must have absolute 0px corners.
*   **Geometric Precision:** Use perfectly square or rectangular containers. 
*   **Vertical Lines:** Incorporate thin 1px vertical lines to act as dividers or timeline markers, reinforcing the technical, blueprint-like feel.

## Components
*   **Buttons:** Rectangular with no radius. Primary buttons feature a solid Neural Cyan background with black text. Secondary buttons are outlined in 1px Electric Indigo with a hover state that fills the background.
*   **Chips/Tags:** Monospaced text (JetBrains Mono) inside a 1px border. No background fill.
*   **Inputs:** Minimalist "Border-Bottom-Only" style. The line should be 1px gray, turning Cyan on focus with a subtle glow effect.
*   **Cards:** 1px translucent borders, deep black interiors with glassmorphism blur. Hovering a card should shift the border color to Electric Indigo.
*   **Timeline:** A minimalist vertical 1px line. Milestones are marked by small 4px x 4px solid squares rather than circles.
*   **Navigation:** A top-fixed bar, ultra-thin, with a heavy backdrop blur. Link items in JetBrains Mono with "01", "02" numbering prefixes.