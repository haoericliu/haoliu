app.HomeView = Backbone.View.extend({

    initialize: function() {
      _.bindAll(this, 'render');
      this.photosView = new app.PhotosView();
      this.render();
    },

    render:function () {
        this.$el.html();
        return this;
    },

    
});
