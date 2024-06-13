from enum import Enum
class DocumentStateEnum(str, Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'