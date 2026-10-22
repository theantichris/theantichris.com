"""Announce newly published Hugo posts; preview JSON unless --send is supplied."""

import argparse
from datetime import date, datetime, time, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tomllib
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def git(*args, repo=Path("."), optional=False):
    result = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, check=False
    )
    if optional and result.returncode:
        return None
    result.check_returncode()
    return result.stdout.decode("utf-8")


def read_post(ref, path, repo):
    source = git("show", f"{ref}:{path}", repo=repo, optional=True)
    if source is None:
        return {}, ""
    parts = source.split("+++", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f"Expected TOML front matter in {path}")
    return tomllib.loads(parts[1]), parts[2].strip()


def published(metadata, now):
    if metadata.get("draft", False):
        return False
    value = metadata.get("publishDate", metadata.get("date"))
    if not value:
        return False
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if isinstance(value, date) and not isinstance(value, datetime):
        value = datetime.combine(value, time.min)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value <= now


def new_posts(before, after="HEAD", *, repo=Path("."), now=None):
    now = now or datetime.now(timezone.utc)
    if not before:
        parent = git("rev-parse", "--verify", f"{after}^", repo=repo, optional=True)
        before = parent.strip() if parent else EMPTY_TREE
    elif set(before) == {"0"}:
        before = EMPTY_TREE
    fields = git(
        "diff", "--name-status", "-z", "--find-renames", before, after,
        "--", "content/posts/", repo=repo
    ).split("\0")
    changes = iter(fields[:-1])
    posts = []
    for status in changes:
        old_path = path = next(changes)
        if status.startswith(("R", "C")):
            path = next(changes)
        if not status.startswith(("A", "M", "R")):
            continue
        if not path.endswith(".md") or Path(path).name.startswith("_"):
            continue
        metadata, body = read_post(after, path, repo)
        previous, _ = read_post(before, old_path, repo)
        if published(metadata, now) and not published(previous, now):
            posts.append((path, metadata, body))
    return posts


def make_status(path, metadata, body, base_url):
    title = metadata["title"]
    description = metadata.get("description", "")
    if not description:
        # Keep a simple first-paragraph fallback for posts without a description.
        description = next(
            (p for p in body.split("\n\n")
             if not p.startswith(("#", "{{", "![", "```"))),
            "",
        )
        description = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", description)
        description = description.replace("`", "")
    description = " ".join(description.split())
    slug = metadata.get("slug", Path(path).stem)
    url = metadata.get("url") or f"/posts/{quote(slug)}/"
    if not url.startswith(("https://", "http://")):
        url = base_url.rstrip("/") + "/" + url.lstrip("/")
    tags = " ".join(
        "#" + re.sub(r"[^\w]", "", tag) for tag in metadata.get("tags", [])
    )
    header = f"📝 New blog post: {title}"
    footer = url + (f"\n\n{tags}" if tags else "")
    budget = max(0, 480 - len(header) - len(footer) - 4)
    if len(description) > budget:
        description = description[:max(0, budget - 1)].rstrip()
        description += "…" if budget else ""
    status = "\n\n".join(part for part in [header, description, footer] if part)
    return {"url": url, "status": status}


def send_status(post, instance, token):
    # Encode content as request data, never as executable shell source.
    request = Request(
        instance.rstrip("/") + "/api/v1/statuses",
        data=urlencode({"status": post["status"], "visibility": "public"}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Idempotency-Key": hashlib.sha256(post["url"].encode()).hexdigest(),
        },
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        response.read()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", default=os.environ.get("BEFORE_SHA"))
    parser.add_argument("--after", default=os.environ.get("AFTER_SHA") or "HEAD")
    parser.add_argument("--send", action="store_true")
    args = parser.parse_args()
    config = tomllib.loads(Path("hugo.toml").read_text())
    posts = [
        make_status(path, metadata, body, config["baseURL"])
        for path, metadata, body in new_posts(args.before, args.after)
    ]
    if args.send and posts:
        instance = os.environ["MASTODON_INSTANCE"]
        token = os.environ["MASTODON_ACCESS_TOKEN"]
        for post in posts:
            send_status(post, instance, token)
            print(f"Announced {post['url']}")
    else:
        print(json.dumps(posts, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
