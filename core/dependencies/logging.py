from fastapi import BackgroundTasks

class Logging:
    def __init__(self, background_tasks: BackgroundTasks):
        self.background_tasks = background_tasks
        
    async def log_info(self, message: str):
        self.background_tasks.add_task(self._log, message, "INFO")