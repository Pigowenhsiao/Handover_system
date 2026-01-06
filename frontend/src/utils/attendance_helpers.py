"""Shared helpers for attendance calculations and validation."""


def build_attendance_notes(regular_reason, contract_reason, regular_label, contract_label):
    parts = []
    if regular_reason:
        parts.append(f"{regular_label}: {regular_reason}")
    if contract_reason:
        parts.append(f"{contract_label}: {contract_reason}")
    return " / ".join(parts)


def compute_attendance_totals(reg_scheduled, reg_present, con_scheduled, con_present):
    total_scheduled = reg_scheduled + con_scheduled
    total_present = reg_present + con_present
    total_absent = (reg_scheduled - reg_present) + (con_scheduled - con_present)
    overall_rate = (total_present / total_scheduled * 100) if total_scheduled > 0 else 0
    return {
        "total_scheduled": total_scheduled,
        "total_present": total_present,
        "total_absent": total_absent,
        "overall_rate": overall_rate,
    }


def validate_attendance_values(regular, contractor, overtime, translate):
    errors = []

    reg_sched = regular.get("scheduled", 0)
    reg_present = regular.get("present", 0)
    reg_absent = regular.get("absent", 0)

    con_sched = contractor.get("scheduled", 0)
    con_present = contractor.get("present", 0)
    con_absent = contractor.get("absent", 0)

    reg_ot = overtime.get("regular", 0)
    con_ot = overtime.get("contract", 0)

    if reg_present + reg_absent > reg_sched:
        errors.append(
            translate(
                "attendance.error_regular_exceeds",
                "Regular staff: present ({present}) + absent ({absent}) > scheduled ({scheduled})",
            ).format(present=reg_present, absent=reg_absent, scheduled=reg_sched)
        )

    if reg_present < 0 or reg_absent < 0 or reg_sched < 0:
        errors.append(
            translate("attendance.error_regular_negative", "Regular staff numbers cannot be negative.")
        )

    if con_present + con_absent > con_sched:
        errors.append(
            translate(
                "attendance.error_contractor_exceeds",
                "Contract staff: present ({present}) + absent ({absent}) > scheduled ({scheduled})",
            ).format(present=con_present, absent=con_absent, scheduled=con_sched)
        )

    if con_present < 0 or con_absent < 0 or con_sched < 0:
        errors.append(
            translate("attendance.error_contractor_negative", "Contract staff numbers cannot be negative.")
        )

    if reg_ot < 0 or con_ot < 0:
        errors.append(translate("attendance.error_overtime_negative", "Overtime count cannot be negative."))

    return errors
