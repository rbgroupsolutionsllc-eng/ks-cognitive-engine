# SQL & Database: Before and After Examples

## Scenario: User Authentication & Query Lookup

### ❌ Before (Naive LLM Output with Anti-Patterns)
<!-- ks-lint-ignore-next -->
```javascript
// BAD: Direct string concatenation, unconstrained SELECT *
async function getUserByEmail(email) {
  const sql = `SELECT * FROM users WHERE email = '${email}'`;
  const result = await pool.query(sql);
  return result.rows[0];
}
```

---

### ✅ After (KS Cognitive Engine Clean Code)
```typescript
import { Pool, QueryResult } from 'pg';

export interface SafeUser {
  id: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: Date;
}

export async function getUserByEmail(pool: Pool, email: string): Promise<SafeUser | null> {
  const query = `
    SELECT id, email, role, created_at AS "createdAt"
    FROM users
    WHERE LOWER(email) = LOWER($1)
    LIMIT 1
  `;
  
  const result: QueryResult<SafeUser> = await pool.query(query, [email.trim()]);
  return result.rows[0] ?? null;
}
```
