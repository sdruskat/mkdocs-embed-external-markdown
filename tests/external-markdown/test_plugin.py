from pytest import fixture
from requests import Response

from external_markdown.plugin import EmbedExternalMarkdown


@fixture
def markdown():
    return """# Test links
## Links that should remain intact
- [external link](https://github.com)
- [external link with anchor](https://ansible-docs.readthedocs.io/zh/stable-2.0/rst/playbooks_variables.html#using-variables-about-jinja2)
- [internal link](#links)
- [site-internal anchored link](testpage.md#test-subsection)
- [site-internal link](testpage.md)"""


class TestEmbedExternalMarkdown:
    def test_keep_anchors(self, mocker, markdown):
        plugin = "external_markdown.plugin.EmbedExternalMarkdown"
        mocker.patch(f"{plugin}.is_valid_url", return_value=True)
        mocker.patch(f"{plugin}.make_request", return_value=Response())
        mocker.patch(f"{plugin}.get_markdown_from_response", return_value=markdown)
        # mocker.patch(
        #     f"{plugin}.update_relative_links",
        # )
        converted_md = EmbedExternalMarkdown().external_markdown(
            "https://BASEURL/FILE.md"
        )

        print(f"\n\n\n{converted_md}\n\n\n")

        assert "[external link](https://github.com)" in converted_md
        assert (
            "[external link with anchor](https://ansible-docs.readthedocs.io/zh/stable-2.0/rst/playbooks_variables"
            ".html#using-variables-about-jinja2)" in converted_md
        )
        assert "[internal link](#links)" in converted_md
        assert (
            "[semi-internal anchored link](testpage.md#test-subsection)" in converted_md
        )
        assert "[semi-internal link](testpage.md)" in converted_md
