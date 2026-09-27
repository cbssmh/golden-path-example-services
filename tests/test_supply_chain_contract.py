import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
DOCKERFILE = ROOT / "Dockerfile"
FULL_SHA = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}$")


class SupplyChainContractTest(unittest.TestCase):
    def setUp(self):
        self.workflow = WORKFLOW.read_text(encoding="utf-8")
        self.dockerfile = DOCKERFILE.read_text(encoding="utf-8")

    def test_external_actions_use_full_commit_shas(self):
        references = re.findall(r"^\s*- uses:\s*([^\s#]+)", self.workflow, re.MULTILINE)
        self.assertTrue(references)
        for reference in references:
            if reference.startswith("./"):
                continue
            self.assertRegex(reference, FULL_SHA)

    def test_workflow_has_no_floating_latest_reference(self):
        self.assertNotRegex(self.workflow.lower(), r"(?:^|[:/@-])latest(?:$|[\s'\"])")
        self.assertNotIn("ubuntu-latest", self.workflow)

    def test_test_job_is_read_only_and_publish_owns_package_write(self):
        test_job, publish_job = self.workflow.split("\n  publish:\n", maxsplit=1)
        self.assertNotIn("packages: write", test_job)
        self.assertIn("packages: write", publish_job)
        self.assertIn("if: github.event_name == 'push'", publish_job)
        self.assertIn("needs: test-and-build", publish_job)

    def test_build_infrastructure_images_are_digest_pinned(self):
        self.assertRegex(
            self.workflow,
            r"BINFMT_IMAGE:\s*docker\.io/tonistiigi/binfmt@sha256:[0-9a-f]{64}",
        )
        self.assertRegex(
            self.workflow,
            r"BUILDKIT_IMAGE:\s*docker\.io/moby/buildkit@sha256:[0-9a-f]{64}",
        )

    def test_python_base_image_is_digest_pinned(self):
        expected = (
            "FROM python:3.12-alpine3.21@sha256:"
            "d4f9227f21409479c7fe92288f2e40b1a56ae591c8ad3b5446dfeaef90f67857"
        )
        self.assertIn(expected, self.dockerfile)


if __name__ == "__main__":
    unittest.main()
