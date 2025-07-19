from typing import Optional

import gel

from utils.logging import get_logger
log = get_logger()


class Database:
    def __init__(self):
        self._client: gel.AsyncIOClient | None = None
    
    async def connect(self) -> None:
        try:
            self._client = gel.create_async_client(tls_security='insecure')
        except Exception as e:
            log.error(f"Failed to connect to Gel!")
            return
        try:
            await self._client.query_single("SELECT 1")
            log.info(f"Connected to Gel!")
        except Exception as e:
            raise log.critical(f"Failed to conect to Gel: {e}")
    
    @property
    def executor(self) -> gel.AsyncIOExecutor:
        if self._client is None:
            raise RuntimeError("Database not connected")
        return self._client
