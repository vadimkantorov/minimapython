mkdir -p _site

python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout home --baseurl /blog --siteurl http://localhost:8000 -i index.md -o ./_site/index.html 
python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout page -i about.md -o ./_site/about.html

python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout post -i _posts/2016-05-19-super-short-article.md -o ./_site/blog/2016-05-19-super-short-article.html
python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout post -i _posts/2016-05-20-super-long-article.md  -o ./_site/blog/2016-05-20-super-long-article.html
python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout post -i _posts/2016-05-20-welcome-to-jekyll.md   -o ./_site/blog/2016-05-20-welcome-to-jekyll.html
python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout post -i _posts/2016-05-20-my-example-post.md     -o ./_site/blog/2016-05-20-my-welcome-post.html
python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout post -i _posts/2016-05-20-this-post-demonstrates-post-content-styles.md -o ./_site/blog/2016-05-20-this-post-demonstrates-post-content-styles.html