from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class File:
  id: str
  name: str
  mimeType: str
  driveFileId: str
  url: str
  uploadedById: str
  fileableId: str
  fileableType: str
  uploadedAt: datetime = field(default_factory=datetime.now)
  createdAt: datetime = field(default_factory=datetime.now)
