# TypeScript & React: Before and After Examples

## Scenario: API Client with State Management

### ❌ Before (Naive LLM Output with Anti-Patterns)
```typescript
import React, { useState, useEffect } from 'react';

// BAD: any type
export default function UserList() {
  const [users, setUsers] = useState<any>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // BAD: unhandled promise rejection
    fetch('/api/users')
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      });
  }, []);

  const deleteUser = (id: any) => {
    // BAD: mutating state directly
    const index = users.findIndex((u: any) => u.id === id);
    if (index !== -1) {
      users.splice(index, 1);
      setUsers(users);
    }
  };

  return <div>...</div>;
}
```

---

### ✅ After (KS Cognitive Engine Clean Code)
```tsx
import React, { useState, useEffect, useCallback } from 'react';

export interface User {
  readonly id: string;
  readonly name: string;
  readonly email: string;
  readonly createdAt: string;
}

export function UserList(): React.JSX.Element {
  const [users, setUsers] = useState<readonly User[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUsers = useCallback(async (signal?: AbortSignal) => {
    try {
      setLoading(true);
      setError(null);
      const res = await fetch('/api/users', { signal });
      if (!res.ok) {
        throw new Error(`Failed to fetch users (HTTP ${res.status})`);
      }
      const data: User[] = await res.json();
      setUsers(data);
    } catch (err: unknown) {
      if (err instanceof Error && err.name === 'AbortError') return;
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    fetchUsers(controller.signal);
    return () => controller.abort();
  }, [fetchUsers]);

  const handleDeleteUser = useCallback((userId: string) => {
    setUsers((prev) => prev.filter((u) => u.id !== userId));
  }, []);

  if (loading) return <p>Loading users...</p>;
  if (error) return <p className="text-red-500">Error: {error}</p>;

  return (
    <ul className="divide-y divide-gray-200">
      {users.map((user) => (
        <li key={user.id} className="flex justify-between py-2">
          <span>{user.name} ({user.email})</span>
          <button 
            type="button" 
            onClick={() => handleDeleteUser(user.id)}
            className="text-red-600 hover:underline"
          >
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
}
```
