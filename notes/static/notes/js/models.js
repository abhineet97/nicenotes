(function ($, Backbone, _, app) {
  var Session = Backbone.Model.extend({
    defaults: {
      token: null
    },
    initialize: function (options) {
      this.options = options;
      $.ajaxPrefilter($.proxy(this._setupAuth, this));
      this.load();
    },
    load: function () {
      var token = localStorage.apiToken;
      if (token) {
        this.set('token', token);
      }
    },
    save: function (token) {
      this.set('token', token);
      if (token == null) {
        localStorage.removeItem('apiToken');
      } else {
        localStorage.apiToken = token;
      }
    },
    delete: function () {
      this.save(null);
    },
    authenticated: function () {
      return this.get('token') !== null;
    },
    _setupAuth: function (settings, originalOptions, xhr) {
      if (this.authenticated()) {
        xhr.setRequestHeader(
          'Authorization',
          'Token ' + this.get('token')
        );
      }
    }
  });

  app.session = new Session();

  app.models.User = Backbone.Model.extend({});
  app.models.Note = Backbone.Model.extend({
    url: function () {
      var originalURL = Backbone.Model.prototype.url.call(this);
      return originalURL + (originalURL.charAt(originalURL.length - 1) === '/' ? '' : '/');
    }
  });

  app.collections.Users = Backbone.Collection.extend({
    model: app.models.User,
    url: app.api.users
  });
  app.users = new app.collections.Users();

  app.collections.Notes = Backbone.Collection.extend({
    model: app.models.Note,
    url: app.api.notes
  });
  app.notes = new app.collections.Notes();

  app.models.Me = Backbone.Model.extend({
    url: app.api.me
  });
  app.me = new app.models.Me();

})(jQuery, Backbone, _, app);
