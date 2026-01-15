from typing import Annotated
from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import mapped_column

intpk = Annotated[int, mapped_column(Integer, primary_key=True, index=True)]
created_at = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now()
    ),
]
str20 = Annotated[str, mapped_column(String(20))]
str50 = Annotated[str, mapped_column(String(50))]
