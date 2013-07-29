app.Category = Backbone.Model.extend({

  urlRoot:"/category",
  
  initialize:function () {
  }

});

app.Categories = Backbone.Collection.extend({
  url:"/categories",
  model: app.Category
});
