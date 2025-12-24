import sys
from typing import Optional
from sqlalchemy.orm import Session

from src.db.session import SessionLocal
from src.repositories.project_repository import ProjectRepository
from src.repositories.task_repository import TaskRepository
from src.services.project_service import ProjectService
from src.services.task_service import TaskService
from src.models.task import TaskStatus
from src.exceptions.repository_exceptions import NotFoundException

class CLI:
    def display_menu(self) -> None:
        print("\n" + "=" * 50)
        print("           مدیر لیست کارهای من (فاز ۲ - RDB)")
        print("=" * 50)
        print("  پروژه‌ها:")
        print("    1 - ایجاد پروژه")
        print("    2 - ویرایش پروژه")
        print("    3 - حذف پروژه")
        print("    4 - نمایش پروژه‌ها")
        print("  تسک‌ها:")
        print("    5 - افزودن تسک به پروژه")
        print("    6 - ویرایش تسک")
        print("    7 - حذف تسک")
        print("    8 - تغییر وضعیت تسک")
        print("    9 - نمایش تسک‌های پروژه")
        print("  دیگر:")
        print("    0 - خروج")
        print("=" * 50)

    def run(self) -> None:
        while True:
            self.display_menu()
            choice = input("انتخاب کنید: ").strip()

            if choice == "0":
                print("\nخداحافظ! 👋")
                sys.exit(0)

            # Open a new DB session for each command
            db: Session = SessionLocal()
            try:
                project_repo = ProjectRepository(db)
                task_repo = TaskRepository(db)
                project_service = ProjectService(project_repo)
                task_service = TaskService(task_repo)

                if choice == "1":  # ایجاد پروژه
                    name = input("نام پروژه: ").strip()
                    if not name:
                        print("❌ نام پروژه نمی‌تواند خالی باشد.")
                        continue
                    desc = input("توضیحات (اختیاری): ").strip() or None
                    project = project_service.create_project(name, desc)
                    print(f"✅ پروژه ایجاد شد - شناسه: {project.id}")

                elif choice == "2":  # ویرایش پروژه
                    try:
                        proj_id = int(input("شناسه پروژه: ").strip())
                    except ValueError:
                        print("❌ شناسه باید عدد باشد.")
                        continue
                    name = input("نام جدید پروژه: ").strip()
                    if not name:
                        print("❌ نام پروژه نمی‌تواند خالی باشد.")
                        continue
                    desc = input("توضیحات جدید (اختیاری): ").strip() or None
                    project = project_service.update_project(proj_id, name, desc)
                    print(f"✅ پروژه با شناسه {proj_id} ویرایش شد.")

                elif choice == "3":  # حذف پروژه
                    try:
                        proj_id = int(input("شناسه پروژه برای حذف: ").strip())
                    except ValueError:
                        print("❌ شناسه باید عدد باشد.")
                        continue
                    project_service.delete_project(proj_id)
                    print(f"✅ پروژه با شناسه {proj_id} و تمام تسک‌های آن حذف شد.")

                elif choice == "4":  # نمایش پروژه‌ها
                    projects = project_service.list_projects()
                    if not projects:
                        print("⚠️  پروژه‌ای وجود ندارد.")
                    else:
                        print("\n--- لیست پروژه‌ها ---")
                        for p in projects:
                            print(f"شناسه: {p.id} | نام: {p.name}")
                            if p.description:
                                print(f"   توضیحات: {p.description}")
                            print("-" * 30)

                elif choice == "5":  # افزودن تسک
                    try:
                        proj_id = int(input("شناسه پروژه: ").strip())
                    except ValueError:
                        print("❌ شناسه باید عدد باشد.")
                        continue
                    title = input("عنوان تسک: ").strip()
                    if not title:
                        print("❌ عنوان تسک نمی‌تواند خالی باشد.")
                        continue
                    desc = input("توضیحات (اختیاری): ").strip() or None
                    deadline = input("مهلت زمانی (مثال: 2025-12-31 14:30 - اختیاری): ").strip() or None
                    task = task_service.create_task(proj_id, title, desc, deadline)
                    status_fa = {"todo": "انجام نشده", "doing": "در حال انجام", "done": "انجام شده"}
                    print(f"✅ تسک اضافه شد - شناسه: {task.id} | وضعیت: {status_fa[task.status.value]}")

                elif choice == "6":  # ویرایش تسک
                    try:
                        task_id = int(input("شناسه تسک: ").strip())
                    except ValueError:
                        print("❌ شناسه باید عدد باشد.")
                        continue
                    title = input("عنوان جدید: ").strip()
                    if not title:
                        print("❌ عنوان نمی‌تواند خالی باشد.")
                        continue
                    desc = input("توضیحات جدید (اختیاری): ").strip() or None
                    deadline = input("مهلت زمانی جدید (اختیاری): ").strip() or None
                    status_input = input("وضعیت جدید (todo/doing/done - اختیاری): ").strip().lower()
                    status = TaskStatus(status_input) if status_input in ["todo", "doing", "done"] else None
                    # Note: update_task needs project_id - we'll get it from task
                    task = task_repo.get_by_id(task.project_id, task_id)  # rough, but works
                    task_service.update_task(task.project_id, task_id, title, desc, deadline, status)
                    print(f"✅ تسک با شناسه {task_id} ویرایش شد.")

                elif choice == "7":  # حذف تسک
                    try:
                        task_id = int(input("شناسه تسک برای حذف: ").strip())
                    except ValueError:
                        print("❌ شناسه باید عدد باشد.")
                        continue
                    # Need project_id - ask or get from task
                    proj_id = int(input("شناسه پروژه تسک: ").strip())
                    task_service.delete_task(proj_id, task_id)
                    print(f"✅ تسک با شناسه {task_id} حذف شد.")

                elif choice == "8":  # تغییر وضعیت تسک
                    try:
                        task_id = int(input("شناسه تسک: ").strip())
                    except ValueError:
                        print("❌ شناسه باید عدد باشد.")
                        continue
                    print("وضعیت‌های ممکن: todo, doing, done")
                    status_str = input("وضعیت جدید: ").strip().lower()
                    if status_str not in ["todo", "doing", "done"]:
                        print("❌ وضعیت نامعتبر است.")
                        continue
                    # Need project_id
                    proj_id = int(input("شناسه پروژه تسک: ").strip())
                    task_service.update_task(proj_id, task_id, None, None, None, TaskStatus(status_str))
                    status_fa = {"todo": "انجام نشده", "doing": "در حال انجام", "done": "انجام شده"}
                    print(f"✅ وضعیت تسک به «{status_fa[status_str]}» تغییر کرد.")

                elif choice == "9":  # نمایش تسک‌های پروژه
                    try:
                        proj_id = int(input("شناسه پروژه: ").strip())
                    except ValueError:
                        print("❌ شناسه باید عدد باشد.")
                        continue
                    tasks = task_service.list_tasks_by_project(proj_id)
                    if not tasks:
                        print("⚠️  تسکی در این پروژه وجود ندارد.")
                    else:
                        print(f"\n--- تسک‌های پروژه {proj_id} ---")
                        status_fa = {"todo": "انجام نشده", "doing": "در حال انجام", "done": "انجام شده"}
                        for t in tasks:
                            dl = t.deadline.strftime('%Y-%m-%d %H:%M') if t.deadline else "ندارد"
                            print(f"شناسه: {t.id} | عنوان: {t.title} | وضعیت: {status_fa[t.status.value]}")
                            print(f"   مهلت: {dl}")
                            if t.description:
                                print(f"   توضیحات: {t.description}")
                            print("-" * 40)

                else:
                    print("❌ گزینه نامعتبر است.")

            except NotFoundException as e:
                print(f"❌ خطا: {e}")
            except ValueError as e:
                print(f"❌ خطا: {e}")
            except Exception as e:
                print(f"❌ خطای غیرمنتظره: {e}")
                db.rollback()
            finally:
                db.close()


if __name__ == "__main__":
    CLI().run()
