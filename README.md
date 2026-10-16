# Aegis

A defensive AI-amplified cyber threat mitigation MVP.

## Run

1. `docker compose up --build`
2. `docker compose exec api alembic upgrade head`
3. `docker compose exec api python /scripts/seed.py`
4. Open `http://localhost:3000/overview`

## Default Seed Users

- admin@example.com / Password123!
- analyst@example.com / Password123!
- viewer@example.com / Password123!
