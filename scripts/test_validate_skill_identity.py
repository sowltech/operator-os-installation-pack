"""Regression tests for validate_skill_identity.py.

Builds minimal fixture skill trees under a TemporaryDirectory and mutates
exactly one thing per test, proving the validator both accepts a clean
tree and genuinely rejects each broken variant.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_skill_identity as vsi  # noqa: E402


def _write(root: Path, folder: str, content: str) -> Path:
    skill_dir = root / folder
    skill_dir.mkdir(parents=True, exist_ok=True)
    path = skill_dir / "SKILL.md"
    path.write_text(content, encoding="utf-8")
    return path


GOOD_A = (
    "---\nname: obsidian-rag-shortcut-bot\n"
    "description: Retrieves grounded answers.\n"
    "title: Obsidian RAG Shortcut Bot\nslug: obsidian-rag-shortcut-bot\nstatus: active\n"
    "---\n\n# Obsidian RAG Shortcut Bot\n\nBody content.\n"
)
GOOD_B = (
    "---\nname: operator-os-recall\n"
    "description: Finds relevant approved vault material.\n"
    "title: Recall\nslug: recall\nstatus: active\n"
    "---\n\n# Recall\n\nBody content.\n"
)


class TestValidateSkillIdentity(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        _write(self.root, "obsidian-rag-shortcut-bot", GOOD_A)
        _write(self.root, "recall", GOOD_B)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_good_tree_passes(self) -> None:
        errors = vsi.validate_all_skills(self.root)
        self.assertEqual(errors, [], f"expected clean fixture to pass, got: {errors}")

    def test_real_repo_files_pass(self) -> None:
        """Runs against the actual committed repo files, not just fixtures."""
        errors = vsi.validate_all_skills(vsi.SKILLS_ROOT)
        self.assertEqual(errors, [], f"expected real repo to pass, got: {errors}")

    def test_duplicate_name_genuinely_fails(self) -> None:
        _write(self.root, "duplicate-of-recall", GOOD_B)  # same name: operator-os-recall
        errors = vsi.validate_all_skills(self.root)
        self.assertTrue(any("duplicate name" in e for e in errors), errors)

    def test_duplicate_slug_genuinely_fails(self) -> None:
        _write(self.root, "another-recall-folder", GOOD_B)  # same slug: recall, different folder
        errors = vsi.validate_all_skills(self.root)
        self.assertTrue(any("duplicate slug" in e for e in errors) or any("does not match its folder name" in e for e in errors), errors)

    def test_non_kebab_case_name_fails(self) -> None:
        broken = GOOD_A.replace("name: obsidian-rag-shortcut-bot", "name: Obsidian_RAG_Bot")
        _write(self.root, "obsidian-rag-shortcut-bot", broken)
        errors = vsi.validate_all_skills(self.root)
        self.assertTrue(any("not safe lowercase kebab-case" in e for e in errors), errors)

    def test_slug_folder_mismatch_fails(self) -> None:
        broken = GOOD_B.replace("slug: recall", "slug: recall-v2")
        _write(self.root, "recall", broken)
        errors = vsi.validate_all_skills(self.root)
        self.assertTrue(any("does not match its folder name" in e for e in errors), errors)

    def test_duplicate_frontmatter_key_fails(self) -> None:
        broken = "---\nname: obsidian-rag-shortcut-bot\nname: something-else\ndescription: x\n---\n\nBody.\n"
        _write(self.root, "obsidian-rag-shortcut-bot", broken)
        errors = vsi.validate_all_skills(self.root)
        self.assertTrue(any("duplicate frontmatter key" in e for e in errors), errors)

    def test_empty_body_fails(self) -> None:
        broken = "---\nname: obsidian-rag-shortcut-bot\ndescription: x\n---\n\n   \n"
        _write(self.root, "obsidian-rag-shortcut-bot", broken)
        errors = vsi.validate_all_skills(self.root)
        self.assertTrue(any("no Markdown instruction body" in e for e in errors), errors)

    def test_secret_shaped_value_fails(self) -> None:
        broken = GOOD_A.replace(
            "status: active\n",
            "status: active\napi_key: sk-abcdefghijklmnop\n",
        )
        _write(self.root, "obsidian-rag-shortcut-bot", broken)
        errors = vsi.validate_all_skills(self.root)
        self.assertTrue(any("secret-shaped" in e for e in errors), errors)

    def test_invalid_status_fails(self) -> None:
        broken = GOOD_B.replace("status: active", "status: whatever")
        _write(self.root, "recall", broken)
        errors = vsi.validate_all_skills(self.root)
        self.assertTrue(any("is not one of active/draft/deprecated" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
