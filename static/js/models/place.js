app.Place = Backbone.Model.extend({

    urlRoot:"/app-rest-php/employees",
//    urlRoot:"http://localhost:3000/employees",

    initialize:function () {
        this.reports = new app.PlaceCollection();
        this.reports.url = this.urlRoot + "/" + this.id + "/reports";
    }

});

app.PlaceCollection = Backbone.Collection.extend({

    model: app.Place,

    url:"/app-rest-php/employees",
//    url:"http://localhost:3000/employees"

    initialize: function() {
      _.bindAll(this, 'placeSearch');
    },

    fetch: function(options) {
      var request = {
        location: app.mapView.map.getCenter(),
        radius: '5000',
        query: options.data['name']
      };

      var service = new google.maps.places.PlacesService(app.mapView.map);
      service.textSearch(request, this.placeSearch);
    },

    placeSearch : function(results, status) {
      if (status == google.maps.places.PlacesServiceStatus.OK) {
        this.reset();
        for (var i = 0; i < results.length; i++) {
          var place = results[i];
          var model = {
            name: place.name,
            address: place.formatted_address,
            lat: place.geometry.location.lat(),
            lon: place.geometry.location.lng(),
            googleid: place.id,
            reference: place.reference,           
          };

          this.add(model);
        }
      }
    },


});
