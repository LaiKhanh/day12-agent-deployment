# Deployment Information

## Production Environment

### Public URL
```
https://2a202600375-production.up.railway.app/
```

### Platform
Railway

## API Testing

### Health Check

**Command:**
```bash
curl https://2a202600375-production.up.railway.app/health
```

**Expected Response:**
```json
{"status": "ok"}
```

### Readiness Check (Redis)

**Command:**
```bash
curl https://2a202600375-production.up.railway.app/ready
```

**Expected Response:**
```json
{"status": "ready"}
```

### Ask Endpoint

**Command:**
```bash
curl -X POST https://2a202600375-production.up.railway.app/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: secret" \
  -d '{"question":"what is docker"}'
```

**Expected Response:**
```json
{
  "answer": "Container là cách đóng gói app để chạy ở mọi nơi. Build once, run anywhere!",
  "history_length": 1
}
```