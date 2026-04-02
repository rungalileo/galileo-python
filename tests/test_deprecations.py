import warnings
from unittest.mock import MagicMock, patch

import pytest

from galileo_core.schemas.shared.scorers.scorer_name import ScorerName

# ================================
# GalileoScorers deprecation tests
# ================================


def test_galileo_scorers_attribute_access_emits_deprecation_warning():
    """Accessing GalileoScorers.<name> should emit a DeprecationWarning."""
    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        from galileo.schema.metrics import GalileoScorers

        _ = GalileoScorers.correctness


def test_galileo_metrics_attribute_access_does_not_warn():
    """Accessing GalileoMetrics.<name> should NOT emit a DeprecationWarning."""
    from galileo.schema.metrics import GalileoMetrics

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _ = GalileoMetrics.correctness
        assert not any(isinstance(x.message, DeprecationWarning) for x in w)


def test_top_level_imported_galileo_scorers_emits_deprecation_on_access():
    """Importing GalileoScorers from the top-level package and accessing attribute should warn."""
    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        from galileo import GalileoScorers

        _ = GalileoScorers.correctness


def test_galileo_scorers_callable_and_lookup_delegate():
    """GalileoScorers('correctness') and GalileoScorers['correctness'] should work and warn."""
    from galileo.schema.metrics import GalileoScorers

    # Value-based lookup uses the ScorerName value (internal name)
    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        member = GalileoScorers("correctness")
        assert member is ScorerName.correctness

    # Name-based lookup uses the member name
    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        member2 = GalileoScorers["correctness"]
        assert member2 is ScorerName.correctness

    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        assert ScorerName.correctness in GalileoScorers


def test_galileo_scorers_isinstance_check():
    """isinstance checks with GalileoScorers should work — delegates to ScorerName."""
    from galileo.schema.metrics import GalileoScorers

    assert isinstance(ScorerName.correctness, GalileoScorers)
    assert not isinstance("not a scorer", GalileoScorers)


# ============================================================
# @deprecated decorator tests for legacy service functions
# ============================================================


