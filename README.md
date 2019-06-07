# TheHive pack for StackStorm

This is a bunch of actions to automate [TheHive](https://thehive-project.org) alerts/cases/jobs processing.

## How to Use

Check example of webhook for usages.

### Actions

#### take_task

Change status to InProgress for `task_id`.

#### complete_task

Change status to Completed for `task_id`.

#### *_by_name

Look for `task_name` in `case_id`.

#### promote_alert_to_case

Create case from `alert_id` with `case_template`.

#### create_task_log

Create log in `task_id`.

#### run_analyzer

Run `analyzer_name` on `artifact_id` of `case_id`.

An optional `linked_task_name` parameter force to verify if a task exists in this case with this name and link the created job to this task.

#### run_analyzer_on_data_type

Same as before but run on every artifacts of `data_type` for `case_id`.

#### *_task_by_job_id

Works only if `job_id` was linked to a `task_id` during `run_analyzer`.
