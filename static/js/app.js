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
    },

    initialize: function () {
     this.$content = $("#content"); 
     this.home();
    },

    home: function () {
        // Since the home view never changes, we instantiate it and render it only once
        if (!app.homelView) {
            app.homelView = new app.HomeView();
            app.homelView.render();
        } else {
            console.log('reusing home view');
            app.homelView.delegateEvents(); // delegate events when the view is recycled
        }
        this.$content.html(app.homelView.el);
        app.shellView.selectMenuItem('home-menu');
    },

});

$(document).on("ready", function () {
    app.loadTemplates(["HomeView"],
        function () {
            app.router = new app.Router();
            Backbone.history.start();
        });
});
