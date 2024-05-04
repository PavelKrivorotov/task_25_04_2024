from typing import Any

from sqlalchemy import Result


def convert_employee(result: Result[Any]) -> list[Any]:
    data = []
    for user_id, \
        username, \
        first_name, \
        last_name, \
        date_of_employment, \
        is_superuser, \
        is_staff, \
        job_id, \
        title, \
        salary, \
        days_to_promotion in result.columns(
            'user_id',
            'username',
            'first_name',
            'last_name',
            'date_of_employment',
            'is_superuser',
            'is_staff',
            'job_id',
            'title',
            'salary',
            'days_to_promotion'
        ).all():

        data.append({
            'user_id': user_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'date_of_employment': date_of_employment,
            'is_superuser': is_superuser,
            'is_staff': is_staff,

            'job_id': job_id,
            'title': title,
            'salary': salary,
            'days_to_promotion': days_to_promotion
        })

    return data

