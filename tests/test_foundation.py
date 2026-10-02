"""Guard the learning journey without relying on external websites or services."""

from html.parser import HTMLParser
from importlib.metadata import metadata
from pathlib import Path
from urllib.parse import unquote, urlsplit

import markdown
from mkdocs.config import load_config
from mkdocs.structure.files import Files, InclusionLevel

import fde_beginners

ROOT = Path(__file__).resolve().parents[1]


def authored_pages() -> list[Path]:
    return sorted(
        [
            *ROOT.glob("*.md"),
            *(ROOT / "docs").rglob("*.md"),
            *(ROOT / "labs").rglob("*.md"),
            *(ROOT / "templates").rglob("*.md"),
            *(ROOT / ".github").rglob("*.md"),
        ]
    )


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value and (tag, name) in {("a", "href"), ("img", "src")}:
                self.targets.append(value)


def test_source_links_resolve_inside_repository() -> None:
    failures = []
    for page in authored_pages():
        parser = Links()
        parser.feed(markdown.markdown(page.read_text(encoding="utf-8"), extensions=["fenced_code"]))
        for target in parser.targets:
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            resolved = (page.parent / unquote(url.path)).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.is_file():
                failures.append(f"{page.relative_to(ROOT)} -> {target}")
    assert not failures, "Broken or escaping links:\n" + "\n".join(failures)


def test_authored_text_avoids_forbidden_dashes() -> None:
    paths = authored_pages()
    for directory in ("src", "scripts", "tests", ".github", "labs"):
        paths.extend(
            path
            for path in (ROOT / directory).rglob("*")
            if path.suffix in {".py", ".yml", ".yaml", ".json"}
        )
    paths.extend(ROOT / name for name in ("pyproject.toml", "mkdocs.yml", ".env.example"))
    failures = [
        str(p.relative_to(ROOT))
        for p in paths
        if any(char in p.read_text(encoding="utf-8") for char in ("\u2013", "\u2014"))
    ]
    assert not failures, f"Forbidden authored punctuation: {failures}"


def test_installed_package_metadata() -> None:
    package = metadata("fde-for-beginners")
    assert package["Requires-Python"] == ">=3.11"
    assert package["License-Expression"] == "MIT"
    assert fde_beginners.__version__ == package["Version"]


def test_documentation_hook_preserves_source_paths() -> None:
    config = load_config(config_file=str(ROOT / "mkdocs.yml"))
    files = config.plugins.on_files(Files([]), config=config)
    expected = {
        p.relative_to(ROOT).as_posix() for p in authored_pages() if ".github" not in p.parts
    } | {"LICENSE"}
    assert {file.src_uri for file in files} == expected
    for file in files:
        assert Path(file.abs_src_path).read_bytes() == (ROOT / file.src_uri).read_bytes()
        if file.src_uri.endswith(".md"):
            assert file.inclusion == InclusionLevel.INCLUDED


def test_navigation_covers_all_learning_pages() -> None:
    config = load_config(config_file=str(ROOT / "mkdocs.yml"))

    def targets(items: list[dict]) -> list[str]:
        result = []
        for item in items:
            for value in item.values():
                result.extend(targets(value) if isinstance(value, list) else [value])
        return result

    navigation = targets(config.nav)
    expected = {
        p.relative_to(ROOT).as_posix() for p in authored_pages() if ".github" not in p.parts
    }
    assert set(navigation) == expected
    assert len(navigation) == len(set(navigation)), "Duplicate navigation entries"
