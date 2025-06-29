from typing import Optional

import gel

from utils.logging import get_logger
log = get_logger()


class Database:
    def __init__(self):
        self._client: Optional[gel.AsyncIOClient] = None
    
    async def connect(self) -> None:
        self._client = gel.create_async_client()
        try:
            await self._client.query_single("SELECT 1")
            log.info(f"Connected to Gel!")
        except Exception as e:
            raise log.critical(f"Failed to conect to Gel: {e}")
