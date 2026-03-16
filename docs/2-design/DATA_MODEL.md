# Data Model

> Define your Supabase schema before writing any code.
> Create tables in the Supabase Dashboard → Table Editor, or via SQL in the SQL Editor.

---

## Entity Relationship Overview

```
[auth.users]  ←── managed by Supabase Auth, do not modify directly
      │
      │ 1
      │
      * (many)
[profiles]    ←── extend user data here (display name, avatar, etc.)
      │
      │ 1
      │
      * (many)
[your_table]
```

---

## Tables

### profiles
Extends Supabase Auth users with app-specific fields. Created automatically via a trigger when a user signs up.

```sql
create table profiles (
  id          uuid primary key references auth.users(id) on delete cascade,
  name        text not null,
  avatar_url  text,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

-- RLS
alter table profiles enable row level security;

create policy "Users can view their own profile"
  on profiles for select using (auth.uid() = id);

create policy "Users can update their own profile"
  on profiles for update using (auth.uid() = id);
```

---

### [your_table] — replace with your main entity

```sql
create table [your_table] (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references auth.users(id) on delete cascade,
  title       text not null,
  content     text,
  status      text not null default 'active'
                check (status in ('active', 'archived')),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

-- Index for fast user queries
create index [your_table]_user_id_idx on [your_table](user_id);

-- RLS — users only see their own rows
alter table [your_table] enable row level security;

create policy "Users can view their own rows"
  on [your_table] for select using (auth.uid() = user_id);

create policy "Users can insert their own rows"
  on [your_table] for insert with check (auth.uid() = user_id);

create policy "Users can update their own rows"
  on [your_table] for update using (auth.uid() = user_id);

create policy "Users can delete their own rows"
  on [your_table] for delete using (auth.uid() = user_id);
```

---

<!-- Add a block for each table in your application -->

---

## Auto-update `updated_at` trigger

Apply this to any table that has an `updated_at` column:

```sql
-- Create the trigger function once
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

-- Apply to each table
create trigger set_updated_at
  before update on [your_table]
  for each row execute function update_updated_at();
```

---

## Auto-create profile on signup trigger

```sql
create or replace function handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, name)
  values (new.id, new.raw_user_meta_data->>'name');
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function handle_new_user();
```

---

## RLS Checklist

Before going to production, verify every table:

- [ ] RLS is **enabled** (`alter table X enable row level security`)
- [ ] There is a SELECT policy limiting rows to the owning user
- [ ] There is an INSERT policy with `with check (auth.uid() = user_id)`
- [ ] UPDATE and DELETE policies are present
- [ ] No policy accidentally exposes other users' data

> Test your policies: in the Supabase dashboard, use the Auth tab to simulate a request as a specific user.

---

## Supabase Storage Buckets (if needed)

| Bucket | Access | Purpose |
|--------|--------|---------|
| `avatars` | Public | User profile images |
| `uploads` | Private (RLS) | User-uploaded files |

```sql
-- Storage RLS example: users can only access their own folder
create policy "User folder access"
  on storage.objects for all
  using (auth.uid()::text = (storage.foldername(name))[1]);
```
