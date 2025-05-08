from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

SQLALCHEMY_DATABASE_URL = "postgresql://newmek_job:w7z2DXWhK$hlTKg@192.168.2.75/job_board"
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logging.critical(f"Failed to create DB engine: {e}")
    raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logging.error(f"Error during DB session: {e}")
        raise
    finally:
        db.close()




# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# import logging
#
# # Use the asyncpg driver
# DATABASE_URL = "postgresql+asyncpg://newmek_job:w7z2DXWhK$hlTKg@192.168.2.75/job_board"
#
# try:
#     engine = create_async_engine(DATABASE_URL, echo=False, future=True)
#     AsyncSessionLocal = sessionmaker(
#         bind=engine,
#         class_=AsyncSession,
#         expire_on_commit=False,
#         autoflush=False,
#         autocommit=False
#     )
# except Exception as e:
#     logging.critical(f"Failed to create async DB engine: {e}")
#     raise
#
# # Dependency to get an async DB session
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         except Exception as e:
#             logging.error(f"Error during async DB session: {e}")
#             raise
