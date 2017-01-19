# zerve

This tool allows you to *package a bunch of files* (HTML, CSS…) and a small
Python module (with no external dependencies) in *a single file application* that,
once executed, will *serve such files via HTTP*.

This can be useful, for example, if you designed a static web site you want to
send a preview of to a customer: with this tool you'll be able to send him a
single file that, once executed, will locally serve the site.

Take for example the [example-documentroot](example-documentroot) directory in
this repository that contains a single-page web site made of an HTML and a CSS
file. If you run

    ./make_zerve example-documentroot

(from the direcotry containng this `README.md` file), you will obtain an
executable file named `zerve`; now every time that you run

    ./zerve

(wherever such file has been moved), a web browser will open pointing to
`http://localhost:8000/`, corresonding to the single-page web site contained in
[example-documentroot](example-documentroot); you can stop the server simply
pressing `ctrl-C`.

The packaged `zerve` application is also able to *serve files from the local
filesystem*; this can be useful, for example, in case you have a (client side,
static) web application depending on a large set of "fixed" files plus a few
data, or configuration, files that you want to be able to specify at runtime.
Running

    ./zerve an/url/resource.html:some/directory/file.html

will serve (beside the file packaged my `make_zerve`) the
`some/directory/file.html` file at URL

    http://localhost:8000/an/url/resource.html

You can specify more than one file with the same syntax, and if you omit the
`an/url/resource.html:` part the file path will be used as the URL path, so for
example `./zerve file.html` will serve `file.html` file at
`http://localhost:8000/file.html` URL. Observe that the content of the specified
files is *cached at run*, so if you modify the file on the filesystem, you'll
need to re-run `zerve` to update the served content.

Use `./zerve -h` to dicover how to change the port the server listens to, or
how to avoid opening a web browser at every run.
