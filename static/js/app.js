var app = {

  views: {},

  models: {},

  loadTemplates: function(views, callback) {

    var deferreds = [];

    $.each(views, function(index, view) {
      if (app[view]) {
        deferreds.push($.get('static/tpl/' + view + '.html', function(data) {
          app[view].prototype.template = _.template(data);
        }, 'html'));
      } else {
        alert(view + " not found");
      }
    });

    $.when.apply(null, deferreds).done(callback);
  }

};

app.Router = Backbone.Router.extend({

  routes: {
    "home": "home",
    "login": "login",
    "logout": "logout",
    "register": "register",
    "upload": "upload",
    "*path": "home",
  },

  initialize: function () {
    app.credential = new app.Credential();
    app.credential.bind('change:loggedIn', this.shell, this);
    this.shell();
  },

  shell: function() {
    if (!app.shellView) {
      app.shellView = new app.ShellView();
    } else {
      app.shellView.delegateEvents();
    } 
    $('body').html(app.shellView.render().el);
    $('body').click(function () {
      $('.dropdown').removeClass("open");
    });

    this.$content = $("#content");

    if (!app.credential.get('loggedIn')) {
      this.register();
    } else {
      this.home();
    }
  },

  home: function() {
    app.photosView = new app.PhotosView(this.$content);
  },

  register: function () {
    if (app.credential.get('loggedIn')) {
      this.navigate('#home', true);
      return;
    }

    // Since the home view never changes, we instantiate it and render it only once
    if (!app.registerView) {
      app.registerView = new app.RegisterView();
      app.registerView.render(null);
    } else {
      console.log('reusing register view');
      app.registerView.delegateEvents(); // delegate events when the view is recycled
    }
    this.$content.html(app.registerView.el);
  },

  login: function() {
    if (app.credential.get('loggedIn')) {
      this.navigate('#home', true);
      return;
    }

    if (!app.loginView) {
      app.loginView = new app.LoginView();
      app.loginView.render(null);
    } else {
      console.log("reusing login view");
      app.loginView.delegateEvents();
    }
    this.$content.html(app.loginView.el);
  },

  logout: function() {
    var a = "hello world";
    var that = this;
    $.ajax({
      url:"/logout",
      type:'POST',
      dataType:"json",
      contentType: 'application/json; charset=utf-8',
      headers: { "X-CSRFToken": $.cookie("csrftoken") },
      data: JSON.stringify(a),
      success:function () {
        app.credential.setSessionId(null);
        that.shell();
      }
    });
  },

  upload: function() {
    app.uploadView = new app.UploadView();
    app.uploadView.render(null);
    this.$content.html(app.uploadView.el);
  }
});

$(document).on("ready", function () {
  app.loadTemplates(["ShellView", "RegisterView", "LoginView", "HomeView", "UploadView", "PhotoView"],
    function () {
      app.router = new app.Router();
      Backbone.history.start();
    });
});
