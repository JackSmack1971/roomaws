# .roo/rules-design-engineer/30-responsive-design.md
> Mobile-first responsive design principles and breakpoint management for consistent cross-device experiences.

## Mobile-First Philosophy
- **Progressive enhancement**: Start with mobile layout, enhance for larger screens.
- **Content priority**: Most important content appears first in mobile layouts.
- **Touch targets**: Minimum 44px touch targets for mobile interactions.
- **Thumb-friendly**: Place important actions within easy thumb reach.

## Breakpoint Strategy
- **Consistent breakpoints**: Use standardized breakpoints across all components.
  - Mobile: < 640px (sm)
  - Tablet: 640px - 1023px (md, lg)
  - Desktop: ≥ 1024px (xl, 2xl)
- **Breakpoint naming**: Use Tailwind's default breakpoint names (sm, md, lg, xl, 2xl).
- **Breakpoint variables**: Define custom breakpoints in tailwind.config.js if needed.

## Layout Patterns
- **Fluid containers**: Use max-width containers with responsive padding.
- **Flexible grids**: CSS Grid and Flexbox for adaptive layouts.
- **Responsive typography**: Scale font sizes appropriately across breakpoints.
- **Adaptive spacing**: Use responsive margin/padding utilities.

## Component Responsiveness
- **Stack vs. row**: Components stack vertically on mobile, horizontal on larger screens.
- **Hide/show elements**: Use responsive visibility classes for conditional display.
- **Flexible sizing**: Use percentage widths and auto margins for fluid behavior.
- **Responsive images**: Use responsive image techniques (srcset, sizes).

## Navigation Patterns
- **Mobile navigation**: Hamburger menus, bottom navigation bars.
- **Tablet navigation**: Collapsible sidebars, tab bars.
- **Desktop navigation**: Full sidebars, top navigation bars.
- **Consistent behavior**: Navigation patterns remain consistent within breakpoint ranges.

## Performance Considerations
- **Lazy loading**: Load content as needed for performance.
- **Image optimization**: Serve appropriate image sizes per device.
- **Critical CSS**: Prioritize above-the-fold content loading.
- **Bundle splitting**: Load component code as needed.

## Testing Requirements
- **Device testing**: Test on actual devices, not just browser dev tools.
- **Orientation testing**: Test both portrait and landscape orientations.
- **Touch testing**: Verify touch interactions work properly.
- **Performance testing**: Ensure responsive designs don't impact performance.

## Implementation Guidelines
- **Utility-first**: Leverage Tailwind's responsive utilities extensively.
- **Component variants**: Create responsive variants of components.
- **Design tokens**: Use consistent spacing, typography, and color tokens.
- **Documentation**: Document responsive behavior in component stories.