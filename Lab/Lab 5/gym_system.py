
"""Manage fitness class bookings and export class rosters."""

import json
from pathlib import Path

CLASS_CAPACITY = {"Yoga": 3, "HIIT": 2, "Spin": 4}
rosters = {}
attendance_log = []


def book_class(member_id, class_name):
    """Book a member into a class if seats are available."""
    if class_name not in rosters:
        rosters[class_name] = []

    if len(rosters[class_name]) >= CLASS_CAPACITY.get(class_name, 0):
        print("Class full:", class_name)
        return False

    rosters[class_name].append(member_id)
    attendance_log.append(f"{member_id} -> {class_name}")
    return True


def cancel_booking(member_id, class_name):
    """Cancel an existing booking."""
    try:
        rosters[class_name].remove(member_id)
    except (KeyError, ValueError):
        print("Nothing to cancel")


def set_capacity(class_name, seats):
    """Set the capacity of a class."""
    if seats < 0:
        raise ValueError("Class capacity cannot be negative")
    CLASS_CAPACITY[class_name] = seats


def add_members(class_name, count):
    """Add walk-in guests to a class."""
    for index in range(count):
        book_class(f"GUEST-{index}", class_name)


def export_roster(file="gym_schedule.json"):
    """Export class rosters to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(rosters, output_file, indent=2)


def clear_old_exports(prefix="old_"):
    """Remove old JSON exports without invoking a shell."""
    for file_path in Path(".").glob(f"{prefix}*.json"):
        if file_path.is_file():
            file_path.unlink()


def show_rosters():
    """Display all class rosters."""
    for class_name, members in rosters.items():
        print(class_name, ":", ", ".join(str(member) for member in members))


def main():
    """Run the fitness booking demonstration."""
    book_class("M1", "Yoga")
    book_class("M2", "Yoga")
    book_class("M3", "Yoga")
    book_class("M4", "Yoga")
    book_class(55, "HIIT")
    book_class("M5", "Pilates")

    set_capacity("Spin", 0)
    add_members("Spin", 3)
    cancel_booking("M9", "Boxing")

    guest_input = input(
        "How many walk-in guests for HIIT? (Enter for 1): "
    ).strip()

    try:
        guest_count = int(guest_input or "1")
        if guest_count < 0:
            raise ValueError("Guest count cannot be negative")
    except ValueError as error:
        raise ValueError(
            "Enter a valid non-negative whole number"
        ) from error

    add_members("HIIT", guest_count)
    clear_old_exports()
    export_roster()
    show_rosters()


if __name__ == "__main__":
    main()
