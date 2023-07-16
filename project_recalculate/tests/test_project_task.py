# See README.rst file on addon root folder for license details

from datetime import date, datetime, time

from odoo.exceptions import ValidationError

from . import base


class TestProjectTaskBegin(base.BaseCase):
    calculation_type = "date_begin"

    def __init__(self, methodName="runTest"):
        super(TestProjectTaskBegin, self).__init__(methodName=methodName)
        # Adapt task results because
        # f(estimated_days, from_day) => (start, end) function is not
        # bijective and here we are testing the inverse
        # f'(start, end) => (estimated_days, from_day)
        #
        # Example: When project date is holiday (02/08/2015)
        #   f(0, 1) => (2015-08-03, 2015-08-03)
        #   f(1, 1) => (2015-08-03, 2015-08-03)
        # So
        #   f'(2015-08-03, 2015-08-03) => (0, 1) or (1, 1)
        #   both are valid
        self.task_days_res = {
            "date_begin": {
                "pj_0": list(self.task_days["date_begin"]),
                "pj_1": list(self.task_days["date_begin"]),
                "pj_2": list(self.task_days["date_begin"]),
            },
            "date_end": {
                "pj_0": list(self.task_days["date_end"]),
                "pj_1": list(self.task_days["date_end"]),
                "pj_2": list(self.task_days["date_end"]),
            },
        }
        begin_special_case = ["task_1", 1, 1]  # ['task_1', 0, 1]
        end_special_case = ["task_3", 1, 1]  # ['task_3', 0, 1]
        self.task_days_res["date_begin"]["pj_0"][1] = begin_special_case
        self.task_days_res["date_begin"]["pj_1"][1] = begin_special_case
        self.task_days_res["date_end"]["pj_0"][3] = end_special_case
        self.task_days_res["date_end"]["pj_1"][3] = end_special_case
        self.task_days_res["date_end"]["pj_2"][3] = end_special_case

    def test_update_recalculated_dates_when_recalculate(self):
        """
        @summary: Check _update_recalculated_dates when recalculate
        """
        project = self.project_create(
            self.num_tasks,
            {
                "calculation_type": self.calculation_type,
                "name": "Test project",
                "date_start": date(2015, 8, 1),
                "date": date(2015, 8, 31),
                "resource_calendar_id": False,
            },
        )

        task = project.tasks[0]
        vals = {
            "date_start": datetime(2015, 8, 3, 8),
            "date_end": datetime(2015, 8, 14, 18),
        }
        # Execute _update_recalculated_dates
        # with context: task_recalculate=True
        task_ctx = task.with_context(task.env.context, task_recalculate=True)
        vals = task_ctx._update_recalculated_dates(vals)
        self.assertTrue("from_days" not in vals, "FAIL: from_days assigned")
        self.assertTrue("estimated_days" not in vals, "FAIL: estimated_days assigned")

    def test_update_recalculate_dates(self):
        """
        @summary: Check _update_recalculate_dates
        """
        project_counter = 0
        for name, start, end in self.project_init_dates:
            # Prepare test case
            project = self.project_create(
                self.num_tasks,
                {
                    "calculation_type": self.calculation_type,
                    "name": name,
                    "date_start": start,
                    "date": end,
                    "resource_calendar_id": False,
                },
            )

            task_counter = 0
            for i in range(self.num_tasks):
                dates = self.task_dates[self.calculation_type][name][i]
                task = project.tasks.filtered(lambda r: r.name == dates[0])
                vals = {
                    "date_start": datetime.combine(dates[1], time(8)),
                    "date_end": datetime.combine(dates[2], time(18)),
                }
                vals = task._update_recalculated_dates(vals)
                # Check test case
                days = self.task_days_res[self.calculation_type][name][i]
                self.assertEqual(
                    vals.get("from_days", False),
                    days[1],
                    "[%d, %d] FAIL: from_days" % (project_counter, task_counter),
                )
                self.assertEqual(
                    vals.get("estimated_days", False),
                    days[2],
                    "[%d, %d] FAIL: estimated_days" % (project_counter, task_counter),
                )
                task_counter += 1
            project_counter += 1

    def test_update_recalculated_dates_when_no_from_days_or_estimated_days(self):
        """
        @summary: Check _update_recalculate_dates when no from_days or estimated_days
        """
        project = self.project_create(
            self.num_tasks,
            {
                "calculation_type": self.calculation_type,
                "name": "Test project",
                "date_start": date(2015, 8, 1),
                "date": date(2015, 8, 31),
                "resource_calendar_id": False,
            },
        )

        # No end date
        task = project.tasks[0]
        task.date_end = False
        vals = {
            "date_start": datetime(2015, 8, 3, 8),
        }
        vals = task._update_recalculated_dates(vals)
        self.assertTrue("from_days" not in vals, "FAIL: from_days assigned")
        self.assertTrue("estimated_days" not in vals, "FAIL: estimated_days assigned")

        # date_end < date_start
        task = project.tasks[0]
        vals = {
            "date_start": datetime(2015, 8, 3, 8),
            "date_end": datetime(2014, 8, 3, 8),
        }
        vals = task._update_recalculated_dates(vals)
        # TODO: Maybe raise an error? Kept because consistency with 14.0
        self.assertTrue("from_days" not in vals, "FAIL: from_days assigned")
        self.assertTrue("estimated_days" not in vals, "FAIL: estimated_days assigned")

        # calculation_type == "date_begin" and not self.project_id.date_start
        project = self.project_create(
            self.num_tasks,
            {
                "calculation_type": "date_begin",
                "name": "Test project",
                "date": date(2015, 8, 31),
                "resource_calendar_id": False,
            },
        )
        task = project.tasks[0]
        vals = {
            "date_end": datetime(2015, 8, 3, 8),
            "date_start": datetime(2014, 8, 3, 8),
        }
        vals = task._update_recalculated_dates(vals)

        self.assertTrue("from_days" not in vals, "FAIL: from_days assigned")
        self.assertTrue("estimated_days" in vals, "FAIL: estimated_days not assigned")

        # calculation_type != "date_begin" and not self.project_id.date
        project = self.project_create(
            self.num_tasks,
            {
                "calculation_type": "date_end",
                "name": "Test project",
                "date_start": date(2015, 8, 31),
                "resource_calendar_id": False,
            },
        )
        task = project.tasks[0]
        vals = {
            "date_end": datetime(2015, 8, 3, 8),
            "date_start": datetime(2014, 8, 3, 8),
        }
        vals = task._update_recalculated_dates(vals)

        self.assertTrue("from_days" not in vals, "FAIL: from_days assigned")
        self.assertTrue("estimated_days" in vals, "FAIL: estimated_days not assigned")

    def test_estimated_days_check(self):
        """
        @summary: Check _estimated_days_check constraint
            * estimated_days > O: OK
            * estimated_days == 0: ValidationError
            * estimated_days < 0: ValidationError
        """
        error_cases = (
            # name, estimated_days
            ("task_0", -5),
            ("task_1", -1),
            ("task_2", 0),
        )
        ok_cases = (
            ("task_10", 1),
            ("task_11", 5),
            ("task_12", 100),
        )
        project = self.project_create(
            0,
            {
                "calculation_type": self.calculation_type,
                "name": "test",
                "resource_calendar_id": False,
            },
        )
        for name, estimated_days in error_cases:
            # ValidationError cases
            with self.assertRaises(ValidationError):
                self.project_task_add(
                    project, {"name": name, "estimated_days": estimated_days}
                )
        # OK cases
        for name, estimated_days in ok_cases:
            self.project_task_add(
                project, {"name": name, "estimated_days": estimated_days}
            )

    def test_project_task_recalculate(self):

        # No user_resource_calendar and user_id
        project = self.project_create(
            self.num_tasks,
            {
                "calculation_type": self.calculation_type,
                "name": "Test project",
                "date_start": date(2015, 8, 1),
                "date": date(2015, 8, 31),
                "resource_calendar_id": False,
            },
        )
        for task in project.tasks:
            if task.user_id:
                resources = self.env["resource.resource"].search(
                    [("user_id", "=", task.user_id.id)]
                )
                for resource in resources:
                    resource.active = False

        project.project_recalculate()

        if project.calculation_type == "date_begin":
            self.assertEqual(project.date, max(project.tasks.mapped("date_end")).date())
        else:
            self.assertEqual(
                project.date_start, min(project.tasks.mapped("date_start")).date()
            )

        # No user_id
        project = self.project_create(
            self.num_tasks,
            {
                "calculation_type": self.calculation_type,
                "name": "Test project",
                "date_start": date(2015, 8, 1),
                "date": date(2015, 8, 31),
                "resource_calendar_id": False,
            },
        )

        for task in project.tasks:
            task.user_id = False
        project.project_recalculate()

        if project.calculation_type == "date_begin":
            self.assertEqual(project.date, max(project.tasks.mapped("date_end")).date())
        else:
            self.assertEqual(
                project.date_start, min(project.tasks.mapped("date_start")).date()
            )

        # No user_id and project_id.resource_calendar_id

        resource_calendar_id = self.env.ref("resource.resource_calendar_std")
        project = self.project_create(
            self.num_tasks,
            {
                "calculation_type": self.calculation_type,
                "name": "Test project",
                "date_start": date(2015, 8, 1),
                "date": date(2015, 8, 31),
                "resource_calendar_id": resource_calendar_id.id,
            },
        )
        for task in project.tasks:
            task.user_id = False
        project.project_recalculate()

        if project.calculation_type == "date_begin":
            self.assertEqual(project.date, max(project.tasks.mapped("date_end")).date())
        else:
            self.assertEqual(
                project.date_start, min(project.tasks.mapped("date_start")).date()
            )


class TestProjectTaskEnd(TestProjectTaskBegin):
    calculation_type = "date_end"