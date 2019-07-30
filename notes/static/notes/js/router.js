(function ($, Backbone, _, app) {
  var AppRouter = Backbone.Router.extend({
    routes: {
      '': 'home',
      'shared': 'shared'
    },
    initialize: function (options) {
      this.contentElement = '#content';
      this.current = null;
      this.header = new app.views.HeaderView();
      $('body').prepend(this.header.el);
      this.header.render();
      Backbone.history.start();
    },
    home: function () {
      var view = new app.views.NotesView({el: this.contentElement});
      view.render();
    },
    shared: function () {
      var view = new app.views.SharedView({el: this.contentElement})
      view.render();
    },
    route: function (route, name, callback) {
      var login, register;
      callback = callback || this[name];
      callback = _.wrap(callback, function (original) {
        var args = _.without(arguments, original);
        if (app.session.authenticated()) {
          original.apply(this, args);
        } else {
          $(this.contentElement).hide();
          login = new app.views.LoginView();
          register = new app.views.RegisterView();
          $(this.contentElement).after(login.el);
          $(this.contentElement).after(register.el);
          var showContent = function () {
            this.header.render();
            $(this.contentElement).show();
            original.apply(this, args);
          };
          login.on('done', function () {
            this.header.render();
            $(this.contentElement).show();
            original.apply(this, args);
            register.remove();
          }, this);
          register.on('done', function () {
            this.header.render();
            $(this.contentElement).show();
            original.apply(this, args);
            login.remove();
          }, this);
          login.render();
          register.render();
        }
      });
      return Backbone.Router.prototype.route.apply(this, [route, name, callback]);
    },
    render: function (view) {
      if (this.current) {
        this.current.undelegateEvents();
        this.current.$el = $();
        this.current.remove();
      }
      this.current = view;
      this.current.render();
    }
  });

  app.router = AppRouter;
})(jQuery, Backbone, _, app);
