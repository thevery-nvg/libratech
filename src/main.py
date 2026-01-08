from src.core.config import settings
from src.core.app import app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=settings.run.host, port=settings.run.port)
