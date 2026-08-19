# Ambiguity Resolver: Zero-Delay Enterprise Assumptions

## Scenario: User sends an ultrashort prompt: `"crea un login"`

---

### ❌ Before (Naive LLM Behavior - Rhetorical Stalling)
> *"¡Hola! Con gusto te ayudo a crear un login. Antes de empezar, por favor indícame:*
> 1. *¿Qué framework prefieres (React, Vue, Angular, Next.js)?*
> 2. *¿Qué base de datos usaremos?*
> 3. *¿Quieres autenticación con JWT o sesiones de cookies?*
> 4. *¿Qué diseño o estilos te gustaría usar?*
> *¡Quedo atento a tus respuestas para comenzar!"*

*(Result: 0 code generated, wasted turn, user frustration).*

---

### ✅ After (KS Cognitive Engine Behavior - Immediate Production Execution)
> *"Creando módulo de autenticación y login de producción basado en el stack detectado (Next.js App Router + TypeScript + Tailwind + Zod + JWT seguro):"*
> 
> ```tsx
> // 1. Server Action / Route Handler con validación Zod y cookies HttpOnly
> // 2. Componente de UI accesible con estados de carga y error
> // 3. Middleware de protección de rutas
> ```
> *(Result: Complete, working, production-grade system delivered on turn 1).*
