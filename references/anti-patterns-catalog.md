# Comprehensive Anti-Patterns Catalog (Negative Prompting)

Negative prompting is the explicit prohibition of anti-patterns and bad coding habits in prompt engineering. By defining what **NOT** to do, LLMs constrain their search space and avoid common shortcuts.

---

## 1. TypeScript & JavaScript Anti-Patterns

### ❌ Anti-Pattern 1: The `any` Escape Hatch
<!-- ks-lint-ignore-next -->
```typescript
// BAD
function processData(input: any): any {
  return input.map((item: any) => item.value);
}
```
### ✅ Clean Replacement: Strict Generics & Unknown
```typescript
// GOOD
interface IdentifiableItem<T> {
  value: T;
}

function processData<T>(input: IdentifiableItem<T>[]): T[] {
  return input.map((item) => item.value);
}
```

---

### ❌ Anti-Pattern 2: Mutating State in React
```tsx
// BAD
const handleAddItem = (newItem: string) => {
  items.push(newItem); // Direct mutation!
  setItems(items);
};
```
### ✅ Clean Replacement: Immutable Array Expansion
```tsx
// GOOD
const handleAddItem = (newItem: string) => {
  setItems((prev) => [...prev, newItem]);
};
```

---

## 2. Python Anti-Patterns

### ❌ Anti-Pattern 1: Bare `except: pass` (Silent Failure)
```python
# BAD
try:
    data = fetch_remote_resource()
except:
    pass  # Swallows KeyboardInterrupt, SystemExit, and obscures real bugs!
```
### ✅ Clean Replacement: Specific Exception Logging
```python
# GOOD
import logging

try:
    data = fetch_remote_resource()
except ResourceNotFoundError as e:
    logging.warning(f"Resource not found, falling back to default: {e}")
    data = default_fallback()
except Exception as e:
    logging.exception(f"Unexpected error fetching resource: {e}")
    raise
```

---

### ❌ Anti-Pattern 2: Mutable Default Arguments
```python
# BAD
def append_entry(entry: str, collection: list = []):
    collection.append(entry)
    return collection
```
### ✅ Clean Replacement: `None` Sentinel Pattern
```python
# GOOD
def append_entry(entry: str, collection: list | None = None) -> list:
    if collection is None:
        collection = []
    collection.append(entry)
    return collection
```

---

## 3. SQL & Database Anti-Patterns

### ❌ Anti-Pattern 1: String Concatenation Query (SQLi)
<!-- ks-lint-ignore-next -->
```javascript
// BAD
const query = `SELECT * FROM users WHERE email = '${userEmail}'`;
```
### ✅ Clean Replacement: Parameterized Prepared Statements
```javascript
// GOOD
const query = `SELECT id, email, created_at FROM users WHERE email = $1 LIMIT 1`;
const result = await db.query(query, [userEmail]);
```
