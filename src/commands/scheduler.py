import schedule
import time
from datetime import datetime
from src.db.session import SessionLocal
from src.repositories.task_repository import TaskRepository
from src.commands.autoclose_overdue import AutocloseOverdueTasksCommand

def run_autoclose_command():
    db: Session = SessionLocal()
    try:
        task_repo = TaskRepository(db)
        command = AutocloseOverdueTasksCommand(task_repo)
        count = command.execute()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Auto-closed {count} overdue tasks.")
    except Exception as e:
        db.rollback()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR during autoclose: {e}")
    finally:
        db.close()

def start_scheduler():
    schedule.every(15).minutes.do(run_autoclose_command)  # Per PDF suggestion
    print("Scheduler started. Overdue task check runs every 15 minutes.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()
