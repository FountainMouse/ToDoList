import sys
from typing import Optional
from datetime import datetime

from src.cli.services.project_service import ProjectService
from src.cli.services.task_service import TaskService
from src.cli.models.task import TaskStatus
from src.cli.exceptions.repository_exceptions import (
    NotFoundException,
    AlreadyExistsException,
    MaxLimitExceededException,
)


class CLI:
    def __init__(self):
        self.project_service = ProjectService()
        self.task_service = TaskService()

    def display_menu(self) -> None:
        print("\n" + "=" * 50)
        print("           مدیر لیست کارهای من (فاز ۱ - حافظه موقت)")
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

            try:
                if choice == "1":  # ایجاد پروژه
                    name = input("نام پروژه: ").strip()
                    if not name:
                        print("❌ نام پروژه نمی‌تواند خالی باشد.")
                        continue
                    desc = input("توضیحات (اختیاری): ").strip() or None
                    project = self.project_service.create(name, desc)
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
                    project = self.project_service.update(proj_id, name, desc)
                    print(f"✅ پروژه با شناسه {proj_id} ویرایش شد.")

                elif choice == "3":  # حذف پروژه
                    try:
                        proj_id = int(input("شناسه پروژه برای حذف: ").strip())
                    except ValueError:
                        print("❌ شناسه باید عدد باشد.")
                        continue
                    self.project_service.delete(proj_id)
                    print(f"✅ پروژه با شناسه {proj_id} و تمام تسک‌های آن حذف شد.")

                elif choice == "4":  # نمایش پروژه‌ها
                    projects = self.project_service.list()
                    if not projects:
                        print("⚠️  پروژه‌ای وجود ندارد.")
                    else:
                        print("\n--- لیست پروژه‌ها ---")
                        for p in projects:
                            print(f"شناسه: {p.id} | نام: {p.name}")
                            print(f"   ایجاد شده در: {p.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
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
                    task = self.task_service.create(proj_id, title, desc, deadline)
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
                    deadline = input("مهلت زمانی جدید (مثال: 2025-12-31 14:30 - اختیاری): ").strip() or None
                    status_input = input("وضعیت جدید (todo/doing/done - اختیاری): ").strip().lower()
                    status = status_input if status_input in ["todo", "doing", "done"] else None
                    task = self.task_service.update(task_id, title, desc, deadline, status)
                    print(f"✅ تسک با شناسه {task_id} ویرایش شد.")

                elif choice == "7":  # حذف تسک
                    try:
                        task_id = int(input("شناسه تسک برای حذف: ").strip())
                    except ValueError:
                        print("❌ شناسه باید عدد باشد.")
                        continue
                    self.task_service.delete(task_id)
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
                    task = self.task_service.change_status(task_id, status_str)
                    status_fa = {"todo": "انجام نشده", "doing": "در حال انجام", "done": "انجام شده"}
                    print(f"✅ وضعیت تسک به «{status_fa[task.status.value]}» تغییر کرد.")

                elif choice == "9":  # نمایش تسک‌های پروژه
                    try:
                        proj_id = int(input("شناسه پروژه: ").strip())
                    except ValueError:
                        print("❌ شناسه باید عدد باشد.")
                        continue
                    tasks = self.task_service.list_by_project(proj_id)
                    if not tasks:
                        print("⚠️  تسکی در این پروژه وجود ندارد.")
                    else:
                        print(f"\n--- تسک‌های پروژه {proj_id} ---")
                        status_fa = {"todo": "انجام نشده", "doing": "در حال انجام", "done": "انجام شده"}
                        for t in tasks:
                            dl = t.deadline.strftime('%Y-%m-%d %H:%M') if t.deadline else "ندارد"
                            print(f"شناسه: {t.id} | عنوان: {t.title} | وضعیت: {status_fa[t.status.value]}")
                            print(f"   مهلت: {dl} | ایجاد: {t.created_at.strftime('%Y-%m-%d %H:%M')}")
                            if t.description:
                                print(f"   توضیحات: {t.description}")
                            print("-" * 40)

                else:
                    print("❌ گزینه نامعتبر است. لطفاً عددی از منو انتخاب کنید.")

            except (ValueError, NotFoundException, AlreadyExistsException, MaxLimitExceededException) as e:
                print(f"❌ خطا: {e}")
            except Exception as e:
                print(f"❌ خطای غیرمنتظره: {e}")


if __name__ == "__main__":
    CLI().run()