class TestLegacyServiceDeprecationWarnings:
    """Tests that legacy service functions emit DeprecationWarning with the correct replacement message."""

    # --- datasets.py ---

    @patch("galileo.datasets.Datasets.get", return_value=None)
    def test_get_dataset_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated get_dataset convenience function
        from galileo.datasets import get_dataset

        # When: calling it
        with pytest.warns(DeprecationWarning, match="galileo.dataset.Dataset.get"):
            get_dataset(id="test-id")

    @patch("galileo.datasets.Datasets.list", return_value=[])
    def test_list_datasets_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated list_datasets convenience function
        from galileo.datasets import list_datasets

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.dataset.Dataset.list"):
            list_datasets()

    @patch("galileo.datasets.Datasets.delete", return_value=None)
    def test_delete_dataset_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated delete_dataset convenience function
        from galileo.datasets import delete_dataset

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="dataset.delete"):
            delete_dataset(id="test-id")

    @patch("galileo.datasets.Datasets.create", return_value=MagicMock())
    def test_create_dataset_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated create_dataset convenience function
        from galileo.datasets import create_dataset

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.dataset.Dataset"):
            create_dataset(name="test", content=[{"input": "hi"}])

    def test_get_dataset_version_history_emits_deprecation_warning(self) -> None:
        # Given: the deprecated get_dataset_version_history convenience function
        from galileo.datasets import get_dataset_version_history

        # When/Then: calling it emits a deprecation warning (ignore errors from unmocked APIs)
        with pytest.warns(DeprecationWarning, match="dataset.get_version_history"):
            try:
                get_dataset_version_history(dataset_id="test-id")
            except Exception:
                pass

    def test_get_dataset_version_emits_deprecation_warning(self) -> None:
        # Given: the deprecated get_dataset_version convenience function
        from galileo.datasets import get_dataset_version

        # When/Then: calling it emits a deprecation warning (ignore errors from unmocked APIs)
        with pytest.warns(DeprecationWarning, match="dataset.get_version"):
            try:
                get_dataset_version(version_index=1, dataset_id="test-id")
            except Exception:
                pass

    def test_extend_dataset_emits_deprecation_warning(self) -> None:
        # Given: the deprecated extend_dataset convenience function
        from galileo.datasets import extend_dataset

        # When/Then: calling it emits a deprecation warning (ignore errors from unmocked APIs)
        with pytest.warns(DeprecationWarning, match="dataset.extend"):
            try:
                extend_dataset(dataset_id="test-id")
            except Exception:
                pass

    def test_list_dataset_projects_emits_deprecation_warning(self) -> None:
        # Given: the deprecated list_dataset_projects convenience function
        from galileo.datasets import list_dataset_projects

        # When/Then: calling it emits a deprecation warning (ignore errors from unmocked APIs)
        with pytest.warns(DeprecationWarning, match="galileo.project.Project.list"):
            try:
                list_dataset_projects(dataset_id="test-id")
            except Exception:
                pass

    # --- experiments.py ---

    @patch("galileo.experiments.Experiments.create", return_value=MagicMock())
    @patch("galileo.experiments.Projects.get", return_value=MagicMock(id="proj-id"))
    def test_create_experiment_emits_deprecation_warning(self, _mock_proj: MagicMock, _mock_exp: MagicMock) -> None:
        # Given: the deprecated create_experiment convenience function
        from galileo.experiments import create_experiment

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.experiment.Experiment"):
            create_experiment(project_name="test-project", experiment_name="test-exp")

    @patch("galileo.experiments.Experiments.get", return_value=MagicMock())
    @patch("galileo.experiments.Projects.get", return_value=MagicMock(id="proj-id"))
    def test_get_experiment_emits_deprecation_warning(self, _mock_proj: MagicMock, _mock_exp: MagicMock) -> None:
        # Given: the deprecated get_experiment convenience function
        from galileo.experiments import get_experiment

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.experiment.Experiment.get"):
            get_experiment(project_name="test-project", experiment_name="test-exp")

    @patch("galileo.experiments.Experiments.list", return_value=[])
    @patch("galileo.experiments.Projects.get", return_value=MagicMock(id="proj-id"))
    def test_get_experiments_emits_deprecation_warning(self, _mock_proj: MagicMock, _mock_exp: MagicMock) -> None:
        # Given: the deprecated get_experiments convenience function
        from galileo.experiments import get_experiments

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.experiment.Experiment.list"):
            get_experiments(project_name="test-project")

    # --- log_streams.py ---

    @patch("galileo.log_streams.LogStreams.get", return_value=MagicMock())
    def test_get_log_stream_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated get_log_stream convenience function
        from galileo.log_streams import get_log_stream

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.log_stream.LogStream.get"):
            get_log_stream(name="test", project_id="proj-id")

    @patch("galileo.log_streams.LogStreams.list", return_value=[])
    def test_list_log_streams_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated list_log_streams convenience function
        from galileo.log_streams import list_log_streams

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.log_stream.LogStream.list"):
            list_log_streams(project_id="proj-id")

    @patch("galileo.log_streams.LogStreams.create", return_value=MagicMock())
    def test_create_log_stream_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated create_log_stream convenience function
        from galileo.log_streams import create_log_stream

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.log_stream.LogStream"):
            create_log_stream(name="test", project_id="proj-id")

    def test_enable_metrics_emits_deprecation_warning(self) -> None:
        # Given: the deprecated enable_metrics convenience function
        from galileo.log_streams import enable_metrics

        # When/Then: calling it emits a deprecation warning (ignore errors from unmocked APIs)
        with pytest.warns(DeprecationWarning, match="log_stream.set_metrics"):
            try:
                enable_metrics(log_stream_name="test", project_id="proj-id", metrics=["correctness"])
            except Exception:
                pass

    # --- prompts.py ---

    @patch("galileo.prompts.GlobalPromptTemplates.get", return_value=MagicMock())
    def test_get_prompt_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated get_prompt convenience function
        from galileo.prompts import get_prompt

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.prompt.Prompt.get"):
            get_prompt(id="test-id")

    @patch("galileo.prompts.GlobalPromptTemplates.delete", return_value=None)
    def test_delete_prompt_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated delete_prompt convenience function
        from galileo.prompts import delete_prompt

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="prompt.delete"):
            delete_prompt(id="test-id")

    @patch("galileo.prompts.GlobalPromptTemplates.update", return_value=MagicMock())
    def test_update_prompt_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated update_prompt convenience function
        from galileo.prompts import update_prompt

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="prompt.save"):
            update_prompt(id="test-id", new_name="new-name")

    def test_create_prompt_emits_deprecation_warning(self) -> None:
        # Given: the deprecated create_prompt convenience function
        from galileo.prompts import create_prompt

        # When/Then: calling it emits a deprecation warning (ignore errors from unmocked APIs)
        with pytest.warns(DeprecationWarning, match="galileo.prompt.Prompt"):
            try:
                create_prompt(name="test", template="hello {{name}}")
            except Exception:
                pass

    @patch("galileo.prompts.GlobalPromptTemplates.list", return_value=[])
    def test_get_prompts_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated get_prompts convenience function
        from galileo.prompts import get_prompts

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.prompt.Prompt.list"):
            get_prompts()

    @patch("galileo.prompts.get_prompts", return_value=[])
    def test_list_prompt_templates_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated list_prompt_templates convenience function
        from galileo.prompts import list_prompt_templates

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.prompt.Prompt.list"):
            list_prompt_templates(project="test-project")

    @patch("galileo.prompts.get_prompt", return_value=MagicMock())
    def test_get_prompt_template_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated get_prompt_template convenience function
        from galileo.prompts import get_prompt_template

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.prompt.Prompt.get"):
            get_prompt_template(name="test", project="test-project")

    def test_create_prompt_template_emits_deprecation_warning(self) -> None:
        # Given: the deprecated create_prompt_template convenience function
        from galileo.prompts import create_prompt_template

        # When/Then: calling it emits a deprecation warning (ignore errors from unmocked APIs)
        with pytest.warns(DeprecationWarning, match="galileo.prompt.Prompt"):
            try:
                create_prompt_template(name="test", project="test-project", messages=[])
            except Exception:
                pass

    def test_run_experiment_emits_deprecation_warning(self) -> None:
        # Given: the deprecated run_experiment convenience function
        from galileo.experiments import run_experiment

        # When/Then: calling it emits a deprecation warning (ignore errors from unmocked APIs)
        with pytest.warns(DeprecationWarning, match="galileo.experiment.Experiment"):
            try:
                run_experiment(experiment_name="test-exp")
            except Exception:
                pass

    # --- projects.py ---

    @patch("galileo.projects.Projects.get", return_value=MagicMock())
    def test_get_project_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated get_project convenience function
        from galileo.projects import get_project

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.project.Project.get"):
            get_project(name="test-project")

    @patch("galileo.projects.Projects.list", return_value=[])
    def test_list_projects_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated list_projects convenience function
        from galileo.projects import list_projects

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.project.Project.list"):
            list_projects()

    @patch("galileo.projects.Projects.create", return_value=MagicMock())
    def test_create_project_emits_deprecation_warning(self, _mock: MagicMock) -> None:
        # Given: the deprecated create_project convenience function
        from galileo.projects import create_project

        # When/Then: calling it emits a deprecation warning
        with pytest.warns(DeprecationWarning, match="galileo.project.Project"):
            create_project(name="test-project")

    # --- Overloaded function: only 1 warning per call ---

    @patch("galileo.datasets.Datasets.get", return_value=None)
    def test_overloaded_get_dataset_emits_exactly_one_warning(self, _mock: MagicMock) -> None:
        # Given: get_dataset has @deprecated on both @overload signatures and the implementation
        from galileo.datasets import get_dataset

        # When: calling the function
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            get_dataset(id="test-id")

        # Then: exactly one DeprecationWarning is emitted (not duplicated by overloads)
        deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 1
        assert "galileo.dataset.Dataset.get" in str(deprecation_warnings[0].message)

    @patch("galileo.prompts.GlobalPromptTemplates.delete", return_value=None)
    def test_overloaded_delete_prompt_emits_exactly_one_warning(self, _mock: MagicMock) -> None:
        # Given: delete_prompt has @deprecated on both @overload signatures and the implementation
        from galileo.prompts import delete_prompt

        # When: calling the function
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            delete_prompt(id="test-id")

        # Then: exactly one DeprecationWarning is emitted
        deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 1
        assert "prompt.delete" in str(deprecation_warnings[0].message)


def test_galileo_scorers_issubclass_check():
    """issubclass checks with GalileoScorers should work — delegates to ScorerName."""
    from galileo.schema.metrics import GalileoScorers

    assert issubclass(type(ScorerName.correctness), GalileoScorers)


def test_galileo_scorers_returns_scorer_name_members():
    """GalileoScorers attribute access should return ScorerName enum members."""
    from galileo.schema.metrics import GalileoScorers

    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        scorer = GalileoScorers.correctness
        assert scorer is ScorerName.correctness
        assert scorer.value == "correctness"
