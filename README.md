Deployed to GitHub Pages at https://vadimkantorov.github.io/minimapython/

Contents of [`_posts`](./_posts), [`index.md`](./index.md), [`about.md`](./about.md), [`_config.json`](./_config.json) taken from the original demo of [jekyll/minima@demo-site](https://github.com/jekyll/minima/tree/demo-site).

### Generate full site from `sitemap.xml`

```shell
python minimapython.py -c _config.json --sitemap-path sitemap.xml -o _site --baseurl /minimapython --siteurl https://vadimkantorov.github.io
```

### Generate full site page-by-page
```shell
mkdir -p ./_site
python minimapython.py -c _config.json --sitemap-path sitemap.xml -i index.md                                 -o _site/index.html 
python minimapython.py -c _config.json --sitemap-path sitemap.xml -i about.md                                 -o _site/about.html

python minimapython.py -c _config.json --sitemap-path sitemap.xml -i _posts/2016-05-19-super-short-article.md -o _site/blog/2016-05-19-super-short-article.html
python minimapython.py -c _config.json --sitemap-path sitemap.xml -i _posts/2016-05-20-my-example-post.md     -o _site/blog/2016-05-20-my-example-post.html
python minimapython.py -c _config.json --sitemap-path sitemap.xml -i _posts/2016-05-20-super-long-article.md  -o _site/blog/2016-05-20-super-long-article.html
python minimapython.py -c _config.json --sitemap-path sitemap.xml -i _posts/2016-05-20-this-post-demonstrates-poscontent-styles.md -o ./_site/blog/2016-05-20-this-post-demonstrates-post-content-styles.html
python minimapython.py -c _config.json --sitemap-path sitemap.xml -i _posts/2016-05-20-welcome-to-jekyll.md   -o _site/blog/2016-05-20-welcome-to-jekyll.html
cp sitemap.xml ./_site
```

