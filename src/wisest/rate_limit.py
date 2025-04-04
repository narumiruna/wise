from aiolimiter import AsyncLimiter

rate_limit = AsyncLimiter(1, 0.05)
