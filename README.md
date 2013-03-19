Dropkick
========

*Swiss-army publishing and sharing.*

Dropkick is a command-line utility enabling you to share and distribute files in
a variety of ways to [DreamObjects](http://dreamhost.com/cloud/dreamobjects).

* Publishing nicely formatted Markdown documents using `dropkick document`.
* Publishing beautiful HTML5 presentations implemented in Markdown using
  `dropkick presentation`.
* Sharing a directory of files as an optionally password protected zip using
  `dropkick share`. 

Installing dropkick (for now) is a manual process, and requires you to run
`python setup.py develop`, or to build a package and install it yourself. Once
we're more complete, a release will go up on the Python Package Index for easier
installation.

Once you have dropkick installed, run `dropkick config`, and provide your S3
credentials for DreamObjects. These credentials will be saved for later use.

--

**Credits**

* Dropkick makes use of the excellent [Strapdown](http://strapdownjs.com)
  JavaScript library for rendering beautiful Markdown documents.
* Dropkick uses the awesome [Reveal.js](http://lab.hakim.se/reveal-js/)
  JavaScript library for creating lovely HTML5 presentations.
* Communication with DreamObjects is enabled by the awesome 
  [boto](https://github.com/boto/boto) library.
