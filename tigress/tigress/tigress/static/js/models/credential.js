app.Credential = Backbone.Model.extend({
    defaults: {
      loggedIn: false,
      sessionId: null
    },
//    urlRoot:"http://localhost:3000/employees",

    initialize: function () {
      var sessionId = $.cookie('swapmeet');
      this.setSessionId(sessionId);
    },

    setSessionId: function(sessionId) {
      this.set({'sessionId': sessionId , 'loggedIn': !!sessionId});
    }



});
