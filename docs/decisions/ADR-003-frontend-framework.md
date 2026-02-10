# ADR-003: Frontend Framework Selection

## Status
Accepted

## Context
We need to select a frontend framework and associated tools for the LLM Test Platform UI. Requirements include:
- Modern React development experience
- TypeScript support
- Fast development iteration
- Component library for consistent UI
- State management for auth and data
- Routing for SPA navigation

## Decision
We will use the following stack:

### Core Framework
- **Vite + React + TypeScript**: Fast build tool with excellent HMR and TypeScript support

### Styling
- **Tailwind CSS v4**: Utility-first CSS framework with Vite plugin
- **Shadcn/ui**: Copy-paste component library (not npm package), built on Radix UI primitives

### State Management
- **Zustand**: Lightweight, TypeScript-friendly state management
- Persist middleware for auth state

### Routing
- **React Router DOM v7**: Standard routing solution for React SPAs

### Additional Libraries
- **class-variance-authority**: For variant-based component styling
- **clsx + tailwind-merge**: For conditional class merging
- **lucide-react**: Icon library

## Alternatives Considered

### Framework
1. **Next.js**: Overkill for this SPA, adds SSR complexity we don't need
2. **Create React App**: Deprecated, slower than Vite
3. **Remix**: Good option but steeper learning curve

### Component Library
1. **Material UI**: Heavy, opinionated design
2. **Chakra UI**: Good but larger bundle size
3. **Ant Design**: Enterprise-focused, less customizable

### State Management
1. **Redux Toolkit**: More boilerplate than needed
2. **Jotai/Recoil**: Atomic state not required for this app
3. **React Query**: Will add later for server state

## Consequences

### Positive
- Fast development with Vite's HMR
- Full TypeScript support
- Customizable UI with Tailwind + Shadcn
- Simple state management with Zustand
- Small bundle size

### Negative
- Shadcn components require manual installation
- Tailwind v4 is newer, less community examples
- Need to set up path aliases manually

## Implementation Notes

### Path Aliases
Configured `@/*` alias in both `vite.config.ts` and `tsconfig.app.json`:
```typescript
// vite.config.ts
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
  },
}
```

### Project Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/      # Layout components
│   │   └── ui/          # Shadcn UI components
│   ├── lib/             # Utilities (cn function)
│   ├── pages/           # Route pages
│   ├── stores/          # Zustand stores
│   ├── App.tsx          # Main app with routing
│   └── index.css        # Tailwind imports + theme
├── .env.example         # Environment template
└── vite.config.ts       # Vite configuration
```

## References
- [Vite Documentation](https://vite.dev/)
- [Shadcn/ui](https://ui.shadcn.com/)
- [Tailwind CSS v4](https://tailwindcss.com/docs/v4-beta)
- [Zustand](https://zustand-demo.pmnd.rs/)
