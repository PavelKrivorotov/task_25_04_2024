from sqlalchemy import select

from auth.models import User
from job.models import Job, UserJob


query = (
    select(
        User.id.label('user_id'),
        User.username.label('username'),
        User.first_name.label('first_name'),
        User.last_name.label('last_name'),
        User.date_of_employment.label('date_of_employment'),
        User.is_superuser.label('is_superuser'),
        User.is_staff.label('is_staff'),
        Job.id.label('job_id'),
        Job.title.label('title'),
        Job.salary.label('salary'),
        Job.days_to_promotion.label('days_to_promotion')
    )
    .join_from(
        User,
        UserJob,
        User.id == UserJob.user_id,

        isouter=True
    )
    .join_from(
        UserJob,
        Job,
        UserJob.job_id == Job.id,

        isouter=True
    )
    .where(User.is_staff == True)
)

