'use strict';

// find camelCase words to make into links
// var linkRe = /\b([a-z]+[a-z0-9_]?[A-Z]+[a-zA-Z0-9_]*)(?![^<]*<\/a>)/g;
var notALinkRe = /_{1}([a-z]+[a-z0-9_]?[A-Z]+[a-zA-Z0-9_]*)(\s+)/g;
var linkRe = /\b([a-z]+[a-z0-9_]?[A-Z]+[a-zA-Z0-9_]*)(\s+)/g;

showdown.setOption('tasklists', true);
showdown.setOption('simplifiedAutoLink', true);
showdown.extension('showdownSupPre', function() {
  return {
    // type determines when run: either
    // on the raw text (lang or on the processed html (output)
    type: 'lang', // lang or output
    filter: function (text, converter, options) {
      var ulRe = /\<ul\>/g;
      text = text.replace(ulRe, "<ul class=\"uk-list uk-list-disc uk-list-collapse\">");
      text = text.replace(linkRe, "<a class=\"wiki-link\" href=\"/content/\$1\"><span uk-icon=\"icon: comment\" ></span> \$1</a>$2");
      text = text.replace(notALinkRe, "$1$2");
      return text;
    },
  };
});
