python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout home --baseurl /blog --siteurl http://localhost:8000 -i index.md -o index.html --paginator-previous-page-path /previous/page/path --paginator-next-page-path /next/page/path --paginator-page 2 --paginator-previous-page 1 --paginator-next-page 3
python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout page -i about.md -o about.html

#python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout post -i ./_posts/2016-05-19-super-short-article.md -o ./blog/2016-05-19-super-short-article.html
#python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout post -i ./_posts/2016-05-20-super-long-article.md -o ./blog/2016-05-20-super-long-article.html
#python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout post -i ./_posts/2016-05-20-welcome-to-jekyll.md -o ./blog/2016-05-20-welcome-to-jekyll.html
#python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout post -i ./_posts/2016-05-20-my-example-post.md -o ./blog/2016-05-20-my-welcome-post.html
#python minimapython.py -c _config.json --sitemap-path sitemap.xml --layout post -i ./_posts/2016-05-20-this-post-demonstrates-post-content-styles.md -o ./blog/2016-05-20-this-post-demonstrates-post-content-styles.html
