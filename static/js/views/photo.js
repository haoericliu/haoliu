app.PhotoView = Backbone.View.extend({
  
  initialize: function(model) {
    this.model = model
  },

  render:function () {
    this.$el.html( this.template(this.model.toJSON()));
    return this;
  },

});

app.PhotosView = Backbone.View.extend({

  initialize: function(el) {
    this.root = el;
    this.photos = new app.Photos();

     _.bindAll(this, "render", "add", "remove", "change");
    this.photos.bind("add", this.add);
    this.photos.bind("remove", this.remove);
    this.photos.bind("change", this.change);
    this.photos.fetch();

    this.photoViews = [];
  },

  render: function() {
    var that = this;
    this._rendered = true;
    this.root.html(this.el);
    return this;
  },

  add: function(photo) {
    var photoView = new app.PhotoView(photo);
    this.photoViews.push(photoView);

    // If the view has been rendered, then
    // we immediately append the rendered donut.
    $(this.el).append(photoView.render().el);
    this.render();
  },

  remove: function(model) {
    console.log(model.get('identifier'));

  },

  change: function(model) {
    console.log('change' + model.get('identifier'));
  }
})




