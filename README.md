Adapted [minima theme](https://github.com/jekyll/minima) for generating HTML pages with a single-file Python script

# Usage
```shell

python minimapython.py -o test.html -i test.txt -c context.json --layout home

```

Example inspired by [jekyll/minima@demo-site](https://github.com/jekyll/minima/tree/demo-site) in branch [vadimkantorov/minimapython@demo-site](../../tree/demo-site)

> [!NOTE]
> Do not forget to set `GitHub Actions` as GitHub Pages source in your repo [`Settings -> Pages -> Build and deployment -> Source`](https://github.com/vadimkantorov/minimapython/settings/pages). Also do not forget to configure or disable branch protection rule (`No restriction`) in [`Settings -> Environments -> github-pages -> Deployment branches and tags`](https://github.com/vadimkantorov/minimapython/settings/environments/).
