"""Publish canonical Markdown at repository paths, without duplicate source pages."""

from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files, InclusionLevel

ROOT = Path(__file__).resolve().parents[1]
ROOT_PAGES = (
    "README.md",
    "START_HERE.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
)


def on_files(files: Files, config: MkDocsConfig) -> Files:
    """Keep relative links identical on GitHub and in the built site."""
    pages = [ROOT / name for name in ROOT_PAGES]
    for folder in ("docs", "labs", "templates"):
        pages.extend(sorted((ROOT / folder).rglob("*.md")))
    generated = Files(
        [
            File.generated(
                config,
                path.relative_to(ROOT).as_posix(),
                abs_src_path=str(path),
                inclusion=InclusionLevel.INCLUDED,
            )
            for path in pages
        ]
    )
    generated.append(File.generated(config, "LICENSE", abs_src_path=str(ROOT / "LICENSE")))
    return generated
