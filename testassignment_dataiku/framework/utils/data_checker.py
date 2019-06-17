import datetime


def check_task_details(task, title, tags, username, done=False):
    task_date = task.get("date")
    task_done = task.get("done")
    task_tags = task.get("tags")
    assert isinstance(task_tags, list)
    if task_tags and isinstance(task_tags[0], dict):
        task_tags = [tag.get("name") for tag in task_tags]

    task_title = task.get("title")
    task_username = task.get("username")

    assert task_title == title, "Created task has incorrect title, expected '{}', got '{}'".format(title, task_title)
    assert task_username == username, "Created task has incorrect username, expected '{}', got '{}'".format(username, task_username)
    assert bool(task_done) == bool(done), "Created task has incorrect done status, expected '{}', got '{}'".format(done, task_done)
    assert sorted(task_tags) == sorted(tags), "Created task has incorrect tags, expected '{}', got '{}'".format(", ".join(tags), ", ".join(task_tags))

    task_date_datetime = datetime.datetime.strptime(task_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    date_now = datetime.datetime.now()
    assert (date_now - task_date_datetime).total_seconds() < 60, "Created task has incorrect date"


def check_tag_details(tag_details, tag, titles):
    assert tag_details.get("tag") == tag, "Got incorrect tag name in tag details"
    assert sorted(tag_details.get("tasks")) == sorted(titles), "Incorrect task titles linked to the tag"

