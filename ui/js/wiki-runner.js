'use strict';
var converter = new showdown.Converter({extensions: ['showdownSupPre']});

// INDEXES OF THE TABS IN THE EDITOR
const VIEWTAB = 0;
const EDITTAB = 1;
const SPLITTAB = 2;

function validatePageName (name){
  var pageRe = /([a-z]+[a-z0-9_]?[A-Z]+[a-zA-Z0-9_]*)/g;
  if(pageRe.exec(name)){
    return true;
  } else {
    return false;
  }
}

var menuEl = document.getElementById("mainMenu");

if (menuEl) {

  var menu = new Vue({
    el: "#mainMenu",
    methods: {
      newPage() {
        console.log("make a new page");
        UIkit.modal("#newPage").show();
        document.getElementById('pageMenu').style.display = "none";
      }
    }
  });

  var fileModal = new Vue({
    el: "#newPage",
    data: {
      pageName: '',
      errorMessage: ''
    },
    methods: {
      save() {
        if (validatePageName(this.pageName)) {
          document.location.href = "/content/" + this.pageName;
        } else {
          this.errorMessage = "not a valid page name must be camelCase";
        }
      }
    }
  });


}

var vEditor;

var editorEl = document.getElementById("editor");
// if the editor is present on the page
if (editorEl) {
  var editEl = document.getElementById("editbox");
  var isInitalRead = true;

  vEditor = new Vue({
    el: "#editor",
    data: {
      markdownContent: editEl.value || "",
      saveFlag: true
    },
    computed: {
      htmlContent: {
        get: function () {
          console.log('get Called');
          if (isInitalRead){
            isInitalRead = false;
          } else {
            // TODO: do this by comparing lastSaved markdown to currentMarkdown0
            this.saveFlag = false;
          }
          var html = converter.makeHtml(this.markdownContent);
          return html;
        },
        set: function (newVal) {
          console.log("set called");
        }
      }
    }
  });

  // keyboard shortcuts
  window.addEventListener("keydown", function(event) {
    // Bind to both command (for Mac) and control (for Win/Linux)
    var uikitTabController = document.getElementById("tabController");
    if (event.shiftKey && event.ctrlKey){
      if (event.keyCode == "E".charCodeAt(0)) {
        UIkit.switcher(uikitTabController).show(EDITTAB);
      } else if (event.keyCode == "V".charCodeAt(0)) {
        UIkit.switcher(uikitTabController).show(VIEWTAB);
      } else if (event.keyCode == "S".charCodeAt(0)) {
        axios.post('/api/content/' + pageName, {
          content: vEditor.markdownContent
        }).then(function () {
          UIkit.notification({
            message: 'saved ...',
            status: 'success',
            pos: 'bottom-right'
          });
          vEditor.saveFlag = true;
        });
      }
    }
  }, false);
}
