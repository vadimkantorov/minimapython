Adapted [minima theme](https://github.com/jekyll/minima) for generating HTML pages with a single-file Python script. This script includes the required CSS and HTML templates (compiled [minima theme](https://github.com/jekyll/minima)'s CSS is taken from https://github.com/vadimkantorov/minimacss). You can modify the templates inline or extract them to a directory and modify the extracted template files. 

# Usage
```shell
# extract all CSS and HTML templates to _snippets dir
python minimapython.py --snippets-dir ./_snippets

python minimapython.py -o test.html -i test.txt -c context.json --layout home

# Generate full site from sitemap.xml
python minimapython.py -c _config.json --sitemap-path sitemap.xml -o _site --baseurl /minimapythond --siteurl https://vadimkantorov.github.io

# Generate full site page-by-page
mkdir -p ./_site
python minimapython.py -c _config.json --sitemap-path sitemap.xml -i index.md                                 -o _site/index.html
python minimapython.py -c _config.json --sitemap-path sitemap.xml -i about.md                                 -o _site/about.html

python minimapython.py -c _config.json --sitemap-path sitemap.xml -i _posts/2016-05-19-super-short-article.md -o _site/blog/2016-05-19-super-short-article.html
python minimapython.py -c _config.json --sitemap-path sitemap.xml -i _posts/2016-05-20-my-example-post.md     -o _site/blog/2016-05-20-my-example-post.html
python minimapython.py -c _config.json --sitemap-path sitemap.xml -i _posts/2016-05-20-super-long-article.md  -o _site/blog/2016-05-20-super-long-article.html
python minimapython.py -c _config.json --sitemap-path sitemap.xml -i _posts/2016-05-20-this-post-demonstrates-poscontent-styles.md -o ./_site/blog/2016-05-20-this-post-demonstrates-post-content-styles.html
python minimapython.py -c _config.json --sitemap-path sitemap.xml -i _posts/2016-05-20-welcome-to-jekyll.md   -o _site/blog/2016-05-20-welcome-to-jekyll.html
cp
```

Example inspired by [jekyll/minima@demo-site](https://github.com/jekyll/minima/tree/demo-site) is in branch [vadimkantorov/minimapython@demo-site](../../tree/demo-site) and auto-deployed to GitHub Pages at https://vadimkantorov.github.io/minimapython/ . Compare to https://jekyll.github.io/minima/ and also check out https://vadimkantorov.github.io/minimapython/sitemap.xml .

> [!NOTE]
> When deploying to GitHub Pages, do not forget to set `GitHub Actions` as GitHub Pages source in your repo [`Settings -> Pages -> Build and deployment -> Source`](https://github.com/vadimkantorov/minimapython/settings/pages). Also do not forget to configure or disable branch protection rule (`No restriction`) in [`Settings -> Environments -> github-pages -> Deployment branches and tags`](https://github.com/vadimkantorov/minimapython/settings/environments/).
