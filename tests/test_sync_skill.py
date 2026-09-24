import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("sync_skill", Path(__file__).resolve().parents[1] / "scripts/sync_skill.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)

class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "source"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text("v1", encoding="utf-8")
        self.target = self.root / "target"

    def deploy(self, apply=False, targets=None, adopt=False):
        with contextlib.redirect_stdout(io.StringIO()):
            sync.deploy(self.source, targets or [self.target], {"template_dir": "test"}, apply, adopt)

    def test_dry_run_does_not_create_target(self):
        self.deploy()
        self.assertFalse(self.target.exists())

    def test_initial_deployment_and_idempotent_repeat(self):
        self.deploy(True)
        self.assertEqual((self.target / "SKILL.md").read_text(), "v1")
        self.deploy(True)
        self.assertFalse((self.target / ".sync-backups").exists())
        self.assertEqual(json.loads((self.target / sync.STATE).read_text())["files"]["SKILL.md"],
                         sync.digest(self.source / "SKILL.md"))

    def test_source_update_keeps_backup_and_extras(self):
        self.deploy(True)
        (self.target / "custom.md").write_text("keep")
        (self.source / "SKILL.md").write_text("v2")
        self.deploy(True)
        self.assertEqual((self.target / "SKILL.md").read_text(), "v2")
        self.assertEqual((self.target / "custom.md").read_text(), "keep")
        backups = list((self.target / ".sync-backups").rglob("SKILL.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "v1")

    def test_local_edit_blocks_all_targets(self):
        self.deploy(True)
        (self.target / "SKILL.md").write_text("local edit")
        fresh = self.root / "fresh"
        with self.assertRaisesRegex(ValueError, "no files written"):
            self.deploy(True, [fresh, self.target])
        self.assertFalse(fresh.exists())
        self.assertEqual((self.target / "SKILL.md").read_text(), "local edit")

    def test_unmanaged_different_file_refused(self):
        self.target.mkdir()
        (self.target / "SKILL.md").write_text("legacy")
        with self.assertRaises(ValueError):
            self.deploy(True)
        self.assertFalse((self.target / sync.STATE).exists())

    def test_identical_existing_file_can_be_adopted(self):
        self.target.mkdir()
        (self.target / "SKILL.md").write_text("v1")
        self.deploy(True)
        self.assertTrue((self.target / sync.STATE).exists())

    def test_overlapping_source_or_targets_refused(self):
        for targets in ([self.source], [self.source / "nested"],
                        [self.target, self.target / "nested"]):
            with self.assertRaises(ValueError):
                self.deploy(True, targets)

    def test_missing_templates_fail_before_writes(self):
        context = self.root / "context"
        skill = context / sync.SKILL
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("test")
        (context / "SYSTEM_REGISTRY.yaml").write_text("{}")
        (context / "SYSTEM_REGISTRY.local.yaml").write_text(json.dumps({
            "logical_roots": {"cloud": str(self.root), "runtime": str(self.root / "runtime")}}))
        with contextlib.redirect_stderr(io.StringIO()):
            result = sync.main(["--context-root", str(context), "--target", str(self.target),
                                "--template-root", str(self.root / "missing"), "--apply"])
        self.assertEqual(result, 2)
        self.assertFalse(self.target.exists())

    def test_adopt_takes_over_a_never_deployed_copy_and_backs_it_up(self):
        self.target.mkdir()
        (self.target / "SKILL.md").write_text("hand-made older version")
        self.deploy(True, adopt=True)
        self.assertEqual((self.target / "SKILL.md").read_text(), "v1")
        backups = list((self.target / ".sync-backups").rglob("SKILL.md"))
        self.assertEqual([b.read_text() for b in backups], ["hand-made older version"])

    def test_adopt_does_not_override_a_deployed_copy_edited_by_hand(self):
        self.deploy(True)
        (self.target / "SKILL.md").write_text("edited after deployment")
        with self.assertRaisesRegex(ValueError, "no files written"):
            self.deploy(True, adopt=True)
        self.assertEqual((self.target / "SKILL.md").read_text(), "edited after deployment")

    def test_the_repository_skill_is_the_source_and_context_repo_is_a_target(self):
        source = Path(sync.__file__).read_text(encoding="utf-8")
        self.assertIn('deploy(repo / "skill"', source)
        self.assertIn("str(context / SKILL)", source)


if __name__ == "__main__":
    unittest.main()
