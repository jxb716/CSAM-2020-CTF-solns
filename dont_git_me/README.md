Don't Git Me!
=============

## Challenge info:

There's a website under construction, but there's a strong suspicion a secret is being exposed. Can you find it?
Connect using your web browser to http://challenges.matrix8.net/dontgitme/

## Solution:

Visiting the website yielded a static page, with nothing interesting hidden in the source. When nothing on the page itself sticks out the next step is to look at website locations that are generally always present, in this case robots.txt.
```
User-agent: *
Disallow: /.git/
```
Checking robots.txt indicated the presence of a .git directory, and navigating to it gave high probability of holding the metadata for a git repo, so next steps are to download and inspect the directory's contents:
```
$ wget -r -np -nH http://challenges.matrix8.net/dontgitme/.git/ ; cd dontgitme
$ git status
On branch master
Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        deleted:    50x.html
        deleted:    index.html
        deleted:    robots.txt

no changes added to commit (use "git add" and/or "git commit -a")
```
As expected, the website's `.git` folder contained information on the website's history; now to see if there's anything interesting in the logs:
```
$ git log
commit c7f1beb235783659b27088acf332baaec66a05c6 (HEAD -> master)
Author: Your Name <you@example.com>
Date:   Mon Sep 21 19:50:34 2020 +0000

    removed some sensitive information

commit cb40164361a3704d450ba096e97fabbfc27c1ada
Author: Your Name <you@example.com>
Date:   Mon Sep 21 19:50:33 2020 +0000

    updated my website with some content

commit 7a3ca20f3580a911c2b6f4115bede3fe1026712e
Author: Your Name <you@example.com>
Date:   Mon Sep 21 19:50:32 2020 +0000

    initial commit
```
Sensitive information, you say... let's check that out. Since the current commit is the one that removed sensitive information, the one before it should still have it and can be revealed with `git diff`:
```
$ git diff HEAD^ HEAD
diff --git a/index.html b/index.html
index 3d377ee..a1e022f 100644
--- a/index.html
+++ b/index.html
@@ -16,8 +16,6 @@
                 <span style="font-family: Segoe UI Emoji; font-size: 3.5em"><F0><9F><91><8B></span>
                 <p class="lead">Hi!</p>
                 <p class="lead">Welcome to my website! I hope you enjoy it! On this website, you'll find all kinds of wonderful web things! This website is still in development, so please be patient while I continue to work on it! Thanks!</p>
-
-                <h2>The flag is Equifax{dont_expose_yer_git_repo_to_webservers}</h2>
             </div>
         </div>
     </body>
```
P.S. This challenge was covered in the first brown-bag session, so if you didn't attend those you missed the chance to get a free flag.
