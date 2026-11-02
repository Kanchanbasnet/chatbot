from backend.database import Base, engine
from backend.models import Conversation, Document, Message  # noqa: F401

Base.metadata.create_all(bind=engine)
print("Tables created.")