from datetime import datetime
from unittest.mock import Mock, patch

from galileo.experiments import Experiments


class TestExperiments:
    @patch("galileo.experiments.create_experiment_v2_projects_project_id_experiments_post")
    def test_create(self, galileo_resources_api_create_experiment: Mock):
        from galileo.resources.models import ExperimentResponse

        now = datetime(2020, 1, 1).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        galileo_resources_api_create_experiment.sync = Mock(
            return_value=ExperimentResponse.from_dict(
                dict(id="test", name="test_experiment", project_id="test", created_at=now, updated_at=now)
            )
        )
        experiment = Experiments().create(project_id="test", name="test_experiment")
        assert experiment.name == "test_experiment"
        assert experiment.project_id == "test"
