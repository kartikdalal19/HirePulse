
# Temporary storage.
# This will later be replaced by PostgreSQL.

job_descriptions = {}


def save_job_description(job_id: str, data: dict):
    job_descriptions[job_id] = data
    return data


def get_job_description(job_id: str):
    return job_descriptions.get(job_id)


def get_all_job_descriptions():
    return list(job_descriptions.values())
