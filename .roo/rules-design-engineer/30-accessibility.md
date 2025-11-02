# .roo/rules-design-engineer/20-accessibility.md
> WCAG 2.1 AA compliance requirements for all UI components and interfaces.

## Core Principles
- **Perceivable**: Information and UI components must be presentable to users in ways they can perceive.
- **Operable**: UI components and navigation must be operable.
- **Understandable**: Information and operation of UI must be understandable.
- **Robust**: Content must be robust enough to be interpreted by a wide variety of user agents.

## Color & Contrast (1.4.3, 1.4.11)
- **Text contrast**: Normal text ≥4.5:1, large text ≥3:1 against background.
- **Non-text contrast**: UI components ≥3:1 against adjacent colors.
- **Color independence**: Don't rely solely on color to convey information.
- **Focus indicators**: Visible focus indicators with ≥3:1 contrast.

## Keyboard Navigation (2.1.1, 2.1.3)
- **All functionality keyboard accessible**: No mouse-only interactions.
- **Logical tab order**: Tab order follows logical reading order.
- **Keyboard traps avoided**: Users can navigate away from all components.
- **Skip links**: Provide mechanism to skip repetitive navigation.

## Screen Reader Support (1.1.1, 1.3.1, 4.1.2)
- **Alt text**: All images have descriptive alt text or are marked decorative.
- **Semantic HTML**: Use appropriate semantic elements (headings, lists, landmarks).
- **ARIA labels**: Use ARIA labels/labels for form controls and interactive elements.
- **Live regions**: Use ARIA live regions for dynamic content updates.

## Focus Management (2.4.3, 2.4.7, 3.2.1)
- **Visible focus**: Focus indicators are always visible and obvious.
- **Focus order**: Logical and predictable focus movement.
- **Modal focus**: Focus trapped within modals, returned to trigger on close.
- **Consistent behavior**: Focus behavior consistent across similar components.

## Forms & Input (1.3.5, 3.3.1-3.3.4)
- **Field labels**: All form fields have visible labels.
- **Error identification**: Form errors clearly identified and described.
- **Error suggestions**: Provide suggestions for correcting input errors.
- **Required fields**: Required fields clearly marked.

## Motion & Animation (2.3.1, 2.3.3)
- **Motion sensitivity**: Respect user's motion preferences (prefers-reduced-motion).
- **Animation control**: Provide controls for animations longer than 5 seconds.
- **No vestibular triggers**: Avoid animations that may cause vestibular disorders.

## Media & Multimedia (1.2.1-1.2.5)
- **Captions**: Synchronized captions for prerecorded video.
- **Audio description**: Audio description for prerecorded video.
- **Media controls**: Custom media players provide accessible controls.

## Implementation Requirements
- **Automated testing**: Use axe-core or similar for automated accessibility checks.
- **Manual testing**: Screen reader testing with NVDA/JAWS/VoiceOver.
- **Cross-browser**: Test in multiple browsers with accessibility tools.
- **Documentation**: Document accessibility features and testing procedures.