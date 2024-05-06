Adapted [minima theme](https://github.com/jekyll/minima) for generating HTML pages with a single-file Python script. This script includes the required CSS and HTML templates (compiled [minima theme](https://github.com/jekyll/minima)'s CSS is taken from https://github.com/vadimkantorov/minimacss). You can modify the templates inline or extract them to a directory and modify the extracted template files.

# Usage
```shell
# extract all CSS and HTML templates to _snippets dir
python minimapython.py --snippets-dir ./_snippets

python minimapython.py -o test.html -i test.txt -c context.json --layout home
```

Example inspired by [jekyll/minima@demo-site](https://github.com/jekyll/minima/tree/demo-site) is in branch [vadimkantorov/minimapython@demo-site](../../tree/demo-site) and auto-deployed to GitHub Pages at https://vadimkantorov.github.io/minimapython/ (compare to https://jekyll.github.io/minima/)

> [!NOTE]
> When deploying to GitHub Pages, do not forget to set `GitHub Actions` as GitHub Pages source in your repo [`Settings -> Pages -> Build and deployment -> Source`](https://github.com/vadimkantorov/minimapython/settings/pages). Also do not forget to configure or disable branch protection rule (`No restriction`) in [`Settings -> Environments -> github-pages -> Deployment branches and tags`](https://github.com/vadimkantorov/minimapython/settings/environments/).
