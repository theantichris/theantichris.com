from datetime import datetime, timezone
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs

from scripts import mastodon_posts as posts

NOW = datetime(2026, 10, 22, 12, tzinfo=timezone.utc)


def post(title="Example", *, draft=False, date="2026-10-20T12:00:00-04:00"):
    return f"""+++
title = '{title}'
date = '{date}'
draft = {str(draft).lower()}
tags = ["go", "machine-learning"]
+++

A post with `code` and [a link](https://example.com).
"""


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.run_git("init", "-q")
        self.write("README.md", "Fixture repository")
        self.commit()

    def run_git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, text=True).strip()

    def write(self, path, text):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self):
        self.run_git("add", ".")
        self.run_git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.com",
                     "-c", "commit.gpgsign=false", "commit", "-qm", "Test fixture")
        return self.run_git("rev-parse", "HEAD")

    def changes(self, before):
        return posts.new_posts(before, repo=self.repo, now=NOW)

    def test_all_new_posts_and_toml_quote_styles(self):
        before = self.run_git("rev-parse", "HEAD")
        self.write("content/posts/first.md", post("Single quoted title"))
        self.write("content/posts/second.md", post().replace("'Example'", '"Double quoted title"'))
        self.commit()
        found = self.changes(before)
        self.assertEqual([item[1]["title"] for item in found],
                         ["Single quoted title", "Double quoted title"])

    def test_corrections_and_renames_do_not_reannounce(self):
        self.write("content/posts/existing.md", post())
        before = self.commit()
        self.write("content/posts/renamed.md", post() + "\nA correction.\n")
        (self.repo / "content/posts/existing.md").unlink()
        self.commit()
        self.assertEqual(self.changes(before), [])

    def test_draft_to_published_transition(self):
        self.write("content/posts/draft.md", post(draft=True))
        before = self.commit()
        self.write("content/posts/draft.md", post())
        self.commit()
        self.assertEqual(len(self.changes(before)), 1)

    def test_drafts_future_dates_and_section_pages_are_skipped(self):
        before = self.run_git("rev-parse", "HEAD")
        self.write("content/posts/draft.md", post(draft=True))
        self.write("content/posts/future.md", post(date="2027-01-01T00:00:00Z"))
        self.write("content/posts/_index.md", post())
        self.commit()
        self.assertEqual(self.changes(before), [])

    def test_publication_uses_timezone_and_publish_date(self):
        self.assertFalse(posts.published({"date": "2026-10-22T09:00:00-04:00"}, NOW))
        self.assertTrue(posts.published({"date": "2026-10-22T07:00:00-04:00"}, NOW))
        self.assertFalse(posts.published({"date": "2026-01-01", "publishDate": "2027-01-01"}, NOW))

    def test_deleted_posts_are_skipped(self):
        self.write("content/posts/deleted.md", post())
        before = self.commit()
        (self.repo / "content/posts/deleted.md").unlink()
        self.commit()
        self.assertEqual(self.changes(before), [])

    def test_zero_before_sha_handles_first_push(self):
        self.write("content/posts/new.md", post())
        self.commit()
        self.assertEqual(len(self.changes("0" * 40)), 1)

    def test_metadata_is_sent_as_literal_request_data(self):
        title = 'Quotes " and `commands` and $(touch sentinel)'
        metadata = {"title": title, "description": title, "tags": ["go", "machine learning"]}
        status = posts.make_status("content/posts/test.md", metadata, "", "https://example.com/")
        with patch.object(posts, "urlopen") as mocked:
            posts.send_status(status, "https://social.example/", "test-token")
        request = mocked.call_args.args[0]
        data = parse_qs(request.data.decode())
        self.assertEqual(data["status"], [status["status"]])
        self.assertIn(title, data["status"][0])
        self.assertEqual(data["visibility"], ["public"])
        self.assertEqual(request.full_url, "https://social.example/api/v1/statuses")
        self.assertFalse((self.repo / "sentinel").exists())

    def test_long_descriptions_keep_the_link_and_valid_unicode(self):
        metadata = {"title": "Example", "description": "Résumé 📝 " * 100, "tags": ["go"]}
        status = posts.make_status("content/posts/test.md", metadata, "", "https://example.com")
        self.assertLessEqual(len(status["status"]), 480)
        self.assertIn("https://example.com/posts/test/", status["status"])
        self.assertTrue(status["status"].endswith("#go"))


if __name__ == "__main__":
    unittest.main()
