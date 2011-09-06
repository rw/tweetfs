TweetFS
=======

Clandestinely store small files and directories on Twitter.

http://github.com/rw/tweetfs

TweetFS remebers the names and permissions of files and directories. Each node
may be downloaded as a separate entity from Twitter. Tweets are enciphered
using the Plainsight library.

This project is a collaboration with @workmajj. It uses his SeqTweet library.

Contact
=======

Robert Winslow

rw@rwinslow.com

@robert_winslow


Installation
============

    sudo pip install tweetfs

Usage
=====

1. Create a ~/.tweetfs directory.
2. Create the file ~/.tweetfs/creds.cfg. It must have the following format:

        [Twitter]
        CONSUMER_KEY = __
        CONSUMER_SECRET = __
        ACCESS_KEY = __
        ACCESS_SECRET = __

   The values can be retrieved using SeqTweet's auth.py script.

3. Add texts into the directory ~/.tweetfs/texts/. I recommend classic novels from Project Gutenberg.
4. Run the following:

        tweetfs upload <file or directory>

   It'll print a list of tweet ids that were created when storing the files.

5. Any file can be retrieved by referencing its tweet id:

        tweetfs download <tweet id> <optional filename to write to>

   Remember to keep the filesizes small--Twitter doesn't let us put many tweets up in a day :-)

License
=======

Copyright (c) 2011, Robert Winslow
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

The names of the contributors may not be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
