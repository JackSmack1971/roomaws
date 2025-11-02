# .roo/rules-design-engineer/40-component-standards.md
> Naming conventions, prop interfaces, and composition patterns for consistent component development.

## Naming Conventions
- **Component files**: PascalCase (Button.tsx, UserProfile.tsx).
- **Component names**: PascalCase, descriptive (PrimaryButton, not Btn).
- **File organization**: One component per file, index.ts for exports.
- **Test files**: ComponentName.test.tsx in same directory.
- **Story files**: ComponentName.stories.tsx in same directory.

## Prop Interfaces
- **Interface naming**: ComponentNameProps (ButtonProps, CardProps).
- **Required vs optional**: Use ? for optional props, avoid undefined unions.
- **Primitive types**: Prefer string | number | boolean over complex unions.
- **Event handlers**: onEventName: (event: EventType) => void.

## Component Structure
- **Export pattern**: export default function ComponentName(props: Props) { ... }
- **Prop destructuring**: const { prop1, prop2, ...rest } = props;
- **Forward refs**: Use React.forwardRef for focusable components.
- **Generic constraints**: Use extends for constrained generics.

## Composition Patterns
- **Compound components**: Related components grouped together.
- **Render props**: For flexible component behavior.
- **Children as function**: For advanced composition patterns.
- **Higher-order components**: For cross-cutting concerns.

## TypeScript Standards
- **Strict mode**: Enable strict TypeScript settings.
- **No any**: Avoid any type, use unknown or specific types.
- **Discriminated unions**: Use for variant props.
- **Utility types**: Leverage Pick, Omit, Partial appropriately.

## Styling Patterns
- **Tailwind first**: Use Tailwind utilities for styling.
- **CSS variables**: For theme values and dynamic styling.
- **Class variance authority**: For component variants.
- **Responsive utilities**: Mobile-first responsive design.

## State Management
- **Local state**: useState for component-specific state.
- **Derived state**: useMemo for computed values.
- **Effects**: useEffect for side effects with proper dependencies.
- **Context**: For theme and global UI state.

## Performance Patterns
- **Memoization**: React.memo for expensive components.
- **Callback stability**: useCallback for event handlers.
- **Lazy loading**: React.lazy for code splitting.
- **Bundle analysis**: Monitor component bundle sizes.

## Documentation Standards
- **JSDoc comments**: For complex prop types and component behavior.
- **Storybook docs**: Comprehensive usage examples.
- **README files**: Component usage and API documentation.
- **Type definitions**: Exported for library consumers.