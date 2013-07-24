app.ShellView = Backbone.View.extend({

    initialize: function () {
    },

    render: function () {
        this.$el.html(this.template());
        return this;
    },

    events: {
        "keyup .search-query": "search",
        "keypress .search-query": "onkeypress"
    },
});