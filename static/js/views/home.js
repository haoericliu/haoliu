app.HomeView = Backbone.View.extend({

    events:{
    },

    render:function (data) {
        this.$el.html(this.template(data));
        return this;
    },
});
