---
name: Modern Heritage
colors:
  surface: '#fff8f5'
  surface-dim: '#e8d7cb'
  surface-bright: '#fff8f5'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fff1e8'
  surface-container: '#fdebdf'
  surface-container-high: '#f7e5d9'
  surface-container-highest: '#f1dfd3'
  on-surface: '#231a13'
  on-surface-variant: '#554336'
  inverse-surface: '#392e27'
  inverse-on-surface: '#ffeee2'
  outline: '#887364'
  outline-variant: '#dbc2b0'
  surface-tint: '#8f4e00'
  primary: '#8f4e00'
  on-primary: '#ffffff'
  primary-container: '#ff9933'
  on-primary-container: '#693800'
  inverse-primary: '#ffb77a'
  secondary: '#775a00'
  on-secondary: '#ffffff'
  secondary-container: '#fec72b'
  on-secondary-container: '#6f5400'
  tertiary: '#5f5e5e'
  on-tertiary: '#ffffff'
  tertiary-container: '#b3b1b1'
  on-tertiary-container: '#444444'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdcc2'
  primary-fixed-dim: '#ffb77a'
  on-primary-fixed: '#2e1500'
  on-primary-fixed-variant: '#6d3a00'
  secondary-fixed: '#ffdf98'
  secondary-fixed-dim: '#f5bf21'
  on-secondary-fixed: '#251a00'
  on-secondary-fixed-variant: '#5a4300'
  tertiary-fixed: '#e5e2e1'
  tertiary-fixed-dim: '#c8c6c5'
  on-tertiary-fixed: '#1c1b1b'
  on-tertiary-fixed-variant: '#474746'
  background: '#fff8f5'
  on-background: '#231a13'
  surface-variant: '#f1dfd3'
typography:
  display:
    fontFamily: Bricolage Grotesque
    fontSize: 64px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Bricolage Grotesque
    fontSize: 40px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Bricolage Grotesque
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Bricolage Grotesque
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Be Vietnam Pro
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Be Vietnam Pro
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Be Vietnam Pro
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 48px
  xl: 80px
  container-margin: 24px
  gutter: 16px
---

## Brand & Style
The design system embodies "Modern Heritage," a visual bridge between the bustling, tactile energy of Indian street culture and the refined precision of contemporary cafe dining. The brand personality is vibrant, warm, and premium, avoiding the cliches of traditional "ethnic" design in favor of an editorial, high-craft aesthetic.

The UI should evoke a sense of aromatic warmth and communal gathering. We achieve this through a "Tactile Modernist" style—pairing the raw, expressive energy of bold typography with the cleanliness of soft-shadowed surfaces and a spacious, editorial layout. The emotional response is one of sophisticated comfort: the reliability of a high-end service with the soul of a roadside chai stall.

## Colors
The palette is rooted in the spices and materials of the craft. 

- **Primary (Saffron Orange):** Used for primary actions and brand emphasis. It represents energy and the core "heat" of the experience.
- **Secondary (Turmeric Yellow):** A supportive, bright accent used for highlights, badges, and secondary buttons.
- **Neutral (Deep Charcoal):** Provides high-contrast grounding for all typography and structural elements, ensuring accessibility and a premium feel.
- **Background (Oat):** A warm, off-white surface that prevents the "clinical" feel of pure white, providing a soft, paper-like canvas for the content.

Use Saffron and Turmeric sparingly as accents against the Charcoal and Oat to maintain a premium "editorial" balance rather than an overwhelming "fast food" look.

## Typography
The typography strategy pairs expressive, quirky display type with a clean, humanist sans-serif.

- **Bricolage Grotesque** is our voice. Its unique terminal shapes and bold weight capture the "heritage" aspect with a contemporary, slightly rustic twist. It should be used for headlines, prices, and impactful pull-quotes.
- **Be Vietnam Pro** handles the heavy lifting. Chosen for its warmth and high legibility, it ensures that long menus and descriptions remain approachable.

Maintain tight leading for headlines to emphasize their "blocky," sign-painted feel, and generous leading for body text to enhance the premium, breathable reading experience.

## Layout & Spacing
This design system utilizes an **Editorial Fluid Grid**. It is designed to feel like a modern food magazine, with varying column spans and significant "white space" (rendered in our Oat background color).

- **Desktop:** 12-column grid with 80px side margins. Elements should frequently "break" the grid or use asymmetrical alignments to feel more organic.
- **Mobile:** 4-column grid with 24px margins. Spacing scales down, but padding within cards remains generous to maintain the "premium" feel.
- **Spacing Rhythm:** Based on an 8px scale. Use `lg` (48px) or `xl` (80px) spacing between major sections to emphasize the "Modern Heritage" premium airiness.

## Elevation & Depth
Depth is created through **Tonal Layers** and **Soft Ambient Shadows**. 

Instead of traditional grey shadows, this design system uses shadows with a tiny hint of the Saffron primary color (#FF9933) mixed into the Charcoal (#1A1A1A) at very low opacity (8-12%). This creates a "warm glow" effect that feels more natural and rustic.

- **Surface Level:** The Oat background is the lowest level.
- **Card Level:** Uses a very soft, diffused shadow (Blur: 24px, Y: 8px) to appear slightly lifted.
- **Interactive Level:** On hover, buttons and cards should increase their shadow spread slightly, mimicking a physical object being picked up.
- **Navigation:** Top bars use a subtle backdrop blur (Glassmorphism) if they overlay photography, but otherwise remain flat on the Oat surface with a thin 1px stroke in a darker shade of Oat.

## Shapes
The shape language is friendly and organic, avoiding sharp corners to reflect the "soft" nature of street food and steam.

- **Standard Elements:** Buttons and small inputs use a 0.5rem (8px) radius.
- **Containers:** Menu cards, modal containers, and hero image frames use a 1rem (16px) radius to emphasize their presence as primary containers.
- **Pill Elements:** Tags and category chips use a fully rounded (pill) style to contrast against the more structured headline type.

## Components
- **Buttons:** Primary buttons are solid Saffron with Charcoal text. Secondary buttons use a Turmeric background. Ghost buttons use a Charcoal outline. All buttons should have a minimum height of 48px to feel "chunky" and tactile.
- **Cards:** Food items and blog posts are housed in Oat-colored cards with a 1px border (#E5E1DA) and soft ambient shadows. Images should have a 16px top-corner radius.
- **Chips/Filters:** Used for dietary labels (e.g., "Vegan," "Spicy"). Use Turmeric with Charcoal text for active states.
- **Inputs:** Text fields use a solid Oat background with a 1px Charcoal border. Labels always sit above the field in `label-md` (uppercase) style.
- **Lists:** Menu lists should use "Dot Leaders" (connecting the item name to the price) to evoke a classic cafe feel, rendered in Bricolage Grotesque.
- **Icons:** Use thick-stroke (2pt) icons with rounded caps to match the typography's weight and the corner radius of the components.